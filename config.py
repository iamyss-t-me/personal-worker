from os import environ

class Config:
    API_ID = environ.get("API_ID")
    API_HASH = environ.get("API_HASH")
    BOT_TOKEN = environ.get("BOT_TOKEN")
    LOG_GROUP = environ.get("LOG_GROUP")
    CHANNEL_ID = environ.get("CHANNEL_ID")
    SEEDR_EMAIL = environ.get("SEEDR_EMAIL")
    SEEDR_PASSWORD = environ.get("SEEDR_PASSWORD")
    MONGO_URI = environ.get("MONGO_URI")
    RSS_URL = environ.get("RSS_URL")
    SCREENSHOTS_COUNT = environ.get("SCREENSHOTS_COUNT")
    OWNER_ID = environ.get("OWNER_ID")
    SLEEP_TIME = environ.get("SLEEP_TIME")
    WORKER = environ.get("WORKER")
    MAIN_CHANNEL = environ.get("MAIN_CHANNEL")
