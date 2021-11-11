# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:07:12 2021

@author: Пользователь
"""

import vk_api

# авторизация 
vk_session = vk_api.VkApi('mylogin', 'mypassword')
vk_session.auth()
vk = vk_session.get_api()
text = ''
newrow = ''

# парсинг

for j in range(100, 9100, 100):
    resp = vk.wall.get(owner_id=-33654179,offset=j-100,count=j)
    # запись в файл
    for i in range(0,len(resp['items'])-1):
        if resp['items'][i]['text'].count('KFC') >0 or \
            resp['items'][i]['text'].count('#deerzone_performance') >0 or \
                resp['items'][i]['text'].count('#deerzone_chart') >0 or \
                    resp['items'][i]['text'].count('#deerzone_history') >0 or \
                        resp['items'][i]['text'].count('#deerzone_facts') >0 or \
                            resp['items'][i]['text'].count('#deerzone_concept') >0 or \
                            resp['items'][i]['text'].count('#deerzone_teaser') >0 or \
                            resp['items'][i]['text'].count('MAMA2021') >0:
            newrow = ''
        else: newrow = '\n' + resp['items'][i]['text']
        text = text + newrow
    print(j)



text1=''
for i in range(0,text.count('\n')):
    if text.split('\n')[i].count('#')>0 or text.split('\n')[i].count('.(') >0 or \
        text.split('\n')[i].count('📺') >0 or text.split('\n')[i].count('🎤') >0 or \
            text.split('\n')[i].count('vk.com') >0:
        newrow=''
    else: newrow ='\n'+text.split('\n')[i]
    if i%50 == 0: print(i)
    text1=text1+newrow
    
text1=text1.replace('●','')
text1=text1.replace('★','')
text1=text1.replace('•','')
text1=text1.replace('\n\n','\n')
text1=text1.replace('\n \n','\n')
text1=text1.replace('📆ПОДТВЕРЖДЕННЫЕ РЕЛИЗЫ📆','')
text1=text1.replace('🥇ЧАРТЫ🥇','')
text1=text1.replace('📻НОВОСТИ 📻','')
text1=text1.replace('💸ПРОДАЖИ💸','')
text1=text1.replace('Голосуйте - vk.cc/5c5PDd','')

f = open('txtfile1.txt','w')  # открытие в режиме записи
f.write(text1[16000:16500])  # запись Hello World в файл
f.close()

len(text1)




