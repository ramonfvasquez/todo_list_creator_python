from datetime import datetime


def log(function):
    def inner(*args):
        file = open("./tools/log.txt", "a")
        file.write(f"{str(datetime.now())} {function(*args)}\n")

    return inner
