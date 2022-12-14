import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
RABBIT_URL = os.environ["RABBIT_URL"]
RABBIT_PORT = os.environ["RABBIT_PORT"]
DB_URL = "http://"+os.environ["DB_URL"]+":"+os.environ["DB_PORT"]