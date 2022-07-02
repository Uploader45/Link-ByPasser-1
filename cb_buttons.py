import os

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from translation import Translation

import pyrogram
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from help_text import help, start, about

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
CRYPT = 'ajRmMzd2ZEdxL055ZC9vMHlwNGZwZUE4Zm9MSzFUVDRETU9ESm4xU1lqcz0%3D'
#API_KEY = environ.get('API_KEY')

bot = Client('LinkByPass bot',
             api_id= "1543212",
             api_hash= "d47de4b25ddf79a08127b433de32dc84",
             bot_token= "5462389029:AAHiRZVyr-WL2e80y0wz-e7hd9oTOIlM5iY")


@bot.on_callback_query()
async def button(bot, update):
    if update.data == "start":
        await update.message.edit_text(
            text=Translation.START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton("HELP", callback_data = "ghelp"),
                        InlineKeyboardButton("ABOUT", callback_data = "about"),
                        InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        ))
    elif update.data == "ghelp":
        await update.message.edit_text(
            text=Translation.HELP_USER,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('ABOUT', callback_data = "about"),
                    InlineKeyboardButton('CLOSE', callback_data = "close")
                ]
            ]
        ))
    elif update.data == "about":
        await update.message.edit_text(
            text=Translation.ABOUT_TEXT,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('HELP', callback_data = "ghelp")
                    InlineKeyboardButton('CLOSE', callback_data = "close")
                ]
            ]
        ))
    elif update.data == "close":
        await update.message.delete()
        try:
            await update.message.reply_to_message.delete()
        except:
            pass
   
    else:
       pass
