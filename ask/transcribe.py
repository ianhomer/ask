import os
import time
import readline
import threading
from typing import Optional
import re

running = False

excludes = [r"\([^\)]*\)", r"\[[^\]]*\]"]


def stop_transcribe():
    global running
    running = False


def register_transcribed_text(transcribe_filename) -> Optional[threading.Thread]:
    global running
    if os.path.exists(transcribe_filename):
        transcribe_thread = threading.Thread(
            target=transcribe_worker, args=(transcribe_filename,)
        )
        running = True
        transcribe_thread.start()
        return transcribe_thread
    return None


def transcribe_worker(transcribe_filename):
    global running
    if os.path.exists(transcribe_filename):
        with open(transcribe_filename, "r") as file:
            file.seek(0, 2)
            while running:
                line = transcribe_filter(file.read())
                if line:
                    readline.insert_text(line)
                    readline.redisplay()
                time.sleep(1)


def transcribe_filter(raw_line):
    line = raw_line.strip()
    if len(line) == 0:
        return None
    for pattern in excludes:
        if re.match(pattern, line):
            return None

    return line
