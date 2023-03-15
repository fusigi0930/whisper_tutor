import io
import os
import openai
import config as c
import re
import binascii

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