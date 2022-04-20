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
        if reaction.emoji.id == 963153387048829009:
            if reaction.emoji.count == 5:
                await reaction.message.reply("Certified Dank!")
