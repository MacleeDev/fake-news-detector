import pandas as pd

df = pd.read_csv("data/train.csv")  # Adjust filename
df = df[["text", "label"]]  # Only text and label
df = df.dropna()
