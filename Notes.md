# NOTES of the project

##

## 01 SERVICES

### 01.1 trades
#### description:
- data source: reading from Kraken API
#### features:
- two data sources:
    - realtime data from Kraken websocket API
    - historical data from kraken rest API
- Redpanda kafka topic:
    - trades with timestamp
- multiple pairs options (BTCUSD, ETHUSD, SOLUSD, XRPUSD, etc.)

### 01.2 candles
#### function:
- realtime data processing with quixstreams

### 01.3 technical-indicators
#### function:
- compute technical indicators

### 01.4 to-feature-store
#### function:
- send data to feature store

### 01.5 news
#### function:
- data source: scraper or reading from an API

### 01.6 news-signal
#### function:
- golden_dataset.py: generate a dataset for the news-signal service

### 01.7 price-predictor
#### function:
- build a price predictor that uses the model we trained before
- build a light weight prediction pipeline in RUST for the price-predictor service

####
