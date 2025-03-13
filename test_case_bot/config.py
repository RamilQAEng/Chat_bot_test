import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
AUTHORIZATION_KEY = os.getenv("AUTHORIZATION_KEY")
SCOPE = os.getenv("SCOPE", "GIGACHAT_API_PERS")
TOKEN_URL = os.getenv("TOKEN_URL")
API_URL = os.getenv("API_URL")