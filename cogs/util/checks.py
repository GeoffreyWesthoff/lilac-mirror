#!/usr/bin/env python
from discord.ext import commands
import yaml

def is_cleared():
    def predicate(ctx: commands.Context):
        config = yaml.load(open('config.yml', 'r'))
        cleared = config['cleared']
        if ctx.message.author.id in cleared:
            return True
        return False
    return commands.check(predicate)

def manage_usrs():
    def predicate(ctx: commands.Context):
        user_perms = ctx.message.author.guild_permissions
        if ctx.message.author.id in ctx.bot.config['cleared']:
            return True
        if user_perms.ban_members and user_perms.kick_members:
            return True
        return False
    return commands.check(predicate)

def manage_guild():
    def predicate(ctx: commands.Context):
        if ctx.message.author.id in ctx.bot.config['cleared']:
            return True
        user_perms = ctx.message.author.guild_permissions
        if user_perms.manage_guild:
            return True
        return False
    return commands.check(predicate)

def manage_roles():
    def predicate(ctx: commands.Context):
        if ctx.message.author.id in ctx.bot.config['cleared']:
            return True
        user_perms = ctx.message.author.guild_permissions
        if user_perms.manage_roles:
            return True
        return False
    return commands.check(predicate)

def manage_messages():
    def predicate(ctx: commands.Context):
        if ctx.message.author.id in ctx.bot.config['cleared']:
            return True
        user_perms = ctx.message.author.guild_permissions
        if user_perms.manage_messages:
            return True
        return False
    return commands.check(predicate)
