import telebot  
import random
from telebot import types
bot = telebot.TeleBot("-", parse_mode = None)

balance = 1000
stake = 0 
deposit = 0
sum_bal = 0

@bot.message_handler(content_types = ['text', 'document', 'audio'])
def start(message):
    if message.text == '/start' or message.text == 'Назад':
        himessage(message.chat.id)
        bot.register_next_step_handler(message, button_reply) 
    elif message.text == 'Баланс' or message.text == "Начать игру":
        button_reply(message)
    else:
        bot.send_message(message.from_user.id, 'Чтобы начать заново введите /start')

def himessage(chat_id):
    bot.send_message(chat_id, f'Текущий баланс: {balance}')
    markup = types.ReplyKeyboardMarkup()
    itembtn_game = types.KeyboardButton("Начать игру")
    itembtn_balance = types.KeyboardButton("Баланс")
    markup.add(itembtn_game)
    markup.add(itembtn_balance)
    bot.send_message(chat_id, "Выбор: ", reply_markup = markup)

def button_reply(message):
    global balance
    if message.text == "Начать игру":
        if balance < 10:
            bot.send_message(message.from_user.id, f"Пополните баланс. Ваш баланс: {balance}")
        else: 
            bot.send_message(message.from_user.id, "Введите сумму: ", reply_markup = types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, dep)
    elif message.text == "Баланс":
        markup = types.ReplyKeyboardMarkup()
        itembtn_back = types.KeyboardButton("Назад")
        itembtn_dep = types.KeyboardButton("Пополнить")
        markup.add(itembtn_back)
        markup.add(itembtn_dep)
        bot.send_message(message.from_user.id, f"Ваш баланс: {balance}" , reply_markup = markup)
        bot.register_next_step_handler(message, dep_func)
        
def dep_func(message):
    if message.text == "Пополнить":
        bot.send_message(message.from_user.id, "Введите сумму: ", reply_markup = types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, sum)
    if message.text == "Назад": 
        himessage(message.chat.id)

def sum(message):
    global sum_bal, balance
    sum_bal = message.text
    try:
        sum_bal = int(message.text)
    except Exception: 
        bot.send_message(message.from_user.id, "Только числа")
        bot.register_next_step_handler(message, sum)
        return
    if sum_bal > 0:
        bot.send_message(message.from_user.id, "Успешно пополнено")
        balance += sum_bal
        markup = types.ReplyKeyboardMarkup()
        itembtn_back = types.KeyboardButton("Назад")
        markup.add(itembtn_back)
        bot.send_message(message.from_user.id, f"Ваш баланс: {balance}" , reply_markup = markup)
    else:
        bot.send_message(message.from_user.id, "Сумма должна быть больше 0")
        bot.register_next_step_handler(message, sum)

def dep(message):
    global balance
    global deposit
    try:
        deposit = int(message.text)
    except Exception: 
        bot.send_message(message.from_user.id, "Только числа")
        bot.register_next_step_handler(message, dep)
        return
    
    if balance >= deposit and deposit > 0:
        balance -= deposit
        game_type(message)
    else:
        bot.send_message(message.from_user.id, "Некорректная сумма. Введите еще раз")
        bot.register_next_step_handler(message, dep)

def game_type(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn_game1 = types.KeyboardButton("Угадай число")
    itembtn_game2 = types.KeyboardButton("Чет-Нечет")
    markup.add(itembtn_game1)
    markup.add(itembtn_game2)
    bot.send_message(message.from_user.id, "Выбор: ", reply_markup = markup)
    bot.register_next_step_handler(message, game)

def game(message):
    global balance, stake, guess
    if message.text == "Угадай число":
        bot.send_message(message.from_user.id, "Отправьте число", reply_markup = types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_numb)

    elif message.text == "Чет-Нечет": 
        markup = types.ReplyKeyboardMarkup()
        itembtn_chet = types.KeyboardButton("Четное")
        itembtn_nechet = types.KeyboardButton("Нечетное")
        markup.add(itembtn_chet)
        markup.add(itembtn_nechet)
        bot.send_message(message.from_user.id, "Выберите: ", reply_markup = markup)
        bot.register_next_step_handler(message, game_2)
        
def game_1 (message):
    global stake, guess, deposit, balance
    stake = message.text
    guess = random.randint(1, 2)
    if guess == int(stake):
        balance += deposit*3
        bot.send_message(message.from_user.id, f"Вы угадали число. Загаданное число: {guess}")
    else:
        bot.send_message(message.from_user.id, f"Вы проиграли. Загаданное число: {guess}")
        
    himessage(message.chat.id)
    
def game_2(message):
    global balance, stake, guess
    guess = random.randint(1, 36)
    if message.text == "Четное":
        if guess % 2 == 0:
            balance += deposit * 2
            bot.send_message(message.from_user.id, f"Вы выиграли. Загаданное число: {guess}, четное")
        else:
            bot.send_message(message.from_user.id, f"Вы проиграли. Загаданное число: {guess}, нечетное")
    else:
        if guess % 2 != 0:
            balance += deposit * 2
            bot.send_message(message.from_user.id, f"Вы выиграли. Загаданное число: {guess}, нечетное")
        else:
            bot.send_message(message.from_user.id, f"Вы проиграли. Загаданное число: {guess}, четное")
    
    himessage(message.chat.id)

def get_numb(message):
    global stake
    stake = message.text
    try:
        stake = int(message.text)
    except Exception: 
        bot.send_message(message.from_user.id, "Только числа")
        bot.register_next_step_handler(message, get_numb)
        return 
    if not (stake > 0 and stake < 37):
        bot.send_message(message.from_user.id, "Отправь число от 1 до 36", reply_markup = types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_numb)
    else:
        bot.send_message(message.from_user.id, f'Ставка: {stake}')
        game_1(message)

bot.polling(none_stop = True)
