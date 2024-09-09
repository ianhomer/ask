import datetime
import os


work_directory = "/tmp/ask"


def save(response):
    now = datetime.datetime.now()
    filename = now.strftime("%Y%m%d-%H%M%S") + ".txt"

    if not os.path.exists(work_directory):
        os.makedirs(work_directory)

    with open(f"{work_directory}/{filename}", "w") as file:
        file.write(response)
