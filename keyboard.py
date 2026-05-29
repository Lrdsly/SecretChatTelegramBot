from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

# ---- YOU CHOOSE THIS ONE ----

ikeyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("راهنما", callback_data="help")]
])

basic_reply_keyboard_buttons = [["حساب من", "راهنما"], ["شروع چت",]]

rkeyboard = ReplyKeyboardMarkup(
    basic_reply_keyboard_buttons,
    resize_keyboard=True
)

def get_keyboard(buttons:list):
    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
    )
