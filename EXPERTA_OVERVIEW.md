# How Experta Is Used in This Project

## The Core Idea: Working Memory + Rules

Experta is a **forward-chaining rule engine** for Python. It works like this:

1. You put **facts** into a "working memory" (the engine's fact store)
2. Rules watch for matching patterns in working memory
3. When a pattern matches, the rule **fires** — it can read data, do calculations, and assert new facts
4. New facts can trigger more rules — this chain continues until nothing new can fire

Think of it as: **facts in → rules fire → more facts out**

---

## The Three Building Blocks

### 1. Facts — `facts.py`

Facts are just Python classes that extend `Fact`. They hold data, nothing else:

```python
class ImportRequest(Fact):
    pass  # fields set at declare time, not at class definition

class EligibilityResult(Fact):
    pass

class RuleFired(Fact):
    pass
```

A `Fact` works like a dict — you set fields when you declare it:
```python
engine.declare(ImportRequest(vehicle_type="car", budget_usd=20000))
```

And read them with `fact["field"]` or `fact.get("field", default)`.

### 2. KnowledgeEngine — the engine classes

Each engine is a class that extends `KnowledgeEngine`. The engine owns the working memory and all the rules:

```python
class EligibilityEngine(KnowledgeEngine):
    @Rule(...)
    def check_origin(self, origin):
        ...
```

You use it like this (from `main.py`):
```python
engine = EligibilityEngine()
engine.reset()                          # clear working memory
engine.declare(ImportRequest(**data))   # put input fact in
engine.run()                            # fire rules until done
result = next(f for f in engine.facts.values() if isinstance(f, EligibilityResult))
```

### 3. Rules — the `@Rule` decorator

A `@Rule` has two parts: a **pattern** (what facts must exist) and a **body** (what to do when they match).

---

## How the Pattern Matching Works

```python
@Rule(
    ImportRequest(origin_country=MATCH.origin),  # pattern
    salience=80,
)
def check_origin(self, origin):                  # origin is bound from the pattern
    if not is_origin_allowed(origin):
        self.declare(EligibilityResult(eligible=False, ...))
        self.halt()
```

- `MATCH.origin` — captures the value of `origin_country` from the `ImportRequest` fact and passes it to the function as `origin`
- `TEST(lambda price, budget: price <= budget)` — a boolean condition; the rule only fires if this returns `True`
- `NOT(EligibilityResult())` — the rule only fires if NO `EligibilityResult` fact exists yet

---

## Salience = Priority

Rules fire highest-salience first. In the eligibility engine:

| Salience | Rule | Purpose |
|---|---|---|
| 80 | `check_origin` | First check — if origin is wrong, halt immediately |
| 75 | `check_vehicle_type` | Second check |
| 70 | `check_age` | Third check |
| 65 | `check_fuel_restriction` | Fourth check |
| 60 | `check_euro6` | Fifth check |
| 55 | `check_airbags` | Sixth check |
| 54 | `check_abs` | Seventh check |
| 53 | `check_esc` | Eighth check |
| 50 | `check_battery_warranty` | Ninth check |
| 10 | `all_checks_passed` | Only fires if nothing above asserted a failure |

`self.halt()` stops all further rule execution — this is how failing fast works. If origin is invalid, none of the lower-salience rules (age, safety, etc.) ever run.

---

## How Each Engine Uses This Pattern

### Engine 1 (Eligibility) — linear pipeline

```
ImportRequest declared
→ check_origin fires (salience 80)
→ check_vehicle_type fires (75)
→ ...
→ all_checks_passed fires (10) only if no EligibilityResult yet
```

One `ImportRequest` in → one `EligibilityResult` out.

### Engine 2 (Selector) — fan-out then fan-in

```
ImportRequest declared
→ load_candidates (salience 100): declares 105 VehicleCandidate facts
→ score_candidate (salience 50): fires ONCE PER VehicleCandidate that matches
  the budget/fuel/brand/type TESTsasserts one VehicleScore per match
→ finalize_recommendations (salience 10): reads all VehicleScores, sorts,
  declares top-N as Recommendation facts
```

One `ImportRequest` in → N `Recommendation` facts out.

Scoring formula (0.0 – 1.0):
- 35% resale_score (local resale value retention, 1–10 scale)
- 35% popularity (local market demand, 1–10 scale)
- 30% price_fit = `max(0, (budget − price) / budget)`
- +0.05 bonus if fuel_type matches fuel_preference
- +0.05 bonus if make matches brand_preference

### Engine 3 (Cost) — two-step calculation

```
ImportRequest declared
→ load_duty_rate (salience 100): looks up excise/customs rates, declares DutyRate
→ compute_total_cost (salience 50): applies the full duty cascade, declares CostBreakdown
```

Duty cascade:
1. CIF = purchase price + sea freight + marine insurance
2. CID = 20% of CIF
3. CID surcharge = 50% of CID
4. Excise duty = LKR/cc × engine_cc (or LKR/kW × motor_kw for EVs)
5. Luxury tax = rate × max(0, CIF_LKR − threshold)
6. VAT = 18% × (CIF + CID + surcharge + excise + luxury tax)
7. Port charges (THC, SLPA wharfage, D/O, clearing agent)
8. JAAI inspection fee (Japan-origin only)

---

## The RuleFired Audit Trail

Every rule — whether it passes or rejects — declares a `RuleFired` fact:

```python
self.declare(RuleFired(
    engine="eligibility",
    rule="check_origin",
    note="Origin 'germany' rejected — not in approved origin list.",
))
```

After `engine.run()`, `main.py` collects these:
```python
def _trail(engine) -> list[str]:
    return [f["note"] for f in engine.facts.values() if isinstance(f, RuleFired)]
```

This becomes the `trail` array in every API response — the human-readable explanation of every decision the engine made, in order.

---

## The Full Data Flow

```
HTTP POST /all
    │
    ▼
AllEnginesRequest (Pydantic validates input)
    │
    ├─► EligibilityEngine.declare(ImportRequest)
    │        rules fire → EligibilityResult + RuleFired trail
    │
    ├─► SelectorEngine.declare(ImportRequest)
    │        rules fire → VehicleCandidate × 105
    │                   → VehicleScore × N (matching only)
    │                   → Recommendation × top_n
    │
    └─► CostEngine.declare(ImportRequest)  ← inputs come from top Recommendation
             rules fire → DutyRate
                        → CostBreakdown
```
