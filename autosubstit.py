# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 00:27:48 2021

@author: Пользователь
"""
import pandas as pd
import numpy as np
import random

data_file = "txtfile.txt"  # Source text file
with open(data_file, 'r',  encoding='utf-8') as file:
    data = file.read().replace('\n', ' ')
data=data[0:100000]

for i in range(1,11):
    data = data.replace(str(i), '')
data = data.replace('.', '')
data = data.replace('!', '')
data = data.replace('"', '')
data = data.replace(':', '')
data = data.replace("'", '')

def new_word(x):
    x=x+ ' '
    upper_x = x[0].upper()+x[1::]
    x = x[0].lower()+x[1::]
    # очистка словаря
    counter=pd.DataFrame({'label':'',
                      'Count': range(0)})

    all_words=''
    listing=[]

    # составление текста из "следующих слов"
    # составление списка вариантов
    for i in range(0,data.count(x)):
        x_frag = data.split(x)[i]
        all_words = all_words + ' ' + x_frag.split(" ")[0]
        listing.append(x_frag.split(" ")[0])
    
    res = []
    for i in listing:
        if i not in res:
            res.append(i)
    listing=res

    # заполнение таблицы слово - количество упоминаний
    for i in range(0,len(listing)-1):
        newrow = {'label':listing[i],
              'Count': all_words.count(listing[i])}
        counter = counter.append(newrow, ignore_index=True)
    
    # удаление пустого символа (хз откуда взялся)
    counter=counter.drop(counter[counter['label']==''].index)
    
    # случайное слово из самых упоминаемых
    if len(counter['Count'])==0:
        new = 'и'
    else:
        new = counter[counter['Count'] > 0.05*max(counter['Count'])].sample(n=1)['label'].values[0]
    return new


def wnext(word_num):
    if word_num.count(' ') == 0: 
        endtext = "Не понимаю инструкций."
    else:
        word = word_num.split(" ")[0]
        num = word_num.split(" ")[1]
        if isinstance(word, str)==False or num.isdigit()==False:
            endtext = "Не понимаю инструкций."
        else: 
            startw = word
            endtext=startw

            for j in range(1,int(num)):
                next_w = new_word(startw)
                endtext=endtext +' ' + next_w
                startw = next_w
    return endtext