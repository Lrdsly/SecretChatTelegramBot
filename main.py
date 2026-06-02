from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

import db.pool as pool
import db.initialize as initializer
import handlers

from dotenv import load_dotenv
import asyncio
import os

# ---- ENJOY CODING TODAY ----

load_dotenv()
TOKEN = os.getenv("TOKEN")


if __name__ == "__main__":
    async def post_init(app):
        await pool.initialize_pool()
        await initializer.init_db()

    # you can change your API address here to use bot in 'bale' or... instead of telegram.
    app = Application.builder().token(TOKEN).base_url("https://tapi.bale.ai/bot").post_init(post_init).build()

    app.add_handler(CommandHandler("start", handlers.start))    
    app.add_handler(CallbackQueryHandler(handlers._help))
    app.add_handler(MessageHandler(filters.TEXT, handlers.handle_text))

    print("start polling...")
    app.run_polling()
