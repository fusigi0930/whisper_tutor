import io
import os
import sys
import common as cm
from contextlib import redirect_stderr
import voice
import utils
import argparse


def main():
    en = voice.Voice()
    en.set_change_voice(True)
    zh = voice.Voice()
    zh.set_lang("zh")

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="read file", required=True)

    args = parser.parse_args()

    print("start reading file: {}".format(args.file))
    try:
        with open(args.file) as f:
            text = f.readlines()

            for l in text:
                if len(l) == 0:
                    continue

                if l[0:3] == "me:":
                    l = l[4:]
                else:
                    l = l[5:]

                if cm.isChinese(l):
                    zh.speak_text(l)
                else:
                    en.speak_text(l)

    except Exception:
        print("file not found")

if __name__ == "__main__":
    main()