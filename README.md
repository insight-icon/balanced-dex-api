# balanced-dex-api
## API Gateway for Balanced Network DEX APIs

##### Links:
> [Balanced Network](https://balanced.network/) |
> [Functional Spec](https://github.com/balancednetwork/docs/blob/master/functional_spec.md#api--ws-endpoints)

#### Steps to run the application

1. Run a kafka node on port 9092, (https://kafka.apache.org/quickstart)
2. Create a topic in kafka
3. Run the command `uvicorn main:app --reload` from project folder (while in development)
