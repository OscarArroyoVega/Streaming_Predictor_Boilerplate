run-dev:
#	copy dev.env to .env
	poetry run python src/main.py

build:
	docker build -t trade_to_ohlc .

run: build
	docker run trade_to_ohlc




