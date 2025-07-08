from soco import discover, SoCo
import time
from spotify_control import search_track_id

def fetch_sonos_speaker(speaker_name):
    era300 = speaker_name
    speaker = None
    devices = list(discover())
    for device in devices:
        if device.player_name == era300:
            speaker=SoCo(device.ip_address)
            
    return speaker

def wake_up(speaker):
    url_welcome = "http://192.168.0.111/audio/welcomeback.wav"
    volume = speaker.volume
    speaker.volume =50
    speaker.play_uri(uri=url_welcome)
    time.sleep(1)
    speaker.volume = volume
 
def could_not_understand(speaker):
    url_error = "http://192.168.0.111/audio/notunderstand.wav"
    volume = speaker.volume
    speaker.volume =50
    speaker.play_uri(uri=url_error)
    time.sleep(1)
    speaker.volume = volume
    
def fetch_curr_state(speaker):
    song = speaker.get_current_track_info()
    return song['title'],song['artist'], song['position']

def play_song(speaker,artist,song,position):
    id = search_track_id(song,artist)
    uri = f"x-sonos-spotify:spotify%3atrack%3a{id}?sid=9&flags=8232&sn=2"
    speaker.play_uri(uri)
    speaker.seek(position)
    
def fetch_queue(speaker):
    queue = speaker.get_queue()
    print(f"Queue has {len(queue)} items.")
    for idx, track in enumerate(queue, start=1):
        print(f"{idx}. {track.title}")
    