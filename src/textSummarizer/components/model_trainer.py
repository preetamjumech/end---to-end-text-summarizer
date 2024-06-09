
from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk
import torch
import os
from textSummarizer.entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
    
    def train(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model_t5 = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model= model_t5)

        dataset_samsum_pt = load_from_disk(self.config.data_path)

        trainer_args = TrainingArguments(
            output_dir=self.config.root_dir, num_train_epochs=1, warmup_steps=50,
            per_device_train_batch_size=1, per_device_eval_batch_size=1,
            weight_decay=0.01, logging_steps=10,
            eval_strategy='steps', eval_steps=50, save_steps=1e6,
            gradient_accumulation_steps=16
        )
        
        trainer = Trainer(model=model_t5, args=trainer_args,
                  tokenizer=tokenizer, data_collator=seq2seq_data_collator,
                  train_dataset=dataset_samsum_pt["test"],  # PLEASE CHANGE THIS TO TRAIN IN REAL TIME, DUE TO RESOURCE CONSARINTS ONLY TEST DATA IS USED
                  eval_dataset=dataset_samsum_pt["validation"])
        

        trainer.train()
        
        model_t5.save_pretrained(os.path.join(self.config.root_dir, "t5-model"))
        tokenizer.save_pretrained(os.path.join(self.config.root_dir, "tokenizer"))