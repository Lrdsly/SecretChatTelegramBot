from telegram.ext import Application, CommandHandler, filters

import db.pool as pool
import db.initialize as initializer
from handlers import start

from dotenv import load_dotenv
import asyncio
import os
import asyncio

# ---- ENJOY CODING TODAY ----

load_dotenv()
TOKEN = os.getenv("TOKEN")


if __name__ == "__main__":
    async def post_init(app):
        await pool.initialize_pool()
        await initializer.init_db()

    # you can change your API address here to use bot in 'bale' or... instead of telegram.
    app = Application.builder().token(TOKEN).base_url("https://tapi.bale.ai/bot").post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))    

    print("start polling...")
    app.run_polling()


