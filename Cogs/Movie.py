import json
import asyncio
import aiohttp
import discord
from PyMovieDb import IMDB
from discord.ext import commands
from discord.commands import SlashCommandGroup

class Movie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.imdb = IMDB()

    movie = SlashCommandGroup("movie", "Movie Commands")

    @movie.command(name="search_movie", description="Search for a movie")
    async def search_show(self, ctx, movie_name: str):
        await ctx.defer()
        movie = self.imdb.search(movie_name, tv=False)
        data = json.loads(movie)

        if "results" in data:
            results = data["results"]
            embed = discord.Embed(
                title=f"Search Results For: {movie_name}",
                description=f"Results Found: {len(results)}",
            )

            for index, show in enumerate(results):
                show_id = show.get("id")
                show_name = show.get("name")
                embed.add_field(
                    name=f"Show {index + 1} | ID : {show_id}",
                    value=f"Name: {show_name}",
                    inline=False,
                )

            view = MovieView(self.bot, results)
            await ctx.respond(embed=embed, view=view)
        else:
            embed = discord.Embed(
                title="Error",
                description="No Results Found\n\nIf You Are Searching For A Show,\nPlease Use `/show show_search` Command",
            )
            await ctx.respond(embed=embed)

    @movie.command(name="get_movie", description="Get a movie by ID")
    async def get_movie(self, ctx, movie_id: str):
        await ctx.defer()
        movie = self.imdb.get_by_id(movie_id, tv=False)
        data = json.loads(movie)

        if "type" in data:
            embed = discord.Embed(
                title=data["name"],
                description=data["description"],
                color=discord.Color.blue(),
            )
            embed.set_thumbnail(url=data["poster"])
            embed.add_field(name="Type", value=data["type"], inline=True)
            embed.add_field(
                name="Date Published", value=data["datePublished"], inline=True
            )
            embed.add_field(
                name="Rating",
                value=f"{data['rating']['ratingValue']} / {data['rating']['bestRating']}",
                inline=True,
            )

            view = LinkView(self.bot, movie_id, data["type"])
            await ctx.respond(embed=embed, view=view)
        else:
            embed = discord.Embed(title="Error", description="No Data Found")
            await ctx.respond(embed=embed)

    @movie.command(name="latest", description="Get the latest movies")
    async def latest(self, ctx):
        url = "https://vidsrc.to/vapi/movie/new"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("result", {}).get("items", [])
                    embed = discord.Embed(
                        title="Latest Movies",
                        color=discord.Color.blue()
                    )
                    movie_list = ""

                    for i, movie in enumerate(items, 1):
                        title = movie.get("title", "Unknown Title")
                        imdb_id = movie.get("imdb_id", "Unknown IMDB ID")
                        movie_list += f"**{title}**\nIMDB ID: {imdb_id}\n\n"

                        if i % 5 == 0 or i == len(items):
                            embed.description = movie_list
                            await ctx.send(embed=embed)
                            embed = discord.Embed(
                                title="Latest Movies",
                                color=discord.Color.blue()
                            )
                            movie_list = ""
                else:
                    await ctx.send("Failed To Fetch Data")

    show = SlashCommandGroup("show", "Show Commands")

    @show.command(name="search_show", description="Search for a TV Show")
    async def search_show(self, ctx, show_name: str):
        await ctx.defer()
        show = self.imdb.search(show_name, tv=True)
        data = json.loads(show)

        if "results" in data:
            results = data["results"]
            embed = discord.Embed(
                title=f"Search Results For: {show_name}",
                description=f"Results Found: {len(results)}",
            )

            for index, show in enumerate(results):
                show_id = show.get("id")
                show_name = show.get("name")
                embed.add_field(
                    name=f"Show {index + 1} | ID : {show_id}",
                    value=f"Name: {show_name}",
                    inline=False,
                )

            view = ShowView(self.bot, results)
            await ctx.respond(embed=embed, view=view)
        else:
            embed = discord.Embed(
                title="Error",
                description="No Results Found\n\nIf You Are Searching For A Movie,\nPlease Use `/movie search_movie` Command",
            )
            await ctx.respond(embed=embed)

    @show.command(name="get_show", description="Get a TV Show by ID")
    async def get_show(self, ctx, show_id: str):
        await ctx.defer()
        show = self.imdb.get_by_id(show_id, tv=True)
        data = json.loads(show)

        if "type" in data:
            embed = discord.Embed(
                title=data["name"],
                description=data["description"],
                color=discord.Color.blue(),
            )
            embed.set_thumbnail(url=data["poster"])
            embed.add_field(name="Type", value=data["type"], inline=True)
            embed.add_field(
                name="Date Published", value=data["datePublished"], inline=True
            )
            embed.add_field(
                name="Rating",
                value=f"{data['rating']['ratingValue']} / {data['rating']['bestRating']}",
                inline=True,
            )

            view = LinkView(self.bot, show_id, data["type"])
            await ctx.respond(embed=embed, view=view)
        else:
            embed = discord.Embed(title="Error", description="No Data Found")
            await ctx.respond(embed=embed)

    @show.command(name="latest", description="Get the latest TV Shows")
    async def latest(self, ctx):
        url = "https://vidsrc.to/vapi/tv/new"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("result", {}).get("items", [])
                    embed = discord.Embed(
                        title="Latest Shows",
                        color=discord.Color.blue()
                    )
                    movie_list = ""

                    for i, movie in enumerate(items, 1):
                        title = movie.get("title", "Unknown Title")
                        imdb_id = movie.get("imdb_id", "Unknown IMDB ID")
                        movie_list += f"**{title}**\nIMDB ID: {imdb_id}\n\n"

                        if i % 5 == 0 or i == len(items):
                            embed.description = movie_list
                            await ctx.send(embed=embed)
                            embed = discord.Embed(
                                title="Latest Shows",
                                color=discord.Color.blue()
                            )
                            movie_list = ""
                else:
                    await ctx.send("Failed To Fetch Data")

