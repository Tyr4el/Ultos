import discord
from discord.ext import commands
import aiohttp
import constants
import traceback
import sys
import asyncio
from typing import Dict


class Manga:
    def __init__(self, mal_id, url, image_url, title, publishing, synopsis, manga_type, chapters, volumes, score,
                 start_date,
                 end_date, members):
        self._mal_id = mal_id
        self._url = url
        self._image_url = image_url
        self._title = title
        self._publishing = publishing  # NOT USING
        self._synopsis = synopsis
        self._manga_type = manga_type  # NOT USING
        self._chapters = chapters
        self._volumes = volumes
        self._score = score
        self._start_date = start_date
        self._end_date = end_date
        self._members = members  # NOT USING

    @property
    def mal_id(self):
        return self._mal_id

    @mal_id.setter
    def mal_id(self, value):
        self._mal_id = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def image_url(self):
        return self._image_url

    @image_url.setter
    def image_url(self, value):
        self._image_url = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def publishing(self):
        return self._publishing

    @property
    def synopsis(self):
        return self._synopsis

    @synopsis.setter
    def synopsis(self, value):
        self._synopsis = value

    @property
    def manga_type(self):
        return self._manga_type

    @property
    def chapters(self):
        return self._chapters

    @chapters.setter
    def chapters(self, value):
        self._chapters = value

    @property
    def volumes(self):
        return self._volumes

    @volumes.setter
    def volumes(self, value):
        self._volumes = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = value

    @property
    def members(self):
        return self._members

    @classmethod
    def from_json(cls, data: Dict) -> 'Manga':
        return cls(
            mal_id=data['mal_id'],
            url=data['url'],
            image_url=data['image_url'],
            title=data['title'],
            publishing=data['publishing'],
            synopsis=data['synopsis'],
            manga_type=data['type'],
            chapters=data['chapters'],
            volumes=data['volumes'],
            score=data['score'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            members=data['members'])


class Anime:
    def __init__(self, mal_id, url, image_url, title, airing, synopsis, anime_type, episodes, score, start_date,
                 end_date, members, rated):
        self._mal_id = mal_id
        self._url = url
        self._image_url = image_url
        self._title = title
        self._airing = airing  # NOT USING
        self._synopsis = synopsis
        self._anime_type = anime_type  # NOT USING
        self._episodes = episodes  # NOT USING
        self._score = score
        self._start_date = start_date  # NOT USING
        self._end_date = end_date  # NOT USING
        self._members = members  # NOT USING
        self._rated = rated  # NOT USING

    @property
    def airing(self):
        return self._airing

    @property
    def anime_type(self):
        return self._anime_type

    @property
    def episodes(self):
        return self._episodes

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def members(self):
        return self._members

    @property
    def rated(self):
        return self._rated

    @property
    def mal_id(self):
        return self._mal_id

    @mal_id.setter
    def mal_id(self, value):
        self._mal_id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def synopsis(self):
        return self._synopsis

    @synopsis.setter
    def synopsis(self, value):
        self._synopsis = value

    @property
    def image_url(self):
        return self._image_url

    @image_url.setter
    def image_url(self, value):
        self._image_url = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def rating(self):
        return self._rated

    @rating.setter
    def rating(self, value):
        self._rated = value

    @property
    def num_episodes(self):
        return self._episodes

    @num_episodes.setter
    def num_episodes(self, value):
        self._episodes = value

    @classmethod
    def from_json(cls, data: Dict) -> 'Anime':
        return cls(
            mal_id=data['mal_id'],
            url=data['url'],
            image_url=data['image_url'],
            title=data['title'],
            airing=data['airing'],
            synopsis=data['synopsis'],
            anime_type=data['type'],
            episodes=data['episodes'],
            score=data['score'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            members=data['members'],
            rated=data['rated'])


class AnimeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Anime
    @commands.command(aliases=['animesearch'])
    @commands.guild_only()
    async def anime(self, ctx, *, anime_name=""):
        """Provides the top 15 search results on MAL for the search query and lets the user select a MAL ID to get more
        information about that anime"""
        if anime_name == "":
            await ctx.send(f"{constants.error_string} Please enter an anime to search for.")
            return
        anime_name_replaced = anime_name.replace(" ", "%20")

        try:
            async with self.bot.session.get(f"https://api.jikan.moe/v3/search/anime/?q={anime_name_replaced}"
                                            f"&page=1&limit=15") as r:
                if r is not None:
                    json = await r.json()
                    animes = {item['mal_id']: Anime.from_json(item) for item in json['results']}
                    joined_names = ""
                    for anime in animes.values():
                        joined_names += f"**{anime.mal_id}** - {anime.title}\n"

                    embed = discord.Embed(
                        title='Search Results',
                        description=f"""**Top 15 Search Results for '{anime_name}'**\n
                                {joined_names}""",
                        color=0x1b39a3
                    )
                    embed.add_field(name="Note", value="If you do not see the anime you were searching for, try "
                                                       "refining your search")
                    embed.add_field(name="\u200B", value="**Enter an ID from the left in 60 seconds to see more about "
                                                         "that title**")

                    await ctx.send(embed=embed)

                    def id_check(m):
                        return m.author == ctx.author and m.channel == ctx.channel and int(m.content) in animes

                    try:
                        msg = await self.bot.wait_for('message', timeout=60.0, check=id_check)
                    # Catch a TimeoutError here
                    except asyncio.TimeoutError:
                        await ctx.send(f"{constants.error_string} Sorry, **{ctx.author.name}**, you took too long.  "
                                       f"Try your search again.")
                    # If the search succeeds
                    else:
                        selected_anime = animes[int(msg.content)]
                        anime_embed = discord.Embed(
                            title="Queried Anime",
                            description=f"**[{selected_anime.title}]({selected_anime.url})**\n\n"
                            f"{selected_anime.synopsis}",
                            color=discord.Colour.red()
                        )
                        anime_embed.add_field(name="Score", value=selected_anime.score, inline=True)
                        anime_embed.add_field(name="# of Episodes", value=selected_anime.episodes, inline=True)
                        anime_embed.add_field(name="Rating", value=selected_anime.rated, inline=True)
                        anime_embed.set_thumbnail(url=selected_anime.image_url)
                        anime_embed.set_footer(text=f"Airing - {selected_anime.start_date} - {selected_anime.end_date}")
                        await ctx.send(embed=anime_embed)
        except aiohttp.ClientConnectorError:
            await ctx.send(f"{constants.error_string} **{ctx.author.name}**, there was a problem with "
                           f"the search or API.  Please try your search again later.")

    # Manga
    @commands.command(aliases=['mangasearch'])
    @commands.guild_only()
    async def manga(self, ctx, *, manga_name=""):
        """Provides the top 15 search results on MAL for the search query and lets the user select a MAL ID to get more
        information about that manga"""
        if manga_name == "":
            await ctx.send(f"{constants.error_string} Please enter a manga to search for.")
            return
        manga_name_replaced = manga_name.replace(" ", "%20")
        try:
            async with self.bot.session.get(f"https://api.jikan.moe/v3/search/manga/?q={manga_name_replaced}"
                                            f"&page=1&limit=15") as r:
                if r is not None:
                    json = await r.json()
                    mangas = {item['mal_id']: Manga.from_json(item) for item in json['results']}
                    joined_names = ""
                    for manga in mangas.values():
                        joined_names += f"**{manga.mal_id}** - {manga.title}\n"

                    embed = discord.Embed(
                        title='Search Results',
                        description=f"""**Top 15 Search Results for '{manga_name}'**\n
                                    {joined_names}""",
                        color=0x1b39a3
                    )
                    embed.add_field(name="Note", value="If you do not see the anime you were searching for, try "
                                                       "refining your search")

                    await ctx.send(embed=embed)
                    await ctx.send(f"{constants.success_string} Search results returned successfully.\n"
                                   f"⚠ | **{ctx.author.name}**, enter an ID from the left to see more about that title")

                    def id_check(m):
                        return m.author == ctx.author and m.channel == ctx.channel and int(m.content) in mangas

                    try:
                        msg = await self.bot.wait_for('message', timeout=60.0, check=id_check)
                    # Catch a TimeoutError here
                    except asyncio.TimeoutError:
                        await ctx.send(f"{constants.error_string} Sorry, **{ctx.author.name}**, you took too long.  "
                                       f"Try your search again.")
                    # If the search succeeds
                    else:
                        selected_manga = mangas[int(msg.content)]
                        manga_embed = discord.Embed(
                            title="Queried Manga",
                            description=f"**[{selected_manga.title}]({selected_manga.url})**\n\n"
                            f"{selected_manga.synopsis}",
                            color=discord.Colour.dark_red()
                        )
                        manga_embed.add_field(name="Score", value=selected_manga.score, inline=False)
                        manga_embed.add_field(name="# of Volumes", value=selected_manga.volumes, inline=True)
                        manga_embed.add_field(name="# of Chapters", value=selected_manga.chapters, inline=True)
                        manga_embed.set_thumbnail(url=selected_manga.image_url)
                        manga_embed.set_footer(text=f"Publishing Dates - {selected_manga.start_date} - "
                        f"{selected_manga.end_date}")
                        await ctx.send(embed=manga_embed)
        except aiohttp.ClientConnectorError:
            await ctx.send(f"{constants.error_string} **{ctx.author.name}**, there was a problem with "
                                   f"the search or API.  Please try your search again later.")


def setup(bot):
    bot.add_cog(AnimeCog(bot))
