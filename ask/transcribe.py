import os
import time
import readline
import threading
from typing import Optional
import re
from keyboard import press

running = False

excludes = [r"^\([^\)]*\)$", r"^\[[^\]]*\]$", r"^thank you[\.]?$", r"^\.$"]


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
            loops_before_submit = 4
            line_inserted = False
            while running:
                line = transcribe_filter(file.read())
                if line:
                    loops_before_submit = 4
                    line_inserted = True
                    readline.insert_text(" " + line)
                    readline.redisplay()
                if line_inserted:
                    if loops_before_submit < 1:
                        if len(readline.get_line_buffer()) > 0:
                            readline.insert_text("\n")
                            readline.redisplay()
                        line_inserted = False
                    else:
                        loops_before_submit -= 1
                time.sleep(0.5)


def transcribe_filter(raw_line):
    line = raw_line.strip()
    if len(line) == 0:
        return None
    line_lower = line.lower()
    for pattern in excludes:
        if re.match(pattern, line_lower):
            return None

    return line
