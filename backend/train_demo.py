from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    Trainer,
    TrainingArguments,
)
from datasets import Dataset
import torch

# Tiny dataset
data = [
    {"text": "Government confirms new vaccine is safe", "label": 1},
    {"text": "Aliens landed in Nairobi last night!", "label": 0},
    {"text": "Stock market hits record high today", "label": 1},
    {"text": "Scientists discovered a cure for aging", "label": 0},
]

dataset = Dataset.from_list(data)

# Tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")


def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True, max_length=64)


dataset = dataset.map(tokenize, batched=True)

# Model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# Training arguments
training_args = TrainingArguments(
    output_dir="./models/demo_bert",
    num_train_epochs=1,
    per_device_train_batch_size=2,
    logging_steps=1,
    save_steps=10,
    save_total_limit=1,
    eval_strategy="no",
)

trainer = Trainer(model=model, args=training_args, train_dataset=dataset)

trainer.train()
trainer.save_model("./models/demo_bert")
