import os

from dotenv import load_dotenv

from .logflow_client import LogFlowClient

load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("LOGFLOW_API_KEY", "NO API KEY SET IN .env")
API_URL = os.getenv("API_URL", "http://localhost:8100")


def test_logflow_client():
    if API_KEY == "NO API KEY SET IN .env":
        print("FATAL: Please update API_KEY in test_logflow_client.py before running.")
        return  # Use return instead of exit(1) in async function

    log_client = LogFlowClient(api_url=API_URL, api_key=API_KEY)
    print("\n--- Sending Test Logs ---")

    # 1. Simple INFO log
    log_client.info("User session started.", metadata={"session_id": "abc-12345"})

    # 2. WARNING log with complex metadata
    user_id = 5
    while user_id > 0:
        log_client.warning(
            "Database query took too long.",
            metadata={
                "user_id": user_id,
                "query_time_ms": 1250,
                "endpoint": "/v1/users/profile",
            },
        )
        user_id -= 1

    # 3. CRITICAL log
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        log_client.critical(
            "A critical exception occurred during calculation.",
            metadata={
                "exception_type": str(type(e)),
                "stack_trace": "See main service logs for full traceback.",
                "retry_attempt": 1,
            },
        )

    print("\nLogs sent successfully (queued status should be confirmed by API).")
    print(
        "Check your worker logs (docker-compose logs worker) and database for persistence."
    )


if __name__ == "__main__":
    # for _ in range(100):
    test_logflow_client()
