from telegram import Update
from telegram.ext import ContextTypes

import keyboard as k
from keyboard import get_keyboard
from db.users import get_or_register_user
from db import redis as r
from db.pool import fetchone
from db.anon import end_connection

# ---- ENJOY CODING TODAY ----

# 1 -----
async def start(update: Update, context: ContextTypes.DefaultType):
    u = update.effective_user
    user = await get_or_register_user(telegram_id=u.id,
                                        personal_id=None,
                                        name=u.first_name, lastname=u.last_name,
                                        username=u.username)
    await update.message.reply_text("سلام! خوش آومدی", reply_markup=k.keyboard0)

# 2 -----
async def _help(update: Update, context: ContextTypes.DefaultType):
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
                                            reply_markup=k.keyboard1)

# 4 -----
async def end_chat(update: Update, context: ContextType.DefaultContext):
    user_id = update.message.chat.id
    against_id = await r.get_against_id(user_id)
    await end_connection(user_id, against_id)
    await r.end_connection(user_id, against_id)

# 5 -----
async def next_chat(update: Update, context: ContextType.DefaultContext):
    await end_chat(update, context)
    await find_chat(update, context)

# 6 -----
async def handle_text(update: Update, context: ContextType.DefaultContext):
    keboard = None
    text = update.message.text
    user_tid = update.message.chat.id

    if await r.get_user_state(user_tid) == "in-chat":
        reply_text = "پیام شما ارسال شد، در انتظار پاسخ شخص مقابل."
        
        against = await r.get_against_id(user_tid)
        if text == "پایان ارتباط":
            await end_chat(update, context)
            reply_text = "ارتباط شما به پایان رسید."
            other_text = f"مخاطب گفتگو رو پایان داد."
            keyboard = k.keyboard0
        elif text == "رد کردن":
            await next_chat(update, context)
            reply_text = "ارتباط شما به پایان رسید،\n در حال جتستجوی مخاطب بعد."
            other_text = f"مخاطب گفتگو رو پایان داد"
            keyboard = k.keyboard0
        else:
            other_text = text
            keyboard = k.keyboard1
    
        await context.bot.send_message(chat_id=against, text=other_text, reply_markup=keyboard)
        await update.message.reply_text(reply_text, reply_markup=keyboard)

    elif text == "راهنما":
        await update.message.reply_text("فقط روی دکمه شروع چت کلیک کن تا به یک کاربر تصادفی متصل بشی")
    elif text == "شروع چت":
        await update.message.reply_text("در جستجوی یک کاربر، لطفا صبور باشید.")
        await find_chat(update, context)
