# redpanda management
start-redpanda:
	docker-compose -f redpanda.yml up -d

stop-redpanda:
	docker-compose -f redpanda.yml down

# redpanda topics management
add-one-partition-to-trades-topic:
	docker compose -f redpanda.yml exec redpanda rpk topic add-partitions trades --num 1

build-technical-indicators-live:
	docker compose -f technical-indicators-pipeline.yml build

build-technical-indicators-historical:
	docker compose -f technical-indicators-pipeline-historical.yml build

# technical indicators pipeline
start-technical-indicators-live: build-technical-indicators-live
	docker compose -f technical-indicators-pipeline.yml up -d

stop-technical-indicators-live:
	docker compose -f technical-indicators-pipeline.yml down

# for historical data
start-technical-indicators-historical: build-technical-indicators-historical
	powershell -Command "$$env:RUN_ID = Get-Date -Format 'yyyyMMdd_HHmmss'; docker compose -f technical-indicators-pipeline-historical.yml up -d"

stop-technical-indicators-historical:
	docker compose -f technical-indicators-pipeline-historical.yml down
