import aiohttp
import requests

import discord
from discord.ext import commands


class Entertainment(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="meme", description="Sends A Random Meme")
    async def meme(self, ctx):

        url = "https://meme-api.com/gimme"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                meme_json = await response.json()
                meme_url = meme_json["url"]

                await ctx.respond(meme_url, view=Meme_Refresh())

    @commands.slash_command(name="joke", description="Sends A Random Joke")
    async def joke(self, ctx):

        url = "https://v2.jokeapi.dev/joke/Any"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                joke_json = await response.json()

                setup = joke_json["setup"]
                delivery = joke_json["delivery"]

                embed = discord.Embed(title="Here's A Joke", color=0x00FF00)

                if setup:
                    embed.add_field(name="\u200b", value=setup, inline=False)
                    
                embed.add_field(name="\u200b", value=delivery, inline=False)

                await ctx.respond(embed=embed, view=Joke_Refresh())

    @commands.slash_command(name="quote", description="Sends A Random Quote")
    async def quote(self, ctx):

        url = "https://api.quotable.io/random"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                quote_json = await response.json()

                content = quote_json["content"]
                author = quote_json["author"]

                embed = discord.Embed(
                    title="Here's A Quote", description=content, color=0x00FF00
                )
                embed.add_field(name="Author", value=f"{author}", inline=False)

                await ctx.respond(embed=embed, view=Quote_Refresh())

    @commands.slash_command(name="fact", description="Sends A Random Fact")
    async def fact(self, ctx):

        url = "https://uselessfacts.jsph.pl/random.json?language=en"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                fact_json = await response.json()

                fact = fact_json["text"]

                embed = discord.Embed(
                    title="Here's A Fact", description=fact, color=0x00FF00
                )

                await ctx.respond(embed=embed, view=Fact_Refresh())


# Refresh Buttons


class Meme_Refresh(discord.ui.View):

    def __init__(self):
        super().__init__()

    async def on_timeout(self):
        self.disable_all_items()

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="🔃")
    async def button_callback(self, button, interaction):

        url = "https://meme-api.com/gimme"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                meme_json = await response.json()
                meme_url = meme_json["url"]

                await interaction.response.edit_message(content=meme_url, view=self)


class Joke_Refresh(discord.ui.View):

    def __init__(self):
        super().__init__()

    async def on_timeout(self):
        self.disable_all_items()

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="🔃")
    async def button_callback(self, button, interaction):

        
        url = "https://v2.jokeapi.dev/joke/Any"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                joke_json = await response.json()

                setup = joke_json["setup"]
                delivery = joke_json["delivery"]

                embed = discord.Embed(title="Here's A Joke", color=0x00FF00)

                if setup:
                    embed.add_field(name="\u200b", value=setup, inline=False)

                embed.add_field(name="\u200b", value=delivery, inline=False)

                await interaction.response.edit_message(embed=embed, view=self)


class Quote_Refresh(discord.ui.View):

    def __init__(self):
        super().__init__()

    async def on_timeout(self):
        self.disable_all_items()

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="🔃")
    async def button_callback(self, button, interaction):

        url = "https://api.quotable.io/random"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                quote_json = await response.json()

                content = quote_json["content"]
                author = quote_json["author"]

                embed = discord.Embed(
                    title="Here's A Quote", description=content, color=0x00FF00
                )
                embed.add_field(name="Author", value=f"{author}", inline=False)

                await interaction.response.edit_message(embed=embed, view=self)


class Fact_Refresh(discord.ui.View):

    def __init__(self):
        super().__init__()

    async def on_timeout(self):
        self.disable_all_items()

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="🔃")
    async def button_callback(self, button, interaction):

        url = "https://uselessfacts.jsph.pl/random.json?language=en"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                fact_json = await response.json()

                fact = fact_json["text"]

                embed = discord.Embed(
                    title="Here's A Fact", description=fact, color=0x00FF00
                )

                await interaction.response.edit_message(embed=embed, view=self)


# COG Setup


def setup(bot):
    bot.add_cog(Entertainment(bot))
