from importlib import import_module
from platform import python_version

from Zaa import *
from Zaa.config import *
from Zaa.modules import loadModule
from pyrogram import __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def loadprem():
    modules = loadModule()
    for mod in modules:
        imported_module = import_module(f"Zaa.modules.{mod}")
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                CMD_HELP[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module