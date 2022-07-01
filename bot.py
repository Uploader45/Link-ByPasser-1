import re
from transition import Translation
import time
import cloudscraper
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from os import environ
import aiohttp
from pyrogram import Client, filters
from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from pyrogram.errors import UserNotParticipant, UserBannedInChannel 

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
CRYPT = 'ajRmMzd2ZEdxL055ZC9vMHlwNGZwZUE4Zm9MSzFUVDRETU9ESm4xU1lqcz0%3D'
#API_KEY = environ.get('API_KEY')

bot = Client('LinkByPass bot',
             api_id= "1543212",
             api_hash= "d47de4b25ddf79a08127b433de32dc84",
             bot_token= "5462389029:AAHiRZVyr-WL2e80y0wz-e7hd9oTOIlM5iY")


@bot.on_message(filters.command('start'))
async def start(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await update.reply_text("You are Banned")
        return
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text("**Your Banned**")
               return
        except UserNotParticipant:
            await update.reply_text(
                text="**Join Update Channel**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        else:
            await update.reply_text(Translation.START_TEXT.format(update.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton("HELP", callback_data = "ghelp"),
                        InlineKeyboardButton("ABOUT", callback_data = "about"),
                        InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        ),
        reply_to_message_id=update.message_id
    ) 
      try:
       await message.reply_text(Translation.START_TEXT,quote=True)
    except Exception as e:
        await message.reply(f'**Error** : {e}', quote=True)

@bot.on_message(filters.command('help'))
async def help(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await update.reply_text("You are Banned")
        return
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text("**Your Banned**")
               return
        except UserNotParticipant:
            await update.reply_text(
                text="**Join Update Channel**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        else:
            await update.reply_text(Translation.HELP_TEXT.format(update.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton("ABOUT", callback_data = "about"),
                        InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        ),
        reply_to_message_id=update.message_id
    ) 
      try:
       await message.reply_text(Translation.HELP_TEXT,quote=True)
    except Exception as e:
        await message.reply(f'**Error** : {e}', quote=True)


#@bot.on_message(filters.regex(r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"))
@bot.on_message(filters.command('bpp'))
async def link_handler(bot, message):
 # link = message.matches[0].group(0)
  l = message.text.split(' ', 1)

  if len(l) == 1:
        return await message.reply_text('Send Any Gplink ,DropLink,Rocklink')
  link = l[1]
  mess = await message.reply_text("**Bypassing...⏳**",quote=True)
  if 'gplinks.co' in link:
    try:
        short_link = await gplinks_bypass(link)
      #  mess = await message.reply_text("**Bypassing...⏳**",quote=True)
        await mess.edit_text(f"**Bypassed URL** : {short_link} \n\n ©cc: {message.from_user.mention}",disable_web_page_preview=True)
    except Exception as e:
        await mess.edit_text(f"**Error** : {e}")
  elif 'droplink.co' in link:
     try:
        short_link = await droplink_bypass(link)
     #   mess = await message.reply_text("**Bypassing...⏳**",quote=True)
        await mess.edit_text(f"**Bypassed URL** : {short_link} \n\n ©cc: {message.from_user.mention}",disable_web_page_preview=True)
     except Exception as e:
        await mess.edit_text(f"**Error** : {e}")
  elif 'rocklinks.net' in link:
     try:
        short_link = await rocklink_bypass(link)
      #  mess = await message.reply_text("**Bypassing...⏳**",quote=True)
        await mess.edit_text(f"**Bypassed URL** : {short_link} \n\n ©cc: {message.from_user.mention}",disable_web_page_preview=True)
     except Exception as e:
        await mess.edit_text(f"**Error** : {e}")
  elif 'hubdrive.cc' in link:
     try:
        short_link = await hubdrive_bypass(link)
     #   mess = await message.reply_text("**Bypassing...⏳**",quote=True)
        await mess.edit_text(f"**Bypassed URL** : {short_link} \n\n ©cc: {message.from_user.mention}",disable_web_page_preview=True)
     except Exception as e:
        await mess.edit_text(f"**Error** : {e}")
     pass

async def gplinks_bypass(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    res = client.head(url)
    header_loc = res.headers['location']
    param = header_loc.split('postid=')[-1]
    req_url = f'{p.scheme}://{p.netloc}/{param}'

    p = urlparse(header_loc)
    ref_url = f'{p.scheme}://{p.netloc}/'

    h = { 'referer': ref_url }
    res = client.get(req_url, headers=h, allow_redirects=False)

    bs4 = BeautifulSoup(res.content, 'html.parser')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'referer': ref_url,
        'x-requested-with': 'XMLHttpRequest',
    }
    time.sleep(10)
    res = client.post(final_url, headers=h, data=data)
    try:
        return res.json()['url'].replace('\/','/')
    except: 
        return "An Error Occured "

async def droplink_bypass(url):
    client = requests.Session()
    res = client.get(url)

    ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]

    h = {'referer': ref}
    res = client.get(url, headers=h)

    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest'
    }
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    time.sleep(3.1)
    res = client.post(final_url, data=data, headers=h)
    try:
        return res.json()['url'].replace('\/','/')
    except: 
        return "An Error Occured "

async def rocklink_bypass(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'rocklinks.net' in url:
        DOMAIN = "https://pastebin.techymedies.com/"
    else:
        DOMAIN = "https://rocklink.in"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    if 'rocklinks.net' in url:
        final_url = f"{DOMAIN}/{code}?quelle=" 
    else:
        final_url = f"{DOMAIN}/{code}"

    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    time.sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: 
        return "An Error Occured "
         
#hubdrive-dl

async def parse_info(res):
    info_parsed = {}
    title = re.findall('>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall('>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    return info_parsed

async def hubdrive_bypass(url):
    client = requests.Session()
    client.cookies.update({'crypt': CRYPT})
    
    res = client.get(url)
    info_parsed = await parse_info(res)
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    
    data = { 'id': file_id }
    
    headers = {
        'x-requested-with': 'XMLHttpRequest'
    }
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except: return {'error': True, 'src_url': url}
    
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url

    return info_parsed['gdrive_url']




bot.run()
