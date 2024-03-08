import logging
import datetime
import ephem

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import API_KEY
from handlers import (greet_user, guess_number, send_cat_picture,
                      talk_to_me, user_coordinates)

logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

today_date = datetime.date.today()
solar_systems = {'Mercury': ephem.Mercury(today_date), 'Venus': ephem.Venus(today_date),
                 'Mars': ephem.Mars(today_date), 'Jupiter': ephem.Jupiter(today_date),
                 'Saturn': ephem.Saturn(today_date), 'Uranus': ephem.Uranus(today_date),
                 'Neptune': ephem.Neptune(today_date)}


def constellation_finder(update, context):
    input_planet = update.message.text.split()[1]
    update.message.reply_text(ephem.constellation(solar_systems[input_planet])[1])

def main():
    mybot = Updater(API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', constellation_finder))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Send a cat)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('bot start')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()