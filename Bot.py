import os
import re

import csv
import json

import aiohttp
import asyncio
import datetime 
import requests

import discord
from discord.ext import commands, tasks

bot = discord.Bot()

# Main BOT Events
        
@bot.event
async def on_ready():
    print(f'======================= ')
    print(f'STATUS : ONLINE')
    print(f'======================= ')
    print(f'BOT : {bot.user}')
    await bot.change_presence(activity=discord.Game(name="With Stars"))

    start_time = datetime.datetime.now()
    bot.start_time = start_time


@bot.slash_command(name='ping', description="Sends Bot's Latency")
async def ping(ctx):

    latency = bot.latency * 1000
    uptime = datetime.datetime.now() - bot.start_time

    uptime_seconds = uptime.total_seconds()
    uptime_str = str(datetime.timedelta(seconds=uptime_seconds)).split(".")[0]

    num_servers = len(bot.guilds)

    embed = discord.Embed(
        title="_*Pong !*_",
        color=0x2f3136
    )

    embed.add_field(name="Uptime", value=uptime_str, inline=False)
    embed.add_field(name="Latency", value=f"{latency:.2f}ms", inline=False)
    embed.add_field(name="Servers", value=num_servers, inline=False)

    await ctx.respond(embed=embed)

@bot.slash_command(name='botinfo', description="Sends Bot's Information")
async def botinfo(ctx):
    embed = discord.Embed(
        title="Bot Information",
        description="Information About The Bot",
        color=0x2f3136
    )

    embed.add_field(name="Bot Name", value=bot.user, inline=False)
    embed.add_field(name="Bot Owner", value="SpreadSheets600", inline=False)
    embed.add_field(name="Bot Created At", value=bot.user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name="Github", value="[Click Here](https://github.com/SpreadSheets600)")

    await ctx.respond(embed=embed, view=Invite())


class Invite(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
        button = discord.ui.Button(
            label='Invite Me',
            style=discord.ButtonStyle.url,
            url='https://discord.com/oauth2/authorize?client_id=1111555652612018246&permissions=8&scope=bot'
        )
        self.add_item(button)

@bot.slash_command()
async def meaning(ctx, word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            first_meaning = data[0]['meanings'][0]
            embed = discord.Embed(title=f"Meaning Of {word.capitalize()}", color=discord.Color.blue())
            embed.add_field(name="Part of Speech", value=first_meaning['partOfSpeech'].capitalize())
            embed.add_field(name="Definition", value=first_meaning['definitions'][0]['definition'], inline=False)
            if 'synonyms' in first_meaning:
                embed.add_field(name="Synonyms", value=", ".join(first_meaning['synonyms']).capitalize(), inline=False)
            if 'example' in first_meaning:
                embed.add_field(name="Example", value=first_meaning['example'], inline=False)
            
            other_meanings = data[0]['meanings'][1:]
            if other_meanings:
                embed.set_footer(text="Click the button for more meanings")
                view = MeaningView(ctx, other_meanings, word)
                await ctx.respond(embed=embed, view=view)
            else:
                await ctx.respond(embed=embed)
        else:
            await ctx.respond(f"No Meaning Found For {word}")
    else:
        await ctx.respond("Failed To Fetch Meaning")

class MeaningView(discord.ui.View):

    def __init__(self, ctx, meanings, word):
        super().__init__()
        self.ctx = ctx
        self.word = word
        self.meanings = meanings
        self.current_meaning_index = 0

    @discord.ui.button(label="Next Meaning", style=discord.ButtonStyle.secondary, custom_id="next_meaning")
    async def button_callback(self, button, interaction):
        self.current_meaning_index = (self.current_meaning_index + 1) % len(self.meanings)
        await self.show_current_meaning()

    async def show_current_meaning(self):
        word = self.word.capitalize()
        meaning = self.meanings[self.current_meaning_index]
        embed = discord.Embed(title=f"Meaning Of {word} ({self.current_meaning_index + 1}/{len(self.meanings)})", color=discord.Color.blue())
        embed.add_field(name="Part Of Speech", value=meaning['partOfSpeech'].capitalize())
        embed.add_field(name="Definition", value=meaning['definitions'][0]['definition'], inline=False)
        if 'synonyms' in meaning:
            embed.add_field(name="Synonyms", value=", ".join(meaning['synonyms']).capitalize(), inline=False)
        if 'example' in meaning:
            embed.add_field(name="Example", value=meaning['example'], inline=False)
        embed.set_footer(text=f"Page {self.current_meaning_index + 1}/{len(self.meanings)}")
        await self.ctx.respond(embed=embed)



bot.load_extension('Cogs.Fun')
bot.load_extension('Cogs.AFK')
bot.load_extension('Cogs.Help')
bot.load_extension('Cogs.Anime')
bot.load_extension('Cogs.Utils')
bot.load_extension('Cogs.Reminder')
bot.load_extension('Cogs.Moderation')
bot.load_extension('Cogs.Information')
bot.load_extension('Cogs.Entertainment')


bot.run('')
