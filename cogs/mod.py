#!/usr/bin/env python
from discord.ext import commands
import discord
from cogs.util.checks import manage_usrs

class Mod:
    """Moderation Commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @manage_usrs()
    async def ban(self, ctx, *, mention: str):
        """Bans a user. 
        
        You must provide a mention for the bot to ban."""
        to_ban = None
        if ctx.message.mentions:
            to_ban = ctx.message.mentions[0]
        else:
            await ctx.send(':warning: You did not mention a user to ban.')
            return

        await ctx.message.guild.ban(to_ban)
        await ctx.send(':white_check_mark: Successfully banned user {}#{}'\
                            .format(to_ban.name, to_ban.discriminator))

    @commands.command()
    @manage_usrs()
    async def kick(self, ctx, *, mention: str):
        """Kicks a user. 
        
        You must provide a mention for the bot to kick."""
        to_kick = None
        if ctx.message.mentions:
            to_kick = ctx.message.mentions[0]
        else:
            await ctx.send(':warning: You did not mention a user to kick.')
            return

        await ctx.message.kick(to_kick)
        await ctx.send(':white_check_mark: Successfully kicked user {}#{}'\
                            .format(to_kick.name, to_kick.discriminator))


def setup(bot):
    bot.add_cog(Mod(bot))