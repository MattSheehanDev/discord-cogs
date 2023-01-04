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

        }
        default_guild: Dict[str, Any] = {
            "dank_enabled": True,
            "dank_emojis": [
                963153387048829009
            ],
            "dank_count": 1,
            "dank_hall": 966164843222671410,
            "responses": [
                "Certified Dank!"
            ],
            "blacklist": [

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
    async def channelDankHallCount(self, ctx: commands.Context, channel_id: int, dankhall_id: int, count: int) -> None:
        """Change the Hall-of-Fame channel where messages are re-posted (server config)."""
        # channel = channel_id
        # if type(channel_id) == int:
        channel = ctx.guild.get_channel(channel_id)

        # # dankhall = dankhall_id
        # # if type(dankhall_id) == int:
        # dankhall = ctx.guild.get_channel(dankhall_id)
        
        await self.config.channel(channel).set_raw("dank_hall", value=dankhall_id)
        await self.config.channel(channel).set_raw("dank_count", value=count)
        print(f"----------------")
        print(f"CHANNEL CONFIG CHANNEL: {channel}", file=sys.stderr)
        print(f"CHANNEL CONFIG HALL: {dankhall_id}", file=sys.stderr)
        print(f"CHANNEL CONFIG COUNT: {count}", file=sys.stderr)
        print(f"----------------")
        await ctx.tick()


    @certifiedDankAdmin.command()
    async def addBlacklist(self, ctx: commands.Context, channel: int) -> None:
        """Append given channel to the black list."""
        async with self.config.guild(ctx.guild).blacklist() as blacklist:
            if channel in blacklist:
                await ctx.send("That channel is already blacklisted.")
                return
            blacklist.append(channel)
        await ctx.tick()

    @certifiedDankAdmin.command()
    async def removeBlacklist(self, ctx: commands.Context, channel: int) -> None:
        """Remove given channel from the black list."""
        async with self.config.guild(ctx.guild).blacklist() as blacklist:
            if channel not in blacklist:
                await ctx.send("That channel doesn't exists in the blacklist.")
                return
            blacklist.remove(channel)
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
    

    @commands.group()
    @commands.mod_or_permissions()
    @commands.guild_only()
    async def certifiedDankDebug(self, ctx: commands.Context) -> None:
        """Gets the debug commands for certifiedDank cog."""
        pass

    @certifiedDankDebug.command()
    async def clearAllChannelConfigs(self, ctx: commands.Context) -> None:
        """Clear all channel configs"""
        await self.config.clear_all_channels()
        print(f"Channel configs cleared : {self.config.get_raw()}", file=sys.stderr)
        await ctx.tick()

    # @certifiedDankAdmin.command()
    # async def emoji(self, ctx: commands.Context, *, emoji: str) -> None:
    #     """Add an emoji to the emojis list for the current channel."""
    #     try:
    #         emote: discord.Emoji = await commands.EmojiConverter().convert(ctx=ctx, argument=emoji)
    #     except:
    #         if emojis.count(emoji) > 1:
    #             await ctx.send("Please provide one emoji only.")
    #             return
    #         emote: list = list(emojis.get(emoji))
        
    #     if not emote or emote is None:
    #         await ctx.send("Couldn't find any emoji, please retry.")
    #         return

    #     if isinstance(emote, discord.Emoji):
    #         await self.config.guild(ctx.guild).set_raw("dank_emoji", value=emote.id)
    #     else:
    #         await self.config.guild(ctx.guild).set_raw("dank_emoji", value=emote[0])

    #     await ctx.tick()

    @certifiedDankAdmin.command()
    async def addEmoji(self, ctx: commands.Context, *, emoji: str) -> None:
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

        async with self.config.guild(ctx.guild).dank_emojis() as dank_emojis:
            emote_id = None
            if isinstance(emote, discord.Emoji):
                emote_id = emote.id
            else:
                emote_id = emote[0]

            if emote_id in dank_emojis:
                await ctx.send("That emoji already exists in the list.")
                return
            dank_emojis.append(emote_id)

        await ctx.tick()

    @certifiedDankAdmin.command()
    async def removeEmoji(self, ctx: commands.Context, *, emoji: str) -> None:
        """Remove an emoji to the emojis list for the current channel."""
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

        async with self.config.guild(ctx.guild).dank_emojis() as dank_emojis:
            emote_id = None
            if isinstance(emote, discord.Emoji):
                emote_id = emote.id
            else:
                emote_id = emote[0]

            if emote_id not in dank_emojis:
                await ctx.send("That emoji does not exists in the list.")
                return
            dank_emojis.remove(emote_id)

        await ctx.tick()