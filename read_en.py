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

    args = cm.arguParse()

    if args.file == None:
        print("please select a file")
        sys.exit()

    en.set_speed(args.speed)

    print("start reading file: {}".format(args.file))
    try:
        with open(args.file) as f:
            text = f.readlines()

            if args.output != None:
                str = ''.join(text)
                en.speak_text(str, args.output)

            for l in text:
                if len(l) == 0:
                    continue

                if l[0:3] == "me:":
                    l = l[4:]
                elif l[0:4] == "npc:":
                    l = l[5:]

                if cm.isChinese(l):
                    zh.speak_text(l)
                else:
                    en.speak_text(l)

    except Exception as e:
        print("file not found")
        print(e)


if __name__ == "__main__":
    main()