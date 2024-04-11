import asyncio
import os, random
from datetime import datetime, timedelta
from telethon import events
from core.client import client
from extra.poll_creator import create_poll
from extra.evaluator import calculate_expression
import pytz

# this imports file the files mentions in plugins/__init__.py
import plugins

IST = pytz.timezone('Asia/Kolkata')
IST_OFFSET_FIX = timedelta(hours=0, minutes=23)

nimcet_exam_date = datetime(2024, 6, 8, 14, 0, 0, tzinfo=IST) + IST_OFFSET_FIX
cuet_exam_date = datetime(2024, 3, 19, 18, 15, 0, tzinfo=IST) + IST_OFFSET_FIX

delete_timer = 36000
admins_id = [1330729713, 5463589388, 6164352361]

def create_cuet_response():
    cuet_remaining_time = datetime.now(IST) - cuet_exam_date
    cuet_remaining_days = cuet_remaining_time.days
    cuet_remaining_hours, cuet_remainder = divmod(cuet_remaining_time.seconds, 3600)
    cuet_remaining_minutes, cuet_remaining_seconds = divmod(cuet_remainder, 60)
    cuet_response = f"**⏳ CUET 2024 Over ⏳**\n\n**{cuet_remaining_days}** __Days__ **{cuet_remaining_hours}** __Hours__ **{cuet_remaining_minutes}** __Mins__ **{cuet_remaining_seconds}** __Secs__ Ago"
    return cuet_response

def create_nimcet_response():
    nimcet_remaining_time = nimcet_exam_date - datetime.now(IST)
    nimcet_remaining_days = nimcet_remaining_time.days
    nimcet_remaining_hours, nimcet_remainder = divmod(nimcet_remaining_time.seconds, 3600)
    nimcet_remaining_minutes, nimcet_remaining_seconds = divmod(nimcet_remainder, 60)
    nimcet_response = f"**⏳ Countdown to NIMCET 2024 ⏳**\n\n**{nimcet_remaining_days}** __Days__ **{nimcet_remaining_hours}** __Hours__ **{nimcet_remaining_minutes}** __Mins__ **{nimcet_remaining_seconds}** __Secs__"
    return nimcet_response

async def send_and_delete(event, message, wait_time=5):
    message = await event.respond(message)
    if wait_time is None: return
    await asyncio.sleep(wait_time)
    await client.delete_messages(event.chat_id, message)

async def reply_and_delete(event, message, wait_time=5):
    message = await event.reply(message)
    if wait_time is None: return
    await asyncio.sleep(wait_time)
    await client.delete_messages(event.chat_id, message)

@client.on(events.NewMessage)
async def handle_message(event):
    global delete_timer
    message = event.message.message.lower()

    if message.startswith('/settime'):
        user = await event.get_sender()
        if user.id in admins_id:
            try:
                time = float(message.split()[1])
                if time < 0:
                    delete_timer = None
                    await event.reply(f"Auto-delete is disabled!")
                else:
                    delete_timer = time
                    await event.reply(f"Auto-delete set to {delete_timer} seconds!")
            except:
                await event.reply("**Usage:**\n\n/settime `time`")
        else:
            await send_and_delete(event, "**Not for you!**")
        return
    elif message.startswith('/delete'):
        user = await event.get_sender()
        if user.id in admins_id:
            reply_to = getattr(event.message.reply_to, 'reply_to_msg_id', None)
            await client.delete_messages(event.chat_id, event.message)
            await client.delete_messages(event.chat_id, reply_to)

    elif message.startswith('/time'):
        if 'cuet' in message:
            cuet_response = create_cuet_response()
            await client.delete_messages(event.chat_id, event.message)
            await send_and_delete(event, cuet_response, delete_timer)
        else:
            nimcet_response = create_nimcet_response()
            await client.delete_messages(event.chat_id, event.message)
            await send_and_delete(event, nimcet_response, delete_timer)
    elif message.startswith('/cuet'):
        cuet_response = create_cuet_response()
        await client.delete_messages(event.chat_id, event.message)
        await send_and_delete(event, cuet_response, delete_timer)
    elif message.startswith('/nimcet'):
        nimcet_response = create_nimcet_response()
        await client.delete_messages(event.chat_id, event.message)
        await send_and_delete(event, nimcet_response, delete_timer)
    elif message.startswith('/poll'):
        reply_to = getattr(event.message.reply_to, 'reply_to_msg_id', None)

        if reply_to is None:
            await event.reply("__Reply to a message to make poll!__")
            return

        message_parts = message.split()
        correct_option = None
        if len(message_parts) > 1:
            correct_option = message_parts[1][0]
            correct_option = correct_option if correct_option in ['a', 'b', 'c', 'd'] else None
            
        if correct_option is not None:
            await client.delete_messages(event.chat_id, event.message)

        options_poll = create_poll(correct_option)

        await client.send_message(entity=event.chat_id, file=options_poll, reply_to=reply_to)

    elif message.startswith('/cal'):
        message = message[4:].strip()
        if len(message) < 1:
            reply_and_delete(event, "Provide expression to calculate result.", 5)
            return
        
        try:
            expression_evaluation = calculate_expression(message)
        except TimeoutError:
            expression_evaluation = "Calculation timed out!"

        if expression_evaluation is not None:
            await event.reply(expression_evaluation)

    elif random.randint(1, 50) == 1:
        nimcet_response = create_nimcet_response()
        await event.respond(nimcet_response)
    

async def main():
    await client.start(bot_token=os.getenv('TELEGRAM_BOT_TOKEN'))
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
