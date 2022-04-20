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


class certifiedDank(EventMixin, commands.Cog, metaclass=CompositeClass):
    """certifiedDank"""

    def __init__(self, bot: Red):
        self.bot: Red = bot
        self.config: Config = Config.get_conf(
            self, identifier=2091831, force_registration=True)

        default_channel: Dict[str, Any] = {
            "enabled": False,
        }
        default_guild: Dict[str, int] = {
            "dank_emoji": 963153387048829009,
            "dank_count": 1,
        }
        self.config.register_channel(**default_channel)
        self.config.register_guild(**default_guild)
