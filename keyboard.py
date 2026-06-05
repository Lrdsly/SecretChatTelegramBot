from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

import db.messages as messages
import db.semi_anon as semi
import db.redis as r

# ---- YOU CHOOSE THIS ONE ----

ikeyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("راهنما", callback_data="help")]
])

def get_keyboard(buttons:list):
    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
    )

keyboard0 = get_keyboard([["حساب من", "راهنما"], ["شروع چت",], ["گفتگو های من"]])
keyboard1 = get_keyboard([["پایان ارتباط", "رد کردن"], ["بازگشت"]])
keyboard2 = get_keyboard([["توقف جستجو"]])
keyboard3 = get_keyboard([["لینک ناشناس من"], ["اطلاعات من"], ["بازگشت"]])


async def get_semi_chat_buttons(user_id):
    """ 
        return a markupKeyboard which include sa_connections rows which user is the 'against' part of them
        also store all of these sa_connection id into redis 
    """

    chats_id = await semi.get_semi_chats_id(user_id)
    if not chats_id: return False

    chats_count = len(chats_id)
    chatmap = {f"user{i+1}":chats_id[i][0] for i in range(chats_count)}
    await r.store_chat_id_hash(chatmap, user_id)

    if chats_count > 1:
        buttons = []

        for i in range(chats_count):
            unread_messages = await messages.get_unread_messages_count(chats_id[i][0])
            buttons.append(f"user{i+1} ({unread_messages})")

        keyboard_buttons = [
            buttons[i:i+2]
            for i in range(0, len(buttons), 2)
            ]
        keyboard_buttons.append(["بازگشت"])
        keyboard = get_keyboard(keyboard_buttons)
        return keyboard

    elif chats_count == 1: 
        keyboard = get_keyboard([[f"user1 ({await messages.get_unread_messages_count(chats_id[0][0])})"], ["بازگشت"]])
        return keyboard
