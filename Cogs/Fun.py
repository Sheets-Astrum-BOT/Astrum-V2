import random
import aiohttp
import requests

import discord
from urllib.parse import quote
from discord.ext import commands

def get_gif(query):

    api_key = 'AIzaSyBadJ6mJ2zUDmZnQBoXQqjFjy6RFYgnpEc'
    url = f'https://tenor.googleapis.com/v2/search?q={query}&key={api_key}'

    response = requests.get(url)
    data = response.json()

    gif_urls = [entry['media_formats']['gif']['url'] for entry in data['results']]
    random_gif_url = random.choice(gif_urls)

    return random_gif_url


def moviequote():

    url = "https://juanroldan1989-moviequotes-v1.p.rapidapi.com/api/v1/quotes"

    querystring = {"actor":"Al Pacino"}

    headers = {
        "Authorization": "Token token=yd8WzkWNEEzGtqMSgiZBrwtt",
        "X-RapidAPI-Key": "1cd68ddeb1mshb590a11eaf553edp111b0bjsn640bd1591c6c",
        "X-RapidAPI-Host": "juanroldan1989-moviequotes-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name="roll", description="Roll Between Two Numbers")
    async def roll(self, ctx, min: int = 1, max: int = 100):
        if min > max:
            embed = discord.Embed(
                title="Error",
                description="The Minimum Value Can't Be Greater Than The Maximum Value",
                color=0x2F3136,
            )

            await ctx.respond(embed=embed)
            return
        if min == max:
            embed = discord.Embed(
                title=f"The Value Is {min}",
            )
            await ctx.respond(embed=embed)
            return

        embed = discord.Embed(
            title=f"The Value Is {random.randint(min, max)}",
            description=f"Rolled Between {min} And {max}",
            color=0x2F3136,
        )

        await ctx.respond(embed=embed)

    @commands.slash_command(name="coinflip", description="Flip A Coin")
    async def coinflip(self, ctx):
        coin = random.choice(["Heads", "Tails"])
        embed = discord.Embed(title=f"The Coin Landed On {coin}", color=0x2F3136)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="dice", description="Roll A Dice")
    async def dice(self, ctx):
        dice = random.choice([1, 2, 3, 4, 5, 6])
        embed = discord.Embed(title=f"The Dice Landed On {dice}", color=0x2F3136)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="8ball", description="Ask The Magic 8 Ball")
    async def eightball(self, ctx, *, question: str):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        embed = discord.Embed(
            title="Magic 8 Ball",
            description=f"Question: {question}\nAnswer: {random.choice(responses)}",
            color=0x2F3136,
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(name="rps", description="Play Rock Paper Scissors")
    async def rps(self, ctx, choice: str):
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)
        if choice.lower() not in choices:
            embed = discord.Embed(
                title="Error",
                description="Please Choose Rock, Paper, Or Scissors",
                color=0x2F3136,
            )
            await ctx.respond(embed=embed)
            return
        if choice.lower() == bot_choice:
            embed = discord.Embed(
                title="Rock Paper Scissors",
                description=f"Both Chose {choice.capitalize()}, It's A Tie",
                color=0x2F3136,
            )
            await ctx.respond(embed=embed)
            return
        if choice.lower() == "rock":
            if bot_choice == "scissors":
                embed = discord.Embed(
                    title="Rock Paper Scissors",
                    description=f"{ctx.author.mention} Chose Rock, I Chose Scissors, You Win",
                    color=0x2F3136,
                )
                await ctx.respond(embed=embed)
                return
            else:
                embed = discord.Embed(
                    title="Rock Paper Scissors",
                    description=f"{ctx.author.mention} Chose Rock, I Chose Paper, You Lose",
                    color=0x2F3136,
                )
                await ctx.respond(embed=embed)
                return
        if choice.lower() == "paper":
            if bot_choice == "rock":
                embed = discord.Embed(
                    title="Rock Paper Scissors",
                    description=f"{ctx.author.mention} Chose Paper, I Chose Rock, You Win",
                    color=0x2F3136,
                )
                await ctx.respond(embed=embed)
                return
            else:
                embed = discord.Embed(
                    title="Rock Paper Scissors",
                    description=f"{ctx.author.mention} Chose Paper, I Chose Scissors, You Lose",
                    color=0x2F3136,
                )
                await ctx.respond(embed=embed)
                return
        if choice.lower() == "scissors":
            if bot_choice == "paper":
                embed = discord.Embed(
                    title="Rock Paper Scissors",
                    description=f"{ctx.author.mention} Chose Scissors, I Chose Paper, You Win",
                    color=0x2F3136,
                )
                await ctx.respond(embed=embed)
                return
            else:
                embed = discord.Embed(
                    title="Rock Paper Scissors",
                    description=f"{ctx.author.mention} Chose Scissors, I Chose Rock, You Lose",
                    color=0x2F3136,
                )
                await ctx.respond(embed=embed)

    @commands.slash_command(
        name="moviequote", description="Get A Random Quote From A Movie"
    )
    async def moviequote(self, ctx):

        api_url = "https://api.seriesquotes.10cyrilc.me/pic/solid?background_color=black&text_color=white&text_size=200&x=3600&y=2400"

        embed = discord.Embed(title="Random Movie Quote", color=0xFF5733)
        embed.set_image(url=api_url)

        await ctx.respond(embed=embed)

    @commands.slash_command(name="customquote", description="Generate A Random Quote")
    async def customquote(self, ctx, text: str):

        encoded_text = quote(text)

        api_url = f'https://api.seriesquotes.10cyrilc.me/pic/custom?text_color=&background_color=&text="{encoded_text}"&x=3600&y=2400'

        embed = discord.Embed(title="Random Quote", color=0xFF5733)
        embed.set_image(url=api_url)

        embed.set_footer(text=f"Quote By : {ctx.author.display_name}")

        await ctx.respond(embed=embed)

    @commands.slash_command(name="gif", description="Search For A Gif")
    async def gif(self, ctx, query: str):

        gif_url = get_gif(query)

        await ctx.respond(gif_url, view=GIF_Refresh(query))

    @commands.slash_command(name="roast", description="Roast A User")
    async def roast(self, ctx, user: discord.Member):

        url = "https://insult.mattbas.org/api/insult"

        response = requests.get(url)
        insult = response.text

        if ctx.author == user:

            embed = discord.Embed(
                title="Yo Mama Roast",
                description=f"{ctx.author.mention} Roasted Themselves\n\n### {insult}\n\nYou Alyaws Get Something New To Learn Daily",
                color=0xFF5733,
            )

            roast_gif = get_gif('anime_laugh')

            embed.set_image(url=roast_gif)
            embed.set_footer(text="Ouch, Did It Hurt ?")

            await ctx.respond(embed=embed)
            return
        
        if ctx.author.id == 849178172556705793:

            embed = discord.Embed(
                title="What A Noob Trying To Roast ?",
                description=f"The Bot Roasted <@849178172556705793>\n\n### {insult}",
                color=0xFF5733,
            )

            roast_gif = get_gif('aime_laugh')

            embed.set_image(url=roast_gif)
            embed.set_footer(text="Ouch, Did It Hurt ?")

            await ctx.respond(embed=embed)
            return

        if ctx.author.id == 727012870683885578:
                
                embed = discord.Embed(
                    title="Yo Mama Roast",
                    description=f"## The Lord Roasted\n\n### {insult}",
                    color=0xFF5733,
                )
    
                roast_gif = get_gif('anime_laugh')
    
                embed.set_image(url=roast_gif)
                embed.set_footer(text="Ouch, Did It Hurt ?")
    
                await ctx.respond(embed=embed)
                return

        else:

            embed = discord.Embed(
                title="Yo Mama Roast",
                description=f"{ctx.author.mention} Roasted {user.mention}\n\n### {insult}",
                color=0xFF5733,
            )

            roast_gif = get_gif('aime_roast')

            embed.set_image(url=roast_gif)
            embed.set_footer(text="Ouch, Did It Hurt ?")

            await ctx.respond(f'{user.mention}',embed=embed)

class GIF_Refresh(discord.ui.View):

    def __init__(self, query):
        super().__init__()
        self.query = query

    async def on_timeout(self):
        self.disable_all_items()

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="🔃")
    async def button_callback(self, button, interaction):

        api_key = 'AIzaSyBadJ6mJ2zUDmZnQBoXQqjFjy6RFYgnpEc'
        url = f'https://tenor.googleapis.com/v2/search?q={self.query}&key={api_key}'

        response = requests.get(url)
        data = response.json()

        gif_urls = [entry['media_formats']['gif']['url'] for entry in data['results']]
        random_gif_url = random.choice(gif_urls)

        await interaction.response.edit_message(content=random_gif_url, view=self)

def setup(bot):
    bot.add_cog(Fun(bot))
