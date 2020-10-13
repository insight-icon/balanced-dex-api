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

* POST /balanced/event

Receives event or trade and process the input data to update state of the system. Return updates in the state of the system.

* POST /balanced/search

Receives a pattern for searching the redis database for the matching keys.

* GET /balanced/depth/{market}

Gets order book for the given market, or all market if market value is *.

* GET /balanced/kline/{interval}/count/{count}

Gets klines for the given interval, starting from current till count
 
### protocol - ws

* WS /balanced/transaction/subscribe/{address}

Push any event or trade relating to the user address.

* WS /balanced/depth/subscribe/{market}

Push new depth values for corresponding market.

* WS /balanced/kline/subscribe/{market}/{interval}

Push new kline values for the corresponding interval.

## Tests

* Run tests while application is running, by using the following command from project folder

```bash
PYTHONPATH=. pytest
``` 