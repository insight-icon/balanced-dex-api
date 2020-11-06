# balanced-dex-api

> WIP 

Backend APIs for the Balanced Token DEX. Contains both REST and websocket endpoints for retrieving and subscribing to transactions of the token. Based on FastAPI. 

## Services 

- **blockparser**
    - WIP - Waiting on contracts to be run on testnet 
    - Polls node and filters events based on address then forwards the event logs to Kafka topic  
- **orders** 
    - Takes order events and builds K-Lines (candlestick charts) for DEX 
    - Historical request filled from REST API and realtime updates based on websocket connection 
    - Currently tested based on mocked event logs until contracts running 
    - OpenAPI spec and rendered docs 
    - Checkout it's [README](./orders/README.md) for more info on endpoints 
- **loans** 
    - WIP - Still scoping 
    
## Stack 

- **Kafka** 
    - Main message bus of the stack. 
    - Currently configured with schema registry and confluent control center
- **Redis**
    - Main backend for orders service and websocket connection manager 

## Backend Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.

## Backend local development

* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

* Now you can open your browser and interact with these URLs:

Frontend, built with Docker, with routes handled based on the path: http://localhost

Backend, JSON based web API based on OpenAPI: http://localhost/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost/redoc

Traefik UI, to see how the routes are being handled by the proxy: http://localhost:8090

Confluent Control, UI for kafka cluster: http://localhost:9021/ 

**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.

To check the logs, run:

```bash
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker-compose logs orders
```

#### Test Coverage

Because the test scripts forward arguments to `pytest`, you can enable test coverage HTML report generation by passing `--cov-report=html`.

To run the local tests with coverage HTML reports:

```Bash
DOMAIN=backend sh ./scripts/test-local.sh --cov-report=html
```

To run the tests in a running stack with coverage HTML reports:

```bash
docker-compose exec backend bash /app/tests-start.sh --cov-report=html
```
