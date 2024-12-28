import os
from typing import Optional, Tuple

import comet_ml
import torch
from datasets import Dataset, load_dataset
from loguru import logger
from transformers import AutoTokenizer, TrainingArguments
from trl import SFTTrainer
from unsloth import FastLanguageModel


def load_base_llm_and_tokenizer(
    base_llm_name: str,
    max_seq_length: Optional[int] = 2048,
    dtype: Optional[str] = None,
    load_in_4bit: Optional[bool] = True,
) -> Tuple[FastLanguageModel, AutoTokenizer]:
    """
    Loads the base llm and its tokenizer
    """
    logger.info(f'Loading base llm and tokenizer for {base_llm_name}')
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=base_llm_name,
        max_seq_length=max_seq_length,
        dtype=dtype,
        load_in_4bit=load_in_4bit,
        # token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
    )
    return model, tokenizer


def add_lora_adapter(model: FastLanguageModel, eos_token: str) -> FastLanguageModel:
    """
    Adds a LoRA adapter to the model
    """
    # TODO: expose these parameters as function arguments so we can tune them
    # TODO: add a futh" uses 30% less VRAM, fits 2x larger batch sizes!
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,  # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
        target_modules=[
            'q_proj',
            'k_proj',
            'v_proj',
            'o_proj',
            'gate_proj',
            'up_proj',
            'down_proj',
        ],
        lora_alpha=16,
        lora_dropout=0,  # Supports any, but = 0 is optimized
        bias='none',  # Supports any, but = "none" is optimized
        # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
        use_gradient_checkpointing='unsloth',  # True or "unsloth" for very long context
        random_state=3407,
        use_rslora=False,  # We support rank stabilized LoRA
        loftq_config=None,  # And LoftQ
    )
    return model


def load_dataset_and_format(
    dataset_path: str, tokenizer: AutoTokenizer
) -> Tuple[Dataset, Dataset]:
    """
    Loads the dataset and preprocesses it
    """
    logger.info(f'Loading dataset from {dataset_path}')
    dataset = load_dataset('json', data_files=dataset_path)

    dataset = dataset['train']
    logger.info(f'example dataset: {dataset[0]}')

    def format_prompts(examples):
        # chat template to format the data for the model
        alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

        ### Instruction:
        {instruction}

        ### Input:
        {input}

        ### Response:
        {output}"""

        instructions = examples['instruction']
        inputs = examples['input']
        outputs = examples['output']
        texts = []
        for instr, inp, out in zip(instructions, inputs, outputs):
            text = (
                alpaca_prompt.format(instruction=instr, input=inp, output=out)
                + tokenizer.eos_token
            )  # must add eos_token to the end of the input and output
            texts.append(text)
        return {
            'text': texts,
        }

    dataset = dataset.map(format_prompts, batched=True)

    dataset = dataset.train_test_split(test_size=0.1, seed=1024)
    train_dataset = dataset['train']
    test_dataset = dataset['test']
    logger.info(f'example train dataset: {train_dataset[0]}')
    logger.info(f'example test dataset: {test_dataset[0]}')
    return train_dataset, test_dataset


def fine_tune_model(
    model: FastLanguageModel,
    tokenizer: AutoTokenizer,
    train_dataset: Dataset,
    test_dataset: Dataset,
    max_seq_length: int,
) -> FastLanguageModel:
    """
    Fine tunes the model using supervised fine tuning
    """
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        dataset_text_field='text',
        max_seq_length=max_seq_length,
        dataset_num_proc=2,
        packing=False,  # Can make training 5x faster for short sequences.
        args=TrainingArguments(
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            warmup_steps=5,
            num_train_epochs=1,
            max_steps=60,
            learning_rate=2e-4,
            fp16=not torch.cuda.is_bf16_supported(),
            bf16=torch.cuda.is_bf16_supported(),
            logging_steps=1,
            optim='adamw_8bit',
            weight_decay=0.01,
            lr_scheduler_type='linear',
            seed=3407,
            output_dir='outputs',
            report_to='comet_ml',
        ),
    )
    logger.info(f'trainer: {trainer}')
    trainer.train()

    return model


def run(
    base_llm_name: str,
    dataset_path: str,
    comet_project_name: str,
    max_seq_length: int,
    # comet_api_key: str, TODO: we introduce a comet api key directly in the terminal, so we need to make it more programatic
):
    """
    Fine tuning the model using supervised fine tuning
    the training results are logget to comet ml
    the final artifact is saved as an ollama model, so it can be used to generate signals locally
    """

    # 0. login to comet ml so we can log the training results
    os.environ['COMET_LOG_ASSETS'] = 'True'
    comet_ml.login(
        project_name=comet_project_name,
        # api_key=comet_api_key # TODO: we introduce a comet api key directly in the terminal, so we need to make it more programatic
    )
    logger.info(f'Logged in to comet ml with project {comet_project_name}')

    # 1. load the base llm and tokenizer
    model, tokenizer = load_base_llm_and_tokenizer(base_llm_name)
    # 2. add the lora adapter
    model = add_lora_adapter(model, tokenizer.eos_token)
    # 3. load the dataset with (instruction, input, output) tuples into  a huggingface dataset object\
    # the dataset is formatted with the alpaca prompt template
    train_dataset, test_dataset = load_dataset_and_format(dataset_path, tokenizer)
    # 4. finetune the model
    model = fine_tune_model(
        model, tokenizer, train_dataset, test_dataset, max_seq_length=max_seq_length
    )
    # 5. save the model


if __name__ == '__main__':
    from fire import Fire

    Fire(run)
