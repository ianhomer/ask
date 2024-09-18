import os
import time
import threading
from typing import Optional
import re
from .input import prompt_session
from typing import List

running = False

# whisper generates descriptions of sounds (in square or round brakects) and
# sometimes generates random words. We can filter these out since they have
# limited value for this chat bot context.
excludes = [
    r"^\([^\)]+\)$",
    r"^\[[^\]]+\]$",
    r"^\*[^\*]+\*$",
    r"^thank you[\.]?$",
    r"^you[\.]?$",
    r"^yeah[\.]?$",
    r"^\.+$",
    r"^\.$",
]


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
    last_line = None
    if os.path.exists(transcribe_filename):
        with open(transcribe_filename, "r") as file:
            file.seek(0, 2)
            loops_before_submit = 0
            line_inserted = False
            while running:
                if prompt_session.app.is_running:
                    current_buffer = prompt_session.app.current_buffer
                    chunk = transcribe_filter(file.read())
                    if chunk:
                        for line in chunk.split("\n"):
                            if line != last_line:
                                line_inserted = True
                                loops_before_submit = 4
                                current_buffer.insert_text(" " + line)
                                last_line = line
                    if line_inserted:
                        if loops_before_submit < 1:
                            if len(current_buffer.text) > 0:
                                current_buffer.validate_and_handle()
                                line_inserted = False
                            else:
                                print("X" + current_buffer.text + "X")
                        else:
                            loops_before_submit -= 1
                time.sleep(0.5)


def filter_single_line(raw_line) -> Optional[str]:
    line = raw_line.strip()
    for pattern in excludes:
        if re.match(pattern, line, re.IGNORECASE):
            return None
    return line


def transcribe_filter(raw_line):
    lines: List[str] = [
        line
        for line in [filter_single_line(line) for line in raw_line.split("\n")]
        if line
    ]
    if len(lines) == 0:
        return None

    return "\n".join(lines)
