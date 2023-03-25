import io
import os
import openai
import config as c
import re
import binascii
import argparse

def arguParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="file name", required=False)
    parser.add_argument("-s", "--speed", help="set the tts speak speed", type=float, default=0.95)

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

def isChinese(text):
    ucs2T = text.encode('utf16')
    print(ucs2T)
    if re.search(u'[\u4e00-\u9fff]', text):
        return True

    return False