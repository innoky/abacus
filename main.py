#---------------------------------------------------------------------------
import time
from random import randint
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
import openai
import speech_recognition as sr
from sympy.solvers import solve
from sympy import Symbol, diff, cos, sin, tan, sqrt
import sympy as sp
import networkx as nx
import numpy as np
import networkx as nx
import pylab as plt
from networkx.drawing.nx_agraph import graphviz_layout
import pygraphviz

import soundfile as sf
from sympy.solvers import solve
from sympy import Symbol, diff, cos, sin, tan, sqrt, sympify

from subprocess import Popen
from speech_recognition import (Recognizer, AudioFile)
from speech_recognition import (UnknownValueError, RequestError)


import telebot

from telebot import types

openai.api_key = "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"

def generate_response(text):
    prompt = text

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Ты - система которая рассказывает как строить графики математических функций. В своих ответах не используй ссылки на другие сайты."},
            {"role": "user", "content": "Как построить график следующей функции? : " + prompt}
        ]
    )
    return response.choices[0].message.content
class SpeechOggAudioFileToText:
    def __init__(self):
        self.recognizer = Recognizer()

    def ogg_to_wav(self, file):
        files = os.listdir(os.curdir)
        args = ['ffmpeg','-i', file, 'test'+ str(len(files)) +'.wav']
        process = Popen(args)
        process.wait()
    @property
    def text(self):
        files = os.listdir(os.curdir)
        AUDIO_FILE = 'test'+ str(len(files)-1) +'.wav'
        with AudioFile(AUDIO_FILE) as source:
            audio = self.recognizer.record(source)
        try:
            text = self.recognizer.recognize_google(audio, language='RU')
            return text
        except UnknownValueError:
            print("Не удаётся распознать аудио файл")
        except RequestError as error:
            print("Не удалось запросить результаты: {0}".format(error))

