# Logflow

Logflow is a logging system designed to be used in distributed applications. It is non-blocking and supports structured logging, making it easy to collect logs in a centralized location for analysis and monitoring.

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

The app api uses uvicorn --reload so changes should automatically be recognised.

## Running Tests

To run the tests, use the following command:

```
python logflow_client_test.py
```

This is a simple test runner that generates some synchronous logs via FastAPI -> Redis -> Celery -> File and Postgres.

Note: This architecture is not something I will continue with as a logging system that requires HTTP calls isn't viable in production. I will modify this to instead use an agent that reads from stdout or log file - `Flient Bit`.
