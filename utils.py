from emoji import emojize
from random import choice, randint
from telegram import KeyboardButton, ReplyKeyboardMarkup
from settings import USER_EMOJI

def main_keyboard():
    return ReplyKeyboardMarkup([['Send a cat', KeyboardButton('My location', request_location=True)]])

def play_random_nambers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Your number: {user_number}, my: {bot_number}. You win!'
    elif user_number == bot_number:
        message = f'Your number: {user_number}, my: {bot_number}. Tie!'
    else:
        message = f'Your number: {user_number}, my: {bot_number}. You lose!'
    return message

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']