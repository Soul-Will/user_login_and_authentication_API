from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.environ.get("DB_URL")
SENDER_MAIL = os.environ.get("SENDER_MAIL")
PASSWORD = os.environ.get("PASSWORD")
ALGORITHM = os.environ.get("ALGORITHM")
SECRET_KEY = os.environ.get("SECRET_KEY")

