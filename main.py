#---------------------------------------------------------------------------
import time
import random
import os
import subprocess
import sys
import re
import sqlite3
import os.path
from pylatexenc.latex2text import LatexNodes2Text
from pylatexenc.latexencode import unicode_to_latex
from PIL import Image
import numpy as np

from sympy.solvers import solve
from sympy import Symbol, diff, cos, sin, tan, sqrt, sympify

import telebot

from telebot import types


db = sqlite3.connect('server.db', check_same_thread=False)
sql = db.cursor()


#---------------------------------------------------------------------------

bot = telebot.TeleBot('6034911129:AAGCeWmDB1Wgh6B4FDKoi3H_QeaHa07v9nk')



#---------------------------------------------------------------------------

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в телеграмм бот проекта Abacus, подробно о моем функционале можно прочитать тут \n\n [Documentation](https://telegra.ph/Documentation-01-31)', parse_mode="MarkdownV2")
    user_id = message.from_user.id
    user_name = message.from_user.username
    sql.execute(f"""CREATE TABLE IF NOT EXISTS users (
        id TEXT,
        username TEXT
    )""")
    db.commit()

    sql.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?, ?)", (user_id, user_name))
        db.commit()
        print("registerd")
        os.mkdir("users/"+ str(user_id))
    else:
        print("id EXISTS")
        for value in sql.execute("SELECT * FROM users"):
            print(value)


@bot.message_handler(content_types=['text'])



#---------------------------------------------------------------------------



def lalala(message):
    if message.chat.type == 'private':
#______________________________________________________________________________________________________
        calc_data = message.text.replace("+","").replace("-","").replace("*","").replace("/","").replace(" ","").replace("0(","0*(").replace("1(","1*(").replace("2(","2*(").replace("3(","3*(").replace("4(","4*(").replace("5(","5*(").replace("6(","6*(").replace("7(","7*(").replace("8(","8*(").replace("9(","9*(").replace(")(",")*(").replace("^","")
        if calc_data.isdigit():
            bot.send_message(message.chat.id, eval(message.text.replace("^", "**")))

        elif message.text == "Alice":
            messagetoedit = bot.send_message(message.chat.id, '''
　 　∧,,,∧
　 （ ・ω・） I love Alice!
　　( つ旦O
　　と＿)_)
        ''')
            time.sleep(1)
            for _ in range(3):
                bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text='''
　 　∧,,,∧
　 （ ・◎・） slrrrp
　　(　ﾞノ ヾ
　　と＿)_)
            ''')
                time.sleep(1)
                bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text='''
　　 ∧,,,∧
　 （ ・ω・） Hmm, she is beautiful...
　　( つ旦O
　　と＿)_)
            ''')
                time.sleep(2)
                bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text='''
　　∧,,,∧
　 （ ・ω・）
　　( つ　O. __
　　と＿)_) （__(）､;.o：。
　　　　　　　　　　ﾟ*･:.｡
            ''')
                time.sleep(1)
                bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text='''
　 　　　 _ _　 ξ
　　　 (´ 　 ｀ヽ、　　 　 __
　　⊂,_と（　 　 ）⊃　 （__(） I miss her...
　　　　　　Ｖ　Ｖ　　　　　　 　 　 ﾟ*･:.｡
            ''')
                time.sleep(2)
                bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text='''
　 　∧,,,∧
　 （ ・ω・） I love Alice!
　　( つ旦O
　　と＿)_)
            ''')
                time.sleep(0.5)
            bot.delete_message(message.chat.id, message.message_id)
