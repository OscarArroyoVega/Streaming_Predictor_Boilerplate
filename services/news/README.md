this service retrieves news from the news api and stores it in the feature store

1. data picked from cryptopanic api
2. through the rest api of the service / REMOVE REPLICATE VALUES
3. as there is no streaming api (websocket) /
4. we will use a cron job to retrieve the news every 30 seconds- 1 minute
5. an indicator feature will be created for each news
6. the indicator feature will be stored in the feature store
