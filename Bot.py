import os
import re

import csv
import json

import aiohttp
import asyncio
import datetime 
import requests

import discord
from typing import List
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
        
class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y + 1)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view 
        state = view.board[self.y][self.x]

        if state in (view.X, view.O):
            return await interaction.response.send_message("This Position Is Already Occupied!", ephemeral=True)

        current_player_id = view.players[view.current_player_index].id

        if interaction.user.id != current_player_id:
            return await interaction.response.send_message("It's Not Your Turn!", ephemeral=True)

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = view.X
            o = view.players[1]
            content = f"It Is Now {o.mention}'s Turn"
            view.current_player_index = (view.current_player_index + 1) % 2 
            view.current_player = view.O
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            x = view.players[0]
            content = f"It Is Now {x.mention} Turn"
            view.current_player_index = (view.current_player_index + 1) % 2 
            view.current_player = view.X

        self.disabled = True
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                x = view.players[0]
                content = f"{x.mention} Won ! Congratulations !"

            elif winner == view.O:
                o = view.players[1]
                content = f"{o.mention} Won ! Congratulations !"

            else:
                content = "Damnn ! It's A Tie !"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    X = -1
    O = 1
    Tie = 2

    def __init__(self, challenger: discord.Member, opponent: discord.Member):
        super().__init__()
        self.players = [challenger, opponent]
        self.current_player_index = 0
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for row in self.board:
            if row.count(row[0]) == len(row) and row[0] != 0:
                return row[0]

        for col in range(len(self.board)):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != 0:
                return self.board[0][col]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != 0:
            return self.board[0][2]

        for row in self.board:
            if 0 in row:
                return None

        return self.Tie


class ChallengeView(discord.ui.View):
    def __init__(self, challenger: discord.Member, opponent: discord.Member):
        super().__init__()
        self.challenger = challenger
        self.opponent = opponent

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

    @discord.ui.button(label='Accept', style=discord.ButtonStyle.success)
    async def accept_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Challenge Accepted !", ephemeral=True)
        game = TicTacToe(self.challenger, self.opponent)
        await interaction.message.edit(content=f"Tic Tac Toe: {self.challenger.mention} Goes First !", view=game)

    @discord.ui.button(label='Decline', style=discord.ButtonStyle.danger)
    async def decline_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Challenge Declined !", ephemeral=True)
        self.stop()


@bot.slash_command(name="tictactoe", description="Challenge Another Player To Play Tic Tac Toe")
async def tictactoe(ctx: commands.Context, opponent: discord.Member):
    challenger = ctx.author
    if opponent == ctx.author:
        return await ctx.respond("You Cannot Challenge Yourself!")

    await ctx.respond(f"Challenging {opponent.mention} To Play Tic Tac Toe!", ephemeral=True)
    challenge_message = await ctx.send(f"{opponent.mention}, You Have Been Challenged By {challenger.mention} To Play Tic Tac Toe!", view=ChallengeView(challenger, opponent))

    def check(reaction, user):
        return user == opponent and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == challenge_message.id

    game = TicTacToe(challenger, opponent)
    await challenge_message.edit(content=f"Tic Tac Toe: {challenger.mention} goes first!", view=game)

bot.load_extension('Cogs.AI')
bot.load_extension('Cogs.Fun')
bot.load_extension('Cogs.AFK')
bot.load_extension('Cogs.Help')
bot.load_extension('Cogs.Anime')
bot.load_extension('Cogs.Utils')
bot.load_extension('Cogs.Movie')
bot.load_extension('Cogs.Emotes')
bot.load_extension('Cogs.Reminder')
bot.load_extension('Cogs.Translate')
bot.load_extension('Cogs.Moderation')
bot.load_extension('Cogs.Information')
bot.load_extension('Cogs.Entertainment')

bot.run('TOKEN')