class MovieView(discord.ui.View):
    def __init__(self, bot, results):
        super().__init__()
        self.bot = bot
        self.imdb = IMDB()
        self.results = results

        options = [
            discord.SelectOption(label=show.get("name"), value=str(show.get("id")))
            for show in results
        ]

        self.select = discord.ui.Select(
            placeholder="Choose A Movie", min_values=1, max_values=1, options=options
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        selected_movie_id = self.select.values[0]
        selected_movie = next(
            (show for show in self.results if str(show.get("id")) == selected_movie_id),
            None,
        )

        if selected_movie:
            movie_name = selected_movie.get("name")
            movie_id = selected_movie.get("id")
            movie = self.imdb.get_by_id(movie_id)
            data = json.loads(movie)

            if "type" in data:
                embed = discord.Embed(
                    title=data["name"],
                    description=data["description"],
                    color=discord.Color.blue(),
                )
                embed.set_thumbnail(url=data["poster"])
                embed.add_field(name="Type", value=data["type"], inline=True)
                embed.add_field(
                    name="Date Published", value=data["datePublished"], inline=True
                )
                embed.add_field(
                    name="Rating",
                    value=f"{data['rating']['ratingValue']} / {data['rating']['bestRating']}",
                    inline=True,
                )

                view = LinkView(self.bot, movie_id, data["type"])
                await interaction.followup.send(embed=embed, view=view)
            else:
                await interaction.followup.send("No Data Found")

class ShowView(discord.ui.View):
    def __init__(self, bot, results):
        super().__init__()
        self.bot = bot
        self.imdb = IMDB()
        self.results = results

        options = [
            discord.SelectOption(label=show.get("name"), value=str(show.get("id")))
            for show in results
        ]

        self.select = discord.ui.Select(
            placeholder="Choose A Show", min_values=1, max_values=1, options=options
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        selected_show_id = self.select.values[0]
        selected_show = next(
            (show for show in self.results if str(show.get("id")) == selected_show_id),
            None,
        )

        if selected_show:
            show_name = selected_show.get("name")
            show_id = selected_show.get("id")
            show = self.imdb.get_by_id(show_id)
            data = json.loads(show)

            if "type" in data:
                embed = discord.Embed(
                    title=data["name"],
                    description=data["description"],
                    color=discord.Color.blue(),
                )
                embed.set_thumbnail(url=data["poster"])
                embed.add_field(name="Type", value=data["type"], inline=True)
                embed.add_field(
                    name="Date Published", value=data["datePublished"], inline=True
                )
                embed.add_field(
                    name="Rating",
                    value=f"{data['rating']['ratingValue']} / {data['rating']['bestRating']}",
                    inline=True,
                )

                view = LinkView(self.bot, show_id, data["type"])
                await interaction.followup.send(embed=embed, view=view)
            else:
                await interaction.followup.send("No Data Found")

class LinkView(discord.ui.View):

    def __init__(self, bot, id, type):
        super().__init__()
        self.bot = bot
        self.id = id
        self.type = type

        self.movie_url = f"https://vidsrc.to/embed/movie/{id}"
        self.show_url = f"https://vidsrc.to/embed/tv/{id}"

        if type == "Movie":
            self.movie_button = discord.ui.Button(
                style=discord.ButtonStyle.link, label="Movie", url=self.movie_url
            )
            self.add_item(self.movie_button)

        else:
            self.show_button = discord.ui.Button(
                style=discord.ButtonStyle.link, label="TVSeries", url=self.show_url
            )
            self.add_item(self.show_button)

    async def on_button_click(self, interaction):
        if self.type == "Movie":
            await interaction.response.send_message(self.movie_url, ephemeral=True)
        else:
            await interaction.response.send_message(self.show_url, ephemeral=True)

def setup(bot):
    bot.add_cog(Movie(bot))
