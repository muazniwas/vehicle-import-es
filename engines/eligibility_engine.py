"""
Engine 1 — Import Eligibility Checker.

Checks whether a vehicle described by ImportRequest satisfies every rule
under Sri Lanka's current import regime (Gazette Extraordinary No. 2421/44,
effective 1 February 2025).

Rules fire in salience order (highest first). The first failing rule asserts
EligibilityResult(eligible=False, ...) and halts the engine. If all rules
pass, the lowest-salience rule asserts EligibilityResult(eligible=True, ...).

Each rule also asserts a RuleFired fact to build an explanation trail.
"""

from experta import KnowledgeEngine, Rule, Fact, NOT, MATCH, AND
from facts import ImportRequest, EligibilityResult, RuleFired
from knowledge_base.import_regulations import (
    ALLOWED_ORIGINS,
    VEHICLE_TYPES,
    get_age_limit,
    get_allowed_fuels,
    is_origin_allowed,
    GENERAL_CONDITIONS,
)


def _age_years(
    manufacture_year: int,
    manufacture_month: int,
    bol_year: int,
    bol_month: int,
) -> float:
    """Fractional vehicle age in years at Bill of Lading date."""
    manufacture_months = manufacture_year * 12 + manufacture_month
    bol_months = bol_year * 12 + bol_month
    return (bol_months - manufacture_months) / 12.0


