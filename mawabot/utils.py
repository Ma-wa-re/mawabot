#
# utils.py
#
# mawabot - Maware's selfbot
# Copyright (c) 2017 Ma-wa-re, Ammon Smith
#
# mawabot is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

import logging
import unicodedata

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

COGS_DIR = 'mawabot.cogs.'

__all__ = [
    'Reloader',
    'Wrapper',
    'normalize_caseless',
]

class Reloader:
    __slots__ = (
        'bot',
    )

    def __init__(self, bot):
        self.bot = bot

    def load_cog(self, cogname):
        if COGS_DIR not in cogname:
            cogname = f'{COGS_DIR}{cogname}'
        self.bot.load_extension(cogname)

    def unload_cog(self, cogname):
        if COGS_DIR not in cogname:
            cogname = f'{COGS_DIR}{cogname}'
        self.bot.unload_extension(cogname)

    @commands.command()
    async def load(self, ctx, cogname: str):
        ''' Loads the cog given '''

        logger.info(f'Cog load requested: {cogname}')

        # Load cog
        try:
            self.load_cog(cogname)
        except Exception as error:
            logger.error('Load failed')
            logger.debug('Reason:', exc_info=error)
            embed = discord.Embed(color=discord.Color.red(), description=f'```{error}```')
            embed.set_author(name='Load failed')
            await ctx.send(embed=embed)
        else:
            logger.info(f'Loaded cog: {cogname}')
            embed = discord.Embed(color=discord.Color.green(), description=f'```{cogname}```')
            embed.set_author(name='Loaded')
            await ctx.send(embed=embed)

    @commands.command()
    async def unload(self, ctx, cogname: str):
        ''' Unloads the cog given '''

        logger.info(f'Cog unload requested: {cogname}')

        # Load cog
        try:
            self.unload_cog(cogname)
        except Exception as error:
            logger.error('Unload failed')
            logger.debug('Reason:', exc_info=error)
            embed = discord.Embed(color=discord.Color.red(), description=f'```{error}```')
            embed.set_author(name='Unload failed')
            await ctx.send(embed=embed)
        else:
            logger.info(f'Unloaded cog: {cogname}')
            embed = discord.Embed(color=discord.Color.green(), description=f'```{cogname}```')
            embed.set_author(name='Unloaded')
            await ctx.send(embed=embed)

    @commands.command()
    async def reload(self, ctx, cogname: str):
        ''' Reloads the cog given '''

        logger.info(f'Cog reload requested: {cogname}')

        # Load cog
        try:
            self.unload_cog(cogname)
            self.load_cog(cogname)
        except Exception as error:
            logger.error('Reload failed')
            logger.debug('Reason:', exc_info=error)
            embed = discord.Embed(color=discord.Color.red(), description=f'```{error}```')
            embed.set_author(name='Reload failed')
            await ctx.send(embed=embed)
        else:
            logger.info(f'Reloaded cog: {cogname}')
            embed = discord.Embed(color=discord.Color.green(), description=f'```{cogname}```')
            embed.set_author(name='Reloaded')
            await ctx.send(embed=embed)

    @commands.command()
    async def cogs(self, ctx):
        '''
        List the cogs that are currently loaded
        '''

        lines = ['```yaml\nCogs Loaded:']

        if self.bot.cogs:
            lines.extend(f' - {cog}' for cog in self.bot.cogs)
        else:
            lines.append(' - None')

        lines.append('```')

        await ctx.message.edit(content='\n'.join(lines))

class Wrapper:
    __slots__ = (
        'item',
    )

    def __init__(self, item=None):
        self.item = item

def paginate(text, page_size=5):
    ''' Splits input into page sized chunks '''
    pages = []
    lines = []
    for line in text.splitlines(keepends=True):
        if len(lines) == page_size:
            pages.append(''.join(lines))
            del lines[:]
        lines.append(line)
    if lines:
        pages.append(''.join(lines))
    return pages

def normalize_caseless(s):
    return unicodedata.normalize('NFKD', s.casefold())
