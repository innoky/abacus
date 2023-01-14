#---------------------------------------------------------------------------
import time
import random
import os
import subprocess
import sys
import os.path
from PIL import Image
import numpy as np

from sympy.solvers import solve
from sympy import Symbol

import telebot

from telebot import types



#---------------------------------------------------------------------------


bot = telebot.TeleBot('5900150945:AAEILo4cgaVVO2rsdE9qUlB5ypM0t47-nrQ')

@bot.message_handler(commands=['start'])



#---------------------------------------------------------------------------



def welcome(message):


    # keyboard (Создание кнопок и приветствие)

    bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, телеграмм бот HS Abacus!  Отправьте мне функцию вида y=x (Например y=x^2-six(x))'.format(message.from_user, bot.get_me()),
        parse_mode='html')

@bot.message_handler(content_types=['text'])



#---------------------------------------------------------------------------



def lalala(message):
    if message.chat.type == 'private':
        if "y" or "x" or "y(x)" in message.text:
            global get_message
            get_message = message.text.lower().replace(" ","")
 			# keyboard (Создание кнопок под текстом)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Посчитать интеграл", callback_data='1')
            item2 = types.InlineKeyboardButton("Нарисовать график", callback_data='2')
            item3 = types.InlineKeyboardButton("Найти корни", callback_data='3')
            item4 = types.InlineKeyboardButton("Найти производную", callback_data='4')

            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, f"<code>{get_message}</code>", parse_mode='html', reply_markup=markup)

        elif message.text == "Помощь" or "/help":
            bot.send_message(message.chat.id, "Я не знаю такой команды")
        elif message.text == "/error" or "Сообщить об ошибке":
            bot.send_message(message.chat.id, "Нашли ошибку, напишите нам @herzogw")
        else:
            bot.send_message(message.chat.id, "Пока что я не умею воспринимать произвольный текст")
#---------------------------------------------------------------------------
#отрисовка графика
#нижний предел интеграла
def lower_lim(message, plus_low):
    plus_high = plus_low + " " + message.text

    msg = bot.send_message(message.chat.id, "Введите верхний предел интегрирования")
    bot.register_next_step_handler(msg, upp_lim, plus_high)

#верхний предел интеграла
def upp_lim(message, plus_high):
    final_int = plus_high + " " + message.text

    clear_func = final_int.replace("^", "**")
    with open("int_get.txt", "w") as file:
        file.write(clear_func)

    os.system('python3 integral.py')
    time.sleep(2)
    with open("int_out.txt", "r") as file:
        for line in file:
            text1 = str(line)
    bot.send_message(message.chat.id, "Ваш интеграл равен ~ ")
    bot.send_message(message.chat.id, round(float(text1), 2), parse_mode = "html")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
        	# keyboard (Работа с кнопками под текстом)
            if call.data == '1':
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите нижний предел интегрирования",
                    reply_markup=None)
                plus_low = "y" + get_message.replace("^", "**").replace("y(x)", "").replace("y", "")
                bot.register_next_step_handler(msg, lower_lim, plus_low)

            elif call.data == '2':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Подождите... Считаем точки",
                    reply_markup=None)
                time.sleep(1)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Рисуем график...",
                    reply_markup=None)
                time.sleep(1)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Отправляем график...",
                    reply_markup=None)
                get_sub = get_message
                clear_graph1 = "y" + get_message.replace("^", "**").replace("y(x)", "").replace("y", "")
                with open("graphdraw.py", "w") as file:
                    file.write(
'''
from numpy import sqrt, sin, cos, pi
import matplotlib.pyplot as plt
import os.path
import numpy as np
x = np.linspace(-5,5,100)
'''
+ f"{clear_graph1}\n" + f"checker='{clear_graph1}'" +
'''
try:
    if "x" in checker:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        # plot the function
        plt.plot(x,y, 'r')
        plt.savefig('graphs/graphdraw.png')
    else:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        # plot the function
        plt.plot([y, y, y, y])
        plt.savefig('graphs/graphdraw.png')
except SyntaxError:
    os.remove("graphs/graphdraw.png")
''')
                os.system("python3 graphdraw.py")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<code>График вашей функции:</code>", parse_mode = "html",
                    reply_markup=None)
                bot.send_photo(call.message.chat.id, open('graphs/graphdraw.png', 'rb'));

            elif call.data == '3':
                clear_equat = ("y" + get_message.replace("^", "**").replace("y(x)", "").replace("y", "")).replace("y=", "")
                x = Symbol('x')
                send_data_arr = solve(clear_equat, x)
                send_data = '\n'.join("x = " + str(value) for value in send_data_arr).replace("sqrt", "√")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Корни, где же они...",
                    reply_markup=None)
                time.sleep(1)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ищем...",
                    reply_markup=None)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вот что мы нашли",
                    reply_markup=None)
                if send_data == "":
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Корни отсутвуют",
                        reply_markup=None)
                elif "I" in send_data:
                    markup_com = types.InlineKeyboardMarkup(row_width=1)
                    item5 = types.InlineKeyboardButton("Показать", callback_data='5')
                    markup_com.add(item5)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Действительные корни отсутвуют, показать комплексные?",
                        reply_markup=markup_com)
                else:
                    bot.send_message(call.message.chat.id, send_data)

            elif call.data == '4':
                bot.send_message(call.message.chat.id, 'Пока что эта функция в разработке!')

            elif call.data == '5':
                clear_equat = ("y" + get_message.replace("^", "**").replace("y(x)", "").replace("y", "")).replace("y=", "")
                x = Symbol('x')
                send_data_arr = solve(clear_equat, x)
                send_data = '\n'.join("x = " + str(value) for value in send_data_arr).replace("sqrt", "√")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вот что мы нашли",
                    reply_markup=None)
                bot.send_message(call.message.chat.id, send_data)
    except Exception as e:
        print(repr(e))

@bot.message_handler(content_types=['photo'])
def photo(message):
    print ('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print ('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print ('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    im1 = Image.open('image.jpg')
    im1.save('image.png')
    os.system('python3 main.py --img_file image.png')
    with open("recog.txt", "r") as file:
        for line in file:
            text1 = str(line)
    bot.send_message(message.chat.id, text1.replace(",", ""))
#---------------------------------------------------------------------------


# Старт
bot.polling(none_stop=True)



#---------------------------------------------------------------------------
