#
# cogs/text/meme.py
#
# mawabot - Maware's selfbot
# Copyright (c) 2017 Ma-wa-re, Ammon Smith
#
# mawabot is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

''' Has commands for meme-y text transformation '''
import asyncio
import logging
import random
import re
import subprocess

import discord
from discord.ext import commands

__all__ = [
    'Meme',
]

CHECK_EM_URL = 'https://media.discordapp.net/attachments/336147052855558148/357986515030376458/check-em.jpg'
BAD_CHECK_EM_URL = 'https://cdn.discordapp.com/attachments/287311630880997377/332092380738224128/raw.gif'
OFF_BY_ONE_URL = 'https://cdn.discordapp.com/attachments/336147052855558148/357987379283361802/0d6.png'

DISCORD_STRINGS = re.compile(r'(<\S*>)')

logger = logging.getLogger(__name__)

class Meme:
    __slots__ = (
        'bot',
        'recent_messages',
        'regional_emojis',
    )

    def __init__(self, bot):
        self.bot = bot
        self.recent_messages = set()
        self.regional_emojis = {
            'a': '\N{REGIONAL INDICATOR SYMBOL LETTER A}',
            'b': '\N{REGIONAL INDICATOR SYMBOL LETTER B}',
            'c': '\N{REGIONAL INDICATOR SYMBOL LETTER C}',
            'd': '\N{REGIONAL INDICATOR SYMBOL LETTER D}',
            'e': '\N{REGIONAL INDICATOR SYMBOL LETTER E}',
            'f': '\N{REGIONAL INDICATOR SYMBOL LETTER F}',
            'g': '\N{REGIONAL INDICATOR SYMBOL LETTER G}',
            'h': '\N{REGIONAL INDICATOR SYMBOL LETTER H}',
            'i': '\N{REGIONAL INDICATOR SYMBOL LETTER I}',
            'j': '\N{REGIONAL INDICATOR SYMBOL LETTER J}',
            'k': '\N{REGIONAL INDICATOR SYMBOL LETTER K}',
            'l': '\N{REGIONAL INDICATOR SYMBOL LETTER L}',
            'm': '\N{REGIONAL INDICATOR SYMBOL LETTER M}',
            'n': '\N{REGIONAL INDICATOR SYMBOL LETTER N}',
            'o': '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
            'p': '\N{REGIONAL INDICATOR SYMBOL LETTER P}',
            'q': '\N{REGIONAL INDICATOR SYMBOL LETTER Q}',
            'r': '\N{REGIONAL INDICATOR SYMBOL LETTER R}',
            's': '\N{REGIONAL INDICATOR SYMBOL LETTER S}',
            't': '\N{REGIONAL INDICATOR SYMBOL LETTER T}',
            'u': '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
            'v': '\N{REGIONAL INDICATOR SYMBOL LETTER V}',
            'w': '\N{REGIONAL INDICATOR SYMBOL LETTER W}',
            'x': '\N{REGIONAL INDICATOR SYMBOL LETTER X}',
            'y': '\N{REGIONAL INDICATOR SYMBOL LETTER Y}',
            'z': '\N{REGIONAL INDICATOR SYMBOL LETTER Z}',
            '0': '0\N{COMBINING ENCLOSING KEYCAP}',
            '1': '1\N{COMBINING ENCLOSING KEYCAP}',
            '2': '2\N{COMBINING ENCLOSING KEYCAP}',
            '3': '3\N{COMBINING ENCLOSING KEYCAP}',
            '4': '4\N{COMBINING ENCLOSING KEYCAP}',
            '5': '5\N{COMBINING ENCLOSING KEYCAP}',
            '6': '6\N{COMBINING ENCLOSING KEYCAP}',
            '7': '7\N{COMBINING ENCLOSING KEYCAP}',
            '8': '8\N{COMBINING ENCLOSING KEYCAP}',
            '9': '9\N{COMBINING ENCLOSING KEYCAP}',
            '!': '\N{HEAVY EXCLAMATION MARK SYMBOL}',
            '?': '\N{BLACK QUESTION MARK ORNAMENT}',
        }

        self.bot.add_listener(self.on_message)

    async def on_message(self, message):
        ''' Handling for text-based messages '''

        if message.id in self.recent_messages:
            return
        else:
            self.recent_messages.add(message.id)
            if len(self.recent_messages) > 10:
                self.recent_messages.pop()

        if message.author == self.bot.user and message.content == 'oh no.':
            logger.info(f"Sending 'oh no.' for {message.id}")
            await self._ohno(message.channel)

    def _regional_indicators(self, text, big=False):
        ''' Helper that formats input text into regional indicators '''

        # Note, can't pass in sep directly, causes a TypeError
        # Something else is probably passing something called sep in automatically
        sep = ' ' if big else '\u200b'
        def mapper(s):
            if s.startswith('<'):
                return s
            return sep.join(self.regional_emojis.get(c.lower(), c) for c in s)

        return ''.join(map(mapper, DISCORD_STRINGS.split(text)))

    @commands.command(aliases=['ri'])
    async def regional_indicators(self, ctx, *, text: str):
        ''' Makes the whole message into regional_indicator emojis '''

        content = self._regional_indicators(text)
        await asyncio.gather(
                ctx.send(content=content),
                ctx.message.delete(),
                )

    @commands.command(aliases=['ril'])
    async def regional_indicators_large(self, ctx, *, text: str):
        ''' Same as regional_indicators except the letters come out larger '''

        content = self._regional_indicators(text, big=True)
        await asyncio.gather(
                ctx.send(content=content),
                ctx.message.delete(),
                )

    @commands.command(aliases=['sw'])
    async def spacewords(self, ctx, *, text: str):
        ''' Spaces out words '''

        content = ' . '.join(' '.join(word) for word in text.split(' '))
        await ctx.message.edit(content=content)

    @commands.command(aliases=['cw'])
    async def crossword(self, ctx, *, text: str):
        ''' "Crossword"-ifys the given text '''

        text = text.upper()
        lines = [text] + list(text[1:])

        await ctx.message.edit(content='\n'.join(lines))

    @commands.command()
    async def kerrhau(self, ctx, *text: str):
        ''' "kerrhau"-ifys the given text '''

        text = list(text)
        words = []

        while text:
            word = []

            for _ in range(random.randint(1, 3)):
                if text:
                    word.append(text.pop(0))

            words.append(' '.join(word))

        last = words[-1][-1]
        words[-1] = words[-1][:-1]
        words.append(last)

        await ctx.message.edit(content='\n'.join(words))

    @commands.command()
    async def clap(self, ctx, *, text: str):
        ''' Replaces spaces with the clap emoji 👏 '''

        content = ' 👏 '.join(text.upper().split())
        await ctx.message.edit(content=content)

    @commands.command()
    async def clap2(self, ctx, *, text: str):
        ''' Clap variant that starts and ends with claps too '''

        content = ''.join(f'👏 {word}' for word in text.upper().split())
        await ctx.message.edit(content=content + ' 👏')

    @staticmethod
    def _cowsay(args, text):
        text = text.replace('\n', '\n\n').replace("```", "'''")
        args.append(text)
        output = subprocess.check_output(args, stderr=subprocess.DEVNULL, timeout=0.5)
        content = '\n'.join((
            '```',
            output.decode('utf-8'),
            '```',
        ))
        return content

    @commands.command()
    async def cowsay(self, ctx, *, text: str):
        ''' Replaces the given text with cowsay '''
        content = self._cowsay(['cowsay'], text)
        await ctx.message.edit(content=content)

    @commands.command()
    async def cowthink(self, ctx, *, text: str):
        ''' Replaces the given text with cowthink '''
        content = self._cowsay(['cowthink'], text)
        await ctx.message.edit(content=content)

    @commands.command()
    async def cowcustom(self, ctx, cowfile: str, *, text: str):
        ''' Replaces the given text with the given cow file '''
        content = self._cowsay(['cowsay', '-f', cowfile], text)
        await ctx.message.edit(content=content)

    @staticmethod
    async def _ohno(sendable):
        ''' oh no. '''
        url = f'https://www.raylu.net/f/ohno/ohno{random.randint(1, 53)}.png'
        embed = discord.Embed().set_image(url=url)
        await sendable.send(embed=embed)

    @commands.command()
    async def ohno(self, ctx):
        ''' Bot command /ohno '''
        await asyncio.gather(
            self._ohno(ctx),
            ctx.message.delete(),
        )

    @staticmethod
    def is_dubs(num):
        return (num % 100) % 11 == 0

    @commands.command(aliases=['dubs', 'trips'])
    async def checkem(self, ctx):
        ''' Check 'em! '''

        number = random.randint(1, 10 ** 16)
        embed = discord.Embed(type='rich', description=f'```{number}```')
        embed.set_footer(
            text='Brought to you by the anti-semitic frog foundation',
            icon_url='https://i.imgur.com/Gn3vKn6.png',
        )

        if self.is_dubs(number):
            embed.set_image(url=CHECK_EM_URL)
        elif self.is_dubs(number + 1) or self.is_dubs(number - 1):
            embed.set_image(url=OFF_BY_ONE_URL)
        else:
            embed.set_image(url=BAD_CHECK_EM_URL)

        await ctx.send(embed=embed)
