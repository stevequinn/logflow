# Logflow

Logflow is a logging system designed to be used in distributed applications. It is non-blocking and supports structured logging, making it easy to collect logs in a centralized location for analysis and monitoring.

Logs are collected using Fluent Bit. Each client should have its own API key for authentication. Logs are sent to a FastAPI application which validates the API key and pushes the logs to a Redis queue. Celery workers then process the logs asynchronously, writing them to either a PostgreSQL database, a file system, or both, depending on configuration.

Ensure you have the following environment variables set in a `.env` file or your environment:

```
LOGFLOW_API_KEY=
```

Ensure you have fluent-bit installed and configure it to send logs to the Logflow API.

See files in `./fluent-bit/` for example configuration.

## Dev Notes

To run, you will need Docker and Docker Compose installed on your machine.

```
docker-compose up --build
```

Once built, you can start or stop the services with:

```
docker-compose up -d
docker-compose down
``` 

To view logs
```
docker-compose logs -f
```

```
docker-compose logs -f worker
```

When making changes to the worker code, restart the worker container to apply the changes:

```
docker-compose restart worker
```

Running multiple celery workers
```
docker compose up --scale worker=2 -d
```

The app api uses uvicorn --reload so changes should automatically be recognised.

## Running Tests

To run the tests, use the following command:

```
python logflow_http_client_test.py
```

This is a simple test runner that generates some synchronous logs via FastAPI -> Redis -> Celery -> File and Postgres.

```
python logflow_filelog_test.py
```

This writes logs to file under the ./logs direectory which are then collected by the Fluent Bit agent and sent to Logflow.

---

Made for fun and to play with log ingestion optimisation petterns.
