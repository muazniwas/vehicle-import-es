"""
Engine 2 — Best Vehicle Selector.

Loads all vehicle models from vehicle_db as VehicleCandidate facts, scores
each one against the user's preferences (budget, fuel type, brand), and
asserts the top 3 as Recommendation facts ranked by fit score.

Scoring formula (0.0 – 1.0):
    35 %  resale_score  — local resale value retention (1–10 scale)
    35 %  popularity    — local market demand (1–10 scale)
    30 %  price_fit     = max(0, (budget − price) / budget)

Bonuses (each +0.05, total capped at 1.0):
    +0.05 if fuel_type exactly matches fuel_preference (not "any")
    +0.05 if make matches brand_preference case-insensitively (not "any")

ImportRequest fields used here:
    budget_usd        float
    fuel_preference   str   "petrol" | "diesel" | "petrol_hybrid"
                             | "electric" | "any"
    brand_preference  str   e.g. "toyota" | "any"
"""

from experta import KnowledgeEngine, Rule, NOT, MATCH, TEST

from facts import (
    ImportRequest,
    VehicleCandidate,
    VehicleScore,
    Recommendation,
    RuleFired,
)
from knowledge_base.vehicle_db import VEHICLES


class SelectorEngine(KnowledgeEngine):

    # ── 1. Load all vehicles as VehicleCandidate facts ───────────────────────

    @Rule(
        ImportRequest(
            budget_usd=MATCH.budget,
            fuel_preference=MATCH.fuel_pref,
            brand_preference=MATCH.brand_pref,
            vehicle_type=MATCH.vtype,
        ),
        salience=100,
    )
    def load_candidates(self, budget, fuel_pref, brand_pref, vtype):
        for v in VEHICLES:
            self.declare(VehicleCandidate(**v))
        self.declare(RuleFired(
            engine="selector",
            rule="load_candidates",
            note=(
                f"Loaded {len(VEHICLES)} vehicles from catalogue. "
                f"Filters — budget: USD {budget:,.0f}, "
                f"fuel: {fuel_pref}, brand: {brand_pref}, "
                f"vehicle type: {vtype}."
            ),
        ))

    # ── 2. Score each candidate that fits the filters ────────────────────────

    @Rule(
        ImportRequest(
            budget_usd=MATCH.budget,
            fuel_preference=MATCH.fuel_pref,
            brand_preference=MATCH.brand_pref,
            vehicle_type=MATCH.vtype,
        ),
        VehicleCandidate(
            make=MATCH.make,
            model=MATCH.model,
            fuel_type=MATCH.fuel,
            vehicle_type=MATCH.vtype_candidate,
            typical_price_usd=MATCH.price,
            resale_score=MATCH.resale,
            popularity=MATCH.pop,
        ),
        TEST(lambda price, budget: price <= budget),
        TEST(lambda fuel, fuel_pref: fuel_pref == "any" or fuel == fuel_pref),
        TEST(lambda make, brand_pref: (
            brand_pref == "any" or make.lower() == brand_pref.lower()
        )),
        TEST(lambda vtype_candidate, vtype: (
            vtype == "any" or vtype_candidate == vtype
        )),
        salience=50,
    )
    def score_candidate(
        self, budget, fuel_pref, brand_pref, vtype,
        make, model, fuel, vtype_candidate, price, resale, pop,
    ):
        price_fit = max(0.0, (budget - price) / budget)
        score = (
            0.35 * (resale / 10.0)
            + 0.35 * (pop / 10.0)
            + 0.30 * price_fit
        )
        if fuel_pref != "any" and fuel == fuel_pref:
            score = min(1.0, score + 0.05)
        if brand_pref != "any" and make.lower() == brand_pref.lower():
            score = min(1.0, score + 0.05)

        self.declare(VehicleScore(make=make, model=model, score=round(score, 4)))
        self.declare(RuleFired(
            engine="selector",
            rule="score_candidate",
            note=(
                f"{make} {model} — score {score:.3f} "
                f"(resale={resale}/10, pop={pop}/10, "
                f"price_fit={price_fit:.2f})"
            ),
        ))

    # ── 3a. Assert top-3 recommendations ────────────────────────────────────

    @Rule(
        ImportRequest(),
        VehicleScore(),
        NOT(Recommendation()),
        salience=10,
    )
    def finalize_recommendations(self):
        scores = sorted(
            (f for f in self.facts.values() if isinstance(f, VehicleScore)),
            key=lambda f: f["score"],
            reverse=True,
        )
        candidates = {
            (f["make"], f["model"]): f
            for f in self.facts.values()
            if isinstance(f, VehicleCandidate)
        }

        for rank, vs in enumerate(scores[:3], start=1):
            vc = candidates.get((vs["make"], vs["model"]))
            if vc is None:
                continue
            self.declare(Recommendation(
                rank=rank,
                make=vs["make"],
                model=vs["model"],
                vehicle_type=vc["vehicle_type"],
                engine_cc=vc["engine_cc"],
                fuel_type=vc["fuel_type"],
                motor_kw=vc["motor_kw"],
                typical_price_usd=vc["typical_price_usd"],
                fit_score=vs["score"],
                reason=(
                    f"Rank {rank} of {len(scores)} matches — "
                    f"fit score {vs['score']:.3f}: "
                    f"resale {vc['resale_score']}/10, "
                    f"popularity {vc['popularity']}/10, "
                    f"price USD {vc['typical_price_usd']:,.0f}"
                ),
            ))

        self.declare(RuleFired(
            engine="selector",
            rule="finalize_recommendations",
            note=(
                f"Top {min(3, len(scores))} recommendations selected "
                f"from {len(scores)} matching vehicles."
            ),
        ))

    # ── 3b. No vehicles matched the filters ──────────────────────────────────

    @Rule(
        ImportRequest(),
        NOT(VehicleScore()),
        NOT(Recommendation()),
        salience=5,
    )
    def no_candidates_found(self):
        self.declare(RuleFired(
            engine="selector",
            rule="no_candidates_found",
            note=(
                "No vehicles matched the search criteria. "
                "Try increasing budget, or set fuel/brand preference to 'any'."
            ),
        ))
