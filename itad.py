import discord
from discord.ext import commands
import aiohttp
import constants
from dataclasses import dataclass
from typing import Dict


@dataclass
class Shop:
    id: str
    name: str

    @classmethod
    def from_json(cls, data: Dict) -> 'Shop':
        return cls(
            id=data['id'],
            name=data['name']
        )


@dataclass
class GameDeal:
    price_new: float
    price_old: float
    price_cut: int
    url: str
    shop: Shop
    drm: str

    @classmethod
    def from_json(cls, data: Dict) -> 'GameDeal':
        return cls(
            price_new=data['price_new'],
            price_old=data['price_old'],
            price_cut=data['price_cut'],
            url=data['url'],
            shop=Shop.from_json(data['shop']),
            drm=data['drm']
        )


class ITADCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: Add functionality for different regions and currencies
    @commands.command()
    @commands.guild_only()
    async def deals(self, ctx, country=None, *, game_name=None):
        if country is None or game_name is None:
            await ctx.send(f"Usage: `$deals <region> <country> <game_name>`")
        else:
            game_name_plain = game_name.replace(" ", "")
            try:
                async with self.bot.session.get(f"https://api.isthereanydeal.com/v01/game/prices/?key="
                                                f"{constants.itad_api_key}&plains={game_name_plain}"
                                                f"&country={country}") as r:
                    if r is not None:
                        json = await r.json()
                        games = {key: value for (key, value) in json['data'].items()}
                        game_embed = discord.Embed(
                            title="Search Results",
                            description=f"Search results for {game_name.capitalize()}",
                            color=discord.Colour.dark_teal()
                        )

                        best_price = min(games[game_name_plain]['list'], key=lambda x: x['price_new'])

                        game_embed.add_field(name=f"{best_price['shop']['name'].capitalize()}",
                                             value=f"Old Price: {best_price['price_old']} \n"
                                             f"New Price: {best_price['price_new']}\n"
                                             f"[Buy]({best_price['url']})",
                                             inline=False)
                        game_embed.add_field(name="\u200b",
                                             value="There may be more stores that have the same price as "
                                                   "this one, but this was the first one returned")
                        await ctx.send(embed=game_embed)
                    else:
                        await ctx.send(f"{constants.error_string} Sorry, I can't find that game.")
            except aiohttp.ClientConnectorError as e:
                await ctx.send(f"{constants.error_string} **{ctx.author.name}**, there was a problem with "
                               f"the search or API.  Please try your search again later.")
                print(e)


def setup(bot):
    bot.add_cog(ITADCog(bot))
