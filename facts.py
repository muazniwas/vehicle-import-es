from experta import Fact


# ── Input ────────────────────────────────────────────────────────────────────

class ImportRequest(Fact):
    """
    Declared once by the UI before any engine runs.

    Engine 1 (eligibility) uses:
        vehicle_type           str   "car" | "suv" | "van" | "pickup"
                                     | "motorcycle" | "three_wheeler"
        manufacture_year       int   e.g. 2021
        manufacture_month      int   1–12
        bill_of_lading_year    int   e.g. 2024
        bill_of_lading_month   int   1–12
        origin_country         str   "japan" | "uk" | "singapore" | "australia"
        fuel_type              str   "petrol" | "diesel" | "petrol_hybrid"
                                     | "electric"
        is_rhd                 bool  True if vehicle is right-hand drive
        euro6_compliant        bool  True if vehicle meets Euro 6 or higher
        has_min_airbags        bool  True if vehicle has ≥ 2 airbags
        has_abs                bool  True if vehicle has ABS
        has_esc                bool  True if vehicle has ESC
        has_battery_warranty   bool  True if EV/hybrid battery warranty ≥ 5yr
                                     / 100,000 km (ignored for petrol/diesel)
        importer_type          str   "individual" | "registered_importer"
                                     | "diplomatic" | "state_institution"

    Engine 2 (selector) adds:
        engine_cc          int
        budget_usd         float
        fuel_preference    str   same values as fuel_type, or "any"
        brand_preference   str   e.g. "toyota", or "any"

    Engine 3 (cost) adds:
        engine_cc           int    engine displacement in cc (0 for electric)
        motor_kw            int    motor power in kW (electric/hybrid only,
                                   None for petrol/diesel)
        purchase_price_usd  float
        usd_to_lkr          float  optional — today's USD/LKR rate; falls back
                                   to USD_TO_LKR_DEFAULT in duty_rules.py
        jpy_to_usd          float  optional — today's JPY/USD rate; falls back
                                   to JPY_TO_USD_RATE_DEFAULT in cost_factors.py
    """
    pass


# ── Engine 1 output ──────────────────────────────────────────────────────────

class EligibilityResult(Fact):
    """
    Asserted by Engine 1.

        eligible    bool   True if the vehicle passes all permit rules
        reason      str    Human-readable explanation
        rule_fired  str    Name of the rule that produced this result
    """
    pass


# ── Engine 2 facts ───────────────────────────────────────────────────────────

class VehicleCandidate(Fact):
    """
    One fact per model loaded from vehicle_db at the start of Engine 2.

        make               str    e.g. "Toyota"
        model              str    e.g. "Aqua"
        engine_cc          int
        fuel_type          str
        origin             str    "japan" | "uk"
        typical_price_usd  float  average auction/market price
        resale_score       int    1–10, value retention in Sri Lanka
        popularity         int    1–10, local market demand
    """
    pass


class VehicleScore(Fact):
    """
    Intermediate fact produced by Engine 2 scoring rules.

        make   str
        model  str
        score  float  weighted fit score (0.0 – 1.0)
    """
    pass


class Recommendation(Fact):
    """
    Final shortlist entry asserted by Engine 2.

        rank               int    1 = best match
        make               str
        model              str
        vehicle_type       str    "car" | "suv" | "van" | "pickup" | ...
        engine_cc          int
        fuel_type          str
        motor_kw           int | None  motor power (EV/hybrid); None for ICE
        typical_price_usd  float
        fit_score          float
        reason             str    why this vehicle was recommended
    """
    pass


# ── Engine 3 facts ───────────────────────────────────────────────────────────

class DutyRate(Fact):
    """
    Asserted by Engine 3 with the resolved duty rates for this specific vehicle.

        fuel_type        str    the vehicle's fuel type
        excise_duty_lkr  float  total excise duty in LKR for this vehicle
                                (LKR/cc × cc for ICE/hybrid; LKR/kW × kW for EV)
        customs_pct      float  customs import duty rate (0.20 = 20 % of CIF)
        cid_surcharge_pct float CID surcharge rate (0.50 = 50 % of CID)
        vat_pct          float  VAT rate (0.18 = 18 %)
        duty_exempt      bool   True for diplomatic importers (Vienna Convention
                                duty-free); when True all duty fields are 0.0
    """
    pass


class CostBreakdown(Fact):
    """
    Asserted by Engine 3 with the full landed cost.

        purchase_price_usd   float
        shipping_usd         float
        insurance_usd        float
        jaai_usd             float  JAAI pre-shipment inspection (Japan only; 0 otherwise)
        cif_usd              float  purchase + shipping + insurance
        cid_usd              float  customs import duty (20 % of CIF)
        cid_surcharge_usd    float  CID surcharge (50 % of CID)
        excise_duty_usd      float  excise duty (converted from LKR)
        luxury_tax_usd       float  luxury tax (converted from LKR; 0 if below threshold)
        vat_usd              float  VAT 18 % on (CIF + CID + surcharge + excise + luxury)
        port_charges_usd     float  Colombo port THC, wharfage, D/O, clearing agent
        total_usd            float  sum of all above
        total_lkr            float  total_usd × usd_to_lkr
        registration_lkr     float  DMT first registration fee
        grand_total_lkr      float  total_lkr + registration_lkr
    """
    pass


# ── Explanation facility ─────────────────────────────────────────────────────

class RuleFired(Fact):
    """
    Asserted every time a rule runs, building an audit trail.

        engine  str   "eligibility" | "selector" | "cost"
        rule    str   rule method name
        note    str   plain-English description of what the rule did
    """
    pass
