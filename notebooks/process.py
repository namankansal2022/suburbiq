import pandas as pd
import numpy as np
import os

INPUT_PATH = os.path.expanduser(
    "~/suburbiq/data/northamerica_pois.parquet"
)
OUTPUT_PATH = os.path.expanduser(
    "~/suburbiq/data/survival_scores.parquet"
)

print("Loading data...")
df = pd.read_parquet(INPUT_PATH)
print(f"Loaded {len(df):,} rows")

# ============================================
# STEP 1: CLEAN THE DATA
# ============================================
print("\nCleaning data...")

# Fix category extraction — handles numpy arrays
def extract_category(labels):
    if labels is None:
        return None
    # Handle numpy array
    if isinstance(labels, np.ndarray):
        if len(labels) == 0:
            return None
        first = labels[0]
    elif isinstance(labels, list):
        if len(labels) == 0:
            return None
        first = labels[0]
    else:
        return None
    
    # Split hierarchy e.g. "Dining > Restaurant > BBQ"
    parts = str(first).split(" > ")
    if len(parts) >= 2:
        return parts[1].strip()
    return parts[0].strip()

print("Extracting categories...")
df["category"] = df["fsq_category_labels"].apply(
    extract_category
)

# Tag active vs closed
# date_closed not null = closed
df["is_closed"] = df["date_closed"].notna()

# Clean locality and region
df["locality"] = df["locality"].str.strip().str.title()
df["region"] = df["region"].str.strip().str.upper()

# Check before dropping
print(f"\nBefore dropna:")
print(f"  Total rows: {len(df):,}")
print(f"  Null locality: {df['locality'].isna().sum():,}")
print(f"  Null category: {df['category'].isna().sum():,}")

# Remove rows with no locality or category
df = df.dropna(subset=["locality", "category"])
print(f"After dropna: {len(df):,} rows")

# Remove very rare categories
category_counts = df["category"].value_counts()
valid_categories = category_counts[
    category_counts >= 50
].index
df = df[df["category"].isin(valid_categories)]

print(f"After category filter: {len(df):,} rows")
print(f"Unique localities: {df['locality'].nunique():,}")
print(f"Unique categories: {df['category'].nunique():,}")

print(f"\nTop 15 categories:")
print(df["category"].value_counts().head(15))

print(f"\nClosed vs Active:")
print(df["is_closed"].value_counts())

# ============================================
# STEP 2: COMPUTE SURVIVAL RATES
# ============================================
print("\nComputing survival rates...")

grouped = df.groupby(
    ["locality", "region", "country", "category"]
).agg(
    total_ever=("fsq_place_id", "count"),
    active_count=("is_closed", lambda x: (~x).sum()),
    closed_count=("is_closed", "sum"),
).reset_index()

# Only keep pairs with enough history
grouped = grouped[grouped["total_ever"] >= 5]

# Survival rate
grouped["survival_rate"] = (
    grouped["active_count"] / grouped["total_ever"]
).round(3)

# ============================================
# STEP 3: AVERAGE LIFESPAN
# ============================================
print("Computing lifespans...")

df["date_created"] = pd.to_datetime(
    df["date_created"], errors="coerce"
)
df["date_closed"] = pd.to_datetime(
    df["date_closed"], errors="coerce"
)

closed_df = df[
    df["is_closed"] & 
    df["date_created"].notna() & 
    df["date_closed"].notna()
].copy()

closed_df["lifespan_days"] = (
    closed_df["date_closed"] - closed_df["date_created"]
).dt.days

# Only keep positive lifespans
closed_df = closed_df[closed_df["lifespan_days"] > 0]

lifespan = closed_df.groupby(
    ["locality", "region", "country", "category"]
)["lifespan_days"].mean().reset_index()

lifespan["avg_lifespan_years"] = (
    lifespan["lifespan_days"] / 365
).round(1)

lifespan = lifespan.drop(columns=["lifespan_days"])

grouped = grouped.merge(
    lifespan,
    on=["locality", "region", "country", "category"],
    how="left"
)

# ============================================
# STEP 4: SUBURBIQ SCORE
# ============================================
print("Computing SuburbIQ scores...")

grouped["density_rank"] = grouped.groupby("category")[
    "active_count"
].rank(pct=True)

grouped["inverse_density"] = 1 - grouped["density_rank"]

grouped["suburbiq_score"] = (
    (grouped["survival_rate"] * 0.6) +
    (grouped["inverse_density"] * 0.4)
) * 100

grouped["suburbiq_score"] = grouped[
    "suburbiq_score"
].round(1)

# ============================================
# STEP 5: SAVE
# ============================================
print(f"\n✅ Final dataset: {len(grouped):,} rows")
print(f"\nSample:")
print(grouped[
    ["locality", "region", "country", "category",
     "active_count", "closed_count", "survival_rate",
     "avg_lifespan_years", "suburbiq_score"]
].head(10).to_string())

print(f"\nScore distribution:")
print(grouped["suburbiq_score"].describe())

print(f"\nTop opportunity areas (score > 80):")
top = grouped[grouped["suburbiq_score"] > 80].sort_values(
    "suburbiq_score", ascending=False
)
print(top[["locality", "region", "category", 
           "survival_rate", "suburbiq_score"]].head(10))

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
grouped.to_parquet(OUTPUT_PATH, index=False)

print(f"\n✅ Saved to {OUTPUT_PATH}")
print(f"File size: {os.path.getsize(OUTPUT_PATH)/1e6:.1f} MB")
print("Ready to build the Streamlit app!")