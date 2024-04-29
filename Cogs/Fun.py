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

    @commands.slash_command(name="slap", description="Slap A User")
    async def slap(self, ctx, user: discord.Member):

        slap_gif = get_gif('anime_slap')

        if user == ctx.author:

            embed = discord.Embed(
                title="Slap",
                description=f"You Can't Slap Yourself, Or Wait Can You ? 🤔",
                color=0x2F3136,
            )

            embed.add_field(
                name="Let Me Help You With That", value="\u200b", inline=False
            )

            embed.set_image(url=slap_gif)

            await ctx.respond(embed=embed)
            return

        if user.id == self.bot.user.id:

            embed = discord.Embed(
                title="Slap",
                description=f"{ctx.author.mention} Can't Slap Me, I'm A Bot",
                color=0x2F3136,
            )

            embed.set_image(url=slap_gif )

            await ctx.respond(embed=embed)
            return

        developer = 727012870683885578

        if user.id == developer:
            embed = discord.Embed(
                title="Slap",
                description=f"{ctx.author.mention} You Can't Slap My Developer\n\nHe's The One Who Made Me :D",
                color=0x2F3136,
            )

            embed.add_field(
                name="Let Me Help You With That", value="\u200b", inline=False
            )

            ember = discord.Embed(
                title="Slap",
                description=f"{user.mention} Got An Slap From The Bot",
                color=0x2F3136,
            )

            ember.add_field(name="Damage", value="Infinite", inline=False)

            ember.set_image(url=slap_gif )

            await ctx.respond(embed=embed)
            await ctx.respond(embed=ember)

            return

        else:

            embed = discord.Embed(
                title="Slap",
                description=f"{ctx.author.mention} Slapped {user.mention}",
                color=0x2F3136,
            )
            embed.add_field(
                name="Reason", value="Because They Deserved It", inline=False
            )
            embed.add_field(
                name="Damage", value=f"{random.randint(10,100)}", inline=False
            )

            embed.set_image(url=slap_gif)

            embed.set_footer(text="Did It Hurt ?")

            await ctx.respond(f"{user.mention}", embed=embed)

    @commands.slash_command(name="hug", description="Hug A User")
    async def hug(self, ctx, user: discord.Member):

        hug_gif = get_gif('anime_hug')

        if user == ctx.author:

            embed = discord.Embed(
                title="Hug",
                description=f"{ctx.author.mention} Hugged Themselves",
                color=0x2F3136,
            )

            embed.add_field(
                name="In The Era Of Self Love", value="\u200b", inline=False
            )
            embed.add_field(name="Because They Needed It", value="\u200b", inline=False)
            embed.set_image(url=hug_gif)

            await ctx.respond(embed=embed)
            return

        if user.id == self.bot.user.id:
            embed = discord.Embed(
                title="Hug",
                description=f"{ctx.author.mention} Hugged Me, I'm A Bot",
                color=0x2F3136,
            )
            await ctx.respond(embed=embed)
            return

        developer = 727012870683885578

        if user.id == developer:
            embed = discord.Embed(
                title="Hug",
                description=f"{ctx.author.mention} Hugged My Developer",
                color=0x2F3136,
            )

            embed.add_field(name="Reason", value="Because They Needed It", inline=False)
            embed.set_image(url=hug_gif)

            await ctx.respond(embed=embed)
            return

        else:

            embed = discord.Embed(
                title="Hug",
                description=f"{ctx.author.mention} Hugged {user.mention}",
                color=0x2F3136,
            )
            embed.add_field(name="Reason", value="Because They Needed It", inline=False)
            embed.set_image(url=hug_gif)

            await ctx.respond(embed=embed)

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

        await ctx.respond(gif_url)

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

    @commands.slash_command(name="kill", description="Kills A User")
    async def kill(self, ctx, user: discord.Member):
            
            kill_gif = get_gif('anime_kill')
    
            if user == ctx.author:
    
                embed = discord.Embed(
                    title="Kill",
                    description=f"{ctx.author.mention} Killed Themselves",
                    color=0xFF5733,
                )
    
                embed.add_field(
                    name="In The Era Of Suicide", value="\u200b", inline=False
                )
                embed.add_field(name="Because They Needed To Do It", value="\u200b", inline=False)
                embed.set_image(url=kill_gif)
    
                await ctx.respond(embed=embed)
                return
    
            if user.id == self.bot.user.id:
                embed = discord.Embed(
                    title="Kill",
                    description=f"{ctx.author.mention} Tried To Kill Me, I'm A Bot",
                    color=0xFF5733,
                )
                await ctx.respond(embed=embed)
                return
    
            developer = 727012870683885578
    
            if user.id == developer:
                embed = discord.Embed(
                    title="Kill",
                    description=f"{ctx.author.mention} Tried To Kill My Developer",
                    color=0xFF5733,
                )
    
                embed.add_field(name="What The Hell ?!", value="Sorry He's My Dev\nIf He Dies No One Looks At This Poor Bot TT", inline=False)
    
                await ctx.respond(embed=embed)
                return
    
            else:
    
                embed = discord.Embed(
                    title="Kill",
                    description=f"{ctx.author.mention} Killed {user.mention}",
                    color=0xFF5733,
                )
                embed.add_field(name="Reason", value="Because They Needed To Die", inline=False)
                embed.set_image(url=kill_gif)
    
                await ctx.respond(f'{user.mention}',embed=embed)

    @commands.slash_command(name="simp", description="Simp For A User")
    async def simp(self, ctx, user: discord.Member):
            
            simp_gif = get_gif('anime_simp')
    
            if user == ctx.author:
    
                embed = discord.Embed(
                    title="Simp",
                    description=f"{ctx.author.mention} Simped For Themselves",
                    color=0xFF5733,
                )
    
                embed.add_field(
                    name="In The Era Of Self Love", value="\u200b", inline=False
                )
                embed.add_field(name="Because They Needed It", value="\u200b", inline=False)
                embed.set_image(url=simp_gif)
    
                await ctx.respond(embed=embed)
                return
    
            if user.id == self.bot.user.id:
                embed = discord.Embed(
                    title="Simp",
                    description=f"{ctx.author.mention} Simped For Me, I'm A Bot",
                    color=0xFF5733,
                )
                await ctx.respond(embed=embed)
                return
    
            developer = 727012870683885578
    
            if user.id == developer:
                embed = discord.Embed(
                    title="Simp",
                    description=f"{ctx.author.mention} Simped For My Developer",
                    color=0xFF5733,
                )
    
                embed.add_field(name="Reason", value="Because They Needed It", inline=False)
                embed.set_image(url=simp_gif)
    
                await ctx.respond(embed=embed)
                return
    
            else:
    
                embed = discord.Embed(
                    title="Simp",
                    description=f"{ctx.author.mention} Simped For {user.mention}",
                    color=0xFF5733,
                )
                embed.add_field(name="Reason", value="Because They Needed It", inline=False)
                embed.set_image(url=simp_gif)
    
                await ctx.respond(f'{user.mention}',embed=embed)

    @commands.slash_command(name="pat", description="Pat A User")
    async def pat(self, ctx, user: discord.Member):
            
            pat_gif = get_gif('anime_pat')
    
            if user == ctx.author:
    
                embed = discord.Embed(
                    title="Pat",
                    description=f"{ctx.author.mention} Patted Themselves",
                    color=0xFF5733,
                )
    
                embed.add_field(
                    name="In The Era Of Self Love", value="\u200b", inline=False
                )
                embed.add_field(name="Because They Needed It", value="\u200b", inline=False)
                embed.set_image(url=pat_gif)
    
                await ctx.respond(embed=embed)
                return
    
            if user.id == self.bot.user.id:
                embed = discord.Embed(
                    title="Pat",
                    description=f"{ctx.author.mention} Patted Me, I'm A Bot",
                    color=0xFF5733,
                )
                await ctx.respond(embed=embed)
                return
    
            developer = 727012870683885578
    
            if user.id == developer:
                embed = discord.Embed(
                    title="Pat",
                    description=f"{ctx.author.mention} Patted My Developer",
                    color=0xFF5733,
                )
    
                embed.add_field(name="Reason", value="Because They Needed It", inline=False)
                embed.set_image(url=pat_gif)
    
                await ctx.respond(embed=embed)
                return
    
            else:
    
                embed = discord.Embed(
                    title="Pat",
                    description=f"{ctx.author.mention} Patted {user.mention}",
                    color=0xFF5733,
                )
                embed.add_field(name="Reason", value="Because They Needed It", inline=False)
                embed.set_image(url=pat_gif)
    
                await ctx.respond(f"{user.mention}",embed=embed)

    @commands.slash_command(name="punch", description="Punch A User")
    async def punch(self, ctx, user: discord.Member):
                
        punch_gif = get_gif('anime_punch')

        if user == ctx.author:

            embed = discord.Embed(
                title="Punch",
                description=f"{ctx.author.mention} Punched Themselves",
                color=0xFF5733,
            )

            embed.add_field(
                name="Hmm Is It Possible ?", value="\u200b", inline=False
            )
            embed.add_field(name="Ha They Are Out Of Thier Minds", value="\u200b", inline=False)
            embed.set_image(url=punch_gif)

            await ctx.respond(embed=embed)
            return

        if user.id == self.bot.user.id:
            embed = discord.Embed(
                title="Punch",
                description=f"{ctx.author.mention} Punched Me, I'm A Bot",
                color=0xFF5733,
            )
            await ctx.respond(embed=embed)
            return

        developer = 727012870683885578

        if user.id == developer:
            embed = discord.Embed(
                title="Punch",
                description=f"{ctx.author.mention} Punched My Developer",
                color=0xFF5733,
            )

            embed.add_field(name="Reason", value="Because They Needed It", inline=False)
            embed.set_image(url=punch_gif)

            await ctx.respond(embed=embed)
            return

        else:

            embed = discord.Embed(
                title="Punch",
                description=f"{ctx.author.mention} Punched {user.mention}",
                color=0xFF5733,
            )
            embed.add_field(name="Reason", value="Because They Needed It", inline=False)
            embed.set_image(url=punch_gif)

            await ctx.respond(f"{user.mention}",embed=embed)

    @commands.slash_command(name="murder", description="Murder A User")
    async def murder(self, ctx, user: discord.Member):
        
        murder_gif = get_gif('anime_murder')
        
        if user == ctx.author:
    
                embed = discord.Embed(
                    title="Murder !?",
                    description=f"{ctx.author.mention} Killed Themselves",
                    color=0xFF5733,
                )
    
                embed.add_field(
                    name="In The Era Of Suicide", value="\u200b", inline=False
                )
                embed.add_field(name="Because They Needed To Do It", value="\u200b", inline=False)
                embed.set_image(url=murder_gif)
    
                await ctx.respond(embed=embed)
                return
    
        if user.id == self.bot.user.id:
            embed = discord.Embed(
                title="Murder ?!",
                description=f"{ctx.author.mention} Tried To Murder Me, I'm A Bot",
                color=0xFF5733,
            )
            await ctx.respond(embed=embed)
            return

        developer = 727012870683885578

        if user.id == developer:
            embed = discord.Embed(
                title="Murder ?!",
                description=f"{ctx.author.mention} Tried To Murder My Developer",
                color=0xFF5733,
            )

            embed.add_field(name="What The Hell ?!", value="Sorry He's My Dev\nIf He Dies No One Looks At This Poor Bot TT", inline=False)

            await ctx.respond(embed=embed)
            return

        else:

            embed = discord.Embed(
                title="Murder ?!",
                description=f"{ctx.author.mention} Murdered {user.mention}",
                color=0xFF5733,
            )
            embed.add_field(name="Reason", value="Because They Were Frustrated", inline=False)
            embed.set_image(url=murder_gif)

            await ctx.respond(f'{user.mention}',embed=embed)

    @commands.slash_command(name="bully", description = "Bully A User")
    async def bully(self, ctx, user: discord.Member):

        bully_gif = get_gif("anime_bully")

        if user == ctx.author:
    
                embed = discord.Embed(
                    title="Bully",
                    description=f"{ctx.author.mention} Bullied Themselves\n\n### Wait WTF",
                    color=0xFF5733,
                )
    
                embed.add_field(
                    name="OMFG Save ME !", value="\u200b", inline=False
                )
                embed.add_field(name="Because They Are Out Of Thier Minds ?", value="\u200b", inline=False)
                embed.set_image(url=bully_gif)
    
                await ctx.respond(embed=embed)
                return
    
        if user.id == self.bot.user.id:
            embed = discord.Embed(
                title="Bully",
                description=f"{ctx.author.mention} Tried To Bully Me, I'm A Bot",
                color=0xFF5733,
            )
            await ctx.respond(embed=embed)
            return

        developer = 727012870683885578

        if user.id == developer:
            embed = discord.Embed(
                title="Kill",
                description=f"{ctx.author.mention} Tried To Bully My Developer",
                color=0xFF5733,
            )

            embed.add_field(name="What The Hell ?!", value="Sorry He's My Dev\nIf He Becomes Sad No One Looks At This Poor Bot TT", inline=False)

            await ctx.respond(embed=embed)
            return

        else:

            embed = discord.Embed(
                title="Kill",
                description=f"{ctx.author.mention} Bullied {user.mention}",
                color=0xFF5733,
            )
            embed.add_field(name="Reason", value="Because They Needed To Get Bullied", inline=False)
            embed.set_image(url=bully_gif)

            await ctx.respond(f'{user.mention}',embed=embed)

    

    @commands.slash_command(name="kiss", description="Kiss A User")
    async def kiss(self, ctx, user: discord.Member):
            
            kiss_gif = get_gif('anime_kiss')
    
            if user == ctx.author:
    
                embed = discord.Embed(
                    title="Kiss",
                    description=f"{ctx.author.mention} Kissed Themselves",
                    color=0xFF5733,
                )
    
                embed.add_field(
                    name="Wait What ?!", value="\u200b", inline=False
                )
                embed.add_field(name="I Think I Need Holy Water", value="\u200b", inline=False)
    
                await ctx.respond(embed=embed)
                return
    
            if user.id == self.bot.user.id:
                embed = discord.Embed(
                    title="Kiss",
                    description=f"{ctx.author.mention} Kissed Me, I'm A Bot",
                    color=0xFF5733,
                )
                await ctx.respond(embed=embed)
                return
    
            developer = 727012870683885578
    
            if user.id == developer:
                embed = discord.Embed(
                    title="Kiss",
                    description=f"{ctx.author.mention} Kissed My Developer",
                    color=0xFF5733,
                )
    
                embed.add_field(name="Reason", value="Because They Needed It", inline=False)
                embed.set_image(url=kiss_gif)
    
                await ctx.respond(embed=embed)
                return
    
            else:
    
                embed = discord.Embed(
                    title="Kiss",
                    description=f"{ctx.author.mention} Kissed {user.mention}",
                    color=0xFF5733,
                )
                embed.add_field(name="Reason", value="Because They Needed It", inline=False)
                embed.set_image(url=kiss_gif)
    
                await ctx.respond(f"{user.mention}",embed=embed)

    @commands.slash_command(name="cuddle", description="Cuddle A User")
    async def cuddle(self, ctx, user: discord.Member):
                
        cuddle_gif = get_gif('anime_cuddle')

        if user == ctx.author:

            embed = discord.Embed(
                title="Cuddle",
                description=f"{ctx.author.mention} Cuddled Themselves",
                color=0xFF5733,
            )

            embed.add_field(
                name="Huh How ?!", value="\u200b", inline=False
            )
            embed.add_field(name="Ahhhhhh Help ME", value="\u200b", inline=False)

            await ctx.respond(embed=embed)
            return

        if user.id == self.bot.user.id:
            embed = discord.Embed(
                title="Cuddle",
                description=f"{ctx.author.mention} Cuddled Me, I'm A Bot",
                color=0xFF5733,
            )
            await ctx.respond(embed=embed)
            return

        developer = 727012870683885578

        if user.id == developer:
            embed = discord.Embed(
                title="Cuddle",
                description=f"{ctx.author.mention} Cuddled My Developer",
                color=0xFF5733,
            )

            embed.add_field(name="Reason", value="Because They Needed It", inline=False)
            embed.set_image(url=cuddle_gif)

            await ctx.respond(embed=embed)
            return

        else:

            embed = discord.Embed(
                title="Cuddle",
                description=f"{ctx.author.mention} Cuddled {user.mention}",
                color=0xFF5733,
            )
            embed.add_field(name="Reason", value="Because They Needed It", inline=False)
            embed.set_image(url=cuddle_gif)

            await ctx.respond(f"{user.mention}",embed=embed)

    @commands.slash_command(name="dance", description="Dance With A User")
    async def dance(self, ctx, user: discord.Member):
                    
        dance_gif = get_gif('anime_dance')

        if user == ctx.author:

            embed = discord.Embed(
                title="Dance",
                description=f"{ctx.author.mention} Danced Alone",
                color=0xFF5733,
            )

            embed.add_field(
                name="Ok Not That Bad", value="\u200b", inline=False
            )
            embed.add_field(name="Because They Found No One TT", value="\u200b", inline=False)

            await ctx.respond(embed=embed)
            return

        if user.id == self.bot.user.id:
            embed = discord.Embed(
                title="Dance",
                description=f"{ctx.author.mention} Danced With Me, I'm A Bot",
                color=0xFF5733,
            )
            await ctx.respond(embed=embed)
            return

        developer = 727012870683885578

        if user.id == developer:
            embed = discord.Embed(
                title="Dance",
                description=f"{ctx.author.mention} Danced With My Developer",
                color=0xFF5733,
            )

            embed.add_field(name="Reason", value="Because They Needed To", inline=False)
            embed.set_image(url=dance_gif)

            await ctx.respond(embed=embed)
            return

        else:

            embed = discord.Embed(
                title="Dance",
                description=f"{ctx.author.mention} Danced With {user.mention}",
                color=0xFF5733,
            )
            embed.add_field(name="Reason", value="Because They Needed To", inline=False)
            embed.set_image(url=dance_gif)

            await ctx.respond(f"{user.mention}",embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
