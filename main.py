from telegram.ext import Application, CommandHandler, filters
from handlers import start

from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

def main():
    # you can change your API address here to use bot in 'bale' or... instead of telegram.
    app = Application.builder().token(TOKEN).base_url("https://tapi.bale.ai/bot").build()

    app.add_handler(CommandHandler("start", start))    

    print("start polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
