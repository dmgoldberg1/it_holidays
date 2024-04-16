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
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
BOT_TOKEN = '6937834872:AAFajRx8Fpk1U0QHGaH3QmroPsXdUb0qvig'
connection = sqlite3.connect('vacancy.db')
cursor = connection.cursor()
ACCESS = False

async def start_command(update, context):
    reply_txt = '''Здравствуй, пользователь! Отправь мне команду
     /cu_the_best
     И мы начнем!
     '''
    await update.message.reply_text(reply_txt)
    print('in start')


async def begin_command(update, context):  # команда входа в диалог с определением кем является пользователь
    callback_button1 = InlineKeyboardButton(text="Работадатель", callback_data="leader")
    callback_button2 = InlineKeyboardButton(text="Работяга", callback_data="worker")
    keyboard = InlineKeyboardMarkup([[callback_button1], [callback_button2]])
    message = 'Кем ты являешься?'
    await context.bot.send_message(update.message.chat.id, message, reply_markup=keyboard)
    return 1


async def start_quiz(call, context):  # обработка ответа на вопрос, кем является пользовательclos
    ans = call.callback_query.data
    print(ans)
    id = call.callback_query.from_user.id
    try:
        ids = cursor.execute("SELECT user_id FROM vacancy").fetchall()[0]
    except Exception as e:
        ids = []
    if ans == 'leader':
        print('amogus')
        lead_message = '''Давай зарегестрируем твою компанию!
            Введи сначала название компании'''
        if id not in ids:
            cursor.execute('INSERT INTO vacancy (user_id, state) VALUES (?, ?)', (id, 1))
            connection.commit()
            await context.bot.send_message(call.callback_query.message.chat.id, lead_message)

    elif ans == 'worker':
        if id not in ids:
            ACCESS = True
            work_message = 'Напиши свое ФИО'
            cursor.execute('INSERT INTO workers (user_id) VALUES (?)', (id,))
            connection.commit()
            await context.bot.send_message(call.callback_query.message.chat.id, work_message)


async def boss_get_company(call, context):
    print('-------------------------------------')
    company_name = call.message.text
    companies = cursor.execute("SELECT company_name FROM vacancy").fetchall()[0]
    id = call.message.chat.id
    local_company = cursor.execute('SELECT company_name FROM vacancy WHERE user_id=?', (id)).fetchall()[0]
    if company_name not in companies:
        cursor.execute('UPDATE vacancy SET company_name = ? WHERE user_id = ?', (company_name, id))
        connection.commit()
        print(company_name)
        message = '''Напиши своё ФИО'''
        await context.bot.send_message(call.message.chat.id, message)
        print('ВОЗВРАЩАЮ 3')
        return 3


async def boss_get_name(call, context):
    print('ОБРАБОТЧИК ИМЕНИ ВЫЗВАН')
    name = call.message.text
    names = cursor.execute("SELECT name FROM vacancy").fetchall()[0]
    id = call.message.chat.id
    if name not in names:
        cursor.execute('UPDATE vacancy SET name = ? WHERE user_id = ?', (name, id))
        connection.commit()
        message = 'Напиши город, в котором располагается компания'
        print(name)
        await context.bot.send_message(call.message.chat.id, message)
        return 4


async def boss_get_city(call, context):
    print('ОБРАБОТЧИК ГОРОДА ВЫЗВАН')
    boss_city = call.message.text
    cities = cursor.execute("SELECT city FROM vacancy").fetchall()[0]
    id = call.message.chat.id
    if boss_city not in cities:
        cursor.execute('UPDATE vacancy SET city = ? WHERE user_id = ?', (boss_city, id))
        connection.commit()
        message = 'Напиши свой ИНН'
        print(boss_city)
        await context.bot.send_message(call.message.chat.id, message)
        return 5


async def boss_get_inn(call, context):
    print('ОБРАБОТЧИК ИНН ВЫЗВАН')
    boss_inn = call.message.text
    inns = cursor.execute("SELECT inn FROM vacancy").fetchall()[0]
    id = call.message.chat.id
    if boss_inn not in inns:
        cursor.execute('UPDATE vacancy SET inn = ? WHERE user_id = ?', (boss_inn, id))
        connection.commit()
        final_message = '''Спасибо, регистрация компании завершена! Теперь вы можете приступить к заполнению вакансий.
        Для создания новой вакансии напишите команду /create_vacancy'''
        print(boss_inn)
        await context.bot.send_message(call.message.chat.id, final_message)
        return ConversationHandler.END