#____________________________________________________________________________________________________________________________________

        elif message.text == "DT":
            messaget = bot.send_message(message.chat.id, '''

░█▀▀▄
░█─░█
░█▄▄▀
        ''')
            time.sleep(0.5)
            for _ in range(3):
                bot.edit_message_text(chat_id=message.chat.id, message_id=messaget.message_id, text='''

░█▀▀▄ ▀█▀
░█─░█ ░█─
░█▄▄▀ ▄█▄
            ''')
                time.sleep(0.5)
                bot.edit_message_text(chat_id=message.chat.id, message_id=messaget.message_id, text='''

░█▀▀▄ ▀█▀ ░█▀▄▀█
░█─░█ ░█─ ░█░█░█
░█▄▄▀ ▄█▄ ░█──░█
            ''')
                time.sleep(0.5)
                bot.edit_message_text(chat_id=message.chat.id, message_id=messaget.message_id, text='''

░█▀▀▄ ▀█▀ ░█▀▄▀█ ─█▀▀█
░█─░█ ░█─ ░█░█░█ ░█▄▄█
░█▄▄▀ ▄█▄ ░█──░█ ░█─░█
            ''')
                time.sleep(0.5)
                bot.edit_message_text(chat_id=message.chat.id, message_id=messaget.message_id, text='''
░█▀▀█ ░█▀▀█ ░█▀▀▀█
░█▀▀▄ ░█▄▄▀ ░█──░█
░█▄▄█ ░█─░█ ░█▄▄▄█
            ''')
                time.sleep(0.5)
                bot.edit_message_text(chat_id=message.chat.id, message_id=messaget.message_id, text='''

░█▀▀▄
░█─░█
░█▄▄▀
                ''')
                time.sleep(0.5)
            bot.delete_message(message.chat.id, message.message_id)
