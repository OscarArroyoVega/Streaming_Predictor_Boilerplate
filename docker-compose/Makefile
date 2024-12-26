# KAFKA ENVIRONMENT__________________________________________________________________________________________________
# redpanda start/stop
start-redpanda:
	docker-compose -f redpanda.yml up -d

stop-redpanda:
	docker-compose -f redpanda.yml down

# redpanda topics management
add-one-partition-to-trades-topic:
	docker compose -f redpanda.yml exec redpanda rpk topic add-partitions trades --num 1



# PIPELINES__________________________________________________________________________________________________________
# technical indicators pipeline
build-technical-indicators-live:
	docker compose -f technical-indicators-pipeline-live.yml build

build-technical-indicators-historical:
	docker compose -f technical-indicators-pipeline-historical.yml build

# technical indicators pipeline
start-technical-indicators-live: build-technical-indicators-live
	docker compose -f technical-indicators-pipeline-live.yml up -d

stop-technical-indicators-live:
	docker compose -f technical-indicators-pipeline-live.yml down

# for historical data
start-technical-indicators-historical: build-technical-indicators-historical
	@echo "Starting new historical run with ID: $${RUN_ID}"
	@echo "$${RUN_ID}" > .last_run_id
	powershell -ExecutionPolicy Bypass -Command "$$env:RUN_ID = Get-Date -Format 'yyyyMMdd_HHmmss'; docker compose -f technical-indicators-pipeline-historical.yml up -d"

stop-technical-indicators-historical:
	docker compose -f technical-indicators-pipeline-historical.yml down

# news signals pipeline
build-news-signals-pipeline-live:
	docker compose -f news-signals-pipeline-live.yml build

start-news-signals-pipeline-live: build-news-signals-pipeline-live
	docker compose -f news-signals-pipeline-live.yml up -d

stop-news-signals-pipeline-live:
	docker compose -f news-signals-pipeline-live.yml down



# CLEANUP COMMANDS__________________________________________________________________________________________________
# List topics
list-topics:
	docker compose -f redpanda.yml exec redpanda rpk topic list

# Delete topic
delete-topic:
	docker compose -f redpanda.yml exec redpanda rpk topic delete $(topic)

# List topics by pattern
list-topics-by-pattern:
	docker compose -f redpanda.yml exec redpanda bash -c 'rpk topic list | grep -i "$(pattern)"'

# Delete all historical topics except the most recent run
cleanup-historical-topics:
	@docker compose -f redpanda.yml exec redpanda bash -c '\
		latest_run=$$(rpk topic list | grep "historical_[0-9]" | sort -r | head -n 1 | grep -o "historical_[0-9_]*"); \
		echo "Keeping topics from latest run: $$latest_run"; \
		for topic in $$(rpk topic list | grep "historical_[0-9]"); do \
			if [[ $$topic != *"$$latest_run"* ]]; then \
				echo "Deleting $$topic"; \
				rpk topic delete "$$topic"; \
			fi; \
		done'

cleanup-changelog-topics:
	@docker compose -f redpanda.yml exec redpanda bash -c '\
		for topic in $$(rpk topic list | grep "changelog__"); do \
			echo "Deleting $$topic"; \
			rpk topic delete "$$topic"; \
		done'

cleanup-misspelled-topics:
	@docker compose -f redpanda.yml exec redpanda bash -c '\
		for topic in $$(rpk topic list | grep -E "technial|indicatores"); do \
			echo "Deleting misspelled topic: $$topic"; \
			rpk topic delete "$$topic"; \
		done'

cleanup-all:
	@echo "Starting full cleanup..."
	@make cleanup-misspelled-topics
	@make cleanup-changelog-topics
	@make cleanup-historical-topics
	@echo "Cleanup complete!"

# Show topic statistics
topic-stats:
	@docker compose -f redpanda.yml exec redpanda bash -c '\
		echo "=== Topic Statistics ==="; \
		echo "Total topics: $$(rpk topic list | wc -l)"; \
		echo "Historical topics: $$(rpk topic list | grep "historical_[0-9]" | wc -l)"; \
		echo "Changelog topics: $$(rpk topic list | grep "changelog__" | wc -l)"; \
		echo "Latest run: $$(rpk topic list | grep "historical_[0-9]" | sort -r | head -n 1)"; \
		echo "======================"'

cleanup-state-store:
	@echo "Cleaning up state store..."
	@docker compose -f technical-indicators-pipeline-historical.yml exec to-feature-store rm -rf /tmp/quixstreams
	@echo "State store cleaned!"


# CHECK COMMANDS__________________________________________________________________________________________________
list-topics:
	docker compose -f redpanda.yml exec redpanda rpk topic list

consume-technical-indicators:
	docker compose -f redpanda.yml exec redpanda rpk topic consume technical_indicators


# UV RESET
uv clean
delet .venv
delet uv.lock
