'''Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите
  бота отвечать, в каком созвездии сегодня находится планета.'''

import logging
import datetime
import ephem
from glob import glob
from random import randint, choice
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from emoji import emojize
from settings import API_KEY, USER_EMOJI

logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

today_date = datetime.date.today()
solar_systems = {'Mercury': ephem.Mercury(today_date), 'Venus': ephem.Venus(today_date),
                 'Mars': ephem.Mars(today_date), 'Jupiter': ephem.Jupiter(today_date),
                 'Saturn': ephem.Saturn(today_date), 'Uranus': ephem.Uranus(today_date),
                 'Neptune': ephem.Neptune(today_date)}

def greet_user(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Hi {context.user_data['emoji']}!")

def constellation_finder(update, context):
    input_planet = update.message.text.split()[1]
    update.message.reply_text(ephem.constellation(solar_systems[input_planet])[1])

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text
    print(text)
    update.message.reply_text(f"{text} {context.user_data['emoji']}")

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']

def play_random_nambers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Your number: {user_number}, my: {bot_number}. You win!'
    elif user_number == bot_number:
        message = f'Your number: {user_number}, my: {bot_number}. Tie!'
    else:
        message = f'Your number: {user_number}, my: {bot_number}. You lose!'
    return message

def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_nambers(user_number)
        except (TypeError, ValueError):
            message = 'Input integer'
    else:
        message = 'Input number'
    update.message.reply_text(message)

def sent_cat_picture(update, context):
    cat_photo_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'))

def main():
    mybot = Updater(API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', constellation_finder))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', sent_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('bot start')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()