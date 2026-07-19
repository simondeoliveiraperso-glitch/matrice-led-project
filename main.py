from config import API_KEY, API_SECRET, USERNAME
import pylast
import threading
import queue
import simulator
import time

song_queue = queue.Queue()

def monitor():
    print("DEBUG: Surveillance Last.fm activée...")
    try:
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
        user = network.get_user(USERNAME)
    except Exception as e:
        print(f"Erreur connexion : {e}")
        return

    last_track_string = None
    while True:
        try:
            current = user.get_now_playing()
            if current:
                track_string = f"{current.artist} - {current.title}"
                if track_string != last_track_string:
                    last_track_string = track_string
                    print(f"DEBUG: Musique -> {track_string}")
                    song_queue.put(("DOWNLOAD", current))
            else:
                if last_track_string is not None:
                    print("DEBUG: Musique arrêtée.")
                    last_track_string = None
                    song_queue.put(("CLEAR", None))
        except Exception as e:
            print(f"Erreur : {e}")
        time.sleep(6)

threading.Thread(target=monitor, daemon=True).start()

if __name__ == "__main__":
    simulator.run_matrix_simulator(song_queue)