class TraverseSolver:
    def __init__(self, expr):
        self.expr = expr

    def _set_graph(self):
        self.G = nx.nx_agraph.from_agraph(pygraphviz.AGraph(sp.dotprint(self.expr)))

    def _set_map(self):
        self._map = dict(zip(self.G.nodes, sp.preorder_traversal(self.expr)))

    def _set_baseNode(self):
        self._baseNode = next(iter(self.G.nodes))

    def get_levels(self, mode='draw'):
        if mode == 'draw':
            d = nx.single_source_shortest_path_length(self.G, self._baseNode)
            u, idx = np.unique(list(d.values()), return_index=True)
            levels = [[str(m) for m in n] for n in reversed(np.split(np.array(list(d.keys())), idx[1:]))]
            return levels
        elif mode == 'traverse':
            print(self.G)

    def set_color(self, node, color):
        self.G.nodes[node]['color'] = color

    def display_graph(self, fig, n, nshape=(2, 3)):
        ax = fig.add_subplot(*nshape, n)
        pos = graphviz_layout(self.G, prog='dot')
        colors = nx.get_node_attributes(self.G, 'color')
        nx.draw(self.G, pos = pos, nodelist=[])
        # draw self.G bbox by bbox:
        for i, n in enumerate(self.G.nodes()):
            nx.draw(nx.subgraph(self.G, [n]), pos={n:pos[n]}, labels = {n:f'${sp.latex(self._map[n])}$'}, nodelist=[],
                    bbox=dict(facecolor=colors[n], edgecolor='black', boxstyle='round,pad=0.7'))

    def solve(self, display_graph=True, nshape=(2, 3)):
        self._set_graph() #store sp.srepr+code in each node
        self._set_map() #sp.srepr+code -> expression (without evaluation)
        self._set_baseNode() #sp.srepr+code of self.
        solutionSteps = [self._map[self._baseNode]] #first step that contains initial expression
        levels = self.get_levels(mode='draw')
        if display_graph:
            fig = plt.figure(figsize=(20,10))
        #Step forward
        for i in range(len(levels)):
            if display_graph:
                for node in self.G.nodes():
                    self.set_color(node, 'lightblue')
            anyChanges = False
            for activeNode in levels[i]:
                beforeEval = self._map[activeNode]
                if display_graph:
                    self.set_color(activeNode, 'yellow')
                if not beforeEval.is_Atom:
                    afterEval = beforeEval.func(*beforeEval.args, evaluate=True) #is beforeEval different with afterEval
                    if beforeEval != afterEval:
                        self._map[activeNode] = afterEval
                        if display_graph:
                            self.set_color(activeNode, 'lime')
                        anyChanges = True
            # Calculate value of baseNode() using changes, no evaluation
            if anyChanges:
                for j in range(i+1, len(levels)):
                    for editNode in levels[j]:
                        args = [self._map[node] for node in self.G[editNode]] #each ancestor
                        if not self._map[editNode].is_Atom:
                            self._map[editNode] = self._map[editNode].func(*args, evaluate=False)
                solutionSteps.append(self._map[self._baseNode])
            if display_graph:
                self.display_graph(fig, n=len(solutionSteps), nshape=nshape)
        plt.show()
        return solutionSteps

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

            steps = types.InlineKeyboardMarkup(row_width=1)
            global calculus_exp
            calculus_exp = message.text
            get_steps = types.InlineKeyboardButton("Пошаговое решение", callback_data='6')


            steps.add(get_steps)
            bot.send_message(message.chat.id, "Значение выражения: \n" + message.text + " = " + str(eval( message.text.replace("^","**"))), reply_markup=steps)



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
                markup22 = types.InlineKeyboardMarkup(row_width=1)
                item_howto = types.InlineKeyboardButton("Как построить этот график?", callback_data='10')


                markup22.add(item_howto)
                bot.send_photo(call.message.chat.id, open('users/'+user_id+'/graphdraw.png', 'rb'), reply_markup=markup22);

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
            elif call.data == '10':

                msg = bot.send_message(call.message.chat.id, '⌛')
                response = generate_response(get_message)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg.message_id, text=response)

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



            elif call.data == '5':
                clear_equat = ("y" + get_message.replace("^", "**").replace("y(x)", "").replace("y", "")).replace("y=", "")
                x = Symbol('x')
                send_data_arr = solve(clear_equat, x)
                send_data = '\n'.join("x = " + str(value) for value in send_data_arr).replace("sqrt", "√")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вот что мы нашли",
                    reply_markup=None)
                bot.send_message(call.message.chat.id,  f"<code>{send_data}</code>", parse_mode="html")
            elif call.data == '6':
                expr = sp.sympify(calculus_exp, evaluate=False)
                steps = TraverseSolver(expr).solve(display_graph=False, nshape=(0,0))
                bot.send_message(call.message.chat.id, "Выражение: \n" + "\n => ". join([sp.StrPrinter(dict(order='none'))._print(step) for step in steps]))

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
                expr = sp.sympify(query.query, evaluate=False)
                steps = TraverseSolver(expr).solve(display_graph=False, nshape=(0,0))
                msgg = "Пошаговое решение: \n" + "\n => ". join([sp.StrPrinter(dict(order='none'))._print(step) for step in steps])
                calc_sum = types.InlineQueryResultArticle(
                        id='1', title="= " + str(eval(matched)),
                    # Описание отображается в подсказке,
                    # message_text - то, что будет отправлено в виде сообщения
                        description=("Выражение: " + query.query),
                        input_message_content=types.InputTextMessageContent(
                        message_text=f"Значение выражения: \n<code>{query.query} = {eval(matched)}</code>\n\n" + msgg, parse_mode="html")
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

@bot.message_handler(content_types=['voice'])

def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    user_id = message.from_user.id
    downloaded_file = bot.download_file(file_info.file_path)
    files = os.listdir(os.curdir)
    with open(str(user_id) + str(len(files)) +'.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)

    speech_ogg = SpeechOggAudioFileToText()
    speech_ogg.ogg_to_wav(str(user_id) + str(len(files)) +'.ogg')
    global get_message
    global user_ind
    user_ind = message.from_user.id
    if "y" or "x" or "y(x)" in speech_ogg.text:
        if ("sin" or "cos" or "tan") in speech_ogg.text:
            bot.send_message(message.chat.id, "<em>Функция переодическая, корни могут иметь период повторения</em>", parse_mode ='html')
        if "\\" in speech_ogg.text:
            get_message = LatexNodes2Text().latex_to_text(speech_ogg.text.replace("\\"+"dfrac", "\\"+"frac")).lower().replace(" ","")
        else:
            get_message = speech_ogg.text.lower().replace(" ","")
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
# Старт
bot.polling(none_stop=True)



#---------------------------------------------------------------------------