class EligibilityEngine(KnowledgeEngine):

    # ── 1. Origin country ────────────────────────────────────────────────────

    @Rule(
        ImportRequest(origin_country=MATCH.origin),
        salience=80,
    )
    def check_origin(self, origin):
        if not is_origin_allowed(origin):
            allowed = ", ".join(sorted(ALLOWED_ORIGINS.keys()))
            self.declare(EligibilityResult(
                eligible=False,
                reason=(
                    f"Origin country '{origin}' is not an approved RHD source "
                    f"market. Allowed origins: {allowed}."
                ),
                rule_fired="check_origin",
            ))
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_origin",
                note=f"Origin '{origin}' rejected — not in approved origin list.",
            ))
            self.halt()
        else:
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_origin",
                note=f"Origin '{origin}' approved.",
            ))

    # ── 2. Vehicle type validity ─────────────────────────────────────────────

    @Rule(
        ImportRequest(vehicle_type=MATCH.vtype),
        salience=75,
    )
    def check_vehicle_type(self, vtype):
        if vtype not in VEHICLE_TYPES:
            valid = ", ".join(sorted(VEHICLE_TYPES))
            self.declare(EligibilityResult(
                eligible=False,
                reason=(
                    f"Vehicle type '{vtype}' is not recognised. "
                    f"Valid types: {valid}."
                ),
                rule_fired="check_vehicle_type",
            ))
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_vehicle_type",
                note=f"Vehicle type '{vtype}' not in allowed list.",
            ))
            self.halt()
        else:
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_vehicle_type",
                note=f"Vehicle type '{vtype}' is valid.",
            ))

    # ── 3. Age limit ─────────────────────────────────────────────────────────

    @Rule(
        ImportRequest(
            vehicle_type=MATCH.vtype,
            manufacture_year=MATCH.mfr_year,
            manufacture_month=MATCH.mfr_month,
            bill_of_lading_year=MATCH.bol_year,
            bill_of_lading_month=MATCH.bol_month,
        ),
        salience=70,
    )
    def check_age(self, vtype, mfr_year, mfr_month, bol_year, bol_month):
        age = _age_years(mfr_year, mfr_month, bol_year, bol_month)
        try:
            max_age = get_age_limit(vtype)
        except KeyError:
            return  # vehicle type unknown — already caught by check_vehicle_type

        if age > max_age:
            self.declare(EligibilityResult(
                eligible=False,
                reason=(
                    f"Vehicle is {age:.1f} years old at B/L date, "
                    f"exceeding the {max_age}-year limit for '{vtype}'."
                ),
                rule_fired="check_age",
            ))
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_age",
                note=(
                    f"Age {age:.1f}yr > {max_age}yr limit for '{vtype}'. "
                    "Import rejected."
                ),
            ))
            self.halt()
        else:
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_age",
                note=f"Age {age:.1f}yr within {max_age}yr limit for '{vtype}'.",
            ))

    # ── 4. Fuel restriction by vehicle type ──────────────────────────────────

    @Rule(
        ImportRequest(vehicle_type=MATCH.vtype, fuel_type=MATCH.fuel),
        salience=65,
    )
    def check_fuel_restriction(self, vtype, fuel):
        allowed = get_allowed_fuels(vtype)
        if fuel not in allowed:
            self.declare(EligibilityResult(
                eligible=False,
                reason=(
                    f"Fuel type '{fuel}' is not permitted for '{vtype}'. "
                    f"Allowed: {', '.join(sorted(allowed))}."
                ),
                rule_fired="check_fuel_restriction",
            ))
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_fuel_restriction",
                note=(
                    f"'{fuel}' not allowed for '{vtype}'. "
                    "Import rejected."
                ),
            ))
            self.halt()
        else:
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_fuel_restriction",
                note=f"Fuel type '{fuel}' allowed for '{vtype}'.",
            ))

    # ── 5. Euro 6 emissions (petrol and diesel only) ─────────────────────────

    @Rule(
        ImportRequest(
            fuel_type=MATCH.fuel,
            euro6_compliant=MATCH.compliant,
        ),
        salience=60,
    )
    def check_euro6(self, fuel, compliant):
        applies_to = GENERAL_CONDITIONS["emissions_standard"]["applies_to"]
        if fuel in applies_to and not compliant:
            self.declare(EligibilityResult(
                eligible=False,
                reason=(
                    "Vehicle does not meet Euro 6 emissions standard. "
                    "Petrol and diesel vehicles must comply with Euro 6 or higher."
                ),
                rule_fired="check_euro6",
            ))
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_euro6",
                note="Euro 6 not met for petrol/diesel vehicle. Import rejected.",
            ))
            self.halt()
        else:
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_euro6",
                note=(
                    "Euro 6 check passed."
                    if fuel in applies_to
                    else f"Euro 6 not applicable for fuel type '{fuel}'."
                ),
            ))

    # ── 6a. Minimum airbags ──────────────────────────────────────────────────

    @Rule(
        ImportRequest(vehicle_type=MATCH.vtype, has_min_airbags=MATCH.airbags),
        salience=55,
    )
    def check_airbags(self, vtype, airbags):
        if vtype in {"motorcycle", "three_wheeler"}:
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_airbags",
                note=f"Airbag requirement not applicable for '{vtype}'.",
            ))
            return
        min_count = GENERAL_CONDITIONS["minimum_airbags"]["count"]
        if not airbags:
            self.declare(EligibilityResult(
                eligible=False,
                reason=(
                    f"Vehicle must have at least {min_count} airbags. "
                    "This is a mandatory safety requirement."
                ),
                rule_fired="check_airbags",
            ))
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_airbags",
                note=f"Minimum {min_count} airbags not met. Import rejected.",
            ))
            self.halt()
        else:
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_airbags",
                note="Airbag requirement met.",
            ))

    # ── 6b. ABS ──────────────────────────────────────────────────────────────

    @Rule(
        ImportRequest(vehicle_type=MATCH.vtype, has_abs=MATCH.abs_ok),
        salience=54,
    )
    def check_abs(self, vtype, abs_ok):
        if vtype == "three_wheeler":
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_abs",
                note="ABS requirement not applicable for 'three_wheeler'.",
            ))
            return
        if not abs_ok:
            self.declare(EligibilityResult(
                eligible=False,
                reason="Anti-lock Braking System (ABS) is mandatory for all imported vehicles.",
                rule_fired="check_abs",
            ))
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_abs",
                note="ABS not present. Import rejected.",
            ))
            self.halt()
        else:
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_abs",
                note="ABS present.",
            ))

    # ── 6c. ESC ──────────────────────────────────────────────────────────────

    @Rule(
        ImportRequest(vehicle_type=MATCH.vtype, has_esc=MATCH.esc_ok),
        salience=53,
    )
    def check_esc(self, vtype, esc_ok):
        if vtype in {"motorcycle", "three_wheeler"}:
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_esc",
                note=f"ESC requirement not applicable for '{vtype}'.",
            ))
            return
        if not esc_ok:
            self.declare(EligibilityResult(
                eligible=False,
                reason="Electronic Stability Control (ESC) is mandatory for all imported vehicles.",
                rule_fired="check_esc",
            ))
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_esc",
                note="ESC not present. Import rejected.",
            ))
            self.halt()
        else:
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_esc",
                note="ESC present.",
            ))

    # ── 7. EV / hybrid battery warranty ─────────────────────────────────────

    @Rule(
        ImportRequest(
            fuel_type=MATCH.fuel,
            has_battery_warranty=MATCH.warranty,
        ),
        salience=50,
    )
    def check_battery_warranty(self, fuel, warranty):
        applies_to = GENERAL_CONDITIONS["ev_battery_warranty"]["applies_to"]
        if fuel in applies_to and not warranty:
            min_yr = GENERAL_CONDITIONS["ev_battery_warranty"]["min_years"]
            min_km = GENERAL_CONDITIONS["ev_battery_warranty"]["min_km"]
            self.declare(EligibilityResult(
                eligible=False,
                reason=(
                    f"EV/hybrid battery must carry a manufacturer warranty of "
                    f"at least {min_yr} years or {min_km:,} km."
                ),
                rule_fired="check_battery_warranty",
            ))
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_battery_warranty",
                note="Battery warranty requirement not met. Import rejected.",
            ))
            self.halt()
        else:
            self.declare(RuleFired(
                engine="eligibility",
                rule="check_battery_warranty",
                note=(
                    "Battery warranty requirement met."
                    if fuel in applies_to
                    else f"Battery warranty not applicable for fuel type '{fuel}'."
                ),
            ))

    # ── 8. All checks passed ─────────────────────────────────────────────────

    @Rule(
        ImportRequest(),
        NOT(EligibilityResult()),
        salience=10,
    )
    def all_checks_passed(self):
        self.declare(EligibilityResult(
            eligible=True,
            reason="Vehicle satisfies all import eligibility requirements.",
            rule_fired="all_checks_passed",
        ))
        self.declare(RuleFired(
            engine="eligibility",
            rule="all_checks_passed",
            note="All eligibility checks passed.",
        ))
