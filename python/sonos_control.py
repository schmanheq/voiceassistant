from soco import discover, SoCo
from soco.exceptions import SoCoUPnPException
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
    phrase = Phrases.phrases[phrase_input]
    uri = phrase['audio_path']
    volume = speaker.volume
    speaker.volume =30
    speaker.play_uri(uri=f"http://192.168.0.111/audio/{uri}")
    time.sleep(phrase['audio_length'])
    speaker.pause()
    speaker.volume = volume


    
def fetch_curr_state(speaker):
    song = speaker.get_current_track_info()
    return song['title'],song['artist'], song['position'], int(song['playlist_position'])

        
def resume(speaker, artist, song, position, playlist_position):
    try:
        speaker.play_from_queue(playlist_position-1)
        speaker.seek(position)
    except SoCoUPnPException as e:
        id = search_track_id(song,artist)
        queue = speaker.get_queue()
        if id is not None:
            uri = f"x-sonos-spotify:spotify%3atrack%3a{id}?sid=9&flags=8232&sn=2"
            speaker.add_uri_to_queue(uri, as_next=True)
            if len(queue)==0:
                library = soco.music_library.MusicLibrary()
                favs = library.get_sonos_favorites(complete_result=True)
                playable = favs[1].reference
                speaker.add_to_queue(playable) 
            speaker.play_from_queue(0)
            speaker.seek(position)
            print("resume: song ID found")

        else:
            library = soco.music_library.MusicLibrary()
            favs = library.get_sonos_favorites(complete_result=True)
            playable = favs[1].reference
            speaker.add_to_queue(playable) 
            speaker.play_from_queue(0)
            print("resume: song ID not found")


def fetch_queue(speaker):
    queue = speaker.get_queue(start=0, max_items=10)
    for idx, track in enumerate(queue, start=1):
        print(f"{idx}. {track.title}")
    return 

    
