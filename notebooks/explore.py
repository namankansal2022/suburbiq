import pandas as pd
import os
HF_TOKEN = "YOUR_HF_TOKEN_HERE"

DATE = "dt=2026-04-14"
OUTPUT_PATH = os.path.expanduser(
    "~/suburbiq/data/northamerica_pois.parquet"
)

TARGET_COUNTRIES = ["US", "CA"]

# US files (1-11) + CA files (12-13)
# Only take 3 US files to keep memory manageable
# CA we take all we can find
US_FILES = list(range(1, 4))    # 3 files = ~1.5M US rows
CA_FILES = list(range(12, 16))  # CA cluster

FILES_TO_CHECK = US_FILES + CA_FILES

print(f"Targeting North America data...")
print(f"US files: {US_FILES}")
print(f"CA files: {CA_FILES}\n")

all_frames = []

for i in FILES_TO_CHECK:
    file_num = str(i).zfill(6)
    url = (
        f"hf://datasets/foursquare/fsq-os-places/"
        f"release/{DATE}/places/parquet/"
        f"places_{file_num}.parquet"
    )

    print(f"File {file_num}...")

    try:
        df = pd.read_parquet(
            url,
            storage_options={"token": HF_TOKEN}
        )

        filtered = df[df["country"].isin(TARGET_COUNTRIES)]

        if len(filtered) > 0:
            counts = filtered["country"].value_counts().to_dict()
            print(f"  ✅ {counts}")
            all_frames.append(filtered)
        else:
            top = df["country"].value_counts().head(2).index.tolist()
            print(f"  → No match. Top: {top}")

    except Exception as e:
        print(f"  ⚠️ Error: {e}")
        continue

# Combine
print("\nCombining...")
combined_df = pd.concat(all_frames, ignore_index=True)

print(f"\n✅ Total POIs: {len(combined_df):,}")
print(f"\nBy country:")
print(combined_df["country"].value_counts())

print(f"\nTop US states:")
us = combined_df[combined_df["country"] == "US"]
print(us["region"].value_counts().head(10))

print(f"\nTop CA provinces:")
ca = combined_df[combined_df["country"] == "CA"]
print(ca["region"].value_counts().head(10))

print(f"\nDate columns check:")
print(combined_df[["name", "country", "locality",
                    "date_created", "date_closed"]].head(10))

print(f"\nCategory sample:")
print(combined_df["fsq_category_labels"].dropna().head(10))

# Save
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
combined_df.to_parquet(OUTPUT_PATH, index=False)

print(f"\n✅ Saved to {OUTPUT_PATH}")
print(f"Total size: {combined_df.memory_usage(deep=True).sum() / 1e9:.2f} GB")
print("Ready to build North America Business Survival Atlas!")