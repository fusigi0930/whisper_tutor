import io
import os
import sys
import common as cm
from contextlib import redirect_stderr
import voice
import utils

def main():
    v = voice.Voice()
    log = utils.Log()
    while True:
        print("say something........")
        text = v.speech_recognise()
        if (len(text) == 0):
            continue

        if (text.lower() == "exit"):
            return

        print(text)
        log.dlog("me: " + text)
        text = cm.talk_to_chatgpt(text)
        v.speak_text(text)
        log.dlog("npc: " + text)

if __name__ == "__main__":
    main()