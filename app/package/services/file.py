"""Set de utilidades para la gestion de ficheros
Ficheros temporales, ficheros del proyecto, crear y borrar carpetas

"""
import os


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


def mkdir(path):
    exists, isfile = check_for_existance(path)

    if not exists:
        os.mkdir(path)

    if isfile:
        raise Exception('This path already exists. And its a file')
