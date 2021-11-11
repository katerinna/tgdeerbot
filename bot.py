# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 18:03:39 2021

@author: Пользователь
"""
import os
# Force CPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0 = all messages are logged, 3 - INFO, WARNING, and ERROR messages are not printed


import h5py
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, TimeDistributed
from tensorflow.keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import keras
from collections import Counter
import pickle
import numpy as np
import random
import sys
import time
import io
import re
import argparse
import pandas as pd
import random

from vectorizernn import *
from autosubstit import *


import csv

def writeresult(userid, name, answer):
    data = {"userid": userid, "username": name, "answer": answer}
    with open('userisd.csv', 'a', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow([data['userid'], data['username'], data['answer']])


TOKEN = 'mytoken'

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
    
button_gen1 = KeyboardButton('Нейронка')
button_gen2 = KeyboardButton('Автоподстановка')
button_gen3 = KeyboardButton('Статистика пользователя')
greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).row(button_gen1,button_gen2).row(button_gen3)

@dp.message_handler(commands=['start'])
async def process_hi1_command(message: types.Message):
    markdown = """
    *bold text*
    _italic text_
    [text](URL)
    """
    await bot.send_message(message.chat.id, 'Привет! \n \nЯ генерирую сообщения на основе последних 5 тысяч новостей @deerzone')
    time.sleep(2)
    text = 'Сейчас появится клавиатура внизу:\n\n• *Нейронка* генерирует текст с помощью алгоритмов машинного обучения\n\n• *Автоподстановка* использует наиболее частые выражения, чтобы дополнить текст'
    await bot.send_message(message.chat.id, text, parse_mode="Markdown")
    time.sleep(4)
    await bot.send_message(message.chat.id, '_Диклеймер!_ Оба алгоритма пишут чушь. Увы.', parse_mode="Markdown")
    time.sleep(2)
    await bot.send_message(message.chat.id, 'Помимо этого, они ещё и очень долго работают. Так что немного терпения.', parse_mode="Markdown")
    time.sleep(2)
    await message.reply("Выбери способ", reply_markup=greet_kb1)


@dp.message_handler()
async def echo_message(msg: types.Message):
    userdata = 'Пользователь: @'+msg.from_user.username
    if (msg.text == "Нейронка"):
        writeresult(msg.from_user.id, msg.from_user.username, "nn")
        await  bot.send_message(msg.from_user.id, '. . .')
        seed = starlist[random.randint(0,len(starlist)-1)]
        res = generate(predict_model, vectorizer, seed=seed, length=random.randrange(40,80))
        x=seed
        for i in range(1,res.count('.')+1):
            x = x+' ' + res.split('.')[i-1]+'.'
        await  bot.send_message(msg.from_user.id, x)
    elif (msg.text == "Автоподстановка"):
        await bot.send_message(msg.from_user.id, "Задайте слово и длину сообщения, например aespa 13")
    elif (msg.text == "Статистика пользователя"):
        userres = pd.read_csv('userisd.csv', sep=',')
        nnstat = len(userres[(userres['userid']==msg.from_user.id) &(userres['answer']=='nn')]) 
        autostat = len(userres[(userres['userid']==msg.from_user.id) &(userres['answer']=='auto')]) 
        textstat = 'Нейросетевых сообщений: ' + str(nnstat) + '\nАвтоподстановочных сообщений: ' + str(autostat)
        await  bot.send_message(msg.from_user.id, userdata)
        await  bot.send_message(msg.from_user.id, textstat)
    else: 
        await bot.send_message(msg.from_user.id, wnext(msg.text))
        writeresult(msg.from_user.id, msg.from_user.username, "auto")

    

if __name__ == '__main__':
    executor.start_polling(dp)