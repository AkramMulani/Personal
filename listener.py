import threading

import numpy as np
import speech_recognition as sr

import commands
import pyaudio


class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.commands = commands.Commands()
        self.listening = False
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100,
                                      input=True, frames_per_buffer=1024)

    def listen(self):
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand you."
        except sr.RequestError:
            return "Sorry, there was an error with the service."

    def respond(self, text):
        print("Response:", text)  # Replace with your own response mechanism
        self.commands.handle_gui_commands(text)

    def get_voice_level(self):
        return np.frombuffer(self.stream.read(1024), dtype=np.int16)

    def start(self):
        if not self.listening:
            self.listening = True
            self.thread = threading.Thread(target=self.listen_loop)
            self.thread.start()

    def stop(self):
        self.listening = False
        self.thread.stop()

    def listen_loop(self):
        while self.listening:
            text = self.listen()
            if text:
                self.respond(text)
