# balanced-dex-api

## Backend Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.

## Backend local development

* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

-- Note: Enter bash `exec` inside the running container:

```console
$ docker-compose exec backend bash
```
* Now you can open your browser and interact with these URLs:

Backend, JSON based web API based on OpenAPI: http://localhost/api/...

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost/redoc

Backend: http://localhost:80

Redis: http://localhost:6379

Mongodb: http://localhost:27017

Kafka control center: http://localhost:9021

Traefik UI, to see how the routes are being handled by the proxy: http://localhost:8090

## APIs

### protocol - http

* POST /api/v1/balanced/event

Receives event or trade and process the input data to update state of the system. Return updates in the state of the system.

* POST /api/v1/balanced/search

Receives a pattern for searching the redis database for the matching keys.

* GET /api/v1/balanced/depth/market/{market}

Gets order book for the given market, or all market if market value is *.

* GET /api/v1/balanced/kline/market/{market}/interval/{interval}/count/{count}

Gets klines for the given interval, starting from current till count
 
### protocol - ws

* WS /api/v1/balanced/transaction/subscribe/address/{address}

Push any event or trade relating to the user address.

* WS /api/v1/balanced/depth/subscribe/market/{market}

Push new depth values for corresponding market.

* WS /api/v1/balanced/kline/subscribe/market/{market}/interval/{interval}

Push new kline values for the corresponding interval.

## Tests

* Run tests while application is running, by using the following command from project folder `/balanced-dex-api/orders/app`

```bash
PYTHONPATH=. pytest
``` 