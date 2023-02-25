import telebot
import json
from datetime import *

history = []
search_res = []
start_date = ''
expence_mode = 0
exp_date = ''
exp_sum = 0
exp_category = ''
choice_mode = ''
event = ''
expence = 0
history_index = 0

API_KEY = '6169568942:AAGfBIaGzIblm.......GpnR8nAG9g6Xc9rNlI'
bot = telebot.TeleBot(API_KEY)

def Selection(message): #Поиск расходов по параметрам. Реализован только строгий поиск по полному совпадению
    global choice_mode
    global expence_mode
    bot.send_message(message.chat.id, '1 - Поиск по дате')
    bot.send_message(message.chat.id, '2 - Поиск по сумме')
    bot.send_message(message.chat.id, '3 - Поиск по описанию')
    bot.send_message(message.chat.id, 'другой вариант - отмена')
    bot.send_message(message.chat.id, 'Выберите режим поиска: ')
    expence_mode = 20

def ResetAll(): #Сброс всех глобальных переменных
    global expence_mode
    global exp_date
    global exp_sum
    global exp_category
    global start_date
    global choice_mode
    global event
    global search_res
    global expence
    global history_index
    search_res = []
    start_date = ''
    expence_mode = 0
    exp_date = ''
    exp_sum = 0
    exp_category = ''
    choice_mode = ''
    event = ''
    expence = 0
    history_index = 0


def load():
    global history
    fname = 'operations.json'
    with open(fname, 'r', encoding='utf-8') as em:
        history = json.load(em)
    return history

def save():
    with open('operations.json', 'w', encoding='utf-8') as em:
        em.write(json.dumps(history, ensure_ascii=False))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Expences manager начал работу')
    try:
        history = load()
        bot.send_message(message.chat.id, 'История расходов загружена')
    except:
        history = []
        bot.send_message(message.chat.id, 'Создана новая история')
        
@bot.message_handler(commands=['list'])
def spisok(message):
    bot.send_message(message.chat.id,('Дата            Сумма       Описание'))
    for i in history:
        bot.send_message(message.chat.id,'    '.join(map(str, i)))

@bot.message_handler(commands=['add'])
def add(message):
    global expence_mode
    bot.send_message(message.chat.id, 'Добавление расхода')
    expence_mode = 1 #Добавление расхода
    bot.send_message(message.chat.id, 'Введите дату расхода в формате dd-mm-yyyy. Для текущей даты нажмите 0:')

@bot.message_handler(commands=['report'])
def report(message):
    global expence_mode
    bot.send_message(message.chat.id, 'Получение отчета о расходах')
    expence_mode = 10 #Отчет
    bot.send_message(message.chat.id, 'Введите начальную дату отчета в формате dd-mm-yyyy: ')

@bot.message_handler(commands=['search'])
def search(message):
    global expence_mode
    global search_res
    bot.send_message(message.chat.id, 'Изменение и удаление расхода')
    expence_mode = 20 #Изменение расхода
    Selection(message) #Выборка расходов по условию

