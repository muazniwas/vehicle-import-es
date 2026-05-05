"""
Sri Lanka motor vehicle import regulations.

Primary source: Gazette Extraordinary No. 2421/44 (effective 1 February 2025),
issued by the Ministry of Finance under the Import and Export Control Act.

Key change from pre-2022 regime: all concessionary permit schemes (SLBFE,
BOI, government officer) are suspended under Condition VIII of this gazette.
Engine CC is no longer a hard eligibility gate — it determines the excise
duty tier only.
"""

from datetime import date

CURRENT_YEAR = date.today().year

# ── Valid domain values ───────────────────────────────────────────────────────

FUEL_TYPES = {"petrol", "diesel", "petrol_hybrid", "electric"}

# PHEV (plug-in hybrid) is classified as petrol_hybrid in the gazette.

VEHICLE_TYPES = {"car", "suv", "van", "pickup", "motorcycle", "three_wheeler"}

# Practical RHD source markets. Japan requires a pre-shipment inspection
# certificate from JAAI (Japan Auto Appraisal Institute).
ALLOWED_ORIGINS = {
    "japan": {
        "display": "Japan",
        "requires_jaai_cert": True,
    },
    "uk": {
        "display": "United Kingdom",
        "requires_jaai_cert": False,
    },
    "australia": {
        "display": "Australia",
        "requires_jaai_cert": False,
    },
    "singapore": {
        "display": "Singapore",
        "requires_jaai_cert": False,
    },
}

# ── Age limits by vehicle category ───────────────────────────────────────────
# Age = years elapsed between date of manufacture and Bill of Lading date.
# If only manufacture year is stated, January 15 of that year is used.

VEHICLE_CATEGORY_AGE_LIMITS = {
    "passenger": {
        "vehicle_types": {"car", "suv", "pickup", "motorcycle"},
        "max_age_years": 3,
        "description": "Passenger vehicles (cars, SUVs, pickups, motorcycles)",
    },
    "commercial": {
        "vehicle_types": {"van"},
        "max_age_years": 5,
        "description": "Public passenger transport and goods vehicles",
    },
    "three_wheeler": {
        "vehicle_types": {"three_wheeler"},
        "max_age_years": 3,
        "description": "Three-wheelers (tuk-tuks) — electric only",
    },
}

# ── Fuel type restrictions by vehicle type ────────────────────────────────────

FUEL_RESTRICTIONS = {
    "three_wheeler": {
        "allowed_fuel_types": {"electric"},
        "reason": "Petrol and diesel three-wheelers are prohibited under the "
                  "2025 gazette. Only electric three-wheelers may be imported.",
    },
}

# ── General conditions (apply to every import) ───────────────────────────────

GENERAL_CONDITIONS = {
    "drive_configuration": {
        "required": "RHD",
        "reason": "Sri Lanka is a left-hand traffic country. LHD vehicles "
                  "are not permitted.",
    },
    "emissions_standard": {
        "required": "Euro 6",
        "applies_to": {"petrol", "diesel"},
        "reason": "Petrol and diesel vehicles must meet Euro 6 or higher. "
                  "Euro 4/5 vehicles are no longer accepted.",
    },
    "minimum_airbags": {
        "count": 2,
        "reason": "Minimum 2 airbags mandatory for all imported vehicles.",
    },
    "abs_required": {
        "required": True,
        "reason": "Anti-lock Braking System (ABS) is mandatory.",
    },
    "esc_required": {
        "required": True,
        "reason": "Electronic Stability Control (ESC) is mandatory.",
    },
    "ev_battery_warranty": {
        "min_years": 5,
        "min_km": 100_000,
        "applies_to": {"electric", "petrol_hybrid"},
        "reason": "EV and hybrid battery must carry a manufacturer warranty "
                  "of at least 5 years or 100,000 km.",
    },
    "import_frequency": {
        "max_per_year": 1,
        "applies_to": "individual",
        "reason": "Private individuals (non-registered importers) are limited "
                  "to one vehicle per 12-month period.",
    },
    "registration_deadline_days": 90,
    "late_registration_penalty_pct_per_month": 3.0,
    "late_registration_penalty_cap_pct": 45.0,
}

# ── Importer categories ───────────────────────────────────────────────────────

IMPORTER_TYPES = {
    "individual": {
        "description": "Private individual (non-registered importer)",
        "max_vehicles_per_year": 1,
        "duty_concession": False,
    },
    "registered_importer": {
        "description": "DMT-registered vehicle dealer / importer",
        "max_vehicles_per_year": None,   # unrestricted
        "duty_concession": False,
    },
    "diplomatic": {
        "description": "Accredited diplomat or embassy / consular staff",
        "max_vehicles_per_year": None,
        "duty_concession": True,         # Vienna Convention duty-free
    },
    "state_institution": {
        "description": "Government or state institution",
        "max_vehicles_per_year": None,
        "duty_concession": False,
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_age_limit(vehicle_type: str) -> int:
    """Return the maximum allowed age (years) for a given vehicle type."""
    for category in VEHICLE_CATEGORY_AGE_LIMITS.values():
        if vehicle_type in category["vehicle_types"]:
            return category["max_age_years"]
    raise KeyError(
        f"Unknown vehicle type '{vehicle_type}'. "
        f"Valid types: {sorted(VEHICLE_TYPES)}"
    )


def get_allowed_fuels(vehicle_type: str) -> set:
    """Return the set of allowed fuel types for a vehicle type."""
    if vehicle_type in FUEL_RESTRICTIONS:
        return FUEL_RESTRICTIONS[vehicle_type]["allowed_fuel_types"]
    return FUEL_TYPES  # no restriction — all fuel types allowed


def is_origin_allowed(origin: str) -> bool:
    """Return True if the origin country is an approved RHD source market."""
    return origin.lower() in ALLOWED_ORIGINS
