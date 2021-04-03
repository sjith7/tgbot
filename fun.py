from random import choice

from ubot import ldr


@ldr.add("kickme", fun=True)
async def kickme(event):
    await event.reply("Ok!!")

    try:
        await event.client.kick_participant(event.chat, await event.get_sender())
    except:
        pass


