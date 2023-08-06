#custom model 
import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, DataCollatorWithPadding, AutoModelForSequenceClassification, TrainingArguments, Trainer
import evaluate
import numpy as np
from transformers import pipeline
class TextClassifier:
    def __init__(self, model_name, num_labels, id2label, label2id):
        self.model_name = model_name
        self.num_labels = num_labels
        self.id2label = id2label
        self.label2id = label2id
        self.model = None
        self.tokenizer = None
        self.data_collator = None
        self.trainer = None

    def load_dataset(self, dataset_path):
        df = pd.read_csv(dataset_path)
        data = {
            "text": df["text"].tolist(),
            "label": df["label"].tolist()
        }
        dataset = Dataset.from_dict(data)
        return dataset.train_test_split()

    def preprocess_function(self, examples):
        return self.tokenizer(examples["text"], truncation=True)

    def compute_metrics(self, eval_pred):
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return evaluate.load("accuracy").compute(predictions=predictions, references=labels)

    def train(self, dataset, output_dir, learning_rate, batch_size, num_epochs, weight_decay):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        tokenized_dataset = dataset.map(self.preprocess_function, batched=True)
        self.data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer, return_tensors="pt")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=self.num_labels,
            id2label=self.id2label,
            label2id=self.label2id
        )
        training_args = TrainingArguments(
            output_dir=output_dir,
            learning_rate=learning_rate,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            num_train_epochs=num_epochs,
            weight_decay=weight_decay,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
        )
        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset["train"],
            eval_dataset=tokenized_dataset["test"],
            tokenizer=self.tokenizer,
            data_collator=self.data_collator,
            compute_metrics=self.compute_metrics
        )
        self.trainer.train()

    def load_model(self, model_path):
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

    def inference(self, text):
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model and tokenizer need to be loaded before making inferences.")
        classifier = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)
        return classifier(text)
