from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

# ---- YOU CHOOSE THIS ONE ----

ikeyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("راهنما", callback_data="help")]
])

def get_keyboard(buttons:list):
    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
    )

keyboard0 = get_keyboard([["حساب من", "راهنما"], ["شروع چت",]])
keyboard1 = get_keyboard([["پایان ارتباط", "رد کردن"]])
