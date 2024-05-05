import json
import asyncio
import aiohttp
import discord
import requests
from discord import option
from discord.ui.item import Item
from discord.ext import commands, tasks

from AnilistPython import Anilist


async def swaifu(tag: str):
    url = "https://api.waifu.im/search"

    params = {"included_tags": [tag], "is_nsfw": "false"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if "images" in data and len(data["images"]) > 0:
                    image_url = data["images"][0]["url"]

                    return image_url


async def nwaifu(tag: str):
    url = f"https://api.waifu.pics/nsfw/{tag}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()

                if "url" in data:
                    image_url = data["url"]

                    return image_url


class AnimeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.anilist = Anilist()
        self.last_entry_id = None
        self.enabled_channels = {}
        self.check_website.start()

        try:
            with open("Anime.json", "r") as file:
                self.enabled_channels = json.load(file)

        except FileNotFoundError:
            pass

    def cog_unload(self):
        self.check_website.cancel()

    @commands.slash_command(
        name="waifu",
        description="Get A Random Waifu Image",
    )
    @option(
        "tag",
        description="Choose The Category",
        choices=["maid", "waifu", "oppai", "selfies", "uniform"],
    )
    async def waifu(self, ctx, tag: str):
        await ctx.defer()

        try:
            image_url = await swaifu(tag)

            if image_url:
                embed = discord.Embed(
                    title="OniChan Here I Am <3",
                    color=discord.Color.blurple(),
                )
                embed.set_image(url=image_url)

                await ctx.respond(embed=embed)

            else:
                await ctx.respond("No Waifu Image Found For This Tag")

        except Exception as e:
            await ctx.respond(f"An Error Occurred : {e}")

    @commands.slash_command(
        name="nwaifu", description="Get A Random NSFW Waifu Image", nsfw=True
    )
    @option(
        "tag",
        description="Choose The Category",
        choices=["waifu", "neko", "trap", "blowjob"],
    )
    async def nwaifu(self, ctx, tag: str):
        await ctx.defer()

        try:
            image_url = await nwaifu(tag)

            if image_url:
                embed = discord.Embed(
                    title="OniChan Here I Am <3",
                    color=discord.Color.blurple(),
                )
                embed.set_image(url=image_url)

                await ctx.respond(embed=embed)

            else:
                await ctx.respond("No Waifu Image Found For This Tag")

        except Exception as e:
            await ctx.respond(f"An Error Occurred : {e}")

    @commands.slash_command(
        name="anisearch", description="Get Information About An Anime"
    )
    async def anisearch(self, ctx, *, anime_name: str):

        await ctx.defer()
        try:

            anime_dict = self.anilist.get_anime(anime_name=anime_name)

            anime_id = self.anilist.get_anime_id(anime_name)
            anime_name = anime_dict["name_english"]
            anime_desc = anime_dict["desc"]
            starting_time = anime_dict["starting_time"]
            next_airing_ep = anime_dict["next_airing_ep"]
            season = anime_dict["season"]
            genres = ", ".join(anime_dict["genres"])
            anime_url = f"https://anilist.co/anime/{anime_id}/"
            anime_score = anime_dict["average_score"]
            current_ep = anime_dict["next_airing_ep"]["episode"] - 1

            if anime_desc != None and len(anime_desc) != 0:
                anime_desc = anime_desc.split("<br>")

            anime_embed = discord.Embed(
                title=anime_dict["name_english"], color=0xA0DB8E
            )
            anime_embed.set_image(url=anime_dict["banner_image"])
            anime_embed.add_field(name="Synopsis", value=anime_desc[0], inline=False)
            anime_embed.add_field(name="\u200b", value="\u200b", inline=False)
            anime_embed.add_field(
                name="Anime ID",
                value=self.anilist.get_anime_id(anime_name),
                inline=True,
            )
            anime_embed.add_field(
                name="Airing Format", value=anime_dict["airing_format"], inline=True
            )
            anime_embed.add_field(
                name="Airing Status", value=anime_dict["airing_status"], inline=True
            )
            anime_embed.add_field(name="Start Date", value=starting_time, inline=True)
            anime_embed.add_field(name="Score", value=anime_score, inline=True)
            anime_embed.add_field(name="Season", value=season, inline=True)
            anime_embed.add_field(name="Genres", value=genres, inline=False)
            anime_embed.add_field(
                name="More Info", value=f"[AniList Page]({anime_url})", inline=False
            )

            anime_embed.set_footer(
                text=f"Next Episode: {next_airing_ep['episode']} | Current Episode: {current_ep}"
            )

            view = StartWatching(anime_name, 1, self.bot)
            await ctx.respond(embed=anime_embed, view=view)

        except Exception as e:
            print(e)
            await ctx.respond(
                f"An Error Occurred Searching For Anime\n```Error: {e}```"
            )

    @commands.slash_command(name="watch", description="Get Streaming Link Of An Anime")
    async def watch(self, ctx, *, anime_name: str, episode: int = 1):

        await ctx.defer()

        try:
            anime_name = anime_name.replace(" ", "-").lower()

            anime_dict = self.anilist.get_anime(anime_name=anime_name)
            cover_image = anime_dict["banner_image"]
            current_ep = anime_dict["next_airing_ep"]["episode"] - 1

            url = f"https://astrumanimeapi.vercel.app/anime/gogoanime/watch/{anime_name}-episode-{episode}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()

                        streaming_link = data.get("headers", {}).get("Referer", None)

                        if streaming_link:
                            anime_title = anime_name.replace("-", " ").capitalize()

                            embed = discord.Embed(
                                title=f"Anime : {anime_title} | Episode : {episode}",
                                color=discord.Color.blue(),
                            )

                            embed.add_field(
                                name="Streaming Link",
                                value=f"Gogo Anime : [Click Here]({streaming_link})",
                                inline=False,
                            )
                            embed.add_field(
                                name="NOTE",
                                value="Use Watch Command To Watch Other Episodes",
                                inline=False,
                            )
                            embed.set_image(url=cover_image)

                            await ctx.respond(embed=embed)

                        else:
                            await ctx.respond(
                                "No Streaming Link Found For This Episode"
                            )
                    else:
                        await ctx.respond(
                            f"Failed To Fetch Streaming Link: {response.status}"
                        )
        except Exception as e:
            await ctx.respond(f"An Error Occurred : {e}")

    @commands.slash_command(
        name="mangasearch", description="Get Information About A Manga"
    )
    async def mangasearch(self, ctx, *, manga_name: str):
        try:
            manga_dict = self.anilist.get_manga(manga_name=manga_name)

            manga_id = self.anilist.get_manga_id(manga_name)
            manga_desc = manga_dict["desc"]
            manga_title = manga_dict["name_english"]
            starting_time = manga_dict["starting_time"]
            airing_format = manga_dict["release_format"]
            airing_status = manga_dict["release_status"]
            season = manga_dict["volumes"]
            genres = ", ".join(manga_dict["genres"])
            manga_url = f"https://anilist.co/manga/{manga_id}/"
            cover_image = manga_dict["banner_image"]
            manga_score = manga_dict["average_score"]

            if manga_desc != None and len(manga_desc) != 0:
                manga_desc = manga_desc.split("<br>")

            manga_embed = discord.Embed(title=manga_title, color=0xA0DB8E)
            manga_embed.set_image(url=cover_image)
            manga_embed.add_field(name="Synopsis", value=manga_desc[0], inline=False)
            manga_embed.add_field(name="\u200b", value="\u200b", inline=False)
            manga_embed.add_field(name="Manga ID", value=manga_id, inline=True)
            manga_embed.add_field(
                name="Release Format", value=airing_format, inline=True
            )
            manga_embed.add_field(
                name="Release Status", value=airing_status, inline=True
            )
            manga_embed.add_field(name="Start Date", value=starting_time, inline=True)
            manga_embed.add_field(name="Score", value=manga_score, inline=True)
            manga_embed.add_field(name="Volumes", value=season, inline=True)
            manga_embed.add_field(name="Genres", value=genres, inline=False)
            manga_embed.add_field(
                name="More Info", value=f"[AniList Page]({manga_url})", inline=False
            )

            await ctx.respond(embed=manga_embed)

        except Exception as e:
            print(e)
            await ctx.respond(
                f"An Error Occurred Searching For Manga\n```Error: {e}```"
            )

    @commands.slash_command(
        name="topanime", description="Get The List For Top Airing Anime"
    )
    async def topanime(self, ctx):

        await ctx.defer()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://astrumanimeapi.vercel.app/anime/gogoanime/top-airing"
            ) as resp:
                data = await resp.json()

                embeds = []
                for index, result in enumerate(data["results"], start=1):

                    anime_name = result["title"]

                    try:

                        anime_dict = self.anilist.get_anime(anime_name=anime_name)

                        anime_name = anime_dict["name_english"]
                        image = anime_dict["banner_image"]

                    except:

                        anime_name = result["title"]
                        image = result["image"]

                    embed = discord.Embed(
                        title=f"{index}. {anime_name}",
                        description="\u200b",
                        color=discord.Color.blurple(),
                    )
                    embed.add_field(
                        name=f"Episode : {result['episodeNumber']}",
                        value="\u200b",
                        inline=False,
                    )
                    embed.add_field(
                        name="Genres", value=", ".join(result["genres"]), inline=False
                    )
                    embed.set_image(url=image)
                    embeds.append(embed)

                await ctx.respond(embed=embeds[0], view=NextAnime(embeds))

    @commands.slash_command(
        name="settings", description="Get The Current Anime Update Settings"
    )
    async def settings(self, ctx):

        guild_id = str(ctx.guild.id)
        channel_id = self.enabled_channels.get(guild_id, None)

        embed = discord.Embed(
            title="Anime Update Settings", color=discord.Color.blurple()
        )

        if channel_id is None:
            embed.description = "Anime Updates Are Not Enabled For This Server."
        else:
            channel = self.bot.get_channel(channel_id)
            embed.description = f"Anime Updates Are Enabled For \nChannel For Anime Updates : {channel.mention}"

        await ctx.respond(
            embed=embed, view=AnimeUpdateSettings(ctx.channel, self.enabled_channels)
        )

    @tasks.loop(minutes=30)
    async def check_website(self):

        for guild_id, channel_id in self.enabled_channels.items():


            guild = self.bot.get_guild(int(guild_id))

            if guild is None:
                continue

            channel = guild.get_channel(int(channel_id))

            if channel is None:
                continue

            print(f"Anime Update For : {guild} Channel : {channel}")

            async with aiohttp.ClientSession() as session:

                async with session.get(
                    "https://astrumanimeapi.vercel.app/anime/gogoanime/recent-episodes"
                ) as resp:

                    data = await resp.json()

                    if self.last_entry_id != data["results"][0]["id"]:
                        result = data["results"][0]

                        try:
                            anime_dict = self.anilist.get_anime(
                                anime_name=result["title"]
                            )
                            anime_name = anime_dict["name_english"]

                            image = anime_dict["banner_image"]

                            anime_id = self.anilist.get_anime_id(result["title"])

                            anime_url = f"https://anilist.co/anime/{anime_id}/"

                        except:
                            anime_name = result["title"]
                            image = result["image"]
                            anime_url = result["url"]

                        embed = discord.Embed(
                            title="Anime Episode Alert ~ OniChann",
                            description="\u200b",
                            color=discord.Color.blurple(),
                        )

                        if anime_name != None:
                            embed.add_field(
                                name=anime_name, value="\u200b", inline=False
                            )

                        else:
                            embed.add_field(
                                name=result["title"], value="\u200b", inline=False
                            )

                        embed.add_field(
                            name=f"Episode : {result['episodeNumber']}",
                            value="\u200b",
                            inline=False,
                        )
                        embed.set_image(url=image)
                        embed.url = anime_url

                        embed.set_footer(text="Use Settings To Enable/Disable Updates")

                        await channel.send(embed=embed)


    @check_website.before_loop
    async def before_check_website(self):
        await self.bot.wait_until_ready()


