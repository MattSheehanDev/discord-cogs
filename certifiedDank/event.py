from __future__ import annotations
from typing import TYPE_CHECKING
from .abc import MixinMeta

if TYPE_CHECKING:
    import discord

from redbot.core import commands


class EventMixin(MixinMeta):
    __slots__: tuple = ()

    # @commands.Cog.listener()
    # async def on_message(self, message: discord.Message) -> None:
    #     if message.author.bot:
    #         return

    #     msg: str = message.content.lower()
    #     if "preview.redd.it" in msg:
    #         newMsg = msg.replace("preview.redd.it", "i.redd.it").split("?")
    #         await message.reply(newMsg[0])

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user) -> None:
        config: dict = await self.config.all_channels()

        # Only apply to enabled channels
        if reaction.message.channel.id not in config:
            return

        if not config[reaction.message.channel.id]["enabled"]:
            return

        guild_conf: dict = await self.config.guild(reaction.message.guild).get_raw()
        emojiId: int = guild_conf["dank_emoji"] or 963153387048829009
        emojiCount: list = guild_conf["dank_count"] or 1

        if reaction.emoji.id == emojiId:
            if reaction.emoji.count == emojiCount:
                await reaction.message.reply("Certified Dank!")
