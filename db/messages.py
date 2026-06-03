from pool import fetchall, execute

# This icecream is for you: &>


# به ازای هر چت یک کوری ارسال میشه . در نسخه های بعدی به گرفتن تمام پیام های ناخوانده با یک کوری بپرداز
async def store_sent_message(sender_id, conversation_id:int, message):
    query = """
                INSERT INTO semi_messages (sender_id, conversation_id, message_text) VALUES (%s, %s, %s)
            """
    await execute(query, (sender_id, conversation_id, message))

async def get_unread_messages(sender_id, conversation_id:int):
    query = """
                SELECT * FROM semi_messages WHERE (sender_id, conversation_id) = (%s, %s)
            """
    messages = await fetchall(query, (sender_id, conversation:int))
    return messages

async def update_messages_status(sender_id:int, conversation_id:int):
    query = """
                UPDATE semi_messages SET is_read = TRUE WHERE
                                    sender_id = %s,
                                    conversation_id = %s,
                                    is_read = FALSE
            """
    await execute(query, (sender_id, conversation_id))