class AnimeUpdateSettings(discord.ui.View):
    def __init__(self, channel, enabled_channels):
        super().__init__()
        self.channel = channel
        self.enabled_channels = enabled_channels

    @discord.ui.button(
        label="Enable Updates",
        style=discord.ButtonStyle.primary,
        custom_id="enable_updates",
    )
    async def enable_button_callback(self, button, interaction):
        await interaction.response.defer()

        self.enabled_channels[str(interaction.guild.id)] = self.channel.id

        with open("Anime.json", "w") as file:
            json.dump(self.enabled_channels, file)

        await interaction.followup.send("Updates Enabled For This Channel.")

    @discord.ui.button(
        label="Disable Updates",
        style=discord.ButtonStyle.danger,
        custom_id="disable_updates",
    )
    async def disable_button_callback(self, button, interaction):
        await interaction.response.defer()

        if str(interaction.guild.id) in self.enabled_channels:
            del self.enabled_channels[str(interaction.guild.id)]
            with open("Anime.json", "w") as file:
                json.dump(self.enabled_channels, file)
            await interaction.followup.send("Updates Disabled For This Channel.")
        else:
            await interaction.followup.send(
                "Updates Were Not Enabled For This Channel."
            )


class NextAnime(discord.ui.View):
    def __init__(self, embeds):
        super().__init__()
        self.embeds = embeds
        self.current_index = 0

    @discord.ui.button(
        label="◀",
        style=discord.ButtonStyle.primary,
        custom_id="prev_anime",
    )
    async def prev_button_callback(self, button, interaction):
        if self.current_index > 0:
            self.current_index -= 1
        else:
            self.current_index = len(self.embeds) - 1

        await interaction.response.edit_message(
            embed=self.embeds[self.current_index], view=self
        )

    @discord.ui.button(
        label="▶",
        style=discord.ButtonStyle.primary,
        custom_id="next_anime",
    )
    async def next_button_callback(self, button, interaction):
        if self.current_index < len(self.embeds) - 1:
            self.current_index += 1
        else:
            self.current_index = 0

        await interaction.response.edit_message(
            embed=self.embeds[self.current_index], view=self
        )


