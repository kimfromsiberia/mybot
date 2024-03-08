from glob import glob
from random import choice

from utils import get_smile, main_keyboard, play_random_nambers

def greet_user(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f"Hi {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
    )

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text
    print(text)
    update.message.reply_text(f"{text} {context.user_data['emoji']}")

def send_cat_picture(update, context):
    cat_photo_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'), reply_markup=main_keyboard())

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
    update.message.reply_text(message, reply_markup=main_keyboard())

def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Your coords {coords} {context.user_data['emoji']}",
        reply_markup=main_keyboard()
    )