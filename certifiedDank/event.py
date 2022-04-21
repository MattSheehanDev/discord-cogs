from __future__ import annotations
from typing import TYPE_CHECKING, final
from .abc import MixinMeta

# if TYPE_CHECKING:
#     import discord

import random
import emojis
import discord
from redbot.core import commands


class EventMixin(MixinMeta):
    __slots__: tuple = ()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user) -> None:
        # await reaction.message.channel.send("Emoji reaction detected.")

        reactionId = reaction.emoji
        if not isinstance(reactionId, str):
            reactionId = reaction.emoji.id
        
        reactionCount = reaction.count
        messageAuthor = reaction.message.author
        authorName = messageAuthor.display_name
        authorMention = messageAuthor.mention
        authorAvatar = messageAuthor.avatar_url
        messageChannel = reaction.message.channel

        messageContent = reaction.message.content
        messageEmbeds = reaction.message.embeds
        messageAttachments = reaction.message.attachments

        # if reactionId is None:
        #     await reaction.message.channel.send("Message reaction Id does not exist")

        # if reactionCount is None:
        #     await reaction.message.channel.send("Message reaction count does not exist")

        config: dict = await self.config.all_channels()

        # Only apply to enabled channels
        if reaction.message.channel.id not in config:
            # await reaction.message.channel.send("Channel id not found in config")
            return

        if not config[reaction.message.channel.id]["enabled"]:
            # await reaction.message.channel.send("Config not enabled for channel.")
            return

        # await reaction.message.channel.send("Configuration found")

        # try:
        guild_conf: dict = await self.config.guild(reaction.message.guild).get_raw()

        # await reaction.message.channel.send("Configuration read")

        # for key in guild_conf:
        #     await reaction.message.channel.send(f'{key}: {guild_conf[key]}')

        # await reaction.message.channel.send(str(reactionId))
        # await reaction.message.channel.send(str(reactionCount))

        emojiId: str | int = guild_conf["dank_emoji"]
        emojiCount: int = guild_conf["dank_count"]
        hallOfFame: int = guild_conf["dank_hall"]
        responses: list = guild_conf["responses"]

        # await reaction.message.channel.send(f'emojiId: {emojiId} , reactionId: {reactionId}')

        # emote: discord.Emoji = await commands.EmojiConverter().convert(ctx=await self.bot.get_context(reaction.message), argument=str(emojiId))

        # reaction.message.channel.send(f'emojiId: {emote.id} , reactionId: {reactionId}')

        if reactionId == emojiId:
            if reactionCount == emojiCount:
                res: str = random.choice(responses)

                await reaction.message.reply(res)
                channel = self.bot.get_channel(hallOfFame)
                # await reaction.message.channel.send("Hall of fame channel found")

                # await reaction.message.channel.send(f"Embedded images: {len(messageEmbeds)}")
                # await reaction.message.channel.send(f"Attached images: {len(messageAttachments)}")

                msg = f"""{str(authorAvatar)} {authorMention}
Channel: {messageChannel.name}
Emoji: {emojiId}"""

                if len(messageEmbeds) == 0 and len(messageAttachments) == 0:
                    msg += f"""
{messageContent}"""
                    await channel.send(msg)
                    return

                if len(messageEmbeds) >= 1:
                    em = messageEmbeds[0]

                    msg += f"""
{em.url}"""
                    await channel.send(msg)
                    # await reaction.message.channel.send(em.url)

                    # embedFile = discord.Embed(title=em.title,url=em.url)
                    # embedFile.set_image(em.url)
                    # await channel.send(msg, embed=em)
                    # await channel.send(embed=messageEmbeds[0])
                    return

                if len(messageAttachments) >= 1:
                    a = messageAttachments[0]

                    msg += f"""
{a.url}"""
                    await channel.send(msg)

                    # embedFile = discord.Embed(title=a.filename,url=a.url)
                    # embedFile.set_image(a.url)
                    # await channel.send(msg, embed=embedFile)
                    # await channel.send(files=messageAttachments)
                    return

                    # except discord.Forbidden:
                    #     await reaction.message.channel.send("I don't have the permissions to add a reaction")
                    # except discord.NotFound:
                    #     await reaction.message.channel.send("Didn't add the emoji, couldn't find it.")
                    # except discord.HTTPException:
                    #     await reaction.message.channel.send("Error while trying to add the emoji.")
                    # finally:
                    #     await reaction.message.channel.send("Unknown error.")
