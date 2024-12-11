# redpanda management
start-redpanda:
	docker-compose -f redpanda.yml up -d

stop-redpanda:
	docker-compose -f redpanda.yml down

# redpanda topics management
add-one-partition-to-trades-topic:
	docker compose -f redpanda.yml exec redpanda rpk topic add-partitions trades --num 1

# technical indicators pipeline
start-technical-indicators-pipeline:
	docker compose -f technical-indicators-pipeline.yml up -d

stop-technical-indicators-pipeline:
	docker compose -f technical-indicators-pipeline.yml down