#___________________________________________________________________________________________________________________________________
        elif "y" or "x" or "y(x)" in message.text:
            global user_ind
            user_ind = message.from_user.id
            global get_message

            if ("sin" or "cos" or "tan") in message.text:
                bot.send_message(message.chat.id, "<em>Функция переодическая, корни могут иметь период повторения</em>", parse_mode ='html')
            if "\\" in message.text:
                get_message = LatexNodes2Text().latex_to_text(message.text.replace("\\"+"dfrac", "\\"+"frac")).lower().replace(" ","")
            else:
                get_message = message.text.lower().replace(" ","")
            get_message = get_message.replace("0x", "0*x").replace("1x", "1*x").replace("2x", "2*x").replace("3x", "3*x").replace("4x", "4*x").replace("5x", "5*x").replace("6x", "6*x").replace("7x", "7*x").replace("8x", "8*x").replace("9x", "9*x")
            get_message = get_message.replace("0(","0*(").replace("1(","1*(").replace("2(","2*(").replace("3(","3*(").replace("4(","4*(").replace("5(","5*(").replace("6(","6*(").replace("7(","7*(").replace("8(","8*(").replace("9(","9*(")
            get_message = get_message.replace(")(",")*(").replace("x(","x*(")

 			# keyboard (Создание кнопок под текстом)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Посчитать интеграл", callback_data='1')
            item2 = types.InlineKeyboardButton("Нарисовать график", callback_data='2')
            item3 = types.InlineKeyboardButton("Найти корни", callback_data='3')
            item4 = types.InlineKeyboardButton("Производная (Beta)", callback_data='4')

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
                user_id = str(user_ind)
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
        fig.set_facecolor("#0E1621")
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.set_facecolor("#0E1621")
        ax.xaxis.set_ticks_position('bottom')
        ax.tick_params(color='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.yaxis.set_ticks_position('left')
        # plot the function
        plt.plot(x,y, 'r')
        plt.savefig("users/''' + user_id +'''/graphdraw.png")
    else:
        fig = plt.figure()
        fig.set_facecolor("#0E1621")
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['bottom'].set_position('zero')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.set_facecolor("#0E1621")
        ax.xaxis.set_ticks_position('bottom')

        ax.yaxis.set_ticks_position('left')
        # plot the function
        plt.plot([y, y, y, y])
        plt.savefig("users/''' + user_id +'''/graphdraw.png")
except SyntaxError:
    print("ok")
''')
                os.system("python3 graphdraw.py")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<code>График вашей функции:</code>", parse_mode = "html",
                    reply_markup=None)
                bot.send_photo(call.message.chat.id, open('users/'+user_id+'/graphdraw.png', 'rb'));

            elif call.data == '3':
                clear_equat = (get_message.replace("^", "**").replace("y(x)=", "").replace("y=", "")).replace("y=", "")
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
                    bot.send_message(call.message.chat.id, f"<code>{send_data}</code>", parse_mode="html")

            elif call.data == '4':
                upload_eq = "result = (diff(" + get_message.replace("y=", "").replace("^","**").replace("y(x)", "").replace("=", "") + "))"
                with open("diff.py", "w") as file:
                    file.write('''
from sympy.solvers import solve
from sympy import Symbol, diff, symbols, cos, sin, tan, sqrt
x, y = symbols("x y") \n
''' + upload_eq +'''
with open("diff_result.txt", "w") as file:
    file.write(str(result))''')
                os.system("python3 diff.py")

                with open("diff_result.txt", "r") as file:
                    for line in file:
                        text1 = str(line)
                text1 = text1.replace("0x", "0*x").replace("1x", "1*x").replace("2x", "2*x").replace("3x", "3*x").replace("4x", "4*x").replace("5x", "5*x").replace("6x", "6*x").replace("7x", "7*x").replace("8x", "8*x").replace("9x", "9*x")
                text1 = text1.replace("0(","0*(").replace("1(","1*(").replace("2(","2*(").replace("3(","3*(").replace("4(","4*(").replace("5(","5*(").replace("6(","6*(").replace("7(","7*(").replace("8(","8*(").replace("9(","9*(")
                text1 = text1.replace(")(",")*(").replace("x(","x*(").replace(" ", "")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Подождите... Ищем производную",
                    reply_markup=None)
                time.sleep(1)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Находим максимумы...",
                    reply_markup=None)
                time.sleep(1)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Взамываем Photomath...",
                    reply_markup=None)
                time.sleep(1)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Производная от вашей функии:",
                    reply_markup=None)
                global diff_glob
                markup_diff = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Get Latex", callback_data='6')
                diff_glob = ("(" + get_message.replace("(x)", "") + ")' = "+ text1)
                bot.send_message(call.message.chat.id, diff_glob, parse_mode="html")


            elif call.data == '5':
                clear_equat = ("y" + get_message.replace("^", "**").replace("y(x)", "").replace("y", "")).replace("y=", "")
                x = Symbol('x')
                send_data_arr = solve(clear_equat, x)
                send_data = '\n'.join("x = " + str(value) for value in send_data_arr).replace("sqrt", "√")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вот что мы нашли",
                    reply_markup=None)
                bot.send_message(call.message.chat.id,  f"<code>{send_data}</code>", parse_mode="html")
            elif call.data == '6':
                a = unicode_to_latex(diff_glob)
                bot.send_message(call.message.chat.id,  a)

    except Exception as e:
        print(repr(e))

@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    try:
        calc_data = query.query.replace("+","").replace("-","").replace("*","").replace("/","").replace(" ","").replace("0(","0*(").replace("1(","1*(").replace("2(","2*(").replace("3(","3*(").replace("4(","4*(").replace("5(","5*(").replace("6(","6*(").replace("7(","7*(").replace("8(","8*(").replace("9(","9*(").replace(")(",")*(").replace("^", "")
        if "y=" in query.query:
            try:
                express_f = query.query
            ############################################################################
                clear_equat_inl = (express_f.replace("^", "**").replace("y(x)=", "").replace("y=", "")).replace("y=", "")
                clear_equat_inl = clear_equat_inl.replace("0x", "0*x").replace("1x", "1*x").replace("2x", "2*x").replace("3x", "3*x").replace("4x", "4*x").replace("5x", "5*x").replace("6x", "6*x").replace("7x", "7*x").replace("8x", "8*x").replace("9x", "9*x")
                clear_equat_inl = clear_equat_inl.replace("0(","0*(").replace("1(","1*(").replace("2(","2*(").replace("3(","3*(").replace("4(","4*(").replace("5(","5*(").replace("6(","6*(").replace("7(","7*(").replace("8(","8*(").replace("9(","9*(")
                clear_equat_inl = clear_equat_inl.replace(")(",")*(").replace("x(","x*(").replace(" ", "")
                clear_equat_inl = clear_equat_inl.replace("**", "^")
                x = Symbol('x')
                send_data_arr = solve(clear_equat_inl, x)
                send_data_2 = '; \n'.join("x = " + str(value) for value in send_data_arr).replace("sqrt", "√")
            ############################################################################
                upload_eq = "result = (diff(" + clear_equat_inl.replace("y=", "").replace("^","**").replace("y(x)", "").replace("=", "") + "))"
                with open("diff.py", "w") as file:
                    file.write('''
from sympy.solvers import solve
from sympy import Symbol, diff, symbols, cos, sin, tan, sqrt
x, y = symbols("x y") \n
''' + upload_eq +'''
with open("diff_result.txt", "w") as file:
    file.write(str(result))''')
                os.system("python3 diff.py")

                with open("diff_result.txt", "r") as file:
                    for line in file:
                        text1 = str(line)
                text1 = text1.replace("0x", "0*x").replace("1x", "1*x").replace("2x", "2*x").replace("3x", "3*x").replace("4x", "4*x").replace("5x", "5*x").replace("6x", "6*x").replace("7x", "7*x").replace("8x", "8*x").replace("9x", "9*x")
                text1 = text1.replace("0(","0*(").replace("1(","1*(").replace("2(","2*(").replace("3(","3*(").replace("4(","4*(").replace("5(","5*(").replace("6(","6*(").replace("7(","7*(").replace("8(","8*(").replace("9(","9*(")
                text1 = text1.replace(")(",")*(").replace("x(","x*(").replace(" ", "")
                text1 = text1.replace("**", "^")
                fx = query.query.replace("y", 'f(x)')
                r_sum = types.InlineQueryResultArticle(
                        id='1', title="Корни: \n" + send_data_2,
                        # Описание отображается в подсказке,
                        # message_text - то, что будет отправлено в виде сообщения
                        description=("Выражение: " + query.query),
                        input_message_content=types.InputTextMessageContent(
                        message_text="Выражение: \n" + f"<code>{query.query}</code>" + "\n \n" + "Корни: \n" + f"<code>{send_data_2}</code>", parse_mode="html")
                )
                r_diff = types.InlineQueryResultArticle(
                        id='2', title="Производная: \n" + "f(x)' = " + text1,
                        # Описание отображается в подсказке,
                        # message_text - то, что будет отправлено в виде сообщения
                        description=("Выражение: " + query.query.replace("y", "f(x)")),
                        input_message_content=types.InputTextMessageContent(

                        message_text="Выражение: \n" + f"<code>{fx}</code>" + "\n \n" + "Производная: \n" + f"<code>f(x)' = {text1}</code>", parse_mode="html")
                )
                bot.answer_inline_query(query.id, [r_sum, r_diff])

            except Exception as e:
                print(query.query)

        elif query.query == "DT":
            dt_sum = types.InlineQueryResultArticle(
                    id='1', title="🥃🥃",
                    # Описание отображается в подсказке,
                    # message_text - то, что будет отправлено в виде сообщения
                    description=("Double cup"),
                    input_message_content=types.InputTextMessageContent(
                    message_text="🥃🥃", parse_mode="html")
            )
            bot.answer_inline_query(query.id, [dt_sum])
        elif calc_data.isdigit():
            try:
                matched = query.query.replace("^", "**")
                calc_sum = types.InlineQueryResultArticle(
                        id='1', title="= " + str(eval(matched)),
                    # Описание отображается в подсказке,
                    # message_text - то, что будет отправлено в виде сообщения
                        description=("Выражение: " + query.query),
                        input_message_content=types.InputTextMessageContent(
                        message_text=f"Значение выражения: \n<code>{query.query} = {eval(matched)}</code>", parse_mode="html")
                        )
                bot.answer_inline_query(query.id, [calc_sum])
            except Exception as e:
                print(query.query)
        elif query.query == "alice":
            al_sum = types.InlineQueryResultArticle(
                    id='1', title="🤍",
                    # Описание отображается в подсказке,
                    # message_text - то, что будет отправлено в виде сообщения
                    description=('''
        　 　∧,,,∧
        　 （ ・ω・） I love Alice!
        　　( つ旦O
        　　と＿)_)
                '''),
                    input_message_content=types.InputTextMessageContent(
                    message_text='''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀∧,,,∧
        　 （ ・ω・） I love Alice!
        　　( つ旦O
        　　と＿)_)
                ''', parse_mode="html")
            )
            bot.answer_inline_query(query.id, [al_sum])


    except AttributeError as ex:
        return



# Старт
bot.polling(none_stop=True)



#---------------------------------------------------------------------------
