from telegram import Update
from telegram.ext import ContextTypes

from keyboard import rkeyboard, get_keyboard
from db.users import get_or_register_user
from db import redis as r
from db.pool import fetchone

# ---- ENJOY CODING TODAY ----

# 1 -----
async def start(update: Update, context: ContextTypes.DefaultType):
    u = update.effective_user
    user = await get_or_register_user(telegram_id=u.id,
                                        personal_id=None,
                                        name=u.first_name, lastname=u.last_name,
                                        username=u.username)
    await update.message.reply_text("سلام! خوش آومدی", reply_markup=rkeyboard)

# 2 -----
async def help(update: Update, context: ContextTypes.DefaultType):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("فقط روی دکمه 'شروع چت' کلیک کن تا به یک کاربر تصادفی متصل بشی.")

# 3 -----
async def find_chat(update: Update, context: ContextType.DefaultType):
    await r.add_to_queue(update.message.chat.id)
    users = await r.match_users()

    if users: # get against data, message to user
        for i in range(2):
            ag_user = await fetchone("SELECT * FROM users WHERE telegram_id = %s", (users[i-1],))
            m = ""
            if ag_user[4]:
                m = ag_user[4]
                if ag_user[5]:
                    m += ag_user[5]
            elif ag_user[6]: m = ag_user[6]
             
            await context.bot.send_message(chat_id=users[i], text=f"شما به کاربر {m} وصل شدید.",
                                            reply_markup=get_keyboard([["پایان ارتباط", "رد کردن"]]))
   
    await update.message.reply_text("صبر کن که ز غوره حلوا سازی")

# 4 -----
async def handle_text(update: Update, context: ContextType.DefaultContext):
    text = update.message.text
    user_tid = update.message.chat.id

    print("8"*20)
    print(await r.get_user_state(user_tid))
    if await r.get_user_state(user_tid) == "in-chat":
        against = await r.get_user_against_id(user_tid)
        await context.bot.send_message(chat_id=against, text=text)
        await update.message.reply_text("پیام شما ارسال شد، در انتظار پاسخ شخص مقابل.")

    elif text == "راهنما":
        await update.message.reply_text("فقط روی دکمه شروع چت کلیک کن تا به یک کاربر تصادفی متصل بشی")
    elif text == "شروع چت":
        await find_chat(update, context)
    

# ------

async def end_chat(user_id):
    pass
