from soco import discover, SoCo
import soco
import time
from spotify_control import search_track_id
from const import Phrases

def fetch_sonos_speaker(speaker_name):
    era300 = speaker_name
    speaker = None
    devices = list(discover())
    for device in devices:
        if device.player_name == era300:
            speaker=SoCo(device.ip_address)
    return speaker

def jarvis(speaker, phrase_input):
    print("_______jarvis Function fired_______")
    phrase = Phrases.phrases[phrase_input]
    uri = phrase['audio_path']
    volume = speaker.volume
    speaker.volume =30
    time.sleep(0.1)
    speaker.play_uri(uri=f"http://192.168.0.111/audio/{uri}")
    time.sleep(phrase['audio_length'])
    speaker.pause()
    speaker.volume = volume


    
def fetch_curr_state(speaker):
    print("_______fetch_curr_state Function fired_______")
    song = speaker.get_current_track_info()
    return song['title'],song['artist'], song['position']

        
def resume(speaker, artist, song, position):
    print("_______resume Function fired_______")
    queue = speaker.get_queue()
    if len(queue)==0:
        library = soco.music_library.MusicLibrary()
        favs = library.get_sonos_favorites(complete_result=True)
        playable = favs[0].reference
        speaker.clear_queue()
        speaker.play_mode = "SHUFFLE"
        speaker.add_to_queue(playable) 
    id = search_track_id(song,artist)

    if id is not None:
    	uri = f"x-sonos-spotify:spotify%3atrack%3a{id}?sid=9&flags=8232&sn=2"
    	index = speaker.add_uri_to_queue(uri,as_next=True)
    	speaker.play_from_queue(index)
    	speaker.seek(position)
    else:
        print("song not found")
        speaker.play_from_queue(0)


def fetch_queue(speaker):
    print("_______ fetch_queue Function fired_______")
    queue = speaker.get_queue(start=0, max_items=10)
    for idx, track in enumerate(queue, start=1):
        print(f"{idx}. {track.title}")
    return 

    
