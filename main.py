#!/usr/bin/env python
from discord.ext import commands
import yaml
import traceback
import discord
import os

class Lilac(commands.Bot):
    """Bot class for Lilac."""

    DATAFILES = [
        'data/welcomes.yml',
        'data/goodbyes.yml',
        'data/autoroles.yml',
        'data/selfroles.yml',
        'data/gblacklist.txt'
    ]

    def __init__(self):
        self.load_files()

        super().__init__(
            command_prefix='l!',
            description='A bot made for moderation, fun, and verifying KnowYourMeme accounts with Discord.'
        )

    def create_data_files(self):
        os.makedirs('data/')
        for file_name in self.DATAFILES:
            open(file_name, 'a').close()

    def load_files(self):
        if not os.path.exists('data/'):
            self.create_data_files()

        if not os.path.exists('config.yml'):
            raise FileNotFoundError('The config.yml file is not present; reclone Lilac.') 

        self.config = {}
        self.welcomes, self.goodbyes = {}, {}
        self.autoroles, self.selfroles = {}, {}
        self.blacklist = list(map(int, [s.strip() for s in open('data/gblacklist.txt')\
                        .readlines()]))
        with open('config.yml', 'r') as config:
            self.config = yaml.load(config)
        with open('data/welcomes.yml', 'r') as welcomes:
            self.welcomes = yaml.load(welcomes)
        with open('data/goodbyes.yml', 'r') as goodbyes:
            self.goodbyes = yaml.load(goodbyes)
        with open('data/autoroles.yml', 'r') as autoroles:
            self.autoroles = yaml.load(autoroles)
        with open('data/selfroles.yml', 'r') as selfroles:
            self.selfroles = yaml.load(selfroles)

    async def on_ready(self):
        """Function executes once bot is ready."""
        print('[INFO] Lilac is ready!')
        print('[INFO] Logged in as {}#{}'.format(self.user.name, self.user.discriminator))

    async def on_command_error(self, ctx, exception):
        """Function executes once bot encounters an error"""
        err = traceback.format_exception(type(exception), exception, \
                                            exception.__traceback__, chain=False)
        err = '\n'.join(err)
        if isinstance(exception, commands.CommandInvokeError):
            exception = exception.original
            if isinstance(exception, discord.Forbidden):
                await ctx.send(':warning: I don\'t have enough perms to do that.')
            else:
                await ctx.send(f':warning: CommandInvokeError: ```{err}``` This should never happen, '+\
                                'please report this to one of the developers.')
        elif isinstance(exception, commands.errors.MissingRequiredArgument):
            fmt_error = ''.join(exception.args)
            await ctx.send(f':warning: {fmt_error}')
        elif isinstance(exception, commands.CommandNotFound):
            await ctx.send(':warning: Command not found.')
        elif isinstance(exception, commands.errors.CheckFailure):
            await ctx.send(':warning: You don\'t have enough perms to perform that action.')
        else:
            await ctx.send(f':warning: An error occured! ```{err}``` This should never happen;'+\
                            ' please report this to one of the developers.')


    async def on_member_join(self, member):
        """Function executes once a member joins a guild."""
        # handle welcome messages
        if member.guild.id in self.welcomes:
            welcome_config = self.welcomes[member.guild.id]

            welcome_channel = None
            if welcome_config[0] is not None:
                welcome_channel = member.guild.get_channel(welcome_config[0])
            else:
                return

            fmt_welcome_message = welcome_config[1].replace('%mention%', member.mention)
            await welcome_channel.send(fmt_welcome_message)
        # handle autoroles
        if member.guild.id in self.autoroles:
            autoroles = self.autoroles[member.guild.id]
            for role_id in autoroles:
                to_add = None
                for role in member.guild.roles:
                    if role.id == role_id:
                        to_add = role
                        print(to_add.name)
                        break

                if to_add:
                    await member.add_roles(to_add)

    async def on_member_remove(self, member):
        if member.guild.id in self.goodbyes:
            goodbye_config = self.goodbyes[member.guild.id]

            goodbye_channel = None
            if goodbye_config[0] is not None:
                goodbye_channel = member.guild.get_channel(goodbye_config[0])
            else:
                return

            fmt_goodbye_message = goodbye_config[1].replace('%name%', member.name)
            await goodbye_channel.send(fmt_goodbye_message)

    async def on_command(self, ctx):
        """Handles on_command event."""
        user_executing = ctx.message.author
        if user_executing.id in self.gblacklist:
            await ctx.send(':warning: You have been blacklisted from using all of Lilac\'s commands!')
            return


    def run(self):
        """Run function for Lilac. Loads cogs and runs the bot."""
        cogs = self.config['cogs']

        for cog in cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                print('[LOAD] Failed to load cog ' + cog)
                print(e)
            else:
                print('[LOAD] Loaded cog {}'.format(cog))

        super().run(self.config['token'])

Bot = Lilac()
Bot.run()

    