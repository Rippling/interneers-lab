from mongoengine import connect
from dotenv import dotenv_values

def init_db():
    config= dotenv_values(".env")
    connect(
        db= config["DB_NAME"],
        username= config["MONGO_USER"],
        password= config["MONGO_PASSWORD"],
        host= config["MONGO_HOST"],
        port= int(config["MONGO_PORT"])
    )
