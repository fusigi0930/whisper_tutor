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

stt_tmpfile = None
tts_tmpfile = None
tts = None
voice_id = None
mic_rec = None
mic_source = None
whisper_model = None
mic_name = "sysdefault"
model = "small"
record_timeout = 6
log_file = None

def dlog(t):
    if log_file == None:
        return

    log_file.write(t + "\n")
    log_file.flush()

def init_mic_rec():
    global mic_rec
    global stt_tmpfile
    global mic_source

    mic_rec = sr.Recognizer()
    mic_rec.energy_threshold = 1000
    mic_rec.dynamic_energy_threshold = False

    if 'linux' in platform:
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if mic_name in name:
                mic_source = sr.Microphone(sample_rate=16000, device_index=index)
                break
    else:
        mic_source = sr.Microphone(sample_rate=16000)

    with mic_source:
        mic_rec.adjust_for_ambient_noise(mic_source)

def init(lang="en", disable_err=True):
    openai.api_key = c.chatgpt_key
    global stt_tmpfile
    global tts_tmpfile
    global tts
    global voice_id
    global whisper_model
    global log_file

    stt_tmpfile = NamedTemporaryFile().name
    tts_tmpfile = NamedTemporaryFile().name
    init_mic_rec()

    filename = "log" + "-" + time.strftime("%Y%m%d-%H%M") + ".log"
    log_file = open(filename, "w")

    if (lang == "en"):
        tts = TTS("tts_models/en/vctk/vits")
        voice_id = "p228"
        whisper_model = whisper.load_model(model+".en")
    else:
        return

def start_speech_recognise():
    global mic_rec
    global stt_tmpfile
    global mic_source
    global whisper_model

    if (mic_rec == None or stt_tmpfile == None or
        mic_source == None or whisper_model == None):
        return '' 

    with mic_source:
        audio_data = mic_rec.listen(
            mic_source, 
            phrase_time_limit=record_timeout
        )

    with open(stt_tmpfile, "wb") as f:
        f.write(audio_data.get_wav_data())

    r = whisper_model.transcribe(stt_tmpfile, fp16=torch.cuda.is_available())
    res_text = r['text'].strip()

    return res_text

def speak_text(t):
    global tts
    global tts_tmpfile
    global voice_id

    if (tts == None) or (tts_tmpfile == None):
        return

    tts.tts_to_file(text=t, speaker=voice_id, file_path=tts_tmpfile)

    w = wave.open(tts_tmpfile, "rb")
    p = pyaudio.PyAudio()
    s = p.open(format = p.get_format_from_width(w.getsampwidth()), 
            channels = w.getnchannels(),
            rate = w.getframerate(),
            output = True)

    data = w.readframes(1024)
    while data:
        s.write(data)
        data = w.readframes(1024)

    s.stop_stream()
    s.close()
    p.terminate()

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