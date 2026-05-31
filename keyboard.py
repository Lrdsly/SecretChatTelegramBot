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

keyboard0 = get_keyboard([["حساب من", "راهنما"], ["شروع چت",], ["گفتگو های من"]])
keyboard1 = get_keyboard([["پایان ارتباط", "رد کردن"], ["بازگشت"]])
keyboard2 = get_keyboard([["توقف جستجو"]])
keyboard3 = get_keyboard([["لینک ناشناس من"], ["اطلاعات من"], ["بازگشت"]])
