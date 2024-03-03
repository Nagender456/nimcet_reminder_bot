import asyncio
import os, random
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient, events
from extra.poll_creator import create_poll
import pytz

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')

# Define IST timezone
IST = pytz.timezone('Asia/Kolkata')

nimcet_exam_date = datetime(2024, 6, 8, 14, 0, 0, tzinfo=IST)
cuet_exam_date = datetime(2024, 3, 19, 16, 0, 0, tzinfo=IST)

client = TelegramClient('session', api_id, api_hash, request_retries=100, connection_retries=100, retry_delay=5)

# Modify your countdown functions to work with IST
def create_cuet_response():
    cuet_remaining_time = cuet_exam_date - datetime.now(IST)
    cuet_remaining_days = cuet_remaining_time.days
    cuet_remaining_hours, cuet_remainder = divmod(cuet_remaining_time.seconds, 3600)
    cuet_remaining_minutes, _ = divmod(cuet_remainder, 60)
    cuet_response = f"**⏳ Countdown to CUET 2024 ⏳**\n\n**{cuet_remaining_days}** __Days__ **{cuet_remaining_hours}** __Hours__ **{cuet_remaining_minutes}** __Minutes__"
    return cuet_response

def create_nimcet_response():
    nimcet_remaining_time = nimcet_exam_date - datetime.now(IST)
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
    elif message.startswith('/poll'):
        reply_to = getattr(event.message.reply_to, 'reply_to_msg_id', None)

        if reply_to is None:
            await event.reply("__Reply to the question to make poll!__")
            return

        message_parts = message.split()
        correct_option = None
        if len(message_parts) > 1:
            correct_option = message_parts[1][0]
            correct_option = correct_option if correct_option in ['a', 'b', 'c', 'd'] else None

        options_poll = create_poll(correct_option)

        await client.send_message(entity=event.chat_id, file=options_poll, reply_to=reply_to)

    elif random.randint(1, 50) == 1:
        if random.randint(1, 3) > 1:
            nimcet_response = create_nimcet_response()
            await event.respond(nimcet_response)
        else:
            cuet_response = create_cuet_response()
            await event.respond(cuet_response)

async def main():
    await client.start(bot_token=os.getenv('TELEGRAM_BOT_TOKEN'))
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
