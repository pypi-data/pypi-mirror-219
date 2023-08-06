"""
My self bot!
Current implementation of GustavSelfBot includes chat logs and commands.
TODO: make custom command and hooks possible
"""

__version__ = "0.0.8"

import os

from GustavSelfBot.__logging__ import *
from GustavSelfBot.__config__ import Config
from GustavSelfBot.__bot__ import bot

log.info("Main module loaded!")

if Config["token"] == "":
    log.error("No token provided!")
    raise Exception("No token provided!")

try:
    os.makedirs("_chatlogs", exist_ok=True)
except (FileNotFoundError, IOError, PermissionError) as e:
    log.error(f"Could not create _chatlogs folder: {e}")
    raise Exception(f"Could not create _chatlogs folder: {e}")
