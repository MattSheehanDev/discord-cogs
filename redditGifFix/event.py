from __future__ import annotations
from typing import TYPE_CHECKING
from .abc import MixinMeta

if TYPE_CHECKING:
    import discord
    
import random
from datetime import datetime, timedelta

from redbot.core import commands

class EventMixin(MixinMeta):
    __slots__: tuple = ()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        #config: dict = await self.config.all_channels()
        #if message.channel.id not in config:
        #    return
		
        msg: str = message.content.lower()
        newMsg = ""
        if "preview.redd.it" in msg:
            newMsg = msg.replace("preview.redd.it", "i.redd.it")
            message.channel.createMessage(newMsg)
            print("GREAT SCOTT")
            print(newMsg)
        print("FAILURE")
		