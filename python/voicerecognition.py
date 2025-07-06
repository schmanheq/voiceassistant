import pvporcupine
import pyaudio
import struct
import speech_recognition as sr
import sys
import signal
import time
from credentials import  Credentials
from myDesk import toggle

# ───── 1  SETUP PORCUPINE AND SPEECHRECOGNITION ──────────────────────────────────────────────────────────────
for i,mic in enumerate(sr.Microphone.list_microphone_names()):
    if mic=='capture':
        MIC_INDEX = i
    else:
        exit
        
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

print("Calibrating…")
with mic as src:                     # one open/close only
    r.adjust_for_ambient_noise(src, duration=1)
print("Done.  Activate with keyword")

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
        with mic as source:
            # Listen for up to 5 seconds
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio)
            if "table" in text:
                toggle("Anhs Tisch")
            print(text)
        except sr.UnknownValueError:
            print("…couldn’t understand that")
        except sr.RequestError as e:
            print("API failure:", e)

        print("Waiting for wake word...")

