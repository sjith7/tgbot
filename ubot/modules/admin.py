from ubot import ldr


@ldr.add("warn", help="Reply")
async def delete_message(event):
    message_to_delete = await event.get_reply_message()

    if message_to_delete and message_to_delete.sender_id == (await event.client.get_me()).id:
        await message_to_delete.delete()


