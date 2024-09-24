## Exercice of the Cohort 2 of Building a Real-Time ML System Together by Pau Labarta Bajo 

### Summary
This is a real world practice to improve MLOPS and ML engigneering skills. 
The objective it to build a ML system for the crypto price prediction problem.

### Tech stack
-docker
-redpanda(Kafka)
-quixtreams 
-hopsworks 
-comet


### the journey
-Build independent Microservices
-Deal with streaming data and kafka topics
-RESTAPI and WebsocketAPI conections
-Pushing and retrieving topics to and from the feature store
-dockerize real-time feature pipeline
-dockerize backfill pipeline 
-build a training pipeline
-feature engineering
-improve the model with CV hiperparamenter tuning
...


## Session 1 todos


- [x] Redpanda up and running
- [x] Push some fake data to Redpanda
- [x] Push real-time (real data) from Kraken websocket API

## Session 2

- [x] Extract config parameters
- [x] Dockerize it
- [ ] Homework -> adjust the code so that instead of a single product_id, the trade_producer
produces data for several product_ids = ['BTC/USD', 'BTC/EUR']
    My thoughts: you will need to update
        * the config types
        * the Kraken Websocket API class


- [x] Trade to ohlc service
- [ ] Homework: Extract config parameters and dockerize the trade_to_ohlc service.

- [x] Topic to feature store service -> a Kafka consumer
- [ ] Start the backfill
    - [x] Implement a Kraken Historical data reader (trade producer)
    - [x] Adjust timestamps used to bucket trades into windows  (trade to ohlc)
    - [x] Save historical ohlcv features in batches to the offline store (topic_to_feature_store)


## Session 4
- [x] Dockerize our real-time feature pipeline
- [x] Dockerize our backfill pipeline and run it.
- [ ] Build a functional training pipeline
    - [x] Implement a class to read OHLC data from the Feature Store
    - [ ] Build a dummy model to predict price into the future
