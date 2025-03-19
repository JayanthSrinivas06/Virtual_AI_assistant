import multiprocessing
import atexit
import threading
from backend.commands import *
from backend.feature import *
from playsound import playsound

MUSIC_DIR = "Notifs/open.mp3"
MUSIC_CLOSE = "Notifs/closing.mp3"

def sound():
       playAssistantSound(MUSIC_DIR)


def startNeils():
        print("Process 1 is running.")
        from main import start
        start()


def listenHotword():
        print("Process 2 is running.")
        from backend.feature import hotword
        hotword()


def playClosingSound():
    playsound(MUSIC_CLOSE)


def on_exit():
    closing_thread = threading.Thread(target=playClosingSound)
    closing_thread.start()
    closing_thread.join()


if __name__ == "__main__":
        atexit.register(on_exit)

        sound_thread = multiprocessing.Process(target=playAssistantSound, args=(MUSIC_DIR,))
        p1 = multiprocessing.Process(target=startNeils)
        p2 = multiprocessing.Process(target=listenHotword)

        sound_thread.start()
        time.sleep(1)

        p1.start()
        p2.start()
        p1.join()

        if p2.is_alive():
                p2.terminate()
                p2.join()

        print("System stopped.")

