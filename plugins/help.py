from . import client
from telethon import events

@client.on(events.NewMessage(pattern='/help*', incoming=True))
async def _(event):

    reply_msg = """
/help - Display this message.
/nimcet - Get NIMCET 2024 timer.
/cuet - Get CUET 2024 timer.
    """

    await event.reply(reply_msg)
