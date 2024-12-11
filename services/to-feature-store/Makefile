# Run locally
run-dev:
	uv run python run.py

# Run with docker
run: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		to-feature-store

# DOCKER
build:
	docker build -f Dockerfile -t to-feature-store .

docker-run: docker-build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		to-feature-store

# MULTISTAGE BUILD METHODS
build-multistage:
	docker build -f multistage.Dockerfile -t to-feature-store:multistage . # TODO: optimize docker file with multistage build https://github.com/Real-World-ML/real-time-ml-system-cohort-3/blob/main/services/trades/multistage.Dockerfile

run-multistage: build-multistage
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		to-feature-store:multistage

build-all: build build-multistage
