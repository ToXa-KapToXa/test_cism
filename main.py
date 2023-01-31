import os
import threading
import yaml
import traceback

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from data import db_session
from data.regular_table import RegularTable
from data.users import Users
from result_xlsx import Result
from text_msg import *
from marker import Marker
from os import listdir


with open('cfg.yml') as fh:
    read_data = yaml.load(fh, Loader=yaml.FullLoader)

updater = Updater(read_data["tg_key"], use_context=True)
bot = Bot(read_data["tg_key"])
dp = updater.dispatcher
db_session.global_init()
user_class = {}


def send_file(user_id, name_file):
    """
    Метод для отправки файла пользователю
    ...
    Attributes
    ----------
    user_id: int
        Телеграм-Id пользователя
    name_file: str
        Имя файла
    """

    with open(name_file, 'rb') as f:
        bot.send_document(chat_id=user_id, document=f)
    os.remove(name_file)


def create_result(res_and_lists, user_id):
    """
    Метод для создания файла-результата
    ...
    Attributes
    ----------
    res_and_lists: tuple
        res - словарь(ключ - версия регулярного выражения, значение - список найденных фраз после прогона)
        list_of_strings - список фраз, считанных из файла(ов)
        list_regulars - словарь(ключ - версия регулярного выражения, значение - регулярное выражение)
        mark - строка(маркер регулярного выражения)
    user_id: int
        Телеграм-Id пользователя
    """

    result = Result(res_and_lists)
    name_file = result.create_result_xlsx()
    send_file(user_id, name_file)


def choice_marker(namefile, user_id, message_id):
    """
    Метод для выбора маркера
    ...
    Attributes
    ----------
    namefile: str
        Имя файла
    user_id: int
        Телеграм-Id пользователя
    message_id: int
        Id сообщения
    """

    marker = Marker(namefile)
    marker.take_regulars_expressions()
    bot.edit_message_text(chat_id=user_id, text=waiting, message_id=message_id)
    create_result(marker.get_data(), user_id)
    bot.edit_message_text(chat_id=user_id, text=ending, message_id=message_id)


def start(update, context):
    """
    Метод для запуска бота.
    Происходит авторизация пользователя.
    В случае успешной авторизации пользователю возвращается клавиатура для выбора маркера
    """

    session = db_session.create_session()
    try:
        users = session.query(Users).all()
        tg_ids = []
        for i in users:
            tg_ids.append(i.tg_id)
        if update.message.from_user.id not in tg_ids:
            update.message.reply_text(fail_authorize)
        else:
            regulars = {'Реклама тг-каналов': 'tg', 'Реклама курсов': 'course',
                        'Реклама товаров на маркетплейсах': 'markets'}
            keyboard_start = []
            for reg in session.query(RegularTable.marker).distinct():
                keyboard_start.append([InlineKeyboardButton(reg[0], callback_data=regulars[reg[0]])])
            keyboard_start = InlineKeyboardMarkup(keyboard_start)
            update.message.reply_text(success_authorize, reply_markup=keyboard_start)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        session.close()


def button(update, context):
    """
    Метод для взаимодействия с кнопками.
    Если выбран маркер, то в сообщении выводятся датасеты для этого маркера.
    Если выбран датасет, создается поток для прогона регулярных выражений.
    """

    session = db_session.create_session()
    try:
        query = update.callback_query
        variant = query.data
        variants = ['tg', 'course', 'markets']
        if variant in variants:
            datasets = listdir(f'datasets/{variant}')
            keyboard_datasets = []
            for key in datasets:
                keyboard_datasets.append([InlineKeyboardButton(key, callback_data=key)])
            keyboard_datasets = InlineKeyboardMarkup(keyboard_datasets)
            bot.edit_message_text(chat_id=query.from_user.id, text=choose_dataset, reply_markup=keyboard_datasets,
                                  message_id=query.message.message_id)
        elif 'dataset' in variant:
            threading.Thread(target=choice_marker, args=(variant, query.from_user.id, query.message.message_id)).start()
    except Exception as e:
        print(traceback.format_exc())
    finally:
        session.close()


dp.add_handler(CommandHandler("start", start))
dp.add_handler(CallbackQueryHandler(button))

if __name__ == "__main__":
    updater.start_polling()
