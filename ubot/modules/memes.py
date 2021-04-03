from random import choice
from ubot import ldr

@ldr.add("mock")
async def mock(event):
    text_arg, reply = await event.get_text(default=filler, return_msg=True)

    mock_text = await mockify(text_arg)

    if reply:
        await reply.reply(mock_text)
    else:
        await event.reply(mock_text)


@ldr.add("vap")
async def vapor(event):
    text_arg, reply = await event.get_text(default=filler, return_msg=True)

    vapor_text = await vaporize(text_arg)

    if reply:
        await reply.reply(vapor_text)
    else:
        await event.reply(vapor_text)


@ldr.add("pop")
async def popifycmd(event):
    text_arg, reply = await event.get_text(default=filler, return_msg=True)

    pop_text = await popify(text_arg)

    if reply:
        await reply.reply(pop_text)
    else:
        await event.reply(pop_text)


async def popify(text):
    text = text.replace(" ", "!_")

    return text

async def mockify(text):
    mock_text = ""

    for letter in text:
        if choice([True, False]):
            mock_text += letter.lower()
        else:
            mock_text += letter.upper()

    return mock_text


async def vaporize(text):
    vapor_text = ""
    char_distance = 65248

    for letter in text:
        ord_letter = ord(letter)
        if ord('!') <= ord_letter <= ord('~'):
            letter = chr(ord_letter + char_distance)
        vapor_text += letter

    return vapor_text




