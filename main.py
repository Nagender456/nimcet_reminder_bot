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
cal_command_chats = [1327011060]

def get_time_difference(time1, time2):
    remaining_time = time2 - time1
    remaining_days = remaining_time.days
    remaining_hours, remainder = divmod(remaining_time.seconds, 3600)
    remaining_minutes, remaining_seconds = divmod(remainder, 60)

    return remaining_days, remaining_hours, remaining_minutes, remaining_seconds

def create_cuet_response():
    days, hours, minutes, seconds = get_time_difference(cuet_exam_date, datetime.now(IST))
    cuet_response = f"**⏳ CUET 2024 Over ⏳**\n\n**{days}** __Days__ **{hours}** __Hours__ **{minutes}** __Mins__ **{seconds}** __Secs__ Ago"
    return cuet_response

def create_nimcet_response():
    days, hours, minutes, seconds = get_time_difference(datetime.now(IST), nimcet_exam_date)
    nimcet_response = f"**⏳ Countdown to NIMCET 2024 ⏳**\n\n**{days}** __Days__ **{hours}** __Hours__ **{minutes}** __Mins__ **{seconds}** __Secs__"
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
    chat_id = await event.get_chat()

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

    elif message.startswith('/cal') and chat_id in cal_command_chats:
        message = message[4:].strip()
        if len(message) < 1:
            reply_and_delete(event, "Provide expression to calculate result.", 5)
            return
        expression_evaluation = calculate_expression(message)
        if expression_evaluation is not None:
            await event.reply(expression_evaluation)

    elif random.randint(1, 100) == 1:
        nimcet_response = create_nimcet_response()
        await event.respond(nimcet_response)

async def main():
    await client.start(bot_token=os.getenv('TELEGRAM_BOT_TOKEN'))
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
