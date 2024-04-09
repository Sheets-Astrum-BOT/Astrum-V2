import requests

import pytz
import discord
from datetime import datetime
from discord.ext import commands

#  Utility Functions


class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='time', description='Gets Time Of A Paticular Location')
    async def time(self, ctx, *, city):
        try:
            timezone = pytz.timezone(f'{city}'.format(city.replace(" ", "_")))

        except pytz.exceptions.UnknownTimeZoneError:
            await ctx.respond(f'Error : Invalid City', view=Time_Usage())

        date = datetime.now(timezone).strftime('%Y-%m-%d')
        time = datetime.now(timezone).strftime('%H:%M:%S')

        city = city.split("/")[1].replace("_", " ")

        embed = discord.Embed(
            title=f"Time In {city}",
            color=0x2f3136
        )

        embed.add_field(name="Date", value=date, inline=False)
        embed.add_field(name="Time", value=time, inline=False)

        await ctx.respond(embed=embed)

    @commands.slash_command(name='weather', description='Gets Weather Of A Paticular Location')
    async def weather(self, ctx, *, city):
        api_key = '34379a10e456c41b137b3f30379215e5'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            city = data['name']
            country = data['sys']['country']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description'].capitalize()
            icon = data['weather'][0]['icon']

            embed = discord.Embed(title=f'Weather In {city}, {country}',
                                  description=description,
                                  color=0x2f3136)
            embed.add_field(name='Temperature', value=f'{temp}°C', inline=True)
            embed.add_field(name='Feels Like',
                            value=f'{feels_like}°C', inline=True)
            embed.add_field(
                name='', value=f'-------------------------', inline=False)
            embed.add_field(name='Humidity',
                            value=f'{humidity} %', inline=False)
            embed.set_thumbnail(
                url=f'https://openweathermap.org/img/wn/{icon}.png')

            await ctx.respond(embed=embed)

        else:
            await ctx.respond(f'Error : Invalid City', view=Weather_Usage())


class Time_Usage(discord.ui.View):

    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Check Usage", style=discord.ButtonStyle.secondary, emoji="❗")
    async def check_usage(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Error",
            description="Invalid City",
            color=0x2f3136
        )

        embed.add_field(
            name="Example", value="`/time America/New_York`", inline=False)
        embed.add_field(name="Fomat Of City",
                        value="`Continent/City`", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


class Weather_Usage(discord.ui.View):

    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Check Usage", style=discord.ButtonStyle.secondary, emoji="❗")
    async def check_usage(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Error",
            description="Invalid City",
            color=0x2f3136
        )

        embed.add_field(
            name="Example", value="`/weather New_York`", inline=False)
        embed.add_field(name="Fomat Of City",
                        value="`City`", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Utils(bot))
