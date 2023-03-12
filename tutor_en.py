import io
import os
import sys
import common as cm
from contextlib import redirect_stderr

def main():
    cm.init()
    while True:
        print("say something........")
        text = cm.start_speech_recognise()
        if (len(text) == 0):
            continue

        if (text.lower() == "exit"):
            return

        print(text)
        cm.dlog("me: " + text)
        text = cm.talk_to_chatgpt(text)
        cm.speak_text(text)
        cm.dlog("npc: " + text)

if __name__ == "__main__":
    main()