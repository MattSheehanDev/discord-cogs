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
        messageUrl = reaction.message.jump_url
        messageTimestamp = reaction.message.created_at

        messageContent = reaction.message.content
        messageEmbeds = reaction.message.embeds
        messageAttachments = reaction.message.attachments


        config: dict = await self.config.all_channels()

        # Only apply to channels that are in the config and have been enabled
        if reaction.message.channel.id not in config:
            return

        if not config[reaction.message.channel.id]["enabled"]:
            return

        guild_conf: dict = await self.config.guild(reaction.message.guild).get_raw()

        # for key in guild_conf:
        #     await reaction.message.channel.send(f'{key}: {guild_conf[key]}')

        emojiId: str | int = guild_conf["dank_emoji"]
        emojiCount: int = guild_conf["dank_count"]
        hallOfFame: int = guild_conf["dank_hall"]
        responses: list = guild_conf["responses"]

        if reactionId == emojiId and reactionCount == emojiCount:
            # Choose a random response to reply to the message with
            res: str = random.choice(responses)

            # Send reploy to the certified dank post
            await reaction.message.reply(res)

            # Get the "hall of fame" channel
            channel = self.bot.get_channel(hallOfFame)

            # Create the embed object
            embed = discord.Embed(title="Certified Dank")
            embed.set_author(name=f"{authorName}", icon_url=str(authorAvatar))
            embed.add_field(name="Channel", value=messageChannel.name, inline=True)
            embed.add_field(name="Emoji", value=f"{emojiId}", inline=True)

            date = messageTimestamp.strftime("%Y/%m/%d")
            embed.add_field(name="Date", value=f"{date}", inline=True)

            embed.add_field(name="Content", value=f"{messageUrl}", inline=False)

            # If the certified dank post is not a post with an embed of attachment
            # then it is probably not a meme post, just text.
            if len(messageEmbeds) == 0 and len(messageAttachments) == 0:
                await channel.send(embed=embed)
                return

            # If there is an embed as part of the post, take the first one
            if len(messageEmbeds) >= 1:
                em = messageEmbeds[0]
                embed.add_field(name="Content", value=f"{messageUrl}", inline=False)
                embed.set_thumbnail(url=f"{em.url}")
                await channel.send(embed=embed)
                await channel.send(f"{em.url}")
                return

            # If there is an attachement as part of the post, take the first one
            if len(messageAttachments) >= 1:
                a = messageAttachments[0]
                embed.add_field(name="Content", value=f"{messageUrl}", inline=False)
                embed.set_thumbnail(url=f"{a.url}")
                await channel.send(embed=embed)
                await channel.send(f"{a.url}")
                return
