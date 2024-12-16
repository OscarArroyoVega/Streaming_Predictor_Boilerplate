run-dev:
	uv run python -m run

run-claude:
	uv run python -m llms.claude

run-ollama:
	uv run python -m llms.ollama

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
