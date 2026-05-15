# this prepares the env so that week8 can send traces to LangSmith
import os
from dotenv import load_dotenv
from week8.config import TRACING_PROJECT_NAME

load_dotenv()


def setup_langsmith_tracing():
    api_key = os.getenv("LANGSMITH_API_KEY")
    if not api_key:
        return False
    os.environ["LANGSMITH_API_KEY"] = api_key
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_PROJECT"] = TRACING_PROJECT_NAME
    endpoint = os.getenv("LANGSMITH_ENDPOINT")
    if endpoint:
        os.environ["LANGSMITH_ENDPOINT"] = endpoint

    return True


def is_langsmith_enabled():
    return os.getenv("LANGSMITH_TRACING", "").lower() == "true"


if __name__ == "__main__":
    enabled = setup_langsmith_tracing()
    if enabled:
        print("LangSmith tracing is enabled.")
        print(f"Project: {os.getenv('LANGSMITH_PROJECT')}")
        if os.getenv("LANGSMITH_ENDPOINT"):
            print(f"Endpoint: {os.getenv('LANGSMITH_ENDPOINT')}")
    else:
        print("LangSmith tracing is disabled because LANGSMITH_API_KEY was not found.")
