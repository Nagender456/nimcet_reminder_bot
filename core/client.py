import os
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')

client = TelegramClient('session', api_id, api_hash, request_retries=100, connection_retries=100, retry_delay=5)
