import os
import eel
from backend.commands import *
from backend.feature import *

def start():
    eel.init("frontend")

    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=True)


