import os
try:
    import telebot
except ModuleNotFoundError:
    os.system('pip install pyTelegramBotAPI')
    import telebot
try:
    import requests
except ModuleNotFoundError:
    os.system('pip install requests')
    import requests

BOT_TOKEN = '7502427863:AAHAtfIiCd7lmG8u_zDzZZnVx71lkENTDgE'
bot = telebot.TeleBot(BOT_TOKEN)

def reset(email):
    url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"
    headers = {
        "authority": "www.instagram.com",
        "method": "POST",
        "path": "/api/v1/web/accounts/account_recovery_send_ajax/",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "csrftoken=BbJnjd.Jnw20VyXU0qSsHLV; mid=ZpZMygABAAH0176Z6fWvYiNly3y2; ig_did=BBBA0292-07BC-49C8-ACF4-AE242AE19E97; datr=ykyWZhA9CacxerPITDOHV5AE; ig_nrcb=1; dpr=2.75; wd=393x466",
        "origin": "https://www.instagram.com",
        "referer": "https://www.instagram.com/accounts/password/reset/?source=fxcal",
        "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; M2101K786) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "x-asbd-id": "129477",
        "x-csrftoken": "BbJnjd.Jnw20VyXU0qSsHLV",
        "x-ig-app-id": "1217981644879628",
        "x-ig-www-claim": "0",
        "x-instagram-ajax": "1015181662",
        "x-requested-with": "XMLHttpRequest"
    }

    data = {
        "email_or_username": email,
        "flow": "fxcal"
    }
    
    response = requests.post(url, headers=headers, data=data)
    return response.json()
    
    
@bot.message_handler(commands=['start'])
def welcome(message):
    try:
        profile_photos = bot.get_user_profile_photos(message.from_user.id)
        if profile_photos.photos:
            photo_file_id = profile_photos.photos[0][0].file_id
            bot.send_photo(chat_id=message.chat.id, 
                           photo=photo_file_id, 
                           caption=f"*Hello, {message.from_user.first_name}! \nYour user ID =* `{message.from_user.id}`",
                           parse_mode="Markdown")
        else:
            bot.send_message(chat_id=message.chat.id, 
                             text=f"*Hello, {message.from_user.first_name}! \nYour user ID =* `{message.from_user.id}`",
                             parse_mode="Markdown")
    except Exception as e:
        print(e)
        bot.send_message(chat_id=message.chat.id, 
                         text="An error occurred while fetching profile photos.")

@bot.message_handler(commands=['reset'])
def send_welcome(message):
    bot.reply_to(
        message,
        f"*Welcome*, [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n*Send me any Instagram username to reset*\n*Example:* `User123`",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def handle_reset(message):
    email_or_username = message.text
    try:
        result = reset(email_or_username)
        if "message" in result:
            bot.reply_to(message, f"{result['message']}")
        else:
           print('')
           # bot.reply_to(message, "No specific message received from Instagram.")
    except Exception as e:
        print(e)
       # bot.reply_to(message, f"An error occurred: {str(e)}")

print("Polling")
bot.polling()