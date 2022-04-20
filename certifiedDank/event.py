from __future__ import annotations
from typing import TYPE_CHECKING, final
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
        # await reaction.message.channel.send("Emoji reaction detected.")

        reactionId = reaction.emoji.id
        reactionCount = reaction.emoji.count

        if reactionId is None:
            await reaction.message.channel.send("Message reaction Id does not exist")
        
        if reactionCount is None:
            await reaction.message.channel.send("Message reaction count does not exist")

        config: dict = await self.config.all_channels()

        # Only apply to enabled channels
        if reaction.message.channel.id not in config:
            await reaction.message.channel.send("Config not found.")
            return

        if not config[reaction.message.channel.id]["enabled"]:
            await reaction.message.channel.send("Config found but not enabled.")
            return

        await reaction.message.channel.send("Configuration found")

        try:
            guild_conf: dict = await self.config.guild(reaction.message.guild).get_raw()

            # await reaction.message.channel.send("Configuration read")

            # for key in guild_conf:
            #     await reaction.message.channel.send(f'{key}: {guild_conf[key]}')

            reaction.message.channel.send(str(reactionId))
            reaction.message.channel.send(str(reactionCount))

            emojiId: int = guild_conf["dank_emoji"]
            emojiCount: int = guild_conf["dank_count"]

            # reaction.message.channel.send(f'emojiId: {emojiId} , emojiCount: {emojiCount}')

            if reactionId == emojiId:
                if reactionCount == emojiCount:
                    await reaction.message.reply("Certified Dank!")

        except discord.Forbidden:
            await reaction.message.channel.send("I don't have the permissions to add a reaction")
        except discord.NotFound:
            await reaction.message.channel.send("Didn't add the emoji, couldn't find it.")
        except discord.HTTPException:
            await reaction.message.channel.send("Error while trying to add the emoji.")
        finally:
            reaction.message.channel.send("Unknown error.")
