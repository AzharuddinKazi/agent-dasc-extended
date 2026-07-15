import pandas as pd
import numpy as np
import json
from pathlib import Path
import os

np.random.seed(42)
OUTPUT_DIR = Path(os.getenv("DSSTAR")) / "data"
N_TRANSACTIONS = 500_000
N_STORES       = 30
N_USERS        = 5_000
N_CARDS        = 8_000

# ── Store metadata ────────────────────────────────────────────────────────────
store_types = ["Flagship", "Outlet", "Online-Only", "Franchise"]
store_tiers = ["Tier 1", "Tier 2", "Tier 3"]

stores = pd.DataFrame({
    "store_id":      [f"STR_{i:03d}" for i in range(1, N_STORES + 1)],
    "store_name":    [f"Store {i}" for i in range(1, N_STORES + 1)],
    "store_type":    np.random.choice(store_types, N_STORES),
    "store_tier":    np.random.choice(store_tiers, N_STORES, p=[0.2, 0.3, 0.5]),
    "region":        np.random.choice(["North", "South", "East", "West", "Central"], N_STORES),
    "risk_band":     np.random.choice(["Low", "Medium", "High"], N_STORES, p=[0.4, 0.4, 0.2]),
})

# ── Users ─────────────────────────────────────────────────────────────────────
users = pd.DataFrame({
    "user_id":       [f"USR_{i:05d}" for i in range(1, N_USERS + 1)],
    "store_id":      np.random.choice(stores["store_id"], N_USERS),
    "age":           np.random.randint(18, 75, N_USERS),
    "account_type":  np.random.choice(["Standard", "Premium", "Business"], N_USERS, p=[0.4, 0.4, 0.2]),
    "membership_status": np.random.choice(["Verified", "Pending", "Expired"], N_USERS, p=[0.80, 0.10, 0.10]),
    "onboarding_channel": np.random.choice(["In-Store", "Digital", "Referral"], N_USERS, p=[0.3, 0.6, 0.1]),
})

# ── Cards ─────────────────────────────────────────────────────────────────────
cards = pd.DataFrame({
    "card_id":       [f"CRD_{i:05d}" for i in range(1, N_CARDS + 1)],
    "user_id":       np.random.choice(users["user_id"], N_CARDS),
    "card_type":     np.random.choice(["Debit", "Credit", "Prepaid"], N_CARDS, p=[0.5, 0.35, 0.15]),
    "card_network":  np.random.choice(["Visa", "Mastercard", "AMEX"], N_CARDS, p=[0.5, 0.4, 0.1]),
    "is_active":     np.random.choice([True, False], N_CARDS, p=[0.9, 0.1]),
    "credit_limit":  np.where(
                        np.random.choice(["Debit", "Credit", "Prepaid"], N_CARDS, p=[0.5, 0.35, 0.15]) == "Credit",
                        np.random.choice([5000, 10000, 25000, 50000], N_CARDS),
                        0
                    ),
})

# ── Transactions ──────────────────────────────────────────────────────────────
mcc_codes = [5411, 5812, 5912, 4111, 5541, 7011, 5999, 6011, 4829, 5732]
channels   = ["POS", "Online", "Kiosk", "Mobile", "In-Store"]
currencies = ["USD", "EUR", "GBP", "CAD", "AUD"]

# inject ~3% fraud
is_fraud = np.random.choice([0, 1], N_TRANSACTIONS, p=[0.97, 0.03])

# fraud transactions have higher amounts and odd hours
amounts = np.where(
    is_fraud,
    np.random.exponential(scale=3000, size=N_TRANSACTIONS).clip(500, 50000),
    np.random.exponential(scale=300,  size=N_TRANSACTIONS).clip(1, 10000)
).round(2)

hours = np.where(
    is_fraud,
    np.random.choice(range(0, 6), N_TRANSACTIONS),      # fraud: late night
    np.random.choice(range(8, 22), N_TRANSACTIONS)      # legit: business hours
)

dates = pd.date_range("2023-01-01", periods=N_TRANSACTIONS, freq="1min")

transactions = pd.DataFrame({
    "transaction_id":  [f"TXN_{i:07d}" for i in range(1, N_TRANSACTIONS + 1)],
    "date":            dates,
    "card_id":         np.random.choice(cards["card_id"], N_TRANSACTIONS),
    "store_id":        np.random.choice(stores["store_id"], N_TRANSACTIONS),
    "amount":          amounts,
    "currency":        np.random.choice(currencies, N_TRANSACTIONS, p=[0.60, 0.20, 0.08, 0.07, 0.05]),
    "channel":         np.random.choice(channels, N_TRANSACTIONS, p=[0.35, 0.30, 0.15, 0.15, 0.05]),
    "mcc":             np.random.choice(mcc_codes, N_TRANSACTIONS),
    "merchant_region": np.random.choice(["North", "South", "East", "West", "Central"], N_TRANSACTIONS),
    "is_fraud":        is_fraud,
    "fraud_type":      np.where(
                           is_fraud,
                           np.random.choice(["Card Not Present", "Account Takeover", "Identity Theft", "Merchant Fraud"], N_TRANSACTIONS),
                           None
                       ),
    "status":          np.random.choice(["Approved", "Declined", "Reversed"], N_TRANSACTIONS, p=[0.92, 0.05, 0.03]),
})

# ── Write files ───────────────────────────────────────────────────────────────
stores.to_csv(OUTPUT_DIR / "store_data.csv", index=False)
users.to_csv(OUTPUT_DIR / "users_data.csv", index=False)
cards.to_csv(OUTPUT_DIR / "cards_data.csv", index=False)
transactions.to_csv(OUTPUT_DIR / "transactions_data.csv", index=False)

print(f"✓ store_data.csv        — {len(stores):,} rows")
print(f"✓ users_data.csv       — {len(users):,} rows")
print(f"✓ cards_data.csv       — {len(cards):,} rows")
print(f"✓ transactions_data.csv — {len(transactions):,} rows")
print(f"\nAll files written to {OUTPUT_DIR}")