async def create_vacancy(update, context):
    print('ОБРАБОТЧИК СОЗДАНИЯ ВАКАНСИЙ ВЫЗВАН')
    message_place = 'На какую должность нужен работник?'
    await context.bot.send_message(update.message.chat.id, message_place)
    return 6


async def vacancy_get_place(call, context):
    print('ОБРАБОТЧИК ДОЛЖНОСТИ ВЫЗВАН')
    vacancy_place = call.message.text
    message_skills = 'Какие навыки необходимы будущему работнику? Напишите их через запятую)'
    print(vacancy_place)
    await context.bot.send_message(call.message.chat.id, message_skills)
    return 7


async def vacancy_get_skills(call, context):
    print('ОБРАБОТЧИК НАВЫКОВ ВЫЗВАН')
    vacancy_skills = call.message.text.split(', ')
    message_exp = 'Какой опыт работы должен быть у сотрудника?'
    print(vacancy_skills)
    await context.bot.send_message(call.message.chat.id, message_exp)
    return 8


async def vacancy_get_exp(call, context):
    print('ОБРАБОТЧИК ОПЫТА ВЫЗВАН')
    vacancy_exp = call.message.text
    message_salary = 'На какую зарплату может рассчитывать сотрудник?'
    print(vacancy_exp)
    await context.bot.send_message(call.message.chat.id, message_salary)
    return 9


async def vacancy_get_salary(call, context):
    print('ОБРАБОТЧИК ЗАРПЛАТЫ ВЫЗВАН')
    vacancy_salary = call.message.text
    message_final = 'Спасибо, процедура создания вакансии заверршена. Она внесена в общую базу вакансий твоей компании'
    print(vacancy_salary)
    await context.bot.send_message(call.message.chat.id, message_final)
    return ConversationHandler.END


async def worker_get_name(call, context):
    print('ВЫЗВАН ОБРАБОТЧИК ИМЕНИ РАБОТЯГИ')
    worker_name = call.message.text
    id = call.message.chat.id
    try:
        names = cursor.execute("SELECT name FROM workers").fetchall()[0]
    except Exception as e:
        names = []
    if worker_name not in names and ACCESS is True:
        cursor.execute('UPDATE workers SET name = ? WHERE user_id = ?', (worker_name, id))
        connection.commit()
        message_phone = 'Укажи номер телефона для связи'
        print(worker_name)
        await context.bot.send_message(call.message.chat.id, message_phone)
        return 10


async def worker_get_phone(call, context):
    print('ОБРАБОТЧИК ТЕЛЕФОНА ВЫЗВАН')
    worker_phone = call.message.text
    id = call.message.chat.id
    try:
        phones = cursor.execute("SELECT phone FROM workers").fetchall()[0]
    except Exception as e:
        phones = []
    if worker_phone not in phones:
        cursor.execute('UPDATE workers SET name = ? WHERE user_id = ?', (worker_phone, id))
        connection.commit()
        message_final = 'Добро пожалавать в нашу систему!'
        await context.bot.send_message(call.message.chat.id, message_final)
        return ConversationHandler.END


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
    conv_worker_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, worker_get_name)],
        states={
            10: [MessageHandler(filters.TEXT, worker_get_phone)]
        },
        fallbacks=[CommandHandler('stop', stop_dialog)]
    )
    conv_leader_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, boss_get_company)],
        states={
            3: [MessageHandler(filters.TEXT, boss_get_name)],
            4: [MessageHandler(filters.TEXT, boss_get_city)],
            5: [MessageHandler(filters.TEXT, boss_get_inn)]
        },
        fallbacks=[CommandHandler('stop', stop_dialog)]
    )
    create_vacancy_handler = ConversationHandler(
        entry_points=[CommandHandler('create_vacancy', create_vacancy)],
        states={
            6: [MessageHandler(filters.TEXT, vacancy_get_place)],
            7: [MessageHandler(filters.TEXT, vacancy_get_skills)],
            8: [MessageHandler(filters.TEXT, vacancy_get_exp)],
            9: [MessageHandler(filters.TEXT, vacancy_get_salary)],

        },
        fallbacks=[CommandHandler('stop', stop_dialog)]
    )
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(conv_handler_start)
    application.add_handler(conv_leader_handler)
    application.add_handler(create_vacancy_handler, group=1)
    application.add_handler(conv_worker_handler, group=2)
    application.run_polling()


if __name__ == '__main__':
    main()
