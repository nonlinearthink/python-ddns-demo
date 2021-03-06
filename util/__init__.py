import os


def check_file(filename):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname) and dirname != "":
        os.makedirs(dirname)
        with open(filename, "w", encoding="utf-8") as f:
            f.write("")
