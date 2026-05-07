# Sri Lanka Vehicle Import Expert System

A rule-based expert system that advises on vehicle importation into Sri Lanka. Built with [Experta](https://experta.readthedocs.io/) (forward-chaining inference), FastAPI, and a vanilla-JS web UI.

Regulations are based on **Gazette Extraordinary No. 2421/44 (1 February 2025)** and associated Sri Lankan customs/excise instruments.

---

## Architecture

The system is composed of three independent inference engines, each backed by a knowledge base module and exposed via a REST API:

```
vehicle-import-es/
├── main.py                     # FastAPI server (4 routes)
├── facts.py                    # Experta fact definitions
├── schemas.py                  # Pydantic request/response models
├── postman_collection.json     # Example API queries
│
├── engines/
│   ├── eligibility_engine.py   # Engine 1: Import permit validation
│   ├── selector_engine.py      # Engine 2: Vehicle recommendations
│   └── cost_engine.py          # Engine 3: Duty & cost calculation
│
├── knowledge_base/
│   ├── import_regulations.py   # Age limits, origin rules, mandatory features
│   ├── duty_rules.py           # Excise duty bands, VAT, luxury tax, customs duty
│   ├── cost_factors.py         # Freight, insurance, port charges, JAAI, DMT fees
│   └── vehicle_db.py           # 177 vehicle models (Japan, UK, Singapore, Australia)
│
└── ui/
    └── index.html              # Interactive single-page web UI
```

---

## Engines

### Engine 1 — Eligibility Checker (`POST /eligibility`)

Validates whether a vehicle qualifies for an import permit. Rules fire in salience order (highest first); the engine halts on the first failure.

| Rule | Check |
|---|---|
| `check_origin` | Origin must be Japan, UK, Singapore, or Australia |
| `check_vehicle_type` | Vehicle type must be a recognised category |
| `check_age` | Age ≤ 3 years (cars/SUVs/pickups/motorcycles) or ≤ 5 years (vans) |
| `check_fuel_restriction` | Three-wheelers must be electric only |
| `check_euro6` | Petrol/diesel must meet Euro 6 emissions standard |
| `check_airbags` | Minimum 2 airbags (cars/SUVs/vans/pickups) |
| `check_abs` | ABS mandatory (cars/SUVs/vans/pickups/motorcycles) |
| `check_esc` | ESC mandatory (cars/SUVs/vans/pickups) |
| `check_battery_warranty` | EV/hybrid battery warranty ≥ 5 years / 100,000 km |

Response includes a full rule-firing trace (`trail`) for explainability.

---

### Engine 2 — Vehicle Selector (`POST /selector`)

Recommends vehicles from a catalogue of 177 models (Japan, UK, Singapore, Australia) that fit the user's budget and preferences.

Scoring formula per candidate:

```
score = 0.35 × (resale_score / 10)
      + 0.35 × (popularity / 10)
      + 0.30 × max(0, (budget − price) / budget)
      + 0.05  [if fuel preference matched]
      + 0.05  [if brand preference matched]
```

Returns the top N recommendations (default: 3) with score breakdowns.

---

### Engine 3 — Cost Estimator (`POST /cost`)

Calculates the full landed cost in Sri Lanka, including all duties and fees.

Tax cascade applied in order:

```
CIF        = purchase_price + shipping + marine_insurance
CID        = 20% × CIF
Surcharge  = 50% × CID             (effective through Jan 2026)
Excise     = LKR/cc or LKR/kW band (varies by fuel type and engine size)
Luxury Tax = % × CIF               (if CIF exceeds threshold; petrol ≥ 5M LKR)
VAT        = 18% × (CIF + CID + surcharge + excise + luxury)
Port fees  = THC + wharfage + D/O + clearing agent
JAAI       = ¥7,560–¥9,720         (Japan-origin vehicles only)
DMT        = LKR 9,450–44,450      (first registration, by vehicle type/size)
```

All amounts are returned itemised in both USD and LKR.

---

### Combined Route (`POST /all`)

Runs all three engines sequentially. Engine 3 uses the top recommendation from Engine 2 as its input vehicle. Returns all three result sets in a single response.

---

## Setup

**Requirements:** Python 3.10+

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

pip install fastapi uvicorn experta pydantic
```

**Start the API server:**

```bash
python main.py
# or
uvicorn main:app --reload
```

The server starts at `http://127.0.0.1:8000`.

**Open the UI:**

Navigate to `ui/index.html` in a browser (or serve it from the same origin as the API). The UI connects to `http://127.0.0.1:8000` by default.

---

## API Reference

All endpoints accept and return JSON. All responses include a `trail` array with the full rule-firing history.

### `POST /eligibility`

```json
{
  "vehicle_type": "car",
  "origin_country": "Japan",
  "fuel_type": "petrol_hybrid",
  "manufacture_year": 2022,
  "manufacture_month": 6,
  "bill_of_lading_date": "2025-03-01",
  "is_euro6": true,
  "airbags": 6,
  "has_abs": true,
  "has_esc": true,
  "has_battery_warranty": true
}
```

### `POST /selector`

```json
{
  "budget_usd": 15000,
  "vehicle_type": "car",
  "origin_country": "Japan",
  "fuel_preference": "petrol_hybrid",
  "brand_preference": "Toyota",
  "top_n": 3
}
```

### `POST /cost`

```json
{
  "vehicle_type": "car",
  "origin_country": "Japan",
  "fuel_type": "petrol_hybrid",
  "engine_cc": 1500,
  "motor_kw": 60,
  "purchase_price_usd": 12000,
  "manufacture_year": 2022,
  "manufacture_month": 6,
  "usd_to_lkr": 310.0,
  "jpy_to_usd": 0.0067
}
```

### `POST /all`

Combines the fields from all three requests above (with optional `budget_usd` and `brand_preference` added to the eligibility fields).

---

## Knowledge Base Sources

| Module | Regulation / Source |
|---|---|
| `import_regulations.py` | Gazette Extraordinary No. 2421/44 (1 Feb 2025) |
| `duty_rules.py` | Customs Tariff Guide 2025 (Chapter 87, HS 8703); Gazettes 2418/43, 2434/04, 2421/41 |
| `cost_factors.py` | SLPA Tariff 2026; JDA Cars, Fastlane, Flexport, MoveHub freight rates |
| `vehicle_db.py` | Market catalogue (177 models, mid-2025 indicative prices) |

> Freight rates are volatile; ±20% tolerance should be expected. Exchange rates default to mid-2025 indicatives and can be overridden per request.

---

## Testing

Import `postman_collection.json` into Postman. The collection includes representative pass and fail cases for all three engines:

- **PASS**: 2022 Toyota Aqua (petrol hybrid, Japan)
- **FAIL — age**: 2018 vehicle (exceeds 3-year limit)
- **FAIL — origin**: Germany (not an allowed source country)
- **FAIL — fuel**: Petrol three-wheeler (electric only)
- **FAIL — safety**: Missing ESC
