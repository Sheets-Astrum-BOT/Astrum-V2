import requests

import discord
from discord.ext import commands

#  Fun Functions

def meme():
    url = 'https://meme-api.com/gimme'

    response = requests.get(url)
    meme_json = response.json()
    meme_url = meme_json["url"]

    return meme_url


def joke():
    url = 'https://v2.jokeapi.dev/joke/Any'

    response = requests.get(url)
    joke_json = response.json()

    setup = joke_json["setup"]
    delivery = joke_json["delivery"]

    embed = discord.Embed(title="Here's A Joke", color=0x00ff00)
    embed.add_field(name="\u200b", value=setup, inline=False)
    embed.add_field(name="\u200b", value=delivery, inline=False)

    return embed


def quote():
    url = 'https://api.quotable.io/random'

    response = requests.get(url)
    quote_json = response.json()

    content = quote_json["content"]
    author = quote_json["author"]

    embed = discord.Embed(title="Here's A Quote",description=content, color=0x00ff00)
    embed.add_field(name="Author", value=f"{author}", inline=False)

    return embed

def facts():
    url = 'https://uselessfacts.jsph.pl/random.json?language=en'

    response = requests.get(url)
    fact_json = response.json()

    fact = fact_json["text"]

    embed = discord.Embed(title="Here's A Fact", description=fact, color=0x00ff00)

    return embed

# Main Fun COG


class Entertainment(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='meme', description="Sends A Random Meme")
    async def meme(self, ctx):

        meme_url = meme()
        message = await ctx.respond(meme_url, view=Meme_Refresh())

    @commands.slash_command(name='joke', description="Sends A Random Joke")
    async def joke(self, ctx):

        embed = joke()
        await ctx.respond(embed=embed, view=Joke_Refresh())

    @commands.slash_command(name='quote', description="Sends A Random Quote")
    async def quote(self, ctx):

        embed = quote()
        await ctx.respond(embed=embed, view=Quote_Refresh())

    @commands.slash_command(name='fact', description="Sends A Random Fact")
    async def fact(self, ctx):

        embed = facts()
        await ctx.respond(embed=embed, view=Fact_Refresh())


# Refresh Buttons


class Meme_Refresh(discord.ui.View):

    def __init__(self):
        super().__init__()

    async def on_timeout(self):
        self.disable_all_items()

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="🔃")
    async def button_callback(self, button, interaction):

        meme_url = meme()
        await interaction.response.edit_message(content=meme_url, view=self)


class Joke_Refresh(discord.ui.View):

    def __init__(self):
        super().__init__()

    async def on_timeout(self):
        self.disable_all_items()

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="🔃")
    async def button_callback(self, button, interaction):

        embed = joke()
        await interaction.response.edit_message(embed=embed, view=self)


class Quote_Refresh(discord.ui.View):

    def __init__(self):
        super().__init__()

    async def on_timeout(self):
        self.disable_all_items()

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="🔃")
    async def button_callback(self, button, interaction):

        embed = quote()
        await interaction.response.edit_message(embed=embed, view=self)

class Fact_Refresh(discord.ui.View):
    
        def __init__(self):
            super().__init__()
    
        async def on_timeout(self):
            self.disable_all_items()
    
        @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="🔃")
        async def button_callback(self, button, interaction):
    
            embed = facts()
            await interaction.response.edit_message(embed=embed, view=self)

# COG Setup

def setup(bot):
    bot.add_cog(Entertainment(bot))
