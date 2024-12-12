# Run locally
run-dev-live:
	copy live.settings.env settings.env
	uv run python run.py

# Run with docker
run-live: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		trades

# Run locally
run-dev-historical:
	copy historical.settings.env settings.env
	uv run python run.py

# Run with docker
run-historical: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		trades

# DOCKER
build:
	docker build -f Dockerfile -t trades .

docker-run: docker-build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		trades

# MULTISTAGE BUILD METHODS
build-multistage:
	docker build -f multistage.Dockerfile -t trades:multistage . # TODO: optimize docker file with multistage build https://github.com/Real-World-ML/real-time-ml-system-cohort-3/blob/main/services/trades/multistage.Dockerfile

run-multistage: build-multistage # TODO: optimize docker file with multistage build https://github.com/Real-World-ML/real-time-ml-system-cohort-3/blob/main/services/trades/multistage.Dockerfile
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		trades:multistage

build-all: build build-multistage
