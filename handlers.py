from telegram import Update
from telegram.ext import ContextTypes 
# ---- ENJOY CODING TODAY ----

async def start(update: Update, context: ContextTypes.DefaultType):
    await update.message.reply_text("سلام! خوش آومدی")

async def add_to_waiting(user_id):
    pass

async def match_user(user_id, partner_id):
    pass

async def get_partner(user_id):
    pass

async def end_chat(user_id):
    pass

