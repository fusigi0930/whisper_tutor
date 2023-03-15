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
from datetime import datetime, timedelta
from queue import Queue
import copy
import random

class Voice:
    def __init__(self):
        self.stt_tmpfile = NamedTemporaryFile().name
        self.tts_tmpfile = NamedTemporaryFile().name
        self.queue_tmpfile = NamedTemporaryFile().name

        self.mic_rec = sr.Recognizer()
        self.mic_source = None
        self.whisper_model = None
        self.mic_name = "sysdefault"
        self.data_queue = Queue()

        if 'linux' in platform:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if self.mic_name in name:
                    self.mic_source = sr.Microphone(sample_rate=16000, device_index=index)
                    break
        else:
            self.mic_source = sr.Microphone(sample_rate=16000)

        with self.mic_source:
            self.mic_rec.adjust_for_ambient_noise(self.mic_source)

        self.model = "small"
        self.lang = "en"

        self.tts = TTS("tts_models/en/vctk/vits", progress_bar=False, gpu=True)
        self.voice_id = self.__randomSpeaker()
        self.whisper_model = whisper.load_model(self.model+".en")

    def __randomSpeaker(self):
        size = len(self.tts.speakers)
        idx = random.randint(0, size-1)
        return self.tts.speakers[idx]


    def set_lang(self, lang):
        if lang == "en":
            self.tts = TTS("tts_models/en/vctk/vits", progress_bar=False, gpu=True)
            self.voice_id = self.__randomSpeaker()
        elif lang == "zh":
            self.tts = TTS("tts_models/zh-CN/baker/tacotron2-DDC-GST",
                vocoder_path="vocoder_models/en/ljspeech/multiband-melgan",
                progress_bar=False, gpu=True)
        else:
            return

        self.lang = lang

    def start_speech_recognise(self):
        with self.mic_source:
            audio_data = self.mic_rec.listen(
                self.mic_source, 
                phrase_time_limit = 6
            )

        with open(self.stt_tmpfile, "wb") as f:
            f.write(audio_data.get_wav_data())

        r = self.whisper_model.transcribe(self.stt_tmpfile, fp16=torch.cuda.is_available())
        res_text = r['text'].strip()

        return res_text

    def speech_recognise(self):
        def record_cb(_, audio:sr.AudioData) -> None:
            data = audio.get_raw_data()
            self.data_queue.put(data)

        stop = self.mic_rec.listen_in_background(
            self.mic_source,
            record_cb
        )

        final_sentence = False
        phrase_time = datetime.utcnow()
        tail_samples = bytes()

        res_text = None

        while True:
            try:
                now = datetime.utcnow()
                if now - phrase_time < timedelta(seconds = 2):
                    time.sleep(0.4)
                    continue

                if not self.data_queue.empty():
                    while not self.data_queue.empty():
                        d = self.data_queue.get();
                        tail_samples += d

                    audio_data = sr.AudioData(
                        tail_samples,
                        self.mic_source.SAMPLE_RATE,
                        self.mic_source.SAMPLE_WIDTH
                    )
                    wav = io.BytesIO(audio_data.get_wav_data())

                    with open(self.queue_tmpfile, 'w+b') as f:
                        f.write(wav.read())

                    qr = self.whisper_model.transcribe(self.queue_tmpfile, fp16=torch.cuda.is_available())
                    tmp_text = qr['text'].strip()

                    if len(tmp_text) == 0 or tmp_text == ".":
                        break
                    elif tmp_text == "Thanks for watching!" or tmp_text == "Thank you.":
                        if res_text != None:
                            break
                        tail_samples = bytes()
                        phrase_time = now
                        continue

                    print(tmp_text)
                    wav = io.BytesIO(audio_data.get_wav_data())
                    with open(self.stt_tmpfile, 'a+b') as f:
                        f.write(wav.read())

                else:
                    r = self.whisper_model.transcribe(self.stt_tmpfile, fp16=torch.cuda.is_available())
                    res_text = r['text'].strip()
                    if res_text == None or len(res_text) > 0:
                        stop(wait_for_stop = True)
                        f = open(self.stt_tmpfile, 'w+b')
                        f.close()
                        return res_text   

                tail_samples = bytes()
                phrase_time = now
            except KeyboardInterrupt:
                return "exit"
            except:
                tail_samples = bytes()
                phrase_time = now
                continue

        stop(wait_for_stop = True)
        r = self.whisper_model.transcribe(self.stt_tmpfile, fp16=torch.cuda.is_available())
        res_text = r['text'].strip()
        f = open(self.stt_tmpfile, 'w+b')
        f.close()
        return res_text            

    def speak_text(self, t):
        if self.lang == "en":
            self.tts.tts_to_file(text=t, speaker=self.voice_id, file_path=self.tts_tmpfile)
        elif self.lang == "zh":
            self.tts.tts_to_file(text="，" + t + "。", file_path=self.tts_tmpfile)

        w = wave.open(self.tts_tmpfile, "rb")
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