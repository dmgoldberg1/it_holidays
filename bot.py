import datetime
import logging
import os
import sqlite3
import time
from io import StringIO

# import aiohttp
# import requests

from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler

# Запускаем логгирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
BOT_TOKEN = '6937834872:AAFajRx8Fpk1U0QHGaH3QmroPsXdUb0qvig'


async def start_command(update, context):
    reply_txt = 'привет, братик'
    await update.message.reply_text(reply_txt)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.run_polling()


if __name__ == '__main__':
    main()
