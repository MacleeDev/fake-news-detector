import pandas as pd

# Load true and fake CSVs
df_true = pd.read_csv("../data/True.csv")  # adjust path if needed
df_fake = pd.read_csv("../data/Fake.csv")

# Add labels
df_true["label"] = 1  # 1 = Real
df_fake["label"] = 0  # 0 = Fake

# Combine datasets
df = pd.concat([df_true, df_fake], ignore_index=True)

# Merge title and text into a single column
df["text"] = df["title"] + " " + df["text"]

# Keep only text + label
df = df[["text", "label"]].dropna()

# Optional: shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save combined dataset
df.to_csv("../data/train_combined.csv", index=False)

print("Combined dataset saved! Sample:")
print(df.head())
