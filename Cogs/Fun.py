import random
import requests

import discord
from urllib.parse import quote
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='slap', description="Slap A User")
    async def slap(self, ctx, user: discord.Member):

        slap_gifs = ['https://i.giphy.com/Gf3AUz3eBNbTW.webp', 
                     'https://i.giphy.com/k1uYB5LvlBZqU.webp']

        if user == ctx.author:

            embed = discord.Embed(
                title="Slap",
                description=f"You Can't Slap Yourself, Or Wait Can You ? 🤔",
                color=0x2f3136
            )

            embed.add_field(
                name='Let Me Help You With That',value='\u200b', inline=False)
            embed.set_image(url=random.choice(slap_gifs))

            ember = discord.Embed(
                title="Slap",
                description=f"{user.mention} Got An Slap From The Bot",
                color=0x2f3136
            )

            ember.set_image(url=random.choice(slap_gifs))

            await ctx.respond(embed=embed)
            await ctx.respond(embed=ember)
            return

        if user.id == self.bot.user.id:
            embed = discord.Embed(
                title="Slap",
                description=f"{ctx.author.mention} Can't Slap Me, I'm A Bot",
                color=0x2f3136
            )
            await ctx.respond(embed=embed)
            return

        developer = 727012870683885578

        if user.id == developer:
            embed = discord.Embed(
                title="Slap",
                description=f"{ctx.author.mention} You Can't Slap My Developer",
                color=0x2f3136
            )

            embed.add_field(
                name='Let Me Help You With That',value='\u200b', inline=False)

            ember = discord.Embed(
                title="Slap",
                description=f"{user.mention} Got An Slap From The Bot",
                color=0x2f3136
            )

            ember.add_field(name='Damage', value='Infinite', inline=False)
            ember.set_image(url=random.choice(slap_gifs))

            await ctx.respond(embed=embed)
            await ctx.respond(embed=ember)
            return

        else :

            embed = discord.Embed(
            title="Slap",
            description=f"{ctx.author.mention} Slapped {user.mention}",
            color=0x2f3136
        )
            embed.add_field(
            name="Reason", value="Because They Deserved It", inline=False)
            embed.add_field(
            name="Damage", value=f'{random.randint(10,100)}', inline=False)
            embed.set_image(url=random.choice(slap_gifs))
            embed.set_footer(text="Did It Hurt ?")

            await ctx.respond(f'{user.mention}',embed=embed)


    @commands.slash_command(name='hug', description="Hug A User")
    async def hug(self, ctx, user: discord.Member):
            
            hug_gifs = ['https://i.giphy.com/GMFUrC8E8aWoo.webp',
                        'https://i.giphy.com/od5H3PmEG5EVq.webp']
    
            if user == ctx.author:
    
                embed = discord.Embed(
                    title="Hug",
                    description=f"{ctx.author.mention} Hugged Themselves",
                    color=0x2f3136
                )
    
                embed.add_field(
                    name="In The Era Of Self Love", value="\u200b", inline=False)
                embed.add_field(
                    name="Because They Needed It", value="\u200b", inline=False)
                embed.set_image(url=random.choice(hug_gifs))
    
                await ctx.respond(embed=embed)
                return
    
            if user.id == self.bot.user.id:
                embed = discord.Embed(
                    title="Hug",
                    description=f"{ctx.author.mention} Hugged Me, I'm A Bot",
                    color=0x2f3136
                )
                await ctx.respond(embed=embed)
                return
    
            developer = 727012870683885578
    
            if user.id == developer:
                embed = discord.Embed(
                    title="Hug",
                    description=f"{ctx.author.mention} Hugged My Developer",
                    color=0x2f3136
                )
    
                embed.add_field(
                    name="Reason", value="Because They Needed It", inline=False)
                embed.set_image(url=random.choice(hug_gifs))
    
                await ctx.respond(embed=embed)
                return
    
            else :
    
                embed = discord.Embed(
                title="Hug",
                description=f"{ctx.author.mention} Hugged {user.mention}",
                color=0x2f3136
            )
                embed.add_field(
                name="Reason", value="Because They Needed It", inline=False)
                embed.set_image(url=random.choice(hug_gifs))
    
                await ctx.respond(embed=embed)

    @commands.slash_command(name='roll', description="Roll Between Two Numbers")
    async def roll(self, ctx, min: int=1, max: int=100):
        if min > max:
            embed = discord.Embed(
                title="Error",
                description="The Minimum Value Can't Be Greater Than The Maximum Value",
                color=0x2f3136
            )

            await ctx.respond(embed=embed)
            return
        if min == max:
            embed = discord.Embed(
                title = f'The Value Is {min}',
            )
            await ctx.respond(embed=embed)
            return
        
        embed = discord.Embed(
            title=f"The Value Is {random.randint(min, max)}",
            description=f"Rolled Between {min} And {max}",
            color=0x2f3136
        )

        await ctx.respond(embed=embed, view = ReRoll())

    @commands.slash_command(name='coinflip', description="Flip A Coin")
    async def coinflip(self, ctx):
        coin = random.choice(["Heads", "Tails"])
        embed = discord.Embed(
            title=f"The Coin Landed On {coin}",
            color=0x2f3136
        )
        await ctx.respond(embed=embed, view = ReFlip())

    @commands.slash_command(name='dice', description="Roll A Dice")
    async def dice(self, ctx):
        dice = random.choice([1, 2, 3, 4, 5, 6])
        embed = discord.Embed(
            title=f"The Dice Landed On {dice}",
            color=0x2f3136
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(name='8ball', description="Ask The Magic 8 Ball")
    async def eightball(self, ctx, *, question: str):
        responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.",
                     "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.",
                     "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
                     "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
        embed = discord.Embed(
            title="Magic 8 Ball",
            description=f"Question: {question}\nAnswer: {random.choice(responses)}",
            color=0x2f3136
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(name='rps', description="Play Rock Paper Scissors")
    async def rps(self, ctx, choice: str):
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)
        if choice.lower() not in choices:
            embed = discord.Embed(
                title="Error",
                description="Please Choose Rock, Paper, Or Scissors",
                color=0x2f3136
            )
            await ctx.respond(embed=embed)
            return
        if choice.lower() == bot_choice:
            embed = discord.Embed(
                title="Rock Paper Scissors",
                description=f"Both Chose {choice.capitalize()}, It's A Tie",
                color=0x2f3136
            )
            await ctx.respond(embed=embed)
            return
        if choice.lower() == "rock":
            if bot_choice == "scissors":
                embed = discord.Embed(
                    title="Rock Paper Scissors",
                    description=f"{ctx.author.mention} Chose Rock, I Chose Scissors, You Win",
                    color=0x2f3136
                )
                await ctx.respond(embed=embed)
                return
            else:
                embed = discord.Embed(
                    title="Rock Paper Scissors",
                    description=f"{ctx.author.mention} Chose Rock, I Chose Paper, You Lose",
                    color=0x2f3136
                )
                await ctx.respond(embed=embed)
                return
        if choice.lower() == "paper":
            if bot_choice == "rock":
                embed = discord.Embed(
                    title="Rock Paper Scissors",
                    description=f"{ctx.author.mention} Chose Paper, I Chose Rock, You Win",
                    color=0x2f3136
                )
                await ctx.respond(embed=embed)
                return
            else:
                embed = discord.Embed(
                    title="Rock Paper Scissors",
                    description=f"{ctx.author.mention} Chose Paper, I Chose Scissors, You Lose",
                    color=0x2f3136
                )
                await ctx.respond(embed=embed)
                return
        if choice.lower() == "scissors":
            if bot_choice == "paper":
                embed = discord.Embed(
                    title="Rock Paper Scissors",
                    description=f"{ctx.author.mention} Chose Scissors, I Chose Paper, You Win",
                    color=0x2f3136
                )
                await ctx.respond(embed=embed)
                return
            else:
                embed = discord.Embed(
                    title="Rock Paper Scissors",
                    description=f"{ctx.author.mention} Chose Scissors, I Chose Rock, You Lose",
                    color=0x2f3136
                )
                await ctx.respond(embed=embed)

    @commands.slash_command(name='moviequote', description="Get A Random Quote From A Movie")
    async def moviequote(self, ctx):
        
        api_url = 'https://api.seriesquotes.10cyrilc.me/pic/solid?background_color=black&text_color=white&text_size=200&x=3600&y=2400'

        embed = discord.Embed(title='Random Movie Quote', color=0xFF5733)
        embed.set_image(url=api_url)

        await ctx.respond(embed=embed)

    @commands.slash_command(name='customquote', description="Generate A Random Quote")
    async def customquote(self, ctx, text: str):

        encoded_text = quote(text)

        api_url = f'https://api.seriesquotes.10cyrilc.me/pic/custom?text_color=&background_color=&text="{encoded_text}"&x=3600&y=2400'

        embed = discord.Embed(title='Random Quote', color=0xFF5733)
        embed.set_image(url=api_url)

        embed.set_footer(text=f'Quote By : {ctx.author.display_name}')

        await ctx.respond(embed=embed)


class ReFlip(discord.ui.View):
    
        def __init__(self):
            super().__init__()
    
        async def on_timeout(self):
            self.disable_all_items()
    
        @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="🔄")
        async def button_callback(self, button, interaction):
    
            coin = random.choice(["Heads", "Tails"])
            embed = discord.Embed(
                title=f"The Coin Landed On {coin}",
                color=0x2f3136
            )
            await interaction.response.edit_message(content=embed, view=self)

class ReRoll(discord.ui.View):

    def __init__(self):
        super().__init__()

    async def on_timeout(self):
        self.disable_all_items()

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="🔃")
    async def button_callback(self, button, interaction):

        embed = discord.Embed(
            title=f"The Value Is {random.randint(min, max)}",
            description=f"Rolled Between {min} And {max}",
            color=0x2f3136
        )
        await interaction.response.edit_message(content=embed, view=self)


def setup(bot):
    bot.add_cog(Fun(bot))
