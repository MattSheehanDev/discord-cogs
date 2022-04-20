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
            "enabled": True,
        }
        default_guild: Dict[str, int] = {
            "dank_emoji": 963153387048829009,
            "dank_count": 1,
        }
        self.config.register_channel(**default_channel)
        self.config.register_guild(**default_guild)

    @commands.group()
    @commands.mod_or_permissions()
    @commands.guild_only()
    async def emojiadmin(self, ctx: commands.Context) -> None:
        """Gets the admin commands for react emojis cog."""
        pass

    @emojiadmin.command()
    async def enable(self, ctx: commands.Context, true_or_false: bool) -> None:
        """Enable / Disable the reaction system."""
        await self.config.channel(ctx.channel).set_raw("enabled", value=true_or_false)
        await ctx.tick()

    @emojiadmin.command()
    async def emoji(self, ctx: commands.Context, id: int) -> None:
        """Enable / Disable the reaction system."""
        await self.config.guild(ctx.guild).set_raw("dank_emoji", value=id)
        await ctx.tick()

    @emojiadmin.command()
    async def count(self, ctx: commands.Context, count: int) -> None:
        """Enable / Disable the reaction system."""
        await self.config.guild(ctx.guild).set_raw("dank_count", value=count)
        await ctx.tick()
