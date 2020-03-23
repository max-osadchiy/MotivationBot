import telebot
import pymongo
import schedule
import time
import motivation
import random
import config

bot = telebot.TeleBot(config.token)

client = pymongo.MongoClient(f"mongodb+srv://maxim:{config.dbpass}@cluster0-d10qd.mongodb.net/test?retryWrites=true&w=majority")
db = client.bot_users
col = db.users

markup = telebot.types.ReplyKeyboardMarkup(True)
markup.row('Цитата', 'Цели')
markup.row('Книги', 'Создать цель')

@bot.message_handler(commands=['start'])
def start_message(message):
    if col.find_one({'_id': f"{message.from_user.id}"}):
        bot.send_message(message.chat.id, 'Привет, этот бот поможет тебе достичь всех твоих целей. Так же сможешь тут ставить свои цели на неделю, месяц, год. Если ты любишь читать книги по мотивациям - мы можем тебе помочь!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Привет, этот бот поможет тебе достичь всех твоих целей. Так же сможешь тут ставить свои цели на неделю, месяц, год. Если ты любишь читать книги по мотивациям - мы можем тебе помочь!', reply_markup=markup)
        user_form_db = {"_id": f"{message.from_user.id}", "name": f"{message.from_user.username}"}
        col.insert_one(user_form_db)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'цитата':
        bot.send_message(message.chat.id, 'Цитата: ' + random.choice(motivation.motivation_quotes))
    elif message.text.lower() == 'цели':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'книги':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'создать цель':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    else:
        bot.send_message(message.chat.id, 'Не понял тебя')

def motivate_message():
    ids = [i['_id'] for i in col.find({})]
    for i in ids:
        bot.send_message(int(i), random.choice(motivation.motivation_quotes))
        print("Send motivation message")

schedule.every(20).seconds.do(motivate_message)
schedule.every().day.at("08:00").do(motivate_message)
schedule.every().day.at("14:00").do(motivate_message)
schedule.every().day.at("20:00").do(motivate_message)
while True:
    schedule.run_pending()
    time.sleep(1)
        
bot.polling()