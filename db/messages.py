from db.pool import fetchall, fetchone, execute

# This icecream is for you: &>


# به ازای هر چت یک کوری ارسال میشه . در نسخه های بعدی به گرفتن تمام پیام های ناخوانده با یک کوری بپرداز
async def store_sent_message(sender_id, conversation_id:int, message):
    query = """
                INSERT INTO semi_messages (sender_id, conversation_id, message_text) VALUES (%s, %s, %s)
            """
    await execute(query, (sender_id, conversation_id, message))

async def get_unread_messages(sender_id, conversation_id:int):
    query = """
                SELECT * FROM semi_messages WHERE (sender_id, conversation_id) = (%s, %s) AND is_read = FALSE
            """
    messages = await fetchall(query, (sender_id, conversation_id))
    return messages

async def get_unread_messages_count(conversation_id:int, reciver_id):
    query = """
                SELECT COUNT(*) FROM semi_messages WHERE
                conversation_id = %s AND
                sender_id <> %s AND
                is_read = FALSE
            """
    return (await fetchone(query, (conversation_id, reciver_id)))[0]

async def update_messages_status(sender_id:int, conversation_id:int):
    query = """
                UPDATE semi_messages SET is_read = TRUE WHERE
                                    sender_id = %s AND
                                    conversation_id = %s AND
                                    is_read = FALSE
            """
    await execute(query, (sender_id, conversation_id))
