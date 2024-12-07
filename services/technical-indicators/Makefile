# Run locally
run-dev:
	uv run python run.py

# Run with docker
run: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		trades

# DOCKER
build:
	docker build -f Dockerfile -t technical-indicators .

docker-run: docker-build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		technical-indicators

# MULTISTAGE BUILD METHODS
build-multistage:
	docker build -f multistage.Dockerfile -t technical-indicators:multistage . # TODO: optimize docker file with multistage build https://github.com/Real-World-ML/real-time-ml-system-cohort-3/blob/main/services/trades/multistage.Dockerfile

run-multistage: build-multistage # TODO: optimize docker file with multistage build https://github.com/Real-World-ML/real-time-ml-system-cohort-3/blob/main/services/trades/multistage.Dockerfile
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		technical-indicators:multistage

build-all: build build-multistage
