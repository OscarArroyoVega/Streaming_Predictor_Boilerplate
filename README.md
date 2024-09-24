## Welcome to Cohort 2 of Building a Real-Time ML System Together

### In a nutshell

In this second iteration of the course I want to cover more ground. I want us to build a better
ML system for the crypto price prediction problem.

As the duration of the course will be the same as in cohort 1 (which means 4 or 5 weeks) I will re-use
a existing code from the first cohort. Which means that I won't be typing it from beginning to end, but copying fragments of code and walking you through their WHY? and HOW?

<div align="center">
    <img src="./media/ml_system_cohort_2.gif" width='750' />
</div>


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