import io
import os
import sys
import common as cm
from contextlib import redirect_stderr
import voice
import utils
import asyncio

def main():
    en = voice.Voice()
    en.set_change_voice(True)
    zh = voice.Voice()
    zh.set_lang("zh")

    engine = "bingchat"

    args = cm.arguParse()

    log = utils.Log()

    if args.file != None:
        log.set_file(args.file)

    en.set_speed(args.speed)

    if args.engine != None and args.engine == "chatgpt":
        engine = "chatgpt"

    while True:
        print("say something........")
        text = en.speech_recognise()
        if (len(text) == 0):
            continue

        if (text.lower()[0:4] == "exit"):
            return

        print(text)
        log.dlog("me: " + text)

        if engine == "chatgpt":
            text = cm.talk_to_chatgpt(text)
        elif engine == "bingchat":
            text = asyncio.run(cm.talk_to_bing(text))

        if cm.isChinese(text):
            zh.speak_text(text)
        else:
            en.speak_text(text)
        log.dlog("npc: " + text)

if __name__ == "__main__":
    main()