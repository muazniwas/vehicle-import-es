"""
Engine 3 — Total Landed Cost Estimator.

Computes the full cost of importing a vehicle to Sri Lanka, following the
duty cascade mandated by Gazette Extraordinary No. 2421/44 (Feb 2025):

    Step 1  CIF         = purchase price + sea freight + marine insurance
    Step 2  CID         = 20 % of CIF
    Step 3  CID surcharge = 50 % of CID  (effective through Jan 2026)
    Step 4  Excise duty = LKR/cc × engine_cc  (or LKR/kW × motor_kw for EV)
    Step 5  Luxury tax  = rate × max(0, CIF_LKR − threshold)
    Step 6  VAT         = 18 % × (CIF + CID + surcharge + excise + luxury tax)
    Step 7  Port charges (THC, SLPA wharfage, D/O, clearing agent)
    Step 8  JAAI inspection fee (Japan-origin only, billed in JPY)

    Grand total = all above (converted to LKR) + DMT first registration fee

Rules:
    load_duty_rate       (salience 100)  look up excise duty for this vehicle
    compute_total_cost   (salience 50)   apply full duty cascade, declare CostBreakdown
    missing_input        (salience 5)    fires if required fields are absent
"""

from experta import KnowledgeEngine, Rule, NOT

from facts import ImportRequest, DutyRate, CostBreakdown, RuleFired
from knowledge_base.duty_rules import (
    CUSTOMS_DUTY_RATE,
    CID_SURCHARGE_RATE,
    VAT_RATE,
    USD_TO_LKR_DEFAULT,
    get_excise_duty_lkr,
    get_luxury_tax_lkr,
)
from knowledge_base.cost_factors import (
    JAAI_FEE_JPY,
    JPY_TO_USD_RATE_DEFAULT,
    get_shipping_usd,
    get_insurance_usd,
    get_port_charges_usd,
    get_registration_lkr,
)

_REQUIRED = [
    "vehicle_type", "origin_country", "fuel_type",
    "engine_cc", "purchase_price_usd",
    "manufacture_year", "manufacture_month",
    "bill_of_lading_year", "bill_of_lading_month",
]


def _age_years(mfr_year, mfr_month, bol_year, bol_month):
    return ((bol_year * 12 + bol_month) - (mfr_year * 12 + mfr_month)) / 12.0


