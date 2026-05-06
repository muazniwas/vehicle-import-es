"""
Non-duty cost factors for the Sri Lanka vehicle import total landed cost.

Covers: sea freight, marine insurance, port charges, JAAI inspection,
and DMT first registration fees.

Sources:
  - JDA Cars (Japan → Colombo RoRo, USD 60/m³):
      jdacars.com/shipping-cost.php
  - Fastlane Forwarding (UK → Sri Lanka FCL rates):
      fastlanefwd.co.uk/fcl_and_lcl_container_shipping_sri_lanka.html
  - Globy / Flexport (Singapore → Colombo indicative FCL/LCL):
      globy.com; flexport.com
  - MoveHub (Australia → Sri Lanka car shipping):
      movehub.com/au/international-shipping/sri-lanka/
  - ProvideCars fee schedule (marine insurance 0.5%):
      providecars.co.jp/bank-info/service-and-commission/
  - YQN port THC comparison (Colombo USD 120–170 / 20 ft):
      resources.yqn.com/compare-terminal-handling-charges-ports
  - SLPA Tariff 2026 (stevedorage, wharfage, occupation):
      slpa.lk/port-colombo/tariff
  - Maersk / Hapag-Lloyd Sri Lanka local charges (D/O fee)
  - AuctionHouseJapan (JAAI fee ¥7,560–¥9,720):
      auctionhousejapan.jp/srilanka/certification/
  - DMT Sri Lanka — Charges for First Registration (official):
      dmt.gov.lk/index.php?option=com_content&view=article&id=39

All USD figures are mid-2025 market-level indicatives (±20% tolerance).
Freight rates are volatile; treat as approximations.
"""

# ── Sea freight (port-to-port, USD) ──────────────────────────────────────────
# Japan ships almost exclusively RoRo at ~USD 60/m³.
# UK, Singapore, Australia ship in 20 ft FCL containers.
# "small" = saloon / hatchback / small SUV (≤ 9.5 m³ / fits 20 ft)
# "large" = full-size SUV / van / pickup (> 9.5 m³ / needs 40 ft or larger slot)

SHIPPING_COSTS_USD = {
    "japan": {
        "small": 550,    # 9.5 m³ × USD 60 = USD 570 → rounded to 550
        "large": 1150,   # 19 m³ × USD 60 = USD 1,140 → rounded to 1,150
    },
    "uk": {
        "small": 2200,   # 20 ft FCL, GBP 1,500–2,000 → midpoint ~USD 2,200
        "large": 2800,   # 40 ft FCL, GBP 2,000–2,500 → midpoint ~USD 2,800
    },
    "singapore": {
        "small": 1400,   # 20 ft FCL indicative, USD 1,100–1,700 → midpoint
        "large": 1600,   # slight premium for heavier / bulkier vehicle
    },
    "australia": {
        "small": 2150,   # 20 ft FCL port-to-port, AUD 3,200–3,500 → ~USD 2,150
        "large": 3250,   # 40 ft / high-cube for vans and pickups
    },
}

# Vehicle types that ship as "large" (all others default to "small")
LARGE_VEHICLE_TYPES = {"suv", "van", "pickup"}

# ── Marine insurance ──────────────────────────────────────────────────────────
# ICC (A) all-risks cover: 0.50 % of (purchase + freight) × 1.10
# The 1.10 multiplier is the standard "CIF + 10 %" insured value convention.

INSURANCE_RATE    = 0.005   # 0.50 % of insured value
INSURANCE_MULTIPLIER = 1.10 # insured value = (purchase + freight) × 1.10
INSURANCE_MIN_USD = 50.0    # floor in USD

# ── Colombo port charges ──────────────────────────────────────────────────────

PORT_CHARGES_USD = {
    # Terminal Handling Charge — paid to shipping line
    "thc_container_20ft": 145,    # Colombo, 20 ft import container, midpoint
    "thc_container_40ft": 245,    # 40 ft import container, midpoint
    "thc_roro_per_vehicle": 115,  # RoRo unit, midpoint of USD 80–150

    # SLPA wharfage — paid to port authority on the container
    "slpa_wharfage_20ft": 32,     # SLPA Tariff 2026 §II Item 43.00
    "slpa_wharfage_40ft": 64,

    # Delivery Order + B/L processing — paid to shipping line/agent
    "documentation": 65,          # D/O + B/L fees, midpoint of USD 50–80

    # Customs clearing agent flat fee (LKR, converted at runtime)
    "clearing_agent_lkr": 25_000, # LKR 25,000 midpoint; ~USD 80 at LKR 315/$
}

# ── JAAI pre-shipment inspection (Japan-origin vehicles only) ─────────────────
# Mandatory for all used vehicles imported to Sri Lanka from Japan.
# Arranged at the Japanese port of departure by the exporter / freight forwarder.

JAAI_FEE_JPY = {
    "kei":      7_560,   # engine ≤ 660 cc
    "standard": 9_720,   # engine > 660 cc
}

# Fallback JPY/USD rate — used only when the user does not supply one.
# Engine 3 will prefer the jpy_to_usd field from ImportRequest.
JPY_TO_USD_RATE_DEFAULT = 1 / 150.0

# ── DMT first registration fees (Sri Lanka, LKR) ─────────────────────────────
# Source: Motor Traffic Fees Regulations No. 04 of 2022
# Includes: registration fee + number plates (LKR 3,300) + inspection (LKR
# 1,000) + documentation (LKR 150). Transfer fee excluded (first registration).

DMT_REGISTRATION_LKR = {
    "car_small":  29_450,  # motor car, engine ≤ 1,600 cc or motor ≤ 80 kW
    "car_large":  44_450,  # motor car, engine > 1,600 cc or motor > 80 kW
    "suv_small":  24_450,  # dual purpose vehicle, engine ≤ 1,000 cc or ≤ 50 kW
    "suv_large":  29_450,  # dual purpose vehicle, engine > 1,000 cc or > 50 kW
    "van":        29_450,  # treated as dual purpose (large)
    "pickup":     29_450,  # treated as dual purpose (large)
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_shipping_usd(origin: str, vehicle_type: str) -> float:
    """Return port-to-port sea freight cost in USD."""
    size = "large" if vehicle_type in LARGE_VEHICLE_TYPES else "small"
    return float(SHIPPING_COSTS_USD[origin][size])


def get_insurance_usd(purchase_price_usd: float, freight_usd: float) -> float:
    """Return marine insurance premium in USD."""
    insured_value = (purchase_price_usd + freight_usd) * INSURANCE_MULTIPLIER
    premium = insured_value * INSURANCE_RATE
    return float(max(premium, INSURANCE_MIN_USD))


def get_port_charges_usd(
    origin: str,
    vehicle_type: str,
    usd_to_lkr: float,
) -> float:
    """
    Return total Colombo port charges in USD.

    Includes THC, SLPA wharfage, documentation, and clearing agent fee.
    RoRo (Japan) and container (others) are handled separately.
    """
    c = PORT_CHARGES_USD
    if origin == "japan":
        thc       = c["thc_roro_per_vehicle"]
        wharfage  = 0.0   # SLPA stevedorage absorbed in RoRo THC for simplicity
    else:
        size     = "large" if vehicle_type in LARGE_VEHICLE_TYPES else "small"
        thc      = c["thc_container_40ft"] if size == "large" else c["thc_container_20ft"]
        wharfage = c["slpa_wharfage_40ft"] if size == "large" else c["slpa_wharfage_20ft"]

    docs          = c["documentation"]
    clearing_usd  = c["clearing_agent_lkr"] / usd_to_lkr
    return float(thc + wharfage + docs + clearing_usd)


def get_jaai_fee_usd(engine_cc: int) -> float:
    """Return JAAI inspection fee in USD (Japan-origin only)."""
    jpy = JAAI_FEE_JPY["kei"] if engine_cc <= 660 else JAAI_FEE_JPY["standard"]
    return float(jpy * JPY_TO_USD_RATE_DEFAULT)


def get_registration_lkr(vehicle_type: str, engine_cc: int) -> float:
    """Return DMT first registration fee in LKR."""
    if vehicle_type == "car":
        key = "car_small" if engine_cc <= 1600 else "car_large"
    elif vehicle_type == "suv":
        key = "suv_small" if engine_cc <= 1000 else "suv_large"
    else:
        key = vehicle_type   # "van" or "pickup"
    return float(DMT_REGISTRATION_LKR[key])
