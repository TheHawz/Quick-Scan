"""Set de utilidades para la gestion de ficheros
Ficheros temporales, ficheros del proyecto, crear y borrar carpetas

"""
import os
import numpy as np


def save_np_to_txt(data, path, file_name="data.txt"):
    file_path = os.path.join(path, file_name)
    np.savetxt(file_path, data)


def check_for_existance(path) -> tuple:
    """Checks for existance of a file or a dir
    If it is a dir => True
    If not => check for file => return that

    Args:
        path ([str]): Path to the desired file or dir

    Returns:
        bool: Whether it exist or not
        bool: if it is a file or not (it is a dir)
    """
    isdir = os.path.isdir(path)
    if isdir:
        return isdir, False

    isfile = os.path.isfile(path)
    if isfile:
        return isfile, True

    return False, None


def check_for_empty(path: str) -> bool:
    '''
    Check if a Directory is empty and also check exceptional situations.
    '''
    if os.path.exists(path) and os.path.isdir(path):
        if os.listdir(path):
            return False
    return True


def mkdir(path):
    exists, _ = check_for_existance(path)

    try:
        if not exists:
            os.makedirs(path)
            return True, ''
        else:
            return True, ''
    except Exception as e:
        return False, str(e)


def touch(path, override=False):
    exists, isfile = check_for_existance(path)

    if exists and override:
        raise Exception
