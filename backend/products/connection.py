from mongoengine import connect

def init_mongo():
    connect(
        db="Products_db",
        username="root",
        password="example",
        host="mongodb://root:example@localhost:27018/Products_db?authSource=admin",
    )