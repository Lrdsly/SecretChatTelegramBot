import re

from telegram import Update
from telegram.ext import ContextTypes

from keyboard import get_keyboard
import keyboard as k

import db.semi_anon as semi
import db.messages as m
from db import redis as r
from db.pool import fetchone
from db.anon import end_connection, verify_a_connection
from db.users import get_or_register_user, get_secret_link, get_user_by_personal_id

# ---- ENJOY CODING TODAY ----

# ----- Generals -----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    user = await get_or_register_user(telegram_id=u.id,
                                        personal_id=None,
                                        name=u.first_name, lastname=u.last_name,
                                        username=u.username)
    # Connect users via secret link
    args = context.args
    reply_text, other_text = await semi.make_connection(u.id, args)
    reply_text = reply_text if reply_text else "سلام، به ربات چت ناشناس خوش آمدید. لطفا یک گزینه را انتخاب کنید."
    if other_text:
        against_id = (await get_user_by_personal_id(args[0]))[1]
        await context.bot.send_message(chat_id=against_id, text=other_text, reply_markup=k.keyboard0)
    await update.message.reply_text(reply_text, reply_markup=k.keyboard0)

async def _help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("فقط روی دکمه 'شروع چت' کلیک کن تا به یک کاربر تصادفی متصل بشی.")

# ----- Anonymous ----------
async def find_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id

    await r.add_to_queue(user_id)
    if await verify_a_connection(user_id):
        matched_users = await r.match_users()
        if matched_users:
            for user_id, against_id in (
                (matched_users[0], matched_users[1]),
                (matched_users[1], matched_users[0]),
                ):

                against_name = (await u.get_user_full_name(against_id))[0]

                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"شما به کاربر {against_name} وصل شدید.",
                    reply_markup=k.keyboard1
                )
    else:
        await r.remove_from_queue(user_id)
        reply_text = "شما در حال حاضر در یک گفتگو هستید، لطفا ابتدا آن را پایان دهید."
        await context.bot.send_message(chat_id=update.message.chat.id, text=reply_text, reply_markup=k.keyboard0)

async def end_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    against_id = await r.get_against_id(user_id)
    await end_connection(user_id, against_id)
    await r.end_connection(user_id, against_id)

async def next_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await end_chat(update, context)
    await find_chat(update, context)

# ----- Semi Anonymous -----

async def select_chat(button_text:str, against_id:int):
    sa_connection_id = await r.get_chat_id_by_button(against_id, button_text)
    if bool(sa_connection_id):
        await r.set_current_semi_chat_id(user_id=against_id, chat_id=sa_connection_id)
        sides = await semi.get_semi_chat_sides(sa_connection_id)
        sender_id = sides[0]

        await r.sa_link_client_to_against(against_id, sender_id)
        
        unread_messages = await m.get_unread_messages(sender_id=int(sender_id), conversation_id=int(sa_connection_id))
        unread_messages = [[i, sender_id, sa_connection_id] for i in unread_messages]
        # hint: if unread_messages is empty, it will be [] which make if select_chat return False, so run that function like if select_chat(...) is not False:
        return unread_messages
    return False

async def semi_end_chat(update: Update, context: ContextTypes.DeafultContext, user_id, against_id):
    await semi.end_sa_connection(user_id, against_id)
    await r.end_connection(user_id, against_id)

# ----- Combination --------
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keboard = None
    text = update.message.text
    user_tid = update.message.chat.id
    user_state = await r.get_user_state(user_tid)

    if text == "راهنما":
        await update.message.reply_text("فقط روی دکمه شروع چت کلیک کن تا به یک کاربر تصادفی متصل بشی")

    elif text == "گفتگو های من":
        reply_text = "لیست گفتگو های ناشناس شما:"

        keys = await k.get_semi_chat_buttons(user_tid)
        if keys:    
            keyboard = k.get_keyboard(keys)
        else:
            keyboard = k.keyboard0
            reply_text = "شما درحال حاضر گفتگوی باز ندارید."

        await update.message.reply_text(text=reply_text, reply_markup=keyboard)
    
    elif text == "حساب من":
        await update.message.reply_text("یک گزینه رو انتخاب کنید", reply_markup=k.keyboard3) 

    # user clicked on user* button.
    elif (match := re.fullmatch(r"(user\d+)\s+\(\d+\)", text)):
        keyboard = await k.get_semi_chat_buttons(user_tid)
        keyboard[-1].append("پایان ارتباط")
        keyboard = k.get_keyboard(keyboard)

        chat_state = await select_chat(match.group(1), user_tid)
        if chat_state is not False:
            await update.message.reply_text(f"گفتگوی {match.group(1)} انتخاب شد.", reply_markup=keyboard)
            if len(chat_state) > 0:
                for message in chat_state:
                    await context.bot.send_message(chat_id=user_tid, text=message[0][3])
                else:
                    # mark message as read only if someone else is seeing that
                    if message[1] != user_tid:
                        await m.update_messages_status(sender_id=message[1], conversation_id=message[2])
            else:
                await update.message.reply_text("شما پیام جدیدی در این گفتگو ندارید.", reply_markup=keyboard)
        else:
            await update.message.reply_text("چنین گفتگویی وجود ندارد", reply_markup=k.keboard0)
   
    elif text == "لینک ناشناس من":
        secret_link = await get_secret_link(user_tid)
        reply_text = "لینک ناشناس شما: کافی است روی این لینک کلیک شود تا به طور ناشناس به شما پیام بدهند\n\n\n\n" + secret_link
        await update.message.reply_text(reply_text, reply_markup=k.keyboard3)

    elif text == "بازگشت":
        await update.message.reply_text("صفحه اصلی:", reply_markup=k.keyboard0)
    
    elif text == "شروع چت":
        await update.message.reply_text("در جستجوی یک کاربر، لطفا صبور باشید.", reply_markup=k.keyboard2)
        await find_chat(update, context)

    elif text == "توقف جستجو":
        if await r.get_user_state(user_tid) == "searching":
            await r.update_user_state(user_tid, "balanced")
            await r.remove_from_queue(user_tid)
            await update.message.reply_text("جستجو لغو شد.", reply_markup=k.keyboard0)

    elif user_state == "anon-chat":
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

    elif user_state == "semi-chat":
        reply_text = "پیام شما ارسال شد، در انتظار پاسخ طرف مقابل."
        other_text = text

        current_chat_id = await r.get_current_semi_chat_id(user_tid)
        sides = await semi.get_semi_chat_sides(current_chat_id)
        actual_target_id = sides[1] if user_tid == sides[0] else sides[0]

        keyboard = await k.get_semi_chat_buttons(user_tid)
        keyboard = k.get_keyboard(keyboard)

        if text == "پایان ارتباط":
            await semi_end_chat(update, context, user_tid, actual_target_id)
            keyboard = k.keyboard0
            reply_text = "گفتگو به پایان رسید"
            other_text = "مخاطب به گفتگو پایان داد"

        else:
            current_chat_id = await r.get_current_semi_chat_id(user_tid)
            await m.store_sent_message(user_tid, current_chat_id, text)

        await update.message.reply_text(reply_text, reply_markup=keyboard)
        await context.bot.send_message(chat_id=int(actual_target_id), text=other_text, reply_markup=keyboard)