@bot.message_handler(content_types='text')
def add(message):
    global expence_mode
    global exp_date
    global exp_sum
    global exp_category
    global start_date
    global choice_mode
    global event
    global search_res
    global expence
    global history_index
    try:
        if expence_mode == 1: #Добавление расхода
            exp_date = message.text
            if exp_date == '0':
                    exp_date = datetime.now()
            else:
                    exp_date = datetime.strptime(exp_date, "%d-%m-%Y")
            if exp_date > datetime.now():
                    bot.send_message(message.chat.id, 'Добавление будующих расходов невозможно')
                    return
            bot.send_message(message.chat.id, 'Введите сумму расхода: ')
            expence_mode = 2
        elif expence_mode == 2: #Добавление расхода
            exp_sum = int(message.text)
            bot.send_message(message.chat.id, 'Введите описание расхода: ')
            expence_mode = 3
        elif expence_mode == 3: #Добавление расхода
            exp_category = message.text
            history.append([str(exp_date.strftime("%d-%m-%Y")), exp_sum, exp_category])
            bot.send_message(message.chat.id, 'Расход успешно добавлен')
            save()
            ResetAll()        
        elif expence_mode == 10: #Формирование отчета
            start_date = message.text
            try:
                start_date = datetime.strptime(start_date, "%d-%m-%Y")
                bot.send_message(message.chat.id, 'Введите конечную дату отчета в формате dd-mm-yyyy. Для текущей даты введите 0 ')
                expence_mode = 11
            except:
                bot.send_message(message.chat.id, 'Некорректный формат даты')
        elif expence_mode == 11: #Формирование отчета
            end_date = message.text
            if end_date == '0':
                end_date = datetime.now()
            else:
                try:
                    end_date = datetime.strptime(end_date, "%d-%m-%Y")
                except:
                    bot.send_message(message.chat.id, 'Некорректный формат даты')
            if start_date > end_date:
                bot.send_message(message.chat.id, 'Начальная дата не может быть больше конечной')
            else:
                report = []
                summa = 0
                for i in history:
                    if datetime.strptime(i[0], "%d-%m-%Y") >= start_date and datetime.strptime(i[0], "%d-%m-%Y") <= end_date:
                        report.append(i) #Формируем отчет
                        summa += i[1] #Суммируем расходы
                bot.send_message(message.chat.id,('Дата            Сумма       Описание'))
                for i in report:
                    bot.send_message(message.chat.id,'    '.join(map(str, i)))
                bot.send_message(message.chat.id,f'Общая сумма расходов за период {summa} рублей')
                expence_mode = 0
                start_date = ''
        elif expence_mode == 20: #Поиск расхода
            if message.text == '1':
                bot.send_message(message.chat.id, 'Введите дату расхода в формате dd-mm-yyyy :')
            elif message.text == '2':
                bot.send_message(message.chat.id, 'Введите сумму расхода :')
            elif message.text == '3':
                bot.send_message(message.chat.id, 'Введите описание расхода :')
            else:
                expence_mode = 0
                return
            expence_mode = 21
            choice_mode = message.text
        elif expence_mode == 21: #Поиск расхода
            if choice_mode == '2':
                event = int(message.text)
            else:
                event = message.text
            for i in history:
                if event in i:
                    search_res.append(i.copy())
                    search_res[-1].append(history.index(i))
            search_res = list(enumerate(search_res)) #Добавляем нумерацию для выбора конкретного расхода
            bot.send_message(message.chat.id,'Номер  Дата            Сумма       Описание')
            for i in search_res:
                bot.send_message(message.chat.id, f'{i[0]+1}          {i[1][0]}   {i[1][1]}           {i[1][2]}')
            bot.send_message(message.chat.id,'Выберите номер расхода для изменения или 0 для нового поиска: ')
            expence_mode = 22
        elif expence_mode == 22: #Выбор расхода для изменения
            try:
                expence = int(message.text)
                if expence > len(search_res) or expence < 0:
                    expence /= 0 
            except:
                bot.send_message(message.chat.id,'введено некоректное значение ')
                return
            if expence == 0:
                ResetAll()
                Selection(message)
                return
            history_index = search_res[expence-1][1][-1] #Индекс выбранного расхода в исходной базе
            bot.send_message(message.chat.id,("Выберите требуемое действие. 1 - Изменить, 2 - удалить: "))
            expence_mode = 23
        elif expence_mode == 23: #Обработка действия
            if message.text == '1':
                bot.send_message(message.chat.id, 'Введите новую дату расхода в формате dd-mm-yyyy. Для текущей даты нажмите 0:')
                expence_mode = 24
            elif  message.text == '2':
                bot.send_message(message.chat.id, 'Вы уверены что хотите удалить расход (y/n):')
                expence_mode = 27
        elif expence_mode == 24: #Изменение расхода
            exp_date = message.text
            if exp_date == '0':
                exp_date = datetime.now()
            else:
                exp_date = datetime.strptime(exp_date, "%d-%m-%Y")
            if exp_date > datetime.now():
                bot.send_message(message.chat.id, 'Добавление будующих расходов невозможно')
                return
            bot.send_message(message.chat.id, 'Введите сумму расхода: ')
            expence_mode = 25
        elif expence_mode == 25: #Изменение расхода
            exp_sum = int(message.text)
            bot.send_message(message.chat.id, 'Введите описание расхода: ')
            expence_mode = 26
        elif expence_mode == 26: #Изменение расхода
            exp_category = message.text
            history[history_index][0] = str(exp_date.strftime("%d-%m-%Y")) #Изменям расход
            history[history_index][1] = exp_sum
            history[history_index][2] = exp_category                                       
            bot.send_message(message.chat.id, 'Запись изменена')
            save()
            ResetAll()
        elif expence_mode == 27: #Удаление расхода
            if message.text == 'y':
                history.pop(history_index) #Удаляем расход
                bot.send_message(message.chat.id, 'Запись удалена')
                save()
            elif message.text != 'n':
                bot.send_message(message.chat.id, 'Вы уверены что хотите удалить расход (y/n):')                
                return
            ResetAll()                      
        else:
            bot.send_message(message.chat.id, 'Список доступных команд:')
            bot.send_message(message.chat.id, '/start - загрузка истории и запуск бота')
            bot.send_message(message.chat.id, '/add - добавить расход')
            bot.send_message(message.chat.id, '/list - список всех расходов')
            bot.send_message(message.chat.id, '/report - отчет за заданный период')
            bot.send_message(message.chat.id, '/search - изменение и удаление расхода')
    except:
        bot.send_message(message.chat.id, 'Некорректный формат данных')
        ResetAll()
        expence_mode = 0

bot.polling()


