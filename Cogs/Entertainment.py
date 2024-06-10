import os
import json
import discord
import aiohttp 
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from discord.commands import SlashCommandGroup


def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return {}


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


meme_config = load_json("MEME.json")
joke_config = load_json("JOKE.json")
quote_config = load_json("QUOTE.json")
fact_config = load_json("FACT.json")
last_sent = load_json("LAST.json")


class Entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.meme_task.start()
        self.joke_task.start()
        self.quote_task.start()
        self.fact_task.start()

    settings = SlashCommandGroup("settings", "Settings Commands")

    @settings.command(name="set_meme_channel", description="Set channel for memes")
    async def set_meme_channel(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.TextChannel,
        frequency: int,
    ):
        meme_config[str(ctx.guild.id)] = {
            "channel_id": channel.id,
            "frequency": frequency,
        }
        save_json("MEME.json", meme_config)

        embed = discord.Embed(
            title="Meme Channel Set",
            description=f"MEME Channel : {channel.mention} \nFrequency : {frequency} Minutes",
            color=0x00FF00,
        )

        await ctx.respond(embed=embed)

    print(settings.subcommands)

    @settings.command(name="set_joke_channel", description="Set channel for jokes")
    async def set_joke_channel(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.TextChannel,
        frequency: int,
    ):
        joke_config[str(ctx.guild.id)] = {
            "channel_id": channel.id,
            "frequency": frequency,
        }
        save_json("JOKE.json", joke_config)

        embed = discord.Embed(
            title="Joke Channel Set",
            description=f"JOKE Channel : {channel.mention} \nFrequency : {frequency} Minutes",
            color=0x00FF00,
        )

        await ctx.respond(embed=embed)

    @settings.command(name="set_quote_channel", description="Set channel for quotes")
    async def set_quote_channel(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.TextChannel,
        frequency: int,
    ):
        quote_config[str(ctx.guild.id)] = {
            "channel_id": channel.id,
            "frequency": frequency,
        }
        save_json("QUOTE.json", quote_config)

        embed = discord.Embed(
            title="Quote Channel Set",
            description=f"QUOTE Channel : {channel.mention} \nFrequency : {frequency} Minutes",
            color=0x00FF00,
        )

        await ctx.respond(embed=embed)

    @settings.command(name="set_fact_channel", description="Set channel for facts")
    async def set_fact_channel(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.TextChannel,
        frequency: int,
    ):
        fact_config[str(ctx.guild.id)] = {
            "channel_id": channel.id,
            "frequency": frequency,
        }
        save_json("FACT.json", fact_config)

        embed = discord.Embed(
            title="Fact Channel Set",
            description=f"FACT Channel : {channel.mention} \nFrequency : {frequency} Minutes",
            color=0x00FF00,
        )

        await ctx.respond(embed=embed)

    @settings.command(name="reset_meme", description="Reset Automatic Meme")
    async def reset_meme(self, ctx: discord.ApplicationContext):
        meme_config.pop(str(ctx.guild.id), None)
        save_json("MEME.json", meme_config)
        await ctx.respond("Automatic Meme Removed")

    @settings.command(name="reset_joke", description="Reset Automatic Joke")
    async def reset_joke(self, ctx: discord.ApplicationContext):
        joke_config.pop(str(ctx.guild.id), None)
        save_json("JOKE.json", joke_config)
        await ctx.respond("Automatic Joke Removed")

    @settings.command(name="reset_quote", description="Reset Automatic Quote")
    async def reset_quote(self, ctx: discord.ApplicationContext):
        quote_config.pop(str(ctx.guild.id), None)
        save_json("QUOTE.json", quote_config)
        await ctx.respond("Automatic Quote Removed")

    @settings.command(name="reset_fact", description="Reset Automatic Fact")
    async def reset_fact(self, ctx: discord.ApplicationContext):
        fact_config.pop(str(ctx.guild.id), None)
        save_json("FACT.json", fact_config)
        await ctx.respond("Automatic Fact Removed")

    @settings.command(
        name="current_settings", description="Shows Current Automatic Fun Settings"
    )
    async def current_settings(self, ctx: discord.ApplicationContext):
        meme_channel = meme_config.get(str(ctx.guild.id))
        joke_channel = joke_config.get(str(ctx.guild.id))
        quote_channel = quote_config.get(str(ctx.guild.id))
        fact_channel = fact_config.get(str(ctx.guild.id))
        embed = discord.Embed(
            title="Current Automatic Fun Settings",
            color=0x00FF00,
        )
        if meme_channel:
            channel = self.bot.get_channel(meme_channel["channel_id"])
            embed.add_field(
                name="Meme Channel",
                value=f"{channel.mention} \nFrequency : {meme_channel['frequency']} Minutes",
                inline=False,
            )
        if joke_channel:
            channel = self.bot.get_channel(joke_channel["channel_id"])
            embed.add_field(
                name="Joke Channel",
                value=f"{channel.mention} \nFrequency : {joke_channel['frequency']} Minutes",
                inline=False,
            )
        if quote_channel:
            channel = self.bot.get_channel(quote_channel["channel_id"])
            embed.add_field(
                name="Quote Channel",
                value=f"{channel.mention} \nFrequency : {quote_channel['frequency']} Minutes",
                inline=False,
            )
        if fact_channel:
            channel = self.bot.get_channel(fact_channel["channel_id"])
            embed.add_field(
                name="Fact Channel",
                value=f"{channel.mention} \nFrequency : {fact_channel['frequency']} Minutes",
                inline=False,
            )
        if not any([meme_channel, joke_channel, quote_channel, fact_channel]):
            embed.add_field(
                name="No Channels", value="No Channel Set Found", inline=False
            )
        await ctx.respond(embed=embed)

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
        url = "https://some-random-api.com/others/joke"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                joke_json = await response.json()
                setup = joke_json.get("joke")
                embed = discord.Embed(title="Here's A Joke", color=0x00FF00)
                if setup:
                    embed.add_field(name="\u200b", value=setup, inline=False)
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

    @settings.command(
        name="automatic_fun_help", description="Shows Help For Automatic Fun Commands"
    )
    async def automatic_fun_help(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="Automatic Fun Help",
            description="These Commands Will Send Random Memes, Jokes, Quotes, Facts In The Specified Channel At Specified Frequency",
            color=0x00FF00,
        )
        embed.add_field(
            name="Set Meme Channel",
            value=f"{self.bot.get_application_command('settings').subcommands[0].mention}",
            inline=False,
        )
        embed.add_field(
            name="Set Joke Channel",
            value=f"{self.bot.get_application_command('settings').subcommands[1].mention}",
            inline=False,
        )
        embed.add_field(
            name="Set Quote Channel",
            value=f"{self.bot.get_application_command('settings').subcommands[2].mention}",
            inline=False,
        )
        embed.add_field(
            name="Set Fact Channel",
            value=f"{self.bot.get_application_command('settings').subcommands[3].mention}",
            inline=False,
        )
        embed.add_field(
            name="Reset Meme Channel",
            value=f"{self.bot.get_application_command('settings').subcommands[4].mention}",
            inline=False,
        )
        embed.add_field(
            name="Reset Joke Channel",
            value=f"{self.bot.get_application_command('settings').subcommands[5].mention}",
            inline=False,
        )
        embed.add_field(
            name="Reset Quote Channel",
            value=f"{self.bot.get_application_command('settings').subcommands[6].mention}",
            inline=False,
        )
        embed.add_field(
            name="Reset Fact Channel",
            value=f"{self.bot.get_application_command('settings').subcommands[7].mention}",
            inline=False,
        )
        embed.add_field(
            name="Current Automatic Fun Settings",
            value=f"{self.bot.get_application_command('settings').subcommands[8].mention}",
            inline=False,
        )
        await ctx.respond(embed=embed)

    def check_and_send(self, ctx, config, key, task, message_fn):
        last_sent_time = last_sent.get(key)
        if not last_sent_time or datetime.now() - datetime.strptime(
            last_sent_time, "%Y-%m-%d %H:%M:%S"
        ) >= timedelta(minutes=config["frequency"]):
            channel = self.bot.get_channel(config["channel_id"])
            if channel:
                self.bot.loop.create_task(message_fn(channel))
                last_sent[key] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_json("last_sent.json", last_sent)

    async def send_meme(self, channel):
        url = "https://meme-api.com/gimme"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                meme_json = await response.json()
                meme_url = meme_json["url"]
                await channel.send(meme_url)

    async def send_joke(self, channel):
        url = "https://some-random-api.com/others/joke"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                joke_json = await response.json()
                setup = joke_json.get("joke")
                embed = discord.Embed(title="Here's A Joke", color=0x00FF00)
                if setup:
                    embed.add_field(name="\u200b", value=setup, inline=False)
                await channel.send(embed=embed)

    async def send_quote(self, channel):
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
                await channel.send(embed=embed)

    async def send_fact(self, channel):
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                fact_json = await response.json()
                fact = fact_json["text"]
                embed = discord.Embed(
                    title="Here's A Fact", description=fact, color=0x00FF00
                )
                await channel.send(embed=embed)

    @tasks.loop(minutes=1)
    async def meme_task(self):
        for guild_id, config in meme_config.items():
            self.check_and_send(
                guild_id, config, f"meme_{guild_id}", "meme_task", self.send_meme
            )

    @tasks.loop(minutes=1)
    async def joke_task(self):
        for guild_id, config in joke_config.items():
            self.check_and_send(
                guild_id, config, f"joke_{guild_id}", "joke_task", self.send_joke
            )

    @tasks.loop(minutes=1)
    async def quote_task(self):
        for guild_id, config in quote_config.items():
            self.check_and_send(
                guild_id, config, f"quote_{guild_id}", "quote_task", self.send_quote
            )

    @tasks.loop(minutes=1)
    async def fact_task(self):
        for guild_id, config in fact_config.items():
            self.check_and_send(
                guild_id, config, f"fact_{guild_id}", "fact_task", self.send_fact
            )

    @meme_task.before_loop
    @joke_task.before_loop
    @quote_task.before_loop
    @fact_task.before_loop
    async def before_tasks(self):
        await self.bot.wait_until_ready()


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
        url = "https://sv443.net/jokeapi/v2/joke/any"
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


def setup(bot):
    bot.add_cog(Entertainment(bot))
