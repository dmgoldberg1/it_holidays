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
    reply_txt = '''Здравствуй, пользователь! Отправь мне команду
     /cu_the_best
     И мы начнем!
     '''
    await update.message.reply_text(reply_txt)
    print('in start')

async def begin_command(update, context): # команда входа в диалог с определением кем является пользователь
    callback_button1 = InlineKeyboardButton(text="Работадатель", callback_data="leader")
    callback_button2 = InlineKeyboardButton(text="Работяга", callback_data="worker")
    keyboard = InlineKeyboardMarkup([[callback_button1], [callback_button2]])
    message = 'Кем ты являешься?'
    await context.bot.send_message(update.message.chat.id, message, reply_markup=keyboard)
    return 1

async def start_quiz(call, context): # обработка ответа на вопрос, кем является пользователь
    ans = call.callback_query.data
    print(ans)
    if ans == 'leader':
        print('amogus')
        message = 'Ты работадатель!'
        await context.bot.send_message(call.callback_query.message.chat.id, message)
    elif ans == 'worker':
        message = 'Ты работяга!'
        await context.bot.send_message(call.callback_query.message.chat.id, message)
    return 0


async def stop_dialog(update, context):
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler_start = ConversationHandler(
        entry_points=[CommandHandler('cu_the_best', begin_command)],
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [CallbackQueryHandler(start_quiz)],

        },
        fallbacks=[CommandHandler('stop', stop_dialog)]

    )
    application.add_handler(CommandHandler("start", start_command))
    #application.add_handler(CommandHandler("cu_the_best", begin_command))
    application.add_handler(conv_handler_start)
    application.run_polling()


if __name__ == '__main__':
    main()
