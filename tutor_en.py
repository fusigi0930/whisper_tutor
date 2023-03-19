import io
import os
import sys
import common as cm
from contextlib import redirect_stderr
import voice
import utils

def main():
    en = voice.Voice()
    en.set_change_voice(True)
    zh = voice.Voice()
    zh.set_lang("zh")

    log = utils.Log()
    while True:
        print("say something........")
        text = en.speech_recognise()
        if (len(text) == 0):
            continue

        if (text.lower()[0:4] == "exit"):
            return

        print(text)
        log.dlog("me: " + text)
        text = cm.talk_to_chatgpt(text)
        if cm.isChinese(text):
            zh.speak_text(text)
        else:
            en.speak_text(text)
        log.dlog("npc: " + text)

if __name__ == "__main__":
    main()