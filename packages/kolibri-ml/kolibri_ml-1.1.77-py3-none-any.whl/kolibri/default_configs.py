from kdmt.path import is_writable
import os
import sys
from kolibri.config_loader import parse_config

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

_settings=parse_config(os.path.join(__location__,"settings.yaml"))
KOLIBRI_DATA_FOLDER = _settings['data']['KOLIBRI_DATA_FOLDER']

RESOURCES_AUTO_DOWNLOAD = os.getenv('RESOURCES_AUTO_DOWNLOAD') or str(_settings['data']['RESOURCES_AUTO_DOWNLOAD'])
RESOURCES_AUTO_DOWNLOAD=RESOURCES_AUTO_DOWNLOAD.lower()=="true"


######################################################################
# data Path
######################################################################

DATA_PATH = []
"""A list of directories where packages from the Kolibri data are downloaded."""

# User-specified locations:
_paths_from_env = os.environ.get("KOLIBRI_DATA_PATH", "").split(os.pathsep)
DATA_PATH += [d for d in _paths_from_env if d]
if "APPENGINE_RUNTIME" not in os.environ and os.path.expanduser("~/") != "~/":
    DATA_PATH.append(os.path.expanduser("~/.kolibri"))

if sys.platform.startswith("win"):
    # Common locations on Windows:
    DATA_PATH += [
        os.path.join(sys.prefix, ".kolibri"),
        os.path.join(sys.prefix, "share", ".kolibri"),
        os.path.join(sys.prefix, "lib", ".kolibri"),
        os.path.join(os.environ.get("APPDATA", "C:\\"), ".kolibri"),
        r"C:\.kolibri",
        r"D:\.kolibri",
        r"E:\.kolibri",
    ]
else:
    # Common locations on UNIX & OS X:
    DATA_PATH += [
        os.path.join(sys.prefix, ".kolibri"),
        os.path.join(sys.prefix, "share", ".kolibri"),
        os.path.join(sys.prefix, "lib", ".kolibri"),
        "/usr/share/.kolibri",
        "/usr/local/share/.kolibri",
        "/usr/lib/.kolibri",
        "/usr/local/lib/.kolibri",
    ]

if KOLIBRI_DATA_FOLDER is None:

    for kolibridir in DATA_PATH:
        if os.path.exists(kolibridir) and is_writable(kolibridir):
                KOLIBRI_DATA_FOLDER= kolibridir

    # On Windows, use %APPDATA%
    if sys.platform == "win32" and "APPDATA" in os.environ:
        homedir = os.environ["APPDATA"]

    # Otherwise, install in the user's home directory.
    else:
        homedir = os.path.expanduser("~/")
        if homedir == "~/":
            raise ValueError("Could not find a default download directory")

        # append ".kolibri" to the home directory
    if os.getenv('KOLIBRI_DATA_FOLDER') =="":
        KOLIBRI_DATA_FOLDER= os.path.join(homedir, ".kolibri")
    else:
        KOLIBRI_DATA_FOLDER=os.path.join(os.getenv('KOLIBRI_DATA_FOLDER'), ".kolibri")

    os.environ['KOLIBRI_DATA_PATH'] = KOLIBRI_DATA_FOLDER


LOG_NAME = os.getenv('LOG_NAME') or _settings['logs']['LOG_NAME']
LOG_LEVEL = os.getenv('LOG_LEVEL') or _settings['logs']['LOG_LEVEL']
LOG_TO_FILE=os.getenv('LOG_TO_FILE') or str(_settings['logs']['LOG_TO_FILE'])
LOG_TO_FILE=LOG_TO_FILE.lower()=="true"

LOGS_DIR = os.path.join(KOLIBRI_DATA_FOLDER, 'logs')
if LOG_TO_FILE:
    if not os.path.exists(LOGS_DIR):
        try:
            os.mkdir(LOGS_DIR)
        except:
            LOG_TO_FILE=False
            pass

DEFAULT_NN_MODEL_FILENAME=os.getenv('DEFAULT_NN_MODEL_FILENAME') or _settings['neural_networks']['DEFAULT_NN_MODEL_FILENAME']
EMBEDDING_SIZE = os.getenv('EMBEDDING_SIZE') or _settings['neural_networks']['EMBEDDING_SIZE']


if os.getenv('Kolibri_DOWNLOAD_URL') is not None:
    os.environ['Kolibri_DOWNLOAD_URL']=_settings['data']['Kolibri_DOWNLOAD_URL']

DEFAULT_SEED=os.getenv('DEFAULT_SEED') or _settings['misc']['DEFAULT_SEED']
TARGET_RANKING_LENGTH = os.getenv('TARGET_RANKING_LENGTH') or _settings['misc']['TARGET_RANKING_LENGTH']

