import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, "config/secrets.json"), encoding="utf-8") as f:
    secrets = json.loads(f.read())
f.close()

class ImproperlyConfigured(Exception):
    pass


def get_secret(setting: str, secrets=secrets) -> str:
    """
    returns parameter from JSON config file

    :param setting: name of parameter
    :type setting: str
    :param secrets: JSON file with params
    :type secrets: object
    :return:
    """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


def file_name_extension_splitter(filename: str) -> dict:
    """
    This function receives file name and creates a dictionary with parameters related to file

    :param filename: Name of received file
    :type filename: str
    :return: dictionary, that collects all information linked with file
    :rtype: dict
    """
    filename = str(filename)
    file_params = dict()
    if '.' in filename:
        file_params["original_name"] = filename
        file_params["name_without_extension"] = filename.rsplit('.', 1)[0].lower().replace(".", "").replace("(", "").replace(")", "")
        file_params["extension"] = filename.rsplit('.', 1)[1].lower()
    return file_params



def create_dir(path: str) -> None:
    """
    This function receives path and creates a new directory if it wasn`t created earlier

    :param path: dirname with path
    :type path: str
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)