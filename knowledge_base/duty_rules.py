"""
Sri Lanka vehicle import duty and tax rules.

Sources:
  - Sri Lanka Customs National Imports Tariff Guide 2025, Chapter 87 (HS 8703)
    customs.gov.lk/wp-content/uploads/2025/02/Tariff-2022-Chapter-87-Final-1.pdf
  - Gazette Extraordinary No. 2421/43 (31 Jan 2025) — CID surcharge
  - Gazette Extraordinary No. 2421/44 (01 Feb 2025) — import control
  - Gazette Notifications 2418/43 and 2421/42 — excise duty rates
  - Gazette Extraordinary No. 2421/41 — luxury tax threshold revision
  - Gazette 2434/04 (28 Apr 2025) — series hybrid EV excise rates

Tax cascade order:
  1. CIF (purchase price + shipping + insurance)
  2. Customs Import Duty (CID)  = 20% of CIF
  3. CID Surcharge              = 50% of CID  (effective through Jan 2026)
  4. Excise Duty                = LKR/cc × engine_cc  (or LKR/kW × motor_kw for EVs)
  5. Luxury Tax                 = rate × max(0, CIF − threshold)
  6. VAT                        = 18% × (CIF + CID + CID Surcharge + Excise + Luxury Tax)
  7. PAL                        = EXEMPT for HS 8703
  8. SSCL                       = EXEMPT under current 2025 tariff guide *

  * Budget 2026 proposals may re-apply SSCL at 2.5% on CIF. Verify against the
    latest gazette before use in a production system.

NOTE ON SERIES HYBRIDS (Nissan Note e-Power, Honda e:HEV series-only):
  These fall under HS 8703.80 (series hybrid EV) in the 2025 gazette, using
  per-kW EV rates — NOT the standard petrol_hybrid per-cc rates.
  For simplicity this system treats Note e-Power as petrol_hybrid (HEV).
  A production system should add a separate "series_hybrid" fuel type.
"""

# ── Flat rates ────────────────────────────────────────────────────────────────

CUSTOMS_DUTY_RATE     = 0.20   # 20 % of CIF
CID_SURCHARGE_RATE    = 0.50   # 50 % on top of CID (expires 31 Jan 2026)
VAT_RATE              = 0.18   # 18 % on (CIF + CID + surcharge + excise + luxury)
PAL_RATE              = 0.00   # Exempt for HS 8703 motor vehicles
SSCL_RATE             = 0.00   # Exempt under current 2025 tariff guide

# Fallback exchange rate — used only when the user does not supply one.
# Engine 3 will prefer the usd_to_lkr field from ImportRequest and log a
# warning when it falls back to this value.
USD_TO_LKR_DEFAULT    = 320.0

# ── Excise duty bands — LKR per cm³ ──────────────────────────────────────────
# Each band: (cc_min_exclusive, cc_max_inclusive, lkr_per_cc)
# First band cc_min = 0 (i.e. 0 < cc ≤ first cc_max, but also covers cc = 0
# which won't be used since 0-cc vehicles are electric and use kW rates).

PETROL_EXCISE_BANDS = [
    (    0, 1000, 2_450),
    ( 1000, 1300, 3_850),
    ( 1300, 1500, 4_450),
    ( 1500, 1600, 5_150),
    ( 1600, 1800, 6_400),
    ( 1800, 2000, 7_700),
    ( 2000, 2500, 8_450),
    ( 2500, 2750, 9_650),
    ( 2750, 3000, 10_850),
    ( 3000, 4000, 12_050),
    ( 4000, 9999, 13_300),
]

DIESEL_EXCISE_BANDS = [
    (    0, 1500, 5_550),
    ( 1500, 1600, 6_950),
    ( 1600, 1800, 8_300),
    ( 1800, 2000, 9_650),
    ( 2000, 2500, 9_650),
    ( 2500, 2750, 10_850),
    ( 2750, 3000, 12_050),
    ( 3000, 4000, 13_300),
    ( 4000, 9999, 14_500),
]

# Self-charging petrol HEV (HS 8703.40) and petrol PHEV (HS 8703.60) share
# the same rates. No band for ≤1000 cc — kei hybrids (660 cc) are covered
# by the first band shown (≤1000 treated as 0–1000).
PETROL_HYBRID_EXCISE_BANDS = [
    (    0, 1000, 2_750),   # kei hybrids (e.g. 660 cc Wagon R Hybrid)
    ( 1000, 1300, 2_750),
    ( 1300, 1500, 3_450),
    ( 1500, 1600, 4_800),
    ( 1600, 1800, 6_300),
    ( 1800, 2000, 6_900),
    ( 2000, 2500, 7_250),
    ( 2500, 2750, 8_450),
    ( 2750, 3000, 9_650),
    ( 3000, 4000, 10_850),
    ( 4000, 9999, 12_050),
]

