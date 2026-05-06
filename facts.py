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
        euro6_compliant        bool  True if vehicle meets Euro 6 or higher
        has_min_airbags        bool  True if vehicle has ≥ 2 airbags
        has_abs                bool  True if vehicle has ABS
        has_esc                bool  True if vehicle has ESC
        has_battery_warranty   bool  True if EV/hybrid battery warranty ≥ 5yr
                                     / 100,000 km (ignored for petrol/diesel)

    Engine 2 (selector) adds:
        engine_cc          int
        budget_usd         float
        fuel_preference    str   same values as fuel_type, or "any"
        brand_preference   str   e.g. "toyota", or "any"

    Engine 3 (cost) adds:
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
        engine_cc          int
        fuel_type          str
        typical_price_usd  float
        fit_score          float
        reason             str    why this vehicle was recommended
    """
    pass


# ── Engine 3 facts ───────────────────────────────────────────────────────────

class DutyRate(Fact):
    """
    One fact per duty band loaded from duty_rules at the start of Engine 3.

        fuel_type    str
        cc_min       int
        cc_max       int    use 9999 for an open-ended upper band
        customs_pct  float  customs duty as % of CIF value
        excise_pct   float  excise duty as % of CIF value
        pal_pct      float  port & airport levy as % of CIF (fixed 7.5)
        vat_pct      float  VAT as % of (CIF + all duties above)
    """
    pass


class CostBreakdown(Fact):
    """
    Asserted by Engine 3 with the full landed cost.

        purchase_price_usd  float
        shipping_usd        float
        insurance_usd       float
        cif_usd             float   purchase + shipping + insurance
        customs_duty_usd    float
        excise_duty_usd     float
        pal_usd             float
        vat_usd             float
        port_charges_usd    float
        total_usd           float
        total_lkr           float
        registration_lkr    float
        grand_total_lkr     float
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
