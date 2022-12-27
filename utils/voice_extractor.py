from __future__ import unicode_literals
from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json 
import difflib
from hazm import *
import librosa
import soundfile as sf
import noisereduce as nr



class VoiceAnalsis:

    def __init__(self, voice_path):
        self.voice_path = voice_path
        self._noise_reducer()

    def extract_text_from_voice(self):

        wf = wave.open(self.voice_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print ("Audio file must be WAV format mono PCM.")
            return False

        model = Model("model")
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                rec.Result()
            else:
                rec.PartialResult()

        return json.loads(rec.FinalResult())['text']

    def is_match_with_text(self,text):
        voice_text = self.extract_text_from_voice()
        normalizer = Normalizer()
        voice_text = ' '.join(normalizer.normalize(voice_text).replace(u'\u200c','').split())
        text = ' '.join(normalizer.normalize(text).replace(u'\u200c','').split())
        seq=difflib.SequenceMatcher(None, voice_text,text)
        return round(seq.ratio(),4)


    def _noise_reducer(self):
        data, rate = librosa.load(self.voice_path)
        noisy_part = data[:]
        reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, verbose=False)
        sf.write(self.voice_path.replace('.wav','.denoise.wav'), reduced_noise, rate)
        self.voice_path = self.voice_path.replace('.wav','.denoise.wav')