class StartWatching(discord.ui.View):
    def __init__(self, anime_name, episode, bot):
        super().__init__()
        self.bot = bot
        self.anilist = Anilist()
        self.anime_name = anime_name
        self.episode = episode

    @discord.ui.button(
        label="Start Watching",
        style=discord.ButtonStyle.primary,
        custom_id="start_watching",
    )
    async def button_callback(self, button, interaction):

        await interaction.response.defer()

        watch_cmd = self.bot.get_command("watch")

        try:
            anime_name = self.anime_name
            episode = self.episode

            anime_name = anime_name.replace(" ", "-").lower()

            anime_dict = self.anilist.get_anime(anime_name=anime_name)
            cover_image = anime_dict["banner_image"]
            current_ep = anime_dict["next_airing_ep"]["episode"] - 1

            url = f"https://astrumanimeapi.vercel.app/anime/gogoanime/watch/{anime_name}-episode-{episode}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()

                        streaming_link = data.get("headers", {}).get("Referer", None)

                        if streaming_link:
                            anime_title = anime_name.replace("-", " ").capitalize()

                            embed = discord.Embed(
                                title=f"Anime : {anime_title} | Episode : {episode}",
                                color=discord.Color.blue(),
                            )

                            embed.add_field(
                                name="Streaming Link",
                                value=f"Gogo Anime : [Click Here]({streaming_link})",
                                inline=False,
                            )
                            embed.add_field(
                                name="NOTE",
                                value=f"Use {watch_cmd} Command To Watch Other Episodes",
                                inline=False,
                            )
                            embed.set_image(url=cover_image)

                            await interaction.respond(embed=embed)

                        else:
                            await interaction.respond(
                                "No Streaming Link Found For This Episode"
                            )
                    else:
                        await interaction.respond(
                            f"Failed To Fetch Streaming Link: {response.status}"
                        )
        except Exception as e:
            await interaction.respond(f"An Error Occurred : {e}")


def setup(bot):
    bot.add_cog(AnimeCog(bot))
