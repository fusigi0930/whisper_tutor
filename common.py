import io
import os
import openai
import config as c
import re
import binascii
import argparse

import asyncio
from EdgeGPT import Chatbot, ConversationStyle

def arguParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="file name", required=False)
    parser.add_argument("-s", "--speed", help="set the tts speak speed", type=float, default=0.95)
    parser.add_argument("-e", "--engine", help="select the chat engine", required=False)

    args = parser.parse_args()
    return args

def talk_to_chatgpt(text):
    openai.api_key = c.chatgpt_key
    message = [
        {
            "role": "user",
            "content": text
        },
    ]

    res = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = message,
    )

    res_text = res.choices[0].message.content.replace('\n', '')
    return res_text

async def talk_to_bing(text):
    bot = Chatbot(cookiePath='./bing-cookies.json')
    jn = (await bot.ask(prompt=text, conversation_style=ConversationStyle.creative, wss_link="wss://sydney.bing.com/sydney/ChatHub"))
    await bot.close()

    # print(':'.join(hex(ord(x))[2:] for x in res_text))
    res_text = re.sub(u'[\U0001f000-\U0001f9ff]', "", jn['item']['messages'][1]['text'])
    return res_text

def isChinese(text):
    ucs2T = text.encode('utf16')
    print(ucs2T)
    if re.search(u'[\u4e00-\u9fff]', text):
        return True

    return False