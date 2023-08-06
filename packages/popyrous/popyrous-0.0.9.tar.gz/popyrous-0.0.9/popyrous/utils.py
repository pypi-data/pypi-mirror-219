from pathlib import Path
from datetime import datetime

def make_path(path:str):
    Path.mkdir(Path(path).parent, parents=True, exist_ok=True)
    return path


def autoname(name):
    """
    Genereate a unique name for a file, based on the current time and the given name.
    Gets the `name` as a string and adds the time stamp to the end of it before returning it.
    """
    return name + "_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")