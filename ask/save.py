import datetime
import os
import webbrowser

from .parse import parse

work_directory = "/tmp/ask"


def save(response_text):
    now = datetime.datetime.now()

    datestamp = now.strftime("%Y%m%d-%H%M%S")
    filename = f"{datestamp}.txt"

    if not os.path.exists(work_directory):
        os.makedirs(work_directory)

    with open(f"{work_directory}/{filename}", "w") as file:
        file.write(response_text)

    parts = parse(response_text)
    if len(parts) > 0:
        type_counts = {}
        for part in parts:
            type = part[0]
            if type not in type_counts:
                type_counts[type] = 0
            else:
                type_counts[type] += 1
            part_filename = f"{work_directory}/{datestamp}-{type_counts[type]}.{type}"
            with open(part_filename, "w") as file:
                file.write(part[1])

            if type == "html":
                webbrowser.open(f"file://{part_filename}", new=0, autoraise=False)
