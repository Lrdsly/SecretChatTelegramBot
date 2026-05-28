from telegram import Update
from telegram.ext import ContextTypes

from keyboard import ikeyboard, rkeyboard
from db.users import get_or_register_user
from db.redis import add_to_queue, match_users
# ---- ENJOY CODING TODAY ----

# 1 -----
async def start(update: Update, context: ContextTypes.DefaultType):
    user = await get_or_register_user(update.message.chat.id)
    await update.message.reply_text("سلام! خوش آومدی", reply_markup=rkeyboard)

# 2 -----
async def help(update: Update, context: ContextTypes.DefaultType):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("فقط روی دکمه 'شروع چت' کلیک کن تا به یک کاربر تصادفی متصل بشی.")

# 3 -----
async def find_chat(update: Update, context: ContextType.DefaultType):
    await add_to_queue(update.message.chat.id)
    users = await match_users()
    print("-"*100)
    print(users)
    if users:
        for i in range(2):
            await context.bot.send_message(chat_id=users[i], text="شما به یکی وصل شدید که فعلا نمیگم کیه")
    await update.message.reply_text("صبر کن که ز غوره حلوا سازی")

# 4 -----
async def handle_text(update: Update, context: ContextType.DefaultContext):
    text = update.message.text
    if text == "راهنما":
        await update.message.reply_text("فقط روی دکمه شروع چت کلیک کن تا به یک کاربر تصادفی متصل بشی")
    elif text == "شروع چت":
        print("-"*100)
        await find_chat(update, context)

# ------
async def match_user(user_id, partner_id):
    pass

async def get_partner(user_id):
    pass

async def end_chat(user_id):
    pass

