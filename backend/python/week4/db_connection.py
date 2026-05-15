import os
from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()


def initialize_mongo():
    mongo_user = os.getenv("MONGO_USER", "root")
    mongo_pass = os.getenv("MONGO_PASS", "example")
    mongo_host = os.getenv("MONGO_HOST", "localhost")
    mongo_port = os.getenv("MONGO_PORT", "27019")
    mongo_db = os.getenv("MONGO_DB", "interneers_lab_week4")

    # mongodb://root:example@localhost:27019/interneers_lab_week4?authSource=admin
    mongo_uri = (
        f"mongodb://{mongo_user}:{mongo_pass}"
        f"@{mongo_host}:{mongo_port}/{mongo_db}?authSource=admin"
    )

    connect(
        db=mongo_db,
        host=mongo_uri,
        alias="default",
    )
