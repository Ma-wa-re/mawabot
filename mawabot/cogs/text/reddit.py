#
# cogs/text/reddit.py
#
# mawabot - Maware's selfbot
# Copyright (c) 2017 Ma-wa-re, Ammon Smith
#
# mawabot is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

''' Has commands that integrate with Reddit '''
import logging

import aiohttp
import discord
from discord.ext import commands

__all__ = [
    'Reddit',
]

logger = logging.getLogger(__name__)

def check_reddit(func):
    async def wrapper(self, ctx):
        if self.bot.config['reddit'] is None:
            content = 'This command requires Reddit integration, but no token was given'
            logger.warning(content)
            await self.bot._send(content)
            return

        await func(self, ctx)
    wrapper.__name__ = func.__name__
    return wrapper

class Reddit:
    __slots__ = (
        'bot',
        'token',
    )

    def __init__(self, bot):
        self.bot = bot
        self.token = None

    def _headers(self):
        assert self.token
        return {'Authorization': f'bearer {self.token}',
                'User-Agent': 'mawabot/1 by aismallard'}

    async def request(self, session, path):
        url = 'https://oauth.reddit.com' + path
        logger.debug(f'Fetching reddit resource: {url}')

        if self.token is None:
            await self.refresh_token(session)

        async with session.get(url, headers=self._headers()) as req:
            if req.status == 401:
                logger.debug('Reddit token out of date, refreshing...')
                await self.refresh_token(session)

                # Try again with new token
                async with session.get(url, headers=self._headers()) as req:
                    req.raise_for_status()
                    data = await req.json()
            else:
                print(req)
                req.raise_for_status()
                data = await req.json()

        return data

    async def refresh_token(self, session):
        logger.info('Getting new Reddit token')
        reddit = self.bot.config['reddit']
        async with session.post('https://www.reddit.com/api/v1/access_token',
                                auth=aiohttp.BasicAuth(reddit['api-id'], reddit['api-secret']),
                                data={'grant_type': 'client_credentials'}) as req:
            req.raise_for_status()
            data = await req.json()
            self.token = data['access_token']

    @commands.command()
    @check_reddit
    async def headpat(self, ctx):
        async with aiohttp.ClientSession() as cs:
            items = await self.request(cs, '/r/headpats/random')
            item = items[0]['data']['children'][0]['data']

        resolutions = item['preview']['images'][0]['resolutions']
        image = resolutions[1]
        image_url = image['url'].replace('&amp;', '&')

        embed = discord.Embed()
        embed.title = item['title']
        embed.url = 'https://www.reddit.com/' + item['permalink']
        embed.set_image(url=image_url)
        embed.image.width = image['width']
        embed.image.height = image['height']

        await ctx.send(embed=embed)
