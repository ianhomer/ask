import os
import re
import threading
import time
from typing import List, Optional

running = False

# whisper generates descriptions of sounds (in square or round brakects) and
# sometimes generates random words. We can filter these out since they have
# limited value for this chat bot context.
excludes = [
    r"^\([^\)]+\)$",
    r"^\*[^\*]+\*$",
    r"^all right[\.]?$",
    r"^thank you[\.]?$",
    r"^you[\.]?$",
    r"^yeah[\.]?$",
    r"^\.+$",
    r"^\.$",
]

remove_filters = [
    # Stip out content within square brakets, e.g. timestamps like
    # [00:00:00.000 --> 00:00:02.000]
    r"\[.*\]",
]


def stop_transcribe():
    global running
    running = False


def is_running():
    global running
    return running


def register_transcribed_text(
    transcribe_filename, inputter, loop_sleep: float = 2
) -> Optional[threading.Thread]:
    global running
    if os.path.exists(transcribe_filename):
        transcribe_thread = threading.Thread(
            target=transcribe_worker,
            args=(transcribe_filename, inputter, loop_sleep),
        )
        transcribe_thread.start()
        return transcribe_thread
    return None


def transcribe_worker(transcribe_filename, inputter, loop_sleep):
    global running
    last_line = None
    if os.path.exists(transcribe_filename):
        running = True
        with open(transcribe_filename, "r") as file:
            file.seek(0, 2)
            loops_before_submit = 0
            line_inserted = False
            while running:
                if inputter.is_running():
                    chunk = transcribe_filter(file.read())
                    if chunk:
                        for line in chunk.split("\n"):
                            if line != last_line:
                                line_inserted = True
                                loops_before_submit = 4
                                inputter.write(" " + line)
                                last_line = line
                    if line_inserted:
                        if loops_before_submit < 1:
                            if inputter.has_text():
                                inputter.flush()
                                line_inserted = False
                        else:
                            loops_before_submit -= 1
                time.sleep(loop_sleep)


def filter_single_line(raw_line) -> Optional[str]:
    line = raw_line
    for pattern in remove_filters:
        line = re.sub(pattern, "", line)

    line = line.strip()
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
