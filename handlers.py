from telegram import Update
from telegram.ext import ContextTypes

import keyboard as k
from keyboard import get_keyboard

from db import redis as r
from db.pool import fetchone
from db.anon import end_connection
from db.semi_anon import get_sa_chats_id as get_sci
import db.semi_anon as semia
from db.users import get_or_register_user

# ---- ENJOY CODING TODAY ----

# ----- Generals -----------
async def start(update: Update, context: ContextTypes.DefaultType):
    u = update.effective_user
    user = await get_or_register_user(telegram_id=u.id,
                                        personal_id=None,
                                        name=u.first_name, lastname=u.last_name,
                                        username=u.username)
    await update.message.reply_text("سلام! خوش آومدی", reply_markup=k.keyboard0)

async def _help(update: Update, context: ContextTypes.DefaultType):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("فقط روی دکمه 'شروع چت' کلیک کن تا به یک کاربر تصادفی متصل بشی.")

# ----- Anonymous ----------
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

async def end_chat(update: Update, context: ContextType.DefaultContext):
    user_id = update.message.chat.id
    against_id = await r.get_against_id(user_id)
    await end_connection(user_id, against_id)
    await r.end_connection(user_id, against_id)

async def next_chat(update: Update, context: ContextType.DefaultContext):
    await end_chat(update, context)
    await find_chat(update, context)

# ----- Semi Anonymous -----

# ----- Combination --------
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
        await update.message.reply_text("در جستجوی یک کاربر، لطفا صبور باشید.", reply_markup=k.keyboard2)
        await find_chat(update, context)

    elif text == "توقف جستجو":
        if await r.get_user_state(user_tid) == "searching":
            await r.update_user_state(user_tid, "balanced")
            await r.remove_from_queue(user_tid)
            await update.message.reply_text("جستجو لغو شد.", reply_markup=k.keyboard0)

    elif text == "گفتگو های من":
        reply_text = "لیست گفتگو های ناشناس شما:"
        
        chats = await get_sci(user_tid)
        chats_count = len(chats)
        
        if chats_count > 1:
            buttons = []

            for i in range(chats_count):
                unread_messages = len(await semi.get_unread_messages(chats[i]))
                buttons.append(f"user{i+1} ({unread_messages})")

            keyboard_buttons = [
                buttons[i:i+2]
                for i in range(0, len(buttons), 2)
            ]
            keyboard_buttons.append(["بازگشت"])
            keyboard = get_keyboard(keyboard_buttons)
        elif chats_count == 1: 
            keyboard = get_keyboard([[f"user1 ({len(await semi.get_unread_messages(chats[0]))})"], ["بازگشت"]])
        else:
            reply_text = "شما درحال حاضر گفتگوی باز ندارید."
            keyboard = k.keyboard0
        await update.message.reply_text(text=reply_text, reply_markup=keyboard)
    
    elif text == "بازگشت":
        await update.message.reply_text("صفحه اصلی:", reply_markup=k.keyboard0)