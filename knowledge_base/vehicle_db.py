"""
Vehicle catalogue for the Sri Lanka import expert system.

Each entry represents a model available in the origin market.
Prices are typical auction / market prices in USD for vehicles
meeting the current age requirement (under 3 years for passenger,
under 5 years for vans).

engine_cc   : 0 for fully electric vehicles
motor_kw    : rated motor output for EVs and hybrids (None if not applicable)
resale_score: 1–10, how well the model holds value in the Sri Lankan market
popularity  : 1–10, demand / recognition in the Sri Lankan market
"""

VEHICLES = [

    # =========================================================================
    # JAPAN — Kei cars, 660 cc, petrol
    # =========================================================================
    {"make": "Suzuki",     "model": "Alto",        "engine_cc": 660,  "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 5000,  "resale_score": 6, "popularity": 7, "motor_kw": None},
    {"make": "Suzuki",     "model": "Wagon R",      "engine_cc": 660,  "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 6000,  "resale_score": 6, "popularity": 7, "motor_kw": None},
    {"make": "Suzuki",     "model": "Spacia",       "engine_cc": 660,  "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "van",    "typical_price_usd": 8500,  "resale_score": 7, "popularity": 6, "motor_kw": None},
    {"make": "Suzuki",     "model": "Hustler",      "engine_cc": 660,  "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 10000, "resale_score": 7, "popularity": 6, "motor_kw": None},
    {"make": "Honda",      "model": "N-Box",        "engine_cc": 660,  "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "van",    "typical_price_usd": 11000, "resale_score": 8, "popularity": 6, "motor_kw": None},
    {"make": "Honda",      "model": "N-One",        "engine_cc": 660,  "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 10000, "resale_score": 7, "popularity": 5, "motor_kw": None},
    {"make": "Honda",      "model": "N-WGN",        "engine_cc": 660,  "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 8500,  "resale_score": 6, "popularity": 5, "motor_kw": None},
    {"make": "Daihatsu",   "model": "Move",         "engine_cc": 660,  "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 6500,  "resale_score": 5, "popularity": 5, "motor_kw": None},
    {"make": "Daihatsu",   "model": "Tanto",        "engine_cc": 660,  "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "van",    "typical_price_usd": 7500,  "resale_score": 6, "popularity": 5, "motor_kw": None},
    {"make": "Nissan",     "model": "Dayz",         "engine_cc": 660,  "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 7500,  "resale_score": 6, "popularity": 5, "motor_kw": None},
    {"make": "Mitsubishi", "model": "eK Wagon",     "engine_cc": 660,  "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 6500,  "resale_score": 5, "popularity": 4, "motor_kw": None},
    {"make": "Mitsubishi", "model": "eK Cross",     "engine_cc": 660,  "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 9500,  "resale_score": 6, "popularity": 4, "motor_kw": None},
    {"make": "Subaru",     "model": "Stella",       "engine_cc": 660,  "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 5500,  "resale_score": 5, "popularity": 3, "motor_kw": None},

    # =========================================================================
    # JAPAN — Kei cars, 660 cc, petrol_hybrid (S-Hybrid mild hybrid)
    # =========================================================================
    {"make": "Suzuki",     "model": "Wagon R Hybrid",  "engine_cc": 660, "fuel_type": "petrol_hybrid", "origin": "japan",  "vehicle_type": "car",  "typical_price_usd": 7500,  "resale_score": 7, "popularity": 7, "motor_kw": 2},
    {"make": "Suzuki",     "model": "Spacia Hybrid",   "engine_cc": 660, "fuel_type": "petrol_hybrid", "origin": "japan",  "vehicle_type": "van",  "typical_price_usd": 10000, "resale_score": 7, "popularity": 6, "motor_kw": 2},
    {"make": "Suzuki",     "model": "Hustler Hybrid",  "engine_cc": 660, "fuel_type": "petrol_hybrid", "origin": "japan",  "vehicle_type": "car",  "typical_price_usd": 11000, "resale_score": 7, "popularity": 6, "motor_kw": 2},

    # =========================================================================
    # JAPAN — Small petrol, 1000–1500 cc
    # =========================================================================
    {"make": "Toyota",     "model": "Vitz",         "engine_cc": 1000, "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 10000, "resale_score": 7, "popularity": 8, "motor_kw": None},
    {"make": "Toyota",     "model": "Raize",        "engine_cc": 1000, "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "suv",    "typical_price_usd": 15500, "resale_score": 7, "popularity": 7, "motor_kw": None},
    {"make": "Toyota",     "model": "Roomy",        "engine_cc": 1000, "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "van",    "typical_price_usd": 14500, "resale_score": 6, "popularity": 5, "motor_kw": None},
    {"make": "Toyota",     "model": "Corolla Axio", "engine_cc": 1500, "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 14500, "resale_score": 7, "popularity": 8, "motor_kw": None},
    {"make": "Honda",      "model": "Fit",          "engine_cc": 1300, "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 11500, "resale_score": 7, "popularity": 8, "motor_kw": None},
    {"make": "Suzuki",     "model": "Swift",        "engine_cc": 1200, "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 10000, "resale_score": 6, "popularity": 6, "motor_kw": None},
    {"make": "Mazda",      "model": "Demio",        "engine_cc": 1300, "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 10000, "resale_score": 6, "popularity": 6, "motor_kw": None},
    {"make": "Nissan",     "model": "March",        "engine_cc": 1200, "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 8500,  "resale_score": 5, "popularity": 5, "motor_kw": None},
    {"make": "Nissan",     "model": "Note",         "engine_cc": 1200, "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "car",    "typical_price_usd": 11000, "resale_score": 6, "popularity": 6, "motor_kw": None},
    {"make": "Daihatsu",   "model": "Rocky",        "engine_cc": 1000, "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "suv",    "typical_price_usd": 14000, "resale_score": 6, "popularity": 5, "motor_kw": None},
    {"make": "Toyota",     "model": "Porte",        "engine_cc": 1300, "fuel_type": "petrol",       "origin": "japan",     "vehicle_type": "van",    "typical_price_usd": 11000, "resale_score": 6, "popularity": 4, "motor_kw": None},

    # =========================================================================
    # JAPAN — Small petrol_hybrid, 1200–1500 cc
    # =========================================================================
    {"make": "Toyota",     "model": "Aqua",         "engine_cc": 1500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 15000, "resale_score": 9, "popularity": 10, "motor_kw": 45},
    {"make": "Toyota",     "model": "Yaris Cross",  "engine_cc": 1500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 19000, "resale_score": 8, "popularity": 8,  "motor_kw": 59},
    {"make": "Toyota",     "model": "Sienta",       "engine_cc": 1500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "van",    "typical_price_usd": 16500, "resale_score": 7, "popularity": 7,  "motor_kw": 59},
    {"make": "Honda",      "model": "Fit Hybrid",   "engine_cc": 1300, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 12500, "resale_score": 8, "popularity": 8,  "motor_kw": 22},
    {"make": "Honda",      "model": "Shuttle",      "engine_cc": 1500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 13500, "resale_score": 7, "popularity": 6,  "motor_kw": 22},
    {"make": "Honda",      "model": "Jade",         "engine_cc": 1500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "van",    "typical_price_usd": 14500, "resale_score": 7, "popularity": 5,  "motor_kw": 22},
    {"make": "Nissan",     "model": "Note e-Power", "engine_cc": 1200, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 14500, "resale_score": 8, "popularity": 8,  "motor_kw": 85},
    {"make": "Suzuki",     "model": "Swift Hybrid", "engine_cc": 1200, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 11000, "resale_score": 7, "popularity": 6,  "motor_kw": 10},

    # =========================================================================
    # JAPAN — Compact cars & sedans, petrol_hybrid, 1800–2500 cc
    # =========================================================================
    {"make": "Toyota",     "model": "Prius",        "engine_cc": 1800, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 21500, "resale_score": 9, "popularity": 9,  "motor_kw": 53},
    {"make": "Toyota",     "model": "Corolla",      "engine_cc": 1800, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 19000, "resale_score": 8, "popularity": 8,  "motor_kw": 53},
    {"make": "Toyota",     "model": "C-HR",         "engine_cc": 1800, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 20000, "resale_score": 8, "popularity": 7,  "motor_kw": 53},
    {"make": "Honda",      "model": "Grace",        "engine_cc": 1500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 14500, "resale_score": 7, "popularity": 6,  "motor_kw": 22},
    {"make": "Toyota",     "model": "Crown",        "engine_cc": 2500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 37500, "resale_score": 7, "popularity": 5,  "motor_kw": 105},
    {"make": "Toyota",     "model": "Camry",        "engine_cc": 2500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 30000, "resale_score": 8, "popularity": 6,  "motor_kw": 88},

    # =========================================================================
    # JAPAN — Compact cars & sedans, petrol, 1500–2000 cc
    # =========================================================================
    {"make": "Honda",      "model": "Civic",        "engine_cc": 1500, "fuel_type": "petrol",        "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 19000, "resale_score": 7, "popularity": 6,  "motor_kw": None},
    {"make": "Mazda",      "model": "Mazda 3",      "engine_cc": 1500, "fuel_type": "petrol",        "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 19000, "resale_score": 7, "popularity": 5,  "motor_kw": None},
    {"make": "Nissan",     "model": "Sylphy",       "engine_cc": 1800, "fuel_type": "petrol",        "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 16500, "resale_score": 6, "popularity": 5,  "motor_kw": None},
    {"make": "Subaru",     "model": "Impreza",      "engine_cc": 1600, "fuel_type": "petrol",        "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 17500, "resale_score": 6, "popularity": 5,  "motor_kw": None},

    # =========================================================================
    # JAPAN — Compact SUVs & crossovers
    # =========================================================================
    {"make": "Honda",      "model": "Vezel",        "engine_cc": 1500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 19000, "resale_score": 8, "popularity": 9,  "motor_kw": 96},
    {"make": "Toyota",     "model": "RAV4",         "engine_cc": 2000, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 30000, "resale_score": 8, "popularity": 7,  "motor_kw": 88},
    {"make": "Toyota",     "model": "Harrier",      "engine_cc": 2000, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 33000, "resale_score": 8, "popularity": 7,  "motor_kw": 88},
    {"make": "Honda",      "model": "CR-V",         "engine_cc": 2000, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 28000, "resale_score": 8, "popularity": 6,  "motor_kw": 135},
    {"make": "Mazda",      "model": "CX-5",         "engine_cc": 2000, "fuel_type": "petrol",        "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 24000, "resale_score": 7, "popularity": 6,  "motor_kw": None},
    {"make": "Mazda",      "model": "CX-5 Diesel",  "engine_cc": 2200, "fuel_type": "diesel",        "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 26000, "resale_score": 7, "popularity": 5,  "motor_kw": None},
    {"make": "Nissan",     "model": "X-Trail",      "engine_cc": 1500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 26000, "resale_score": 7, "popularity": 6,  "motor_kw": 85},
    {"make": "Subaru",     "model": "Forester",     "engine_cc": 2000, "fuel_type": "petrol",        "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 26000, "resale_score": 7, "popularity": 5,  "motor_kw": None},
    {"make": "Subaru",     "model": "XV",           "engine_cc": 2000, "fuel_type": "petrol",        "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 22500, "resale_score": 7, "popularity": 5,  "motor_kw": None},
    {"make": "Toyota",     "model": "Rush",         "engine_cc": 1500, "fuel_type": "petrol",        "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 16500, "resale_score": 7, "popularity": 7,  "motor_kw": None},
    {"make": "Suzuki",     "model": "Jimny",        "engine_cc": 1500, "fuel_type": "petrol",        "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 18500, "resale_score": 9, "popularity": 7,  "motor_kw": None},
    {"make": "Mitsubishi", "model": "Outlander PHEV","engine_cc": 2400,"fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 33000, "resale_score": 7, "popularity": 6,  "motor_kw": 60},

    # =========================================================================
    # JAPAN — Vans & MPVs
    # =========================================================================
    {"make": "Toyota",     "model": "Noah",         "engine_cc": 1800, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "van",    "typical_price_usd": 24000, "resale_score": 7, "popularity": 7,  "motor_kw": 53},
    {"make": "Toyota",     "model": "Voxy",         "engine_cc": 1800, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "van",    "typical_price_usd": 24000, "resale_score": 7, "popularity": 6,  "motor_kw": 53},
    {"make": "Honda",      "model": "Freed",        "engine_cc": 1500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "van",    "typical_price_usd": 17000, "resale_score": 7, "popularity": 7,  "motor_kw": 22},
    {"make": "Honda",      "model": "Stepwgn",      "engine_cc": 1500, "fuel_type": "petrol",        "origin": "japan",    "vehicle_type": "van",    "typical_price_usd": 21500, "resale_score": 7, "popularity": 5,  "motor_kw": None},
    {"make": "Nissan",     "model": "Serena",       "engine_cc": 2000, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "van",    "typical_price_usd": 24000, "resale_score": 7, "popularity": 5,  "motor_kw": 85},
    {"make": "Toyota",     "model": "Alphard",      "engine_cc": 2500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "van",    "typical_price_usd": 50000, "resale_score": 8, "popularity": 6,  "motor_kw": 105},
    {"make": "Toyota",     "model": "Vellfire",     "engine_cc": 2500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "van",    "typical_price_usd": 46500, "resale_score": 8, "popularity": 5,  "motor_kw": 105},
    {"make": "Honda",      "model": "Odyssey",      "engine_cc": 2000, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "van",    "typical_price_usd": 26000, "resale_score": 7, "popularity": 4,  "motor_kw": 135},

    # =========================================================================
    # JAPAN — Large / luxury
    # =========================================================================
    {"make": "Toyota",     "model": "Land Cruiser Prado",        "engine_cc": 2700, "fuel_type": "petrol", "origin": "japan", "vehicle_type": "suv", "typical_price_usd": 55000, "resale_score": 9, "popularity": 7, "motor_kw": None},
    {"make": "Toyota",     "model": "Land Cruiser Prado Diesel", "engine_cc": 2800, "fuel_type": "diesel", "origin": "japan", "vehicle_type": "suv", "typical_price_usd": 58000, "resale_score": 9, "popularity": 7, "motor_kw": None},
    {"make": "Lexus",      "model": "UX Hybrid",    "engine_cc": 2000, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 33000, "resale_score": 7, "popularity": 4,  "motor_kw": 80},
    {"make": "Lexus",      "model": "NX Hybrid",    "engine_cc": 2500, "fuel_type": "petrol_hybrid", "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 45000, "resale_score": 7, "popularity": 4,  "motor_kw": 134},
    {"make": "Mitsubishi", "model": "Pajero Sport", "engine_cc": 2400, "fuel_type": "diesel",        "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 30000, "resale_score": 7, "popularity": 5,  "motor_kw": None},

    # =========================================================================
    # JAPAN — Pickups
    # =========================================================================
    {"make": "Toyota",     "model": "Hilux",        "engine_cc": 2800, "fuel_type": "diesel",        "origin": "japan",    "vehicle_type": "pickup", "typical_price_usd": 33000, "resale_score": 8, "popularity": 6,  "motor_kw": None},
    {"make": "Isuzu",      "model": "D-Max",        "engine_cc": 1900, "fuel_type": "diesel",        "origin": "japan",    "vehicle_type": "pickup", "typical_price_usd": 28500, "resale_score": 7, "popularity": 5,  "motor_kw": None},
    {"make": "Mitsubishi", "model": "Triton",       "engine_cc": 2400, "fuel_type": "diesel",        "origin": "japan",    "vehicle_type": "pickup", "typical_price_usd": 26000, "resale_score": 7, "popularity": 4,  "motor_kw": None},

    # =========================================================================
    # JAPAN — Electric
    # =========================================================================
    {"make": "Nissan",     "model": "Leaf",         "engine_cc": 0,    "fuel_type": "electric",      "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 21500, "resale_score": 6, "popularity": 7,  "motor_kw": 110},
    {"make": "Nissan",     "model": "Ariya",        "engine_cc": 0,    "fuel_type": "electric",      "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 38500, "resale_score": 6, "popularity": 4,  "motor_kw": 160},
    {"make": "Toyota",     "model": "bZ4X",         "engine_cc": 0,    "fuel_type": "electric",      "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 41500, "resale_score": 6, "popularity": 4,  "motor_kw": 150},
    {"make": "Honda",      "model": "e",            "engine_cc": 0,    "fuel_type": "electric",      "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 30000, "resale_score": 5, "popularity": 3,  "motor_kw": 113},
    {"make": "Mitsubishi", "model": "i-MiEV",       "engine_cc": 0,    "fuel_type": "electric",      "origin": "japan",    "vehicle_type": "car",    "typical_price_usd": 15000, "resale_score": 4, "popularity": 4,  "motor_kw": 47},
    {"make": "Lexus",      "model": "UX 300e",      "engine_cc": 0,    "fuel_type": "electric",      "origin": "japan",    "vehicle_type": "suv",    "typical_price_usd": 45000, "resale_score": 6, "popularity": 3,  "motor_kw": 150},

    # =========================================================================
    # UNITED KINGDOM
    # =========================================================================
    {"make": "Ford",       "model": "Fiesta",       "engine_cc": 1000, "fuel_type": "petrol",        "origin": "uk",       "vehicle_type": "car",    "typical_price_usd": 17500, "resale_score": 5, "popularity": 4,  "motor_kw": None},
    {"make": "Ford",       "model": "Focus",        "engine_cc": 1000, "fuel_type": "petrol",        "origin": "uk",       "vehicle_type": "car",    "typical_price_usd": 20000, "resale_score": 5, "popularity": 3,  "motor_kw": None},
    {"make": "Ford",       "model": "Puma",         "engine_cc": 1000, "fuel_type": "petrol_hybrid", "origin": "uk",       "vehicle_type": "suv",    "typical_price_usd": 21000, "resale_score": 6, "popularity": 3,  "motor_kw": 11},
    {"make": "MINI",       "model": "Cooper",       "engine_cc": 1500, "fuel_type": "petrol",        "origin": "uk",       "vehicle_type": "car",    "typical_price_usd": 28000, "resale_score": 6, "popularity": 4,  "motor_kw": None},
    {"make": "MINI",       "model": "Countryman",   "engine_cc": 1500, "fuel_type": "petrol_hybrid", "origin": "uk",       "vehicle_type": "suv",    "typical_price_usd": 33000, "resale_score": 6, "popularity": 3,  "motor_kw": 65},
    {"make": "BMW",        "model": "1 Series",     "engine_cc": 1500, "fuel_type": "petrol",        "origin": "uk",       "vehicle_type": "car",    "typical_price_usd": 33000, "resale_score": 7, "popularity": 4,  "motor_kw": None},
    {"make": "BMW",        "model": "3 Series",     "engine_cc": 2000, "fuel_type": "petrol",        "origin": "uk",       "vehicle_type": "car",    "typical_price_usd": 45000, "resale_score": 7, "popularity": 4,  "motor_kw": None},
    {"make": "Volkswagen", "model": "Golf",         "engine_cc": 1500, "fuel_type": "petrol",        "origin": "uk",       "vehicle_type": "car",    "typical_price_usd": 26000, "resale_score": 6, "popularity": 4,  "motor_kw": None},
    {"make": "Jaguar",     "model": "XE",           "engine_cc": 2000, "fuel_type": "petrol",        "origin": "uk",       "vehicle_type": "car",    "typical_price_usd": 36000, "resale_score": 5, "popularity": 3,  "motor_kw": None},
    {"make": "Land Rover", "model": "Defender",     "engine_cc": 2000, "fuel_type": "diesel",        "origin": "uk",       "vehicle_type": "suv",    "typical_price_usd": 65000, "resale_score": 7, "popularity": 5,  "motor_kw": None},
    {"make": "Vauxhall",   "model": "Corsa-e",      "engine_cc": 0,    "fuel_type": "electric",      "origin": "uk",       "vehicle_type": "car",    "typical_price_usd": 26000, "resale_score": 5, "popularity": 3,  "motor_kw": 100},
    {"make": "Nissan",     "model": "Qashqai",      "engine_cc": 1300, "fuel_type": "petrol_hybrid", "origin": "uk",       "vehicle_type": "suv",    "typical_price_usd": 26000, "resale_score": 6, "popularity": 4,  "motor_kw": 12},

    # =========================================================================
    # SINGAPORE
    # =========================================================================
    {"make": "Honda",        "model": "Jazz",          "engine_cc": 1500, "fuel_type": "petrol",        "origin": "singapore", "vehicle_type": "car",  "typical_price_usd": 21000, "resale_score": 6, "popularity": 4, "motor_kw": None},
    {"make": "Toyota",       "model": "Corolla Altis", "engine_cc": 1800, "fuel_type": "petrol_hybrid", "origin": "singapore", "vehicle_type": "car",  "typical_price_usd": 26000, "resale_score": 7, "popularity": 5, "motor_kw": 53},
    {"make": "Toyota",       "model": "Camry Hybrid",  "engine_cc": 2500, "fuel_type": "petrol_hybrid", "origin": "singapore", "vehicle_type": "car",  "typical_price_usd": 38500, "resale_score": 7, "popularity": 4, "motor_kw": 88},
    {"make": "Honda",        "model": "Civic SG",      "engine_cc": 1500, "fuel_type": "petrol",        "origin": "singapore", "vehicle_type": "car",  "typical_price_usd": 26000, "resale_score": 6, "popularity": 4, "motor_kw": None},
    {"make": "Mercedes-Benz","model": "A-Class",       "engine_cc": 1330, "fuel_type": "petrol",        "origin": "singapore", "vehicle_type": "car",  "typical_price_usd": 38500, "resale_score": 6, "popularity": 3, "motor_kw": None},
    {"make": "Hyundai",      "model": "Ioniq 6",       "engine_cc": 0,    "fuel_type": "electric",      "origin": "singapore", "vehicle_type": "car",  "typical_price_usd": 41500, "resale_score": 6, "popularity": 4, "motor_kw": 160},
    {"make": "Kia",          "model": "EV6",           "engine_cc": 0,    "fuel_type": "electric",      "origin": "singapore", "vehicle_type": "car",  "typical_price_usd": 45000, "resale_score": 6, "popularity": 4, "motor_kw": 168},
    {"make": "Volvo",        "model": "XC40 Recharge", "engine_cc": 0,    "fuel_type": "electric",      "origin": "singapore", "vehicle_type": "suv",  "typical_price_usd": 50000, "resale_score": 6, "popularity": 3, "motor_kw": 170},

    # =========================================================================
    # AUSTRALIA
    # =========================================================================
    {"make": "Toyota",     "model": "HiLux",        "engine_cc": 2800, "fuel_type": "diesel",        "origin": "australia", "vehicle_type": "pickup", "typical_price_usd": 38000, "resale_score": 8, "popularity": 6, "motor_kw": None},
    {"make": "Ford",       "model": "Ranger",       "engine_cc": 2000, "fuel_type": "diesel",        "origin": "australia", "vehicle_type": "pickup", "typical_price_usd": 36000, "resale_score": 7, "popularity": 5, "motor_kw": None},
    {"make": "Toyota",     "model": "Camry AU",     "engine_cc": 2500, "fuel_type": "petrol_hybrid", "origin": "australia", "vehicle_type": "car",    "typical_price_usd": 33000, "resale_score": 7, "popularity": 4, "motor_kw": 88},
    {"make": "Mazda",      "model": "CX-5 AU",      "engine_cc": 2500, "fuel_type": "petrol",        "origin": "australia", "vehicle_type": "suv",    "typical_price_usd": 31000, "resale_score": 7, "popularity": 4, "motor_kw": None},
    {"make": "Subaru",     "model": "Outback",      "engine_cc": 2500, "fuel_type": "petrol",        "origin": "australia", "vehicle_type": "suv",    "typical_price_usd": 33000, "resale_score": 6, "popularity": 3, "motor_kw": None},
    {"make": "Mitsubishi", "model": "Triton AU",    "engine_cc": 2400, "fuel_type": "diesel",        "origin": "australia", "vehicle_type": "pickup", "typical_price_usd": 30500, "resale_score": 7, "popularity": 4, "motor_kw": None},

]


# ── Helpers ───────────────────────────────────────────────────────────────────

def filter_vehicles(
    max_cc: int | None = None,
    fuel_type: str | None = None,
    origin: str | None = None,
    vehicle_type: str | None = None,
    max_price_usd: float | None = None,
) -> list[dict]:
    """Return vehicles matching all supplied criteria (None = no filter)."""
    results = VEHICLES
    if max_cc is not None:
        results = [v for v in results if v["engine_cc"] <= max_cc]
    if fuel_type is not None:
        results = [v for v in results if v["fuel_type"] == fuel_type]
    if origin is not None:
        results = [v for v in results if v["origin"] == origin]
    if vehicle_type is not None:
        results = [v for v in results if v["vehicle_type"] == vehicle_type]
    if max_price_usd is not None:
        results = [v for v in results if v["typical_price_usd"] <= max_price_usd]
    return results


def get_vehicle(make: str, model: str) -> dict | None:
    """Return the first matching vehicle by make and model, or None."""
    make_l, model_l = make.lower(), model.lower()
    return next(
        (v for v in VEHICLES
         if v["make"].lower() == make_l and v["model"].lower() == model_l),
        None,
    )
