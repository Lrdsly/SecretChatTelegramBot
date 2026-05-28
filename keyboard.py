from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

# ---- YOU CHOOSE THIS ONE ----

ikeyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("راهنما", callback_data="help")]
])

rkeyboard = ReplyKeyboardMarkup(
    [["حساب من", "راهنما", "شروع چت"]],
    resize_keyboard=True
)
