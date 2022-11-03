import sqlite3
import telebot
from googletrans import Translator
from config import TOKEN
from telebot import types


bot = telebot.TeleBot(TOKEN)

connect_db = sqlite3.connect('tgbot.sqlite3', check_same_thread=False)
translator = Translator()

def create_table_followers():
    cursor = connect_db.cursor()
    cursor.execute(
        '\
            CREATE TABLE IF NOT EXISTS followers\
                (\
                    id INTEGER PRIMARY KEY,\
                    user_id INTEGER UNIQUE, \
                    first_name TEXT,\
                    last_name TEXT,\
                    username TEXT\
                    )\
        '
    )
    connect_db.commit() #сщчраняем изменения
    cursor.close() 

def add_follwer(user_id, first_name, last_name, username):
    try:
        cursor = connect_db.cursor()
        cursor.execute(
            '''
                INSERT INTO followers (user_id, first_name, last_name, username) 
                VALUES (?, ?, ?, ?) 
            ''',
            (user_id, first_name, last_name, username)   
)
        connect_db.commit()
        cursor.close()
        return True 
    except sqlite3.IntegrityError:
        return False

def delete_follower(user_id):
    cursor = connect_db.cursor()
    cursor.execute('DELETE FROM followers WHERE user_id=?', (user_id,))
    connect_db.commit()
    cursor.close()

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    follow1 = types.KeyboardButton('/follow')
    unfollow = types.KeyboardButton('/unfollow')
    markup.add(follow1)
    markup.add(unfollow)
    bot.send_message(message.chat.id, 'Бот запущен', reply_markup=markup)

@bot.message_handler(commands=['follow'])
def  follow_user(message):
    flag = add_follwer(message.chat.id, message.chat.first_name,
    message.chat.last_name, message.chat.username )
    if flag:
        bot.send_message(message.chat.id, 'You are now following the bot')
    else:
        bot.send_message(message.chat.id, 'You are already followwing the bot')


@bot.message_handler(commands=['unfollow'])
def unfollow_user(message):
    delete_follower(message.chat.id)
    bot.send_message(message.chat.id, 'вы отписались')

translator = Translator()
@bot.message_handler(content_types=['text'])
def start_message(message):
    print(message.text)
    result = translator.translate(message.text, dest='ru')
    result = translator.translate(message.text, dest='en')
    bot.send_message(message.chat.id, result.text)

if __name__ == '__main__':
    create_table_followers()
    bot.polling(non_stop=True)