EXCISE_BANDS = {
    "petrol":        PETROL_EXCISE_BANDS,
    "diesel":        DIESEL_EXCISE_BANDS,
    "petrol_hybrid": PETROL_HYBRID_EXCISE_BANDS,
}

# ── EV excise duty — LKR per kW ──────────────────────────────────────────────
# Source: Gazette 2418/43 + 2434/04 (series hybrid).
# Age bands: "new" = ≤1 year old, "used" = 1–3 years old (>3 years not importable)
# Structure: fuel_sub_type → age_band → list of (kw_min, kw_max, lkr_per_kw)

EV_EXCISE_BANDS = {

    # BEV — fully electric, charged from external source (e.g. Nissan Leaf, bZ4X)
    "bev": {
        "new": [   # vehicle age ≤ 1 year
            (  0,  50, 18_100),
            ( 50, 100, 24_100),
            (100, 200, 36_200),
            (200, 999, 96_600),
        ],
        "used": [  # vehicle age 1–3 years
            (  0,  50, 36_200),
            ( 50, 100, 36_200),
            (100, 200, 64_400),
            (200, 999, 132_800),
        ],
    },

    # Series hybrid EV — petrol engine for charging only, wheels driven electrically
    # (e.g. Nissan Note e-Power). Rates from Gazette 2434/04.
    "series_hybrid": {
        "new": [
            (  0,  50, 30_770),
            ( 50, 100, 40_970),
            (100, 200, 41_630),
            (200, 999, 111_090),
        ],
        "used": [
            (  0,  50, 43_440),
            ( 50, 100, 43_440),
            (100, 200, 63_420),
            (200, 999, 139_440),
        ],
    },
}

# ── Luxury tax ────────────────────────────────────────────────────────────────
# Applied on (CIF − threshold) when CIF > threshold.
# Threshold was raised from Rs. 3.5 Mn to Rs. 5.0 Mn effective 1 Feb 2025
# (Gazette 2421/41).

LUXURY_TAX = {
    "petrol":        {"threshold_lkr": 5_000_000, "rate": 1.00},
    "diesel":        {"threshold_lkr": 5_000_000, "rate": 1.20},
    "petrol_hybrid": {"threshold_lkr": 5_500_000, "rate": 0.80},
    "electric":      {"threshold_lkr": 6_000_000, "rate": 0.60},
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def _lookup_cc_band(bands: list, engine_cc: int) -> int:
    """Return LKR/cc rate for a given engine_cc from an excise band list."""
    for cc_min, cc_max, lkr_per_cc in bands:
        if cc_min < engine_cc <= cc_max:
            return lkr_per_cc
    # Fallback for exactly 0 cc (should not happen for ICE/hybrid)
    return bands[0][2]


def _lookup_kw_band(bands: list, motor_kw: int) -> int:
    """Return LKR/kW rate for a given motor_kw from an EV excise band list."""
    for kw_min, kw_max, lkr_per_kw in bands:
        if kw_min <= motor_kw <= kw_max:
            return lkr_per_kw
    return bands[-1][2]


def get_excise_duty_lkr(
    fuel_type: str,
    engine_cc: int,
    motor_kw: int | None,
    vehicle_age_years: float,
) -> float:
    """
    Return total excise duty in LKR.

    For petrol / diesel / petrol_hybrid: rate (LKR/cc) × engine_cc.
    For electric: rate (LKR/kW) × motor_kw using the BEV age band.
    """
    if fuel_type == "electric":
        if motor_kw is None:
            raise ValueError("motor_kw is required for electric vehicles")
        age_band = "new" if vehicle_age_years <= 1 else "used"
        bands = EV_EXCISE_BANDS["bev"][age_band]
        rate = _lookup_kw_band(bands, motor_kw)
        return float(rate * motor_kw)

    bands = EXCISE_BANDS.get(fuel_type)
    if bands is None:
        raise ValueError(f"Unknown fuel_type '{fuel_type}'")
    rate = _lookup_cc_band(bands, engine_cc)
    return float(rate * engine_cc)


def get_luxury_tax_lkr(fuel_type: str, cif_lkr: float) -> float:
    """Return luxury tax in LKR (0 if CIF is below threshold)."""
    rule = LUXURY_TAX.get(fuel_type)
    if rule is None:
        raise ValueError(f"Unknown fuel_type '{fuel_type}'")
    excess = cif_lkr - rule["threshold_lkr"]
    return float(excess * rule["rate"]) if excess > 0 else 0.0
