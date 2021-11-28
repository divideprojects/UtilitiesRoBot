"""Initialise this directory."""

from .bincheckerbot import bincheckerbot_app
from .fakeinfofenrobot import fakeinfogenbot_app
from .itsproxybot import itsproxybot_app
from .sessiongenbot import stringgenbot_app

bot_list = [
    bincheckerbot_app,
    fakeinfogenbot_app,
    itsproxybot_app,
    stringgenbot_app,
]
