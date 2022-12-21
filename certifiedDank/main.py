from __future__ import annotations
from typing import Any, Dict, List, TYPE_CHECKING
from abc import ABCMeta

if TYPE_CHECKING:
    from redbot.core.bot import Red

import sys
import emojis
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
            "blacklist": [],
        }
        default_guild: Dict[str, Any] = {
            "dank_enabled": True,
            "dank_emoji": 963153387048829009,
            "dank_count": 1,
            "dank_hall": 966164843222671410,
            "responses": [
                "Certified Dank!"
            ]
        }
        self.config.register_channel(**default_channel)
        self.config.register_guild(**default_guild)

    @commands.group()
    @commands.mod_or_permissions()
    @commands.guild_only()
    async def certifiedDankAdmin(self, ctx: commands.Context) -> None:
        """Gets the admin commands for certifiedDank cog."""
        pass

    @certifiedDankAdmin.command()
    async def enable(self, ctx: commands.Context, true_or_false: bool) -> None:
        """Enable / Disable the reaction system for the current guild."""
        print(f"GUILD ID: {ctx.guild.id}", file=sys.stderr)
        await self.config.guild(ctx.guild).set_raw("dank_enabled", value=true_or_false)
        await ctx.tick()

    @certifiedDankAdmin.command()
    async def count(self, ctx: commands.Context, count: int) -> None:
        """Change the number (count) of the emoji required for trigger (server config)."""
        await self.config.guild(ctx.guild).set_raw("dank_count", value=count)
        await ctx.tick()

    @certifiedDankAdmin.command()
    async def dankhall(self, ctx: commands.Context, id: int) -> None:
        """Change the Hall-of-Fame channel where messages are re-posted (server config)."""
        await self.config.guild(ctx.guild).set_raw("dank_hall", value=id)
        await ctx.tick()

    @certifiedDankAdmin.command()
    async def blacklist(self, ctx: commands.Context, channel: int) -> None:
        """Black list the reaction system for the given channel."""
        blacklist = await self.config.channel(ctx.channel).get_raw("blacklist")
        blacklist.append(channel)
        await self.config.channel(ctx.channel).set_raw("blacklist", value=blacklist)
        await ctx.tick()

    @certifiedDankAdmin.command()
    async def addResponse(self, ctx: commands.Context, res: str) -> None:
        """Add certified dank response."""
        async with self.config.guild(ctx.guild).responses() as responses:
            if res in responses:
                await ctx.send("That response already exists in the list.")
                return
            responses.append(res)

        await ctx.tick()

    @certifiedDankAdmin.command()
    async def removeResponse(self, ctx: commands.Context, res: str) -> None:
        """Remove certified dank response."""
        async with self.config.guild(ctx.guild).responses() as responses:
            if res not in responses:
                await ctx.send("That response doesn't exists in the list.")
                return
            responses.remove(res)

        await ctx.tick()

    @certifiedDankAdmin.command()
    async def emoji(self, ctx: commands.Context, *, emoji: str) -> None:
        """Add an emoji to the emojis list for the current channel."""
        try:
            emote: discord.Emoji = await commands.EmojiConverter().convert(ctx=ctx, argument=emoji)
        except:
            if emojis.count(emoji) > 1:
                await ctx.send("Please provide one emoji only.")
                return
            emote: list = list(emojis.get(emoji))
        
        if not emote or emote is None:
            await ctx.send("Couldn't find any emoji, please retry.")
            return

        if isinstance(emote, discord.Emoji):
            await self.config.guild(ctx.guild).set_raw("dank_emoji", value=emote.id)
        else:
            await self.config.guild(ctx.guild).set_raw("dank_emoji", value=emote[0])

        await ctx.tick()
