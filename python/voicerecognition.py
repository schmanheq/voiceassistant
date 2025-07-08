import pvporcupine
import pyaudio
import struct
import speech_recognition as sr
import sys
import signal
import time
from credentials import  Credentials
from myDesk import toggle
from sonos_control import fetch_sonos_speaker, wake_up, could_not_understand, fetch_curr_state, play_song

# ───── 1  SETUP PORCUPINE, SPEECHRECOGNITION, SONOS SPEAKER ──────────────────────────────────────────────────────────────
for i,mic in enumerate(sr.Microphone.list_microphone_names()):
    print(i,mic)
    if mic=='capture':
        MIC_INDEX = i
        break
else:
    sys.exit(1)

        
porcupine = pvporcupine.create(
    access_key=Credentials.porcupine_key,
    keywords=["jarvis"]
)

pa = pyaudio.PyAudio()
stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length,
    input_device_index = MIC_INDEX
)

r = sr.Recognizer()
mic = sr.Microphone(device_index=MIC_INDEX)

speaker_name = "Bedroom"
speaker = fetch_sonos_speaker(speaker_name)
print("Speaker connected")

with mic as src:                     
    r.adjust_for_ambient_noise(src, duration=1)
print("Activate with keyword")

# ───── 3  CLEAN EXIT ON CTRL-C ─────────────────────────────────────────────
def _handle_sigint(sig, frame):
    print("\nStopping...")
    stream.stop_stream()
    stream.close()
    pa.terminate()
    porcupine.delete()
    sys.exit(0)

signal.signal(signal.SIGINT, _handle_sigint)

# ───── 4  MAIN LOOP ─────────────────────────────────────────────────────────
while True:
    # ─ Check wake word in chunks ─
    pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
    pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
    result = porcupine.process(pcm_unpacked)

    if result >= 0:
        print("✓ Wake word detected!")
        song,artist, position = fetch_curr_state(speaker)
        wake_up(speaker)
        with mic as source:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio)
            if "table" in text:
                toggle("Anhs Tisch")
            print(text)
        except sr.UnknownValueError:
            print("…couldn’t understand that")
            could_not_understand(speaker)
        except sr.RequestError as e:
            print("API failure:", e)
        play_song(speaker, artist, song, position)
        print("Waiting for wake word...")

