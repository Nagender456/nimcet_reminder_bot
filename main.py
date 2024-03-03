import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')

nimcet_exam_date = datetime(2024, 6, 8, 14, 0, 0)
cuet_exam_date = datetime(2024, 3, 19, 16, 0, 0)

client = TelegramClient('session', api_id, api_hash)

def create_cuet_response():
    cuet_remaining_time = cuet_exam_date - datetime.now()
    cuet_remaining_days = cuet_remaining_time.days
    cuet_remaining_hours, cuet_remainder = divmod(cuet_remaining_time.seconds, 3600)
    cuet_remaining_minutes, _ = divmod(cuet_remainder, 60)
    cuet_response = f"**⏳ Countdown to CUET 2024 ⏳**\n\n**{cuet_remaining_days}** __Days__ **{cuet_remaining_hours}** __Hours__ **{cuet_remaining_minutes}** __Minutes__"
    return cuet_response

def create_nimcet_response():
    nimcet_remaining_time = nimcet_exam_date - datetime.now()
    nimcet_remaining_days = nimcet_remaining_time.days
    nimcet_remaining_hours, nimcet_remainder = divmod(nimcet_remaining_time.seconds, 3600)
    nimcet_remaining_minutes, _ = divmod(nimcet_remainder, 60)
    nimcet_response = f"**⏳ Countdown to NIMCET 2024 ⏳**\n\n**{nimcet_remaining_days}** __Days__ **{nimcet_remaining_hours}** __Hours__ **{nimcet_remaining_minutes}** __Minutes__"
    return nimcet_response

@client.on(events.NewMessage)
async def handle_message(event):
    message = event.message.message.lower()
    if message.startswith('/time'):
        if 'cuet' in message:
            cuet_response = create_cuet_response()
            await event.respond(cuet_response)
        else:
            nimcet_response = create_nimcet_response()
            await event.respond(nimcet_response)
    elif message.startswith('/cuet'):
        cuet_response = create_cuet_response()
        await event.respond(cuet_response)
    elif message.startswith('/nimcet'):
        nimcet_response = create_nimcet_response()
        await event.respond(nimcet_response)

async def main():
    await client.start(bot_token=os.getenv('TELEGRAM_BOT_TOKEN'))
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