class CostEngine(KnowledgeEngine):

    # ── 1. Resolve excise duty for this vehicle ──────────────────────────────

    @Rule(
        ImportRequest(),
        NOT(DutyRate()),
        salience=100,
    )
    def load_duty_rate(self):
        req = next(f for f in self.facts.values() if isinstance(f, ImportRequest))

        missing = [k for k in _REQUIRED if k not in req]
        if missing:
            self.declare(RuleFired(
                engine="cost",
                rule="load_duty_rate",
                note=f"Cannot compute cost — missing fields: {', '.join(missing)}.",
            ))
            self.halt()
            return

        fuel      = req["fuel_type"]
        engine_cc = req["engine_cc"]
        motor_kw  = req.get("motor_kw", None)
        age       = _age_years(
            req["manufacture_year"], req["manufacture_month"],
            req["bill_of_lading_year"], req["bill_of_lading_month"],
        )

        is_diplomatic = req.get("importer_type", "individual") == "diplomatic"

        if is_diplomatic:
            self.declare(DutyRate(
                fuel_type=fuel,
                excise_duty_lkr=0.0,
                customs_pct=0.0,
                cid_surcharge_pct=0.0,
                vat_pct=0.0,
                duty_exempt=True,
            ))
            self.declare(RuleFired(
                engine="cost",
                rule="load_duty_rate",
                note=(
                    "Diplomatic importer — Vienna Convention duty-free: "
                    "CID, excise duty, VAT, and luxury tax all waived."
                ),
            ))
        else:
            excise_lkr = get_excise_duty_lkr(fuel, engine_cc, motor_kw, age)
            self.declare(DutyRate(
                fuel_type=fuel,
                excise_duty_lkr=excise_lkr,
                customs_pct=CUSTOMS_DUTY_RATE,
                cid_surcharge_pct=CID_SURCHARGE_RATE,
                vat_pct=VAT_RATE,
                duty_exempt=False,
            ))
            self.declare(RuleFired(
                engine="cost",
                rule="load_duty_rate",
                note=(
                    f"Excise duty resolved: LKR {excise_lkr:,.0f} "
                    f"({fuel}, {engine_cc} cc, age {age:.1f} yr)."
                ),
            ))

    # ── 2. Apply full duty cascade and declare CostBreakdown ─────────────────

    @Rule(
        ImportRequest(),
        DutyRate(),
        NOT(CostBreakdown()),
        salience=50,
    )
    def compute_total_cost(self):
        req = next(f for f in self.facts.values() if isinstance(f, ImportRequest))
        dr  = next(f for f in self.facts.values() if isinstance(f, DutyRate))

        duty_exempt = dr.get("duty_exempt", False)
        price    = req["purchase_price_usd"]
        origin   = req["origin_country"]
        vtype    = req["vehicle_type"]
        fuel     = req["fuel_type"]
        engine_cc = req["engine_cc"]
        usd_rate = req.get("usd_to_lkr", USD_TO_LKR_DEFAULT)
        jpy_rate = req.get("jpy_to_usd", JPY_TO_USD_RATE_DEFAULT)

        using_default_usd = "usd_to_lkr" not in req
        using_default_jpy = "jpy_to_usd" not in req

        # ── Step 1: Shipping & insurance ────────────────────────────────────
        shipping_usd  = get_shipping_usd(origin, vtype)
        insurance_usd = get_insurance_usd(price, shipping_usd)

        self.declare(RuleFired(
            engine="cost",
            rule="compute_total_cost",
            note=(
                f"Shipping: USD {shipping_usd:,.0f}, "
                f"insurance: USD {insurance_usd:,.0f}."
            ),
        ))

        # ── JAAI (Japan only) ────────────────────────────────────────────────
        if origin == "japan":
            jpy = JAAI_FEE_JPY["kei"] if engine_cc <= 660 else JAAI_FEE_JPY["standard"]
            jaai_usd = jpy * jpy_rate
            self.declare(RuleFired(
                engine="cost",
                rule="compute_total_cost",
                note=(
                    f"JAAI inspection: ¥{jpy:,} × "
                    f"{'default ' if using_default_jpy else ''}"
                    f"{jpy_rate:.5f} = USD {jaai_usd:.2f}."
                ),
            ))
        else:
            jaai_usd = 0.0

        # ── Step 1 (continued): CIF ──────────────────────────────────────────
        cif_usd = price + shipping_usd + insurance_usd
        cif_lkr = cif_usd * usd_rate

        if using_default_usd:
            self.declare(RuleFired(
                engine="cost",
                rule="compute_total_cost",
                note=(
                    f"USD/LKR rate not supplied — using default {usd_rate}. "
                    "Supply usd_to_lkr in ImportRequest for accuracy."
                ),
            ))

        self.declare(RuleFired(
            engine="cost",
            rule="compute_total_cost",
            note=(
                f"CIF: USD {cif_usd:,.2f} "
                f"= LKR {cif_lkr:,.0f} at {usd_rate}."
            ),
        ))

        # ── Steps 2–3: CID and CID surcharge ────────────────────────────────
        cid_lkr        = cif_lkr * dr["customs_pct"]
        surcharge_lkr  = cid_lkr * dr["cid_surcharge_pct"]

        self.declare(RuleFired(
            engine="cost",
            rule="compute_total_cost",
            note=(
                f"CID: LKR {cid_lkr:,.0f} (20 % of CIF), "
                f"surcharge: LKR {surcharge_lkr:,.0f} (50 % of CID)."
            ),
        ))

        # ── Step 4: Excise duty (from DutyRate fact) ─────────────────────────
        excise_lkr = dr["excise_duty_lkr"]

        self.declare(RuleFired(
            engine="cost",
            rule="compute_total_cost",
            note=f"Excise duty: LKR {excise_lkr:,.0f}.",
        ))

        # ── Step 5: Luxury tax ───────────────────────────────────────────────
        luxury_lkr = 0.0 if duty_exempt else get_luxury_tax_lkr(fuel, cif_lkr)

        if luxury_lkr > 0:
            self.declare(RuleFired(
                engine="cost",
                rule="compute_total_cost",
                note=f"Luxury tax: LKR {luxury_lkr:,.0f} (CIF exceeds threshold).",
            ))

        # ── Step 6: VAT ──────────────────────────────────────────────────────
        vat_base_lkr = cif_lkr + cid_lkr + surcharge_lkr + excise_lkr + luxury_lkr
        vat_lkr      = vat_base_lkr * dr["vat_pct"]

        self.declare(RuleFired(
            engine="cost",
            rule="compute_total_cost",
            note=(
                f"VAT: LKR {vat_lkr:,.0f} "
                f"(18 % of taxable base LKR {vat_base_lkr:,.0f})."
            ),
        ))

        # ── Step 7: Port charges ─────────────────────────────────────────────
        port_usd = get_port_charges_usd(origin, vtype, usd_rate)
        port_lkr = port_usd * usd_rate

        self.declare(RuleFired(
            engine="cost",
            rule="compute_total_cost",
            note=f"Port charges: USD {port_usd:,.2f} = LKR {port_lkr:,.0f}.",
        ))

        # ── Convert all LKR duties back to USD for the breakdown ─────────────
        cid_usd       = cid_lkr       / usd_rate
        surcharge_usd = surcharge_lkr  / usd_rate
        excise_usd    = excise_lkr     / usd_rate
        luxury_usd    = luxury_lkr     / usd_rate
        vat_usd       = vat_lkr        / usd_rate

        # ── Totals ───────────────────────────────────────────────────────────
        total_usd = (
            cif_usd + cid_usd + surcharge_usd
            + excise_usd + luxury_usd + vat_usd
            + port_usd + jaai_usd
        )
        total_lkr = total_usd * usd_rate

        registration_lkr = get_registration_lkr(vtype, engine_cc)
        grand_total_lkr  = total_lkr + registration_lkr

        self.declare(CostBreakdown(
            purchase_price_usd=round(price, 2),
            shipping_usd=round(shipping_usd, 2),
            insurance_usd=round(insurance_usd, 2),
            jaai_usd=round(jaai_usd, 2),
            cif_usd=round(cif_usd, 2),
            cid_usd=round(cid_usd, 2),
            cid_surcharge_usd=round(surcharge_usd, 2),
            excise_duty_usd=round(excise_usd, 2),
            luxury_tax_usd=round(luxury_usd, 2),
            vat_usd=round(vat_usd, 2),
            port_charges_usd=round(port_usd, 2),
            total_usd=round(total_usd, 2),
            total_lkr=round(total_lkr, 0),
            registration_lkr=round(registration_lkr, 0),
            grand_total_lkr=round(grand_total_lkr, 0),
        ))

        self.declare(RuleFired(
            engine="cost",
            rule="compute_total_cost",
            note=(
                f"Grand total: LKR {grand_total_lkr:,.0f} "
                f"(USD {total_usd:,.0f} landed + "
                f"LKR {registration_lkr:,.0f} registration)."
            ),
        ))

    # ── 3. Guard: required fields missing ────────────────────────────────────

    @Rule(
        ImportRequest(),
        NOT(DutyRate()),
        NOT(CostBreakdown()),
        salience=5,
    )
    def missing_input(self):
        req = next(f for f in self.facts.values() if isinstance(f, ImportRequest))
        missing = [k for k in _REQUIRED if k not in req]
        self.declare(RuleFired(
            engine="cost",
            rule="missing_input",
            note=(
                f"Cost engine cannot run — missing: {', '.join(missing)}."
                if missing
                else "Cost engine halted unexpectedly."
            ),
        ))
