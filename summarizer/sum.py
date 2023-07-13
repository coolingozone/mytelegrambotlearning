#aimport libraries
import os
import telebot
import openai
import logging
import openai
import requests
from bs4 import BeautifulSoup

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


# Enable logging

openai.api_key  = 'token' #replace with your opnai api token
logging.basicConfig(filename='sumlog.log',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
bot = telebot.TeleBot("Token") #replace with your bot token

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi, This is youesummarizer  telegram bot that would summarize your web article! Pleae provide the link to the article'")
    #logger.info("message is:  of %s", update.message.text)
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    link=message.text
    res = requests.get(link)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    blacklist = [
        '[document]',
        'noscript',
       'header',
        'html',
        'meta',
        'head', 
       'input',
        'script',
    # there may be more elements you don't want, such as "style", etc.
]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    prompt = f"summarize in point form '{output}'" 
    msg=get_completion(prompt)
   
    logger.info("message is:  of  %s", msg)
    bot.reply_to(message, msg)

    
bot.infinity_polling()