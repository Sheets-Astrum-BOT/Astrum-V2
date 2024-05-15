import random
import aiohttp
import requests

import discord
from urllib.parse import quote
from discord.ext import commands


async def get_gif(query):
    api_key = "AIzaSyBadJ6mJ2zUDmZnQBoXQqjFjy6RFYgnpEc"
    url = f"https://tenor.googleapis.com/v2/search?q={query}&key={api_key}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    gif_urls = [entry["media_formats"]["gif"]["url"] for entry in data["results"]]
    random_gif_url = random.choice(gif_urls)

    return random_gif_url


class Emotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="slap", description="Slap A User")
    async def slap(self, ctx, user: discord.Member):

        gif = get_gif("anime_slap")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Slaps {user.display_name} Hard",
            color=0x00FF00,
        )
        embed.set_image(url=gif)

        damage = random.randint(1, 100)

        embed.add_field(name="\u200b", value=f"It Dealt {damage} Damage", inline=False)
        embed.set_footer(text="Ouuch! Did It Hurt ?")

        await ctx.respond(f"{user.mention}",embed=embed)

    @commands.slash_command(name="hug", description="Hug A User")
    async def hug(self, ctx, user: discord.Member):

        gif = get_gif("anime_hug")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Hugs {user.display_name}", color=0x00FF00
        )

        embed.add_field(name="\u200b", value="Awwww !", inline=False)
        embed.set_footer(text="That's So Generous Of You !")

        embed.set_image(url=gif)

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="kill", description="Kill A User")
    async def kill(self, ctx, user: discord.Member):

        gif = get_gif("anime_kill")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Kills {user.display_name}", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value=f"It Dealt Infinite Damage", inline=False)
        embed.set_footer(text="RIP !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="pat", description="Pat A User")
    async def pat(self, ctx, user: discord.Member):

        gif = get_gif("anime_pat")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Pats {user.display_name}", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Cute !", inline=False)
        embed.set_footer(text="You Deserve It !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="kiss", description="Kiss A User")
    async def kiss(self, ctx, user: discord.Member):

        gif = get_gif("anime_kiss")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Kisses {user.display_name}",
            color=0x00FF00,
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Romantic !", inline=False)
        embed.set_footer(text="You're So Sweet !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="cry", description="Cry")
    async def cry(self, ctx):

        gif = get_gif("anime_cry")

        embed = discord.Embed(title=f"{ctx.author.display_name} Cries", color=0x00FF00)
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="Don't Cry !", inline=False)
        embed.set_footer(text="It's Okay !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="punch", description="Puch a User")
    async def punch(self, ctx, user: discord.Member):

        gif = get_gif("anime_punch")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Punches {user.display_name}",
            color=0x00FF00,
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="It Dealt 100 Damage", inline=False)
        embed.set_footer(text="Ouch !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="bully", description="Bully A User")
    async def bully(self, ctx, user: discord.Member):

        gif = get_gif("anime_bully")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Bullies {user.display_name}",
            color=0x00FF00,
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's Not Nice !", inline=False)
        embed.set_footer(text="Stop Bullying !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="bite", description="Bite A User")
    async def bite(self, ctx, user: discord.Member):

        gif = get_gif("anime_bite")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Bites {user.display_name}", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="It Dealt 50 Damage", inline=False)
        embed.set_footer(text="Ouch !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="lick", description="Lick A User")
    async def lick(self, ctx, user: discord.Member):

        gif = get_gif("anime_lick")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Licks {user.display_name}", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Weird !", inline=False)
        embed.set_footer(text="You're So Strange !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="cuddle", description="Cuddle A User")
    async def cuddle(self, ctx, user: discord.Member):

        gif = get_gif("anime_cuddle")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Cuddles {user.display_name}",
            color=0x00FF00,
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Warm !", inline=False)
        embed.set_footer(text="You're So Sweet !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="dance", description="Dance With A User")
    async def dance(self, ctx, user: discord.Member):

        gif = get_gif("anime_dance")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Dances With {user.display_name}",
            color=0x00FF00,
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Fun !", inline=False)
        embed.set_footer(text="Let's Dance !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="highfive", description="Highfive A User")
    async def highfive(self, ctx, user: discord.Member):

        gif = get_gif("anime_highfive")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Highfives {user.display_name}",
            color=0x00FF00,
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Cool !", inline=False)
        embed.set_footer(text="You're So Awesome !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="handhold", description="Hold Hands With A User")
    async def handhold(self, ctx, user: discord.Member):

        gif = get_gif("anime_handhold")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Holds Hands With {user.display_name}",
            color=0x00FF00,
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Sweet !", inline=False)
        embed.set_footer(text="You're So Lovely !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="smile", description="Smile")
    async def smile(self, ctx):

        gif = get_gif("anime_smile")

        embed = discord.Embed(title=f"{ctx.author.display_name} Smiles", color=0x00FF00)
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Cute !", inline=False)
        embed.set_footer(text="You're So Adorable !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="laugh", description="Laugh")
    async def laugh(self, ctx):

        gif = get_gif("anime_laugh")

        embed = discord.Embed(title=f"{ctx.author.display_name} Laughs", color=0x00FF00)
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Funny !", inline=False)
        embed.set_footer(text="You're So Hilarious !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="blush", description="Blush")
    async def blush(self, ctx):

        gif = get_gif("anime_blush")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Blushes", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Cute !", inline=False)
        embed.set_footer(text="You're So Shy !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="confused", description="Confused")
    async def confused(self, ctx):

        gif = get_gif("anime_confused")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Confused", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Weird !", inline=False)
        embed.set_footer(text="You're So Strange !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="angry", description="Angry")
    async def angry(self, ctx):

        gif = get_gif("anime_angry")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Angry", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Scary !", inline=False)
        embed.set_footer(text="You're So Fierce !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="sad", description="Sad")
    async def sad(self, ctx):

        gif = get_gif("anime_sad")

        embed = discord.Embed(title=f"{ctx.author.display_name} Is Sad", color=0x00FF00)
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Heartbreaking !", inline=False)
        embed.set_footer(text="You're So Emotional !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="happy", description="Happy")
    async def happy(self, ctx):

        gif = get_gif("anime_happy")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Happy", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Joyful !", inline=False)
        embed.set_footer(text="You're So Cheerful !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="surprised", description="Surprised")
    async def surprised(self, ctx):

        gif = get_gif("anime_surprised")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Surprised", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Shocking !", inline=False)
        embed.set_footer(text="You're So Astonished !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="scared", description="Scared")
    async def scared(self, ctx):

        gif = get_gif("anime_scared")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Scared", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Terrifying !", inline=False)
        embed.set_footer(text="You're So Fearful !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="sleep", description="Sleep")
    async def sleep(self, ctx):

        gif = get_gif("anime_sleep")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Sleeping", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Peaceful !", inline=False)
        embed.set_footer(text="You're So Relaxed !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="eat", description="Eat")
    async def eat(self, ctx):

        gif = get_gif("anime_eat")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Eating", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Delicious !", inline=False)
        embed.set_footer(text="You're So Hungry !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="drink", description="Drink")
    async def drink(self, ctx):

        gif = get_gif("anime_drink")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Drinking", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Refreshing !", inline=False)
        embed.set_footer(text="You're So Thirsty !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="think", description="Think")
    async def think(self, ctx):

        gif = get_gif("anime_think")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Thinking", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Smart !", inline=False)
        embed.set_footer(text="You're So Intelligent !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="write", description="Write")
    async def write(self, ctx):

        gif = get_gif("anime_write")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Writing", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Creative !", inline=False)
        embed.set_footer(text="You're So Artistic !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="read", description="Read")
    async def read(self, ctx):

        gif = get_gif("anime_read")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Reading", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Interesting !", inline=False)
        embed.set_footer(text="You're So Curious !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="sing", description="Sing")
    async def sing(self, ctx):

        gif = get_gif("anime_sing")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Singing", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Beautiful !", inline=False)
        embed.set_footer(text="You're So Talented !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="play", description="Play")
    async def play(self, ctx):

        gif = get_gif("anime_play")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Playing", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Fun !", inline=False)
        embed.set_footer(text="You're So Energetic !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)

    @commands.slash_command(name="work", description="Work")
    async def work(self, ctx):

        gif = get_gif("anime_work")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Working", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Hardworking !", inline=False)
        embed.set_footer(text="You're So Dedicated !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="study", description="Study")
    async def study(self, ctx):

        gif = get_gif("anime_study")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Studying", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Intelligent !", inline=False)
        embed.set_footer(text="You're So Smart !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="exercise", description="Exercise")
    async def exercise(self, ctx):

        gif = get_gif("anime_exercise")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Exercising", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Healthy !", inline=False)
        embed.set_footer(text="You're So Fit !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="meditate", description="Meditate")
    async def meditate(self, ctx):

        gif = get_gif("anime_meditate")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Meditating", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Peaceful !", inline=False)
        embed.set_footer(text="You're So Calm !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)

    @commands.slash_command(name="pray", description="Pray")
    async def pray(self, ctx):

        gif = get_gif("anime_pray")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Is Praying", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Spiritual !", inline=False)
        embed.set_footer(text="You're So Religious !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="curse", description="Curse A User")
    async def curse(self, ctx, user: discord.Member):

        gif = get_gif("anime_curse")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Curses {user.display_name}",
            color=0x00FF00,
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Mean !", inline=False)
        embed.set_footer(text="Stop Cursing !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="bless", description="Bless A User")
    async def bless(self, ctx, user: discord.Member):

        gif = get_gif("anime_bless")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Blesses {user.display_name}",
            color=0x00FF00,
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Kind !", inline=False)
        embed.set_footer(text="You're So Generous !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="thank", description="Thank A User")
    async def thank(self, ctx, user: discord.Member):

        gif = get_gif("anime_thank")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Thanks {user.display_name}",
            color=0x00FF00,
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Grateful !", inline=False)
        embed.set_footer(text="You're So Polite !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="welcome", description="Welcome A User")
    async def welcome(self, ctx, user: discord.Member):

        gif = get_gif("anime_welcome")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Welcomes {user.display_name}",
            color=0x00FF00,
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Warm !", inline=False)
        embed.set_footer(text="You're So Friendly !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="bye", description="Say Bye To A User")
    async def bye(self, ctx, user: discord.Member):

        gif = get_gif("anime_bye")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Says Bye To {user.display_name}",
            color=0x00FF00,
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Sad !", inline=False)
        embed.set_footer(text="You're So Emotional !")

        await ctx.respond(f"{user.mention}",embed=embed)


    @commands.slash_command(name="goodmorning", description="Say Good Morning")
    async def goodmorning(self, ctx):

        gif = get_gif("anime_goodmorning")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Says Good Morning", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Bright !", inline=False)
        embed.set_footer(text="You're So Cheerful !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="goodnight", description="Say Good Night")
    async def goodnight(self, ctx):

        gif = get_gif("anime_goodnight")

        embed = discord.Embed(
            title=f"{ctx.author.display_name} Says Good Night", color=0x00FF00
        )
        embed.set_image(url=gif)

        embed.add_field(name="\u200b", value="That's So Dark !", inline=False)
        embed.set_footer(text="You're So Sleepy !")

        await ctx.respond(f"{ctx.author.mention}",embed=embed)


    @commands.slash_command(name="emotemenu", description="Show Emote Menu")
    async def emotemenu(self, ctx):
        embed = discord.Embed(
            title="Emote Menu",
            color=0x00FF00
        )

        emotes = [
            "Slap", "Hug", "Kill", "Pat", "Kiss", "Cry", "Punch", "Bully", "Bite", "Lick",
            "Cuddle", "Dance", "Highfive", "Handhold", "Smile", "Laugh", "Blush", "Confused",
            "Angry", "Sad", "Happy", "Surprised", "Scared", "Sleep", "Eat", "Drink", "Think",
            "Write", "Read", "Sing", "Play", "Work", "Study", "Exercise", "Meditate", "Pray",
            "Curse", "Bless", "Thank", "Welcome", "Bye", "Goodmorning", "Goodnight"
        ]

        columns = 3
        column_size = len(emotes) // columns

        for i in range(columns):
            start = i * column_size
            end = (i + 1) * column_size if i < columns - 1 else len(emotes)
            embed.add_field(name="\u200b", value="\n".join(emotes[start:end]), inline=True)

        embed.set_footer(text="Use /<emote> <user> To Use An Emote")


def setup(bot):
    bot.add_cog(Emotes(bot))
