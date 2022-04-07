from __future__ import annotations
from typing import Any, Dict, List, TYPE_CHECKING
from abc import ABCMeta

if TYPE_CHECKING:
    from redbot.core.bot import Red

import discord
from redbot.core import Config, commands

from .event import EventMixin

class CompositeClass(commands.CogMeta, ABCMeta):
    __slots__: tuple = ()
    pass

class redditGifFix(EventMixin, commands.Cog, metaclass=CompositeClass):
    """redditGifFix"""
	
    def __init__(self, bot: Red):
        self.bot: Red = bot
#        self.config: Config = Config.get_conf(self, identifier=2091831, force_registration=True)
#        self.config.register_channel(**default_channel)
#        self.config.register_guild(**default_guild)

