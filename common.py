import io
import os
import speech_recognition as sr
import whisper
import torch
import sys
import contextlib

from TTS.api import TTS
import pyaudio
import wave

import openai
import config as c

from tempfile import NamedTemporaryFile
from sys import platform
import time

def talk_to_chatgpt(text):
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