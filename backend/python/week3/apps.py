from django.apps import AppConfig
from .db_connection import initialize_mongo


class Week3Config(AppConfig):
    name = "week3"

    def ready(self):
        initialize_mongo()
