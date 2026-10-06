from django.apps import AppConfig
from .db_connection import initialize_mongo
from .seed import startup_seed_and_migration


class Week4Config(AppConfig):
    name = "week4"

    def ready(self):
        initialize_mongo()
        startup_seed_and_migration()
