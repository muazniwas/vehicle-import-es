from typing import Optional
from pydantic import BaseModel


# ── Request models ────────────────────────────────────────────────────────────

class EligibilityRequest(BaseModel):
    vehicle_type: str
    manufacture_year: int
    manufacture_month: int
    bill_of_lading_year: int
    bill_of_lading_month: int
    origin_country: str
    fuel_type: str
    euro6_compliant: bool
    has_min_airbags: bool
    has_abs: bool
    has_esc: bool
    has_battery_warranty: bool


class SelectorRequest(BaseModel):
    vehicle_type: str = "any"
    budget_usd: float
    fuel_preference: str = "any"
    brand_preference: str = "any"
    top_n: int = 3


class CostRequest(BaseModel):
    vehicle_type: str
    manufacture_year: int
    manufacture_month: int
    bill_of_lading_year: int
    bill_of_lading_month: int
    origin_country: str
    fuel_type: str
    engine_cc: int
    motor_kw: Optional[int] = None
    purchase_price_usd: float
    usd_to_lkr: Optional[float] = None
    jpy_to_usd: Optional[float] = None


class AllEnginesRequest(EligibilityRequest):
    # Selector fields (fuel_preference is derived from fuel_type)
    budget_usd: float
    brand_preference: str = "any"
    # Exchange rates for Engine 3 (cost data comes from top recommendation)
    usd_to_lkr: Optional[float] = None
    jpy_to_usd: Optional[float] = None


# ── Response models ───────────────────────────────────────────────────────────

class EligibilityResponse(BaseModel):
    eligible: bool
    reason: str
    rule_fired: str
    trail: list[str]


class RecommendationItem(BaseModel):
    rank: int
    make: str
    model: str
    vehicle_type: str
    engine_cc: int
    fuel_type: str
    motor_kw: Optional[int] = None
    typical_price_usd: float
    fit_score: float
    reason: str


class SelectorResponse(BaseModel):
    matched_count: int
    recommendations: list[RecommendationItem]
    trail: list[str]


class CostResponse(BaseModel):
    purchase_price_usd: float
    shipping_usd: float
    insurance_usd: float
    jaai_usd: float
    cif_usd: float
    cid_usd: float
    cid_surcharge_usd: float
    excise_duty_usd: float
    luxury_tax_usd: float
    vat_usd: float
    port_charges_usd: float
    total_usd: float
    total_lkr: float
    registration_lkr: float
    grand_total_lkr: float
    trail: list[str]


class AllEnginesResponse(BaseModel):
    eligibility: EligibilityResponse
    selector: SelectorResponse
    cost: Optional[CostResponse] = None
