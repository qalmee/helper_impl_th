import os
from sys import platform as _platform

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = 'my precious'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

STOCKFISH_PATH = ""
print (_platform)

if _platform == "linux" or _platform == "linux2":
    # linux
    STOCKFISH_PATH = "./stockfish_10_x64"
elif _platform == "darwin":
    # MAC OS X
    STOCKFISH_PATH = "stockfish-10-64"   
elif _platform == "win32":
    # Windows
    STOCKFISH_PATH = "stockfish.exe"
elif _platform == "win64":
    # Windows 64-bit
    STOCKFISH_PATH = "stockfish.exe"

def get_stockfish_path():
    global STOCKFISH_PATH
    return STOCKFISH_PATH
