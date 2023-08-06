# Copyright 2023 The CambioML Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from accelerate import Accelerator
from datasets import load_dataset
from peft import LoraConfig
from tqdm import tqdm
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    Trainer,
    TrainingArguments, 
    logging, 
    set_seed
)
from transformers.utils import PushToHubMixin
from trl import SFTTrainer
from trl.trainer import ConstantLengthDataset
import os


@dataclass
class RLHFConfig(PushToHubMixin):
    model_path: str
    dataset_name: str
    subset: str
    train_subset: str
    split: str
    size_valid_set: int
    streaming: bool
    shuffle_buffer: int
    seq_length: int
    max_steps: int
    batch_size: int
    gradient_accumulation_steps: int
    eos_token_id: int
    learning_rate: float
    lr_scheduler_type: str
    num_warmup_steps: int
    weight_decay: float
    local_rank: int
    no_fp16: bool
    bf16: bool
    no_gradient_checkpointing: bool
    seed: int
    num_workers: int
    output_dir: str
    log_freq: int
    eval_freq: int
    save_freq: int



class SFT(Trainer):
    def __init__(self, rlhf_config: RLHFConfig):
        self._rlhf_config = rlhf_config
        self.tokenizer = AutoTokenizer.from_pretrained(rlhf_config.model_path)

        self.dataset = self.create_datasets(self.tokenizer, self._rlhf_config)
        self.lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
        )

        self.training_args = TrainingArguments(
            output_dir=self._rlhf_config.output_dir,
            dataloader_drop_last=True,
            evaluation_strategy="steps",
            max_steps=self._rlhf_config.max_steps,
            eval_steps=self._rlhf_config.eval_freq,
            save_steps=self._rlhf_config.save_freq,
            logging_steps=self._rlhf_config.log_freq,
            per_device_train_batch_size=self._rlhf_config.batch_size,
            per_device_eval_batch_size=self._rlhf_config.batch_size,
            learning_rate=self._rlhf_config.learning_rate,
            lr_scheduler_type=self._rlhf_config.lr_scheduler_type,
            warmup_steps=self._rlhf_config.num_warmup_steps,
            gradient_accumulation_steps=self._rlhf_config.gradient_accumulation_steps,
            gradient_checkpointing=not self._rlhf_config.no_gradient_checkpointing,
            fp16=not self._rlhf_config.no_fp16,
            bf16=self._rlhf_config.bf16,
            weight_decay=self._rlhf_config.weight_decay,
            run_name="step1_supervised_finetuning",
            ddp_find_unused_parameters=False,
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self._rlhf_config.model_path, 
            load_in_8bit=True, 
            device_map={"": Accelerator().process_index}
        )

        self.trainer = SFTTrainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.dataset[0],
            eval_dataset=self.dataset[1],
            peft_config=self.lora_config,
            packing=True,
        )

    def train(self):
        self.trainer.train()

    def save(self, path=None):
        if path is None:
            path = os.path.join(self._rlhf_config.output_dir, "supervised_finetuning_final_checkpoint/")
        self.trainer.model.save_pretrained(path)

    def train_and_save(self, output_path=None):
        self.trainer.train()
        self.save(output_path)


    ## TODO: using source code from "supervised_finetuneing.py", need to rewrite to our own `utils.py`
    def prepare_sample_text(self, example):
        """Prepare the text from a sample of the dataset."""
        text = f"Question: {example['question']}\n\nAnswer: {example['response_j']}"
        return text

    ## TODO: using source code from "supervised_finetuneing.py", need to rewrite to our own `utils.py`
    def create_datasets(self, tokenizer, args):
        dataset = load_dataset(
            args.dataset_name,
            data_dir=args.subset,
            split=args.split,
            use_auth_token=True,
            num_proc=args.num_workers if not args.streaming else None,
            streaming=args.streaming,
        )
        if args.streaming:
            print("Loading the dataset in streaming mode")
            valid_data = dataset.take(args.size_valid_set)
            train_data = dataset.skip(args.size_valid_set)
            # if args.train_subset > 0:
            #     train_data = train_data.select(range(args.train_subset))
            train_data = train_data.shuffle(buffer_size=args.shuffle_buffer, seed=args.seed)
        else:
            dataset = dataset.train_test_split(test_size=0.005, seed=args.seed)
            train_data = dataset["train"]
            valid_data = dataset["test"]
            print(f"Size of the train set: {len(train_data)}. Size of the validation set: {len(valid_data)}")

        # chars_per_token = chars_token_ratio(train_data, tokenizer)
        # print(f"The character to token ratio of the dataset is: {chars_per_token:.2f}")

        ## `ConstantLengthDataset` is used for efficient training: we concatenate a lot of 
        ## texts with a EOS token in between and cut chunks of the context size to fill 
        ## the batch without any padding.
        train_dataset = ConstantLengthDataset(
            tokenizer,
            train_data,
            formatting_func=prepare_sample_text,
            infinite=True,
            seq_length=args.seq_length,
            # chars_per_token=chars_per_token,
        )
        valid_dataset = ConstantLengthDataset(
            tokenizer,
            valid_data,
            formatting_func=prepare_sample_text,
            infinite=False,
            seq_length=args.seq_length,
            # chars_per_token=chars_per_token,
        )
        return train_dataset, valid_dataset

    # Add any other methods you need


