# train_bert.py
import os
from datasets import load_dataset, Dataset, DatasetDict
from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    Trainer,
    TrainingArguments,
)
import torch

# -----------------------------
# Config
# -----------------------------
DATA_DIR = "../datasets"
MODEL_DIR = "../models/demo_bert"  # final model will be saved here
os.makedirs(MODEL_DIR, exist_ok=True)

# -----------------------------
# Load CSV datasets
# -----------------------------
true_ds = load_dataset("csv", data_files=os.path.join(DATA_DIR, "true.csv"))["train"]
fake_ds = load_dataset("csv", data_files=os.path.join(DATA_DIR, "fake.csv"))["train"]

# Add labels: 0 = true, 1 = fake
true_ds = true_ds.map(lambda x: {"label": 0})
fake_ds = fake_ds.map(lambda x: {"label": 1})

# -----------------------------
# Concatenate safely
# -----------------------------
dataset = Dataset.from_dict(
    {
        "text": list(true_ds["text"]) + list(fake_ds["text"]),
        "label": list(true_ds["label"]) + list(fake_ds["label"]),
    }
)

# -----------------------------
# Split dataset: 80% train, 20% test
# -----------------------------
dataset = dataset.train_test_split(test_size=0.2)
train_ds = dataset["train"]
test_ds = dataset["test"]

# -----------------------------
# Tokenizer
# -----------------------------
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")


def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True, max_length=256)


train_ds = train_ds.map(tokenize, batched=True)
test_ds = test_ds.map(tokenize, batched=True)

# Set format for PyTorch
train_ds.set_format("torch", columns=["input_ids", "attention_mask", "label"])
test_ds.set_format("torch", columns=["input_ids", "attention_mask", "label"])

# -----------------------------
# Load BERT Model
# -----------------------------
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# -----------------------------
# Training arguments
# -----------------------------
training_args = TrainingArguments(
    output_dir=MODEL_DIR,
    num_train_epochs=2,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    eval_strategy="steps",
    save_strategy="steps",
    save_steps=200,
    eval_steps=200,
    logging_steps=50,
    learning_rate=2e-5,
    logging_dir=os.path.join(MODEL_DIR, "logs"),
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    save_total_limit=2,
)

# -----------------------------
# Metrics function
# -----------------------------
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="binary"
    )
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}


# -----------------------------
# Trainer
# -----------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=test_ds,
    compute_metrics=compute_metrics,
)

# -----------------------------
# Train
# -----------------------------
trainer.train()

# -----------------------------
# Save final model & tokenizer
# -----------------------------
model.save_pretrained(MODEL_DIR)
tokenizer.save_pretrained(MODEL_DIR)

print(f"Model and tokenizer saved at {MODEL_DIR}")
