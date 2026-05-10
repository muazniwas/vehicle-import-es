import sys
sys.path.insert(0, ".")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    EligibilityRequest, EligibilityResponse,
    SelectorRequest, SelectorResponse, RecommendationItem,
    CostRequest, CostResponse,
    AllEnginesRequest, AllEnginesResponse,
)
from facts import (
    ImportRequest,
    EligibilityResult,
    Recommendation,
    VehicleScore,
    CostBreakdown,
    RuleFired,
)
from engines.eligibility_engine import EligibilityEngine
from engines.selector_engine import SelectorEngine
from engines.cost_engine import CostEngine

app = FastAPI(
    title="Sri Lanka Vehicle Import Expert System",
    description=(
        "Expert system for Sri Lanka vehicle import eligibility checking, "
        "vehicle recommendation, and landed cost estimation. "
        "Based on Gazette Extraordinary No. 2421/44 (1 February 2025)."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Private runner helpers ────────────────────────────────────────────────────

def _facts_from(data: dict) -> dict:
    """Drop None values so optional ImportRequest fields remain unset."""
    return {k: v for k, v in data.items() if v is not None}


def _trail(engine) -> list[str]:
    return [f["note"] for f in engine.facts.values() if isinstance(f, RuleFired)]


def _run_eligibility(data: dict) -> EligibilityResponse:
    engine = EligibilityEngine()
    engine.reset()
    engine.declare(ImportRequest(**_facts_from(data)))
    engine.run()

    result = next(
        (f for f in engine.facts.values() if isinstance(f, EligibilityResult)),
        None,
    )
    if result is None:
        raise HTTPException(status_code=500, detail="Eligibility engine produced no result.")

    return EligibilityResponse(
        eligible=result["eligible"],
        reason=result["reason"],
        rule_fired=result["rule_fired"],
        trail=_trail(engine),
    )


def _run_selector(data: dict) -> SelectorResponse:
    engine = SelectorEngine()
    engine.reset()
    engine.declare(ImportRequest(**_facts_from(data)))
    engine.run()

    recs = sorted(
        (f for f in engine.facts.values() if isinstance(f, Recommendation)),
        key=lambda f: f["rank"],
    )
    matched = len([f for f in engine.facts.values() if isinstance(f, VehicleScore)])

    return SelectorResponse(
        matched_count=matched,
        recommendations=[
            RecommendationItem(
                rank=r["rank"],
                make=r["make"],
                model=r["model"],
                vehicle_type=r["vehicle_type"],
                engine_cc=r["engine_cc"],
                fuel_type=r["fuel_type"],
                motor_kw=r["motor_kw"],
                typical_price_usd=r["typical_price_usd"],
                fit_score=r["fit_score"],
                reason=r["reason"],
            )
            for r in recs
        ],
        trail=_trail(engine),
    )


def _run_cost(data: dict) -> CostResponse:
    engine = CostEngine()
    engine.reset()
    engine.declare(ImportRequest(**_facts_from(data)))
    engine.run()

    cb = next(
        (f for f in engine.facts.values() if isinstance(f, CostBreakdown)),
        None,
    )
    if cb is None:
        trail = _trail(engine)
        detail = trail[-1] if trail else "Cost engine produced no result."
        raise HTTPException(status_code=422, detail=detail)

    return CostResponse(
        purchase_price_usd=cb["purchase_price_usd"],
        shipping_usd=cb["shipping_usd"],
        insurance_usd=cb["insurance_usd"],
        jaai_usd=cb["jaai_usd"],
        cif_usd=cb["cif_usd"],
        cid_usd=cb["cid_usd"],
        cid_surcharge_usd=cb["cid_surcharge_usd"],
        excise_duty_usd=cb["excise_duty_usd"],
        luxury_tax_usd=cb["luxury_tax_usd"],
        vat_usd=cb["vat_usd"],
        port_charges_usd=cb["port_charges_usd"],
        total_usd=cb["total_usd"],
        total_lkr=cb["total_lkr"],
        registration_lkr=cb["registration_lkr"],
        grand_total_lkr=cb["grand_total_lkr"],
        trail=_trail(engine),
    )


# ── Routes ────────────────────────────────────────────────────────────────────

@app.post("/eligibility", response_model=EligibilityResponse)
def check_eligibility(req: EligibilityRequest):
    """Check whether a vehicle meets Sri Lanka import eligibility rules."""
    return _run_eligibility(req.model_dump())


@app.post("/selector", response_model=SelectorResponse)
def select_vehicle(req: SelectorRequest):
    """Recommend the best vehicles to import within the given budget and preferences."""
    return _run_selector(req.model_dump())


@app.post("/cost", response_model=CostResponse)
def estimate_cost(req: CostRequest):
    """Estimate the full landed cost of importing a specific vehicle to Sri Lanka."""
    return _run_cost(req.model_dump())


@app.post("/all", response_model=AllEnginesResponse)
def run_all_engines(req: AllEnginesRequest):
    """
    Run all three engines in sequence.

    Engine 2 uses fuel_type as the fuel_preference.
    Engine 3 is skipped if eligibility fails or no vehicles match.
    When Engine 3 runs, its vehicle spec comes from the top recommendation
    returned by Engine 2 — only exchange rates are taken from the request.
    """
    data = req.model_dump()

    eligibility = _run_eligibility(data)

    selector_data = {
        "vehicle_type": data["vehicle_type"],
        "budget_usd": data["budget_usd"],
        "fuel_preference": data["fuel_type"],
        "brand_preference": data["brand_preference"],
    }
    selector = _run_selector(selector_data)

    cost = None
    if eligibility.eligible and selector.recommendations:
        top = selector.recommendations[0]
        cost_data: dict = {
            "vehicle_type": top.vehicle_type,
            "manufacture_year": data["manufacture_year"],
            "manufacture_month": data["manufacture_month"],
            "bill_of_lading_year": data["bill_of_lading_year"],
            "bill_of_lading_month": data["bill_of_lading_month"],
            "origin_country": data["origin_country"],
            "fuel_type": top.fuel_type,
            "engine_cc": top.engine_cc,
            "purchase_price_usd": top.typical_price_usd,
        }
        if top.motor_kw is not None:
            cost_data["motor_kw"] = top.motor_kw
        if data.get("importer_type"):
            cost_data["importer_type"] = data["importer_type"]
        if data.get("usd_to_lkr") is not None:
            cost_data["usd_to_lkr"] = data["usd_to_lkr"]
        if data.get("jpy_to_usd") is not None:
            cost_data["jpy_to_usd"] = data["jpy_to_usd"]
        cost = _run_cost(cost_data)

    return AllEnginesResponse(
        eligibility=eligibility,
        selector=selector,
        cost=cost,
    )
