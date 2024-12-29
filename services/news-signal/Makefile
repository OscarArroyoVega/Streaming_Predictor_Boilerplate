run-dev:
	uv run python -m run

run-claude:
	uv run python -m llms.claude

run-ollama:
	set "OLLAMA_BASE_URL=http://localhost:11434" && uv run python -m llms.ollama

start-ollama:
	ollama serve

stop-ollama:
	ollama stop

build:
	docker build -f Dockerfile -t news-signal .

run-with-anthropic: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		-e MODEL_PROVIDER=anthropic \
		--env-file anthropic_credentials.env \
		news-signal

run-with-ollama: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		-e MODEL_PROVIDER=ollama \
		--env-file ollama.env \
		news-signal

# To generate a golden dataset with (instruction, input, output) tuples to do
# Supervised Fine Tuning
run-golden-dataset:
	uv run python golden_dataset.py

# To generate a golden dataset with (instruction, input, output) tuples to do
# Supervised Fine Tuning.
golden-dataset-with-claude:
	uv run python golden_dataset.py \
		--model_provider anthropic \
		--n 10000 \
		--input_file ./data/cryptopanic_news.csv \
		--output_file ./data/instruction_dataset_claude_10k.jsonl

golden-dataset-with-ollama:
	uv run python golden_dataset.py \
		--model_provider ollama \
		--n 10000 \
		--input_file ./data/cryptopanic_news.csv \
		--output_file ./data/instruction_dataset_ollama_10k.jsonl

venv-gpu-instance:
	curl -LsSf https://astral.sh/uv/install.sh | sh && \
	source $HOME/.local/bin/env && \
	uv sync --group gpu-instance

login-comet:
	uv run comet login

fine-tune:
	python fine_tuning.py \
        --base_llm_name unsloth/Llama-3.2-1B-bnb-4bit \
        --dataset_path ./data/instruction_dataset_ollama_10k.jsonl \
        --comet_project_name news-signal \
        --max_seq_length 1024 \
        --quantization_method q8_0 \
        --hf_username oscararroyovega \
        --hf_token $HF_TOKEN
		--max_steps 60