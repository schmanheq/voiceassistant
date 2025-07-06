# silence_alsa.py
import ctypes
from ctypes import c_char_p, c_int, CFUNCTYPE

# C prototype:  void handler(const char *file, int line,
#                            const char *function, int err, const char *fmt, …)
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def _py_error_handler(file, line, func, err, fmt):
    # do nothing → swallow the message
    pass

c_error_handler = ERROR_HANDLER_FUNC(_py_error_handler)

asound = ctypes.CDLL("libasound.so")
asound.snd_lib_error_set_handler(c_error_handler)#!/usr/bin/env python3
"""
voicerecognition.py – non-blocking speech recogniser
────────────────────────────────────────────────────
* Opens the mic once
* Runs SpeechRecognition’s listener thread
* Prints every phrase it recognises
"""

import queue
import signal
import sys
import speech_recognition as sr

# ───── 1  SETUP ──────────────────────────────────────────────────────────────
AUDIO_QUEUE = queue.Queue()          # recogniser thread → main thread

r = sr.Recognizer()
MIC_INDEX = 3                    # ← change to the index you verified earlier
mic = sr.Microphone(device_index=MIC_INDEX)

print("Calibrating…")
with mic as src:                     # one open/close only
    r.adjust_for_ambient_noise(src, duration=1)
print("Done.  Waiting for speech…")

# ───── 2  BACKGROUND LISTENER ────────────────────────────────────────────────
def _callback(_, audio: sr.AudioData):
    """This runs in a separate thread; just queue the data."""
    AUDIO_QUEUE.put(audio)

stop_listening = r.listen_in_background(mic, _callback)
# (It returns immediately – the thread is now collecting audio.)

# ───── 3  MAIN LOOP ──────────────────────────────────────────────────────────
def transcribe_loop():
    while True:
        audio = AUDIO_QUEUE.get()    # blocks until the callback puts data in
        try:
            text = r.recognize_google(audio)
            print("●", text)
        except sr.UnknownValueError:
            print("…couldn’t understand that")
        except sr.RequestError as e:
            print("API failure:", e)

# ───── 4  CLEAN EXIT ON CTRL-C ───────────────────────────────────────────────
def _handle_sigint(sig, frame):
    print("\nStopping listener…")
    stop_listening(wait_for_stop=False)
    sys.exit(0)

signal.signal(signal.SIGINT, _handle_sigint)

# kick everything off
if __name__ == "__main__":
    transcribe_loop()

