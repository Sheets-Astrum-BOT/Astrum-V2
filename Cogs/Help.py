import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='help', description="Sends Help Embed")
    async def help(self, ctx):
        embed = discord.Embed(
            title="Help",
            description="List of Commands",
            color=0x2f3136
        )

        ping = self.bot.get_application_command('ping')
        invite = self.bot.get_application_command('botinfo')
        meaning = self.bot.get_application_command('meaning')

        embed.add_field(name=f"{ping.mention}", value="Sends Bot's Latency", inline=False)
        embed.add_field(name=f"{invite.mention}", value="Sends Bot's Invite Link", inline=False)
        embed.add_field(name=f"{meaning.mention}", value="Sends Meaning Of A Word", inline=False)

        cembed = discord.Embed(
            title="Help Categories",
            description="List Available Categories",
            color=0x2f3136
        )

        cembed.add_field(name="AFK", value="\u200b", inline=True)
        cembed.add_field(name="Fun", value="\u200b", inline=True)
        cembed.add_field(name="Help", value="\u200b", inline=True)
        cembed.add_field(name="Anime", value="\u200b", inline=True)
        cembed.add_field(name="Utility", value="\u200b", inline=True)
        cembed.add_field(name="Reminder", value="\u200b", inline=True)
        cembed.add_field(name="-----------------------------", value="\u200b", inline=False)
        cembed.add_field(name="Moderation", value="\u200b", inline=False)
        cembed.add_field(name="Information", value="\u200b", inline=False)
        cembed.add_field(name="Entertainment", value="\u200b", inline=False)

        await ctx.respond(embed=embed)
        await ctx.respond(embed=cembed, view=CEmbed(self.bot))


class CEmbed(discord.ui.View):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.select( 
        placeholder = "Choose A Help Category", 
        min_values = 1, 
        max_values = 1, 
        options = [ 
            discord.SelectOption(
                label="AI",
                description="AI Commands"
            ),
            discord.SelectOption(
                label="AFK",
                description="AFK Commands"
            ),
            discord.SelectOption(
                label="Fun",
                description="Fun Commands"
            ),
            discord.SelectOption(
                label="Help",
                description="Help Commands"
            ),
            discord.SelectOption(
                label="Anime",
                description="Anime Commands"
            ),
            discord.SelectOption(
                label="Emotes",
                description="Emote Commands"
            ),
            discord.SelectOption(
                label="Utility",
                description="Utility Commands"
            ),
            discord.SelectOption(
                label="Reminder",
                description="Reminder Commands"
            ),
            discord.SelectOption(
                label="Translate",
                description="Translate Commands"
            ),
            discord.SelectOption(
                label="Moderation",
                description="Moderation Commands"
            ),
            discord.SelectOption(
                label="Information",
                description="Informational Commands"
            ),
            discord.SelectOption(
                label="Entertainment",
                description="Entertainment Commands"
            )
        ]
    )
    async def select_callback(self, select, interaction):

        AIembed = discord.Embed(
            title="Inbuilt AI Tool",
            description="The Bot Contains An Inbuilt AI Tool Based On Google's Gemini AI\nTo Use The AI Feature Just Ping The Bot And Write In Your Question And Let The Bot Answer Your Query",
            color=0x2f3136
        )

        AFKembed = discord.Embed(
            title="AFK",
            description="Simple AFK Tool",
            color=0x2f3136
        )

        afk = self.bot.get_application_command('afk')
        unafk = self.bot.get_application_command('unafk')

        AFKembed.add_field(name=f"{afk.mention}", value="Sets You As AFK", inline=False)
        AFKembed.add_field(name=f"{unafk.mention}", value="Unsets You As AFK", inline=False)

        Funembed = discord.Embed(
            title="Fun",
            description="Simple Commands To Have Fun",
            color=0x2f3136
        )

        Funembed.add_field(name=f"{self.bot.get_application_command('8ball').mention}", value="Ask The 8ball A Question", inline=False)
        Funembed.add_field(name=f"{self.bot.get_application_command('coinflip').mention}", value="Flips A Coin", inline=False)
        Funembed.add_field(name=f"{self.bot.get_application_command('roll').mention}", value="Rolls A Dice", inline=False)
        Funembed.add_field(name=f"{self.bot.get_application_command('rps').mention}", value="Play Rock Paper Scissors", inline=False)
        Funembed.add_field(name=f"{self.bot.get_application_command('customquote').mention}", value="Create A Quote", inline=False)
        Funembed.add_field(name=f"{self.bot.get_application_command('moviequote').mention}", value="Get A Random Quote From Famous Series", inline=False)
        Funembed.add_field(name=f"{self.bot.get_application_command('gif').mention}", value="Sends A Gif", inline=False)


        Helpembed = discord.Embed(
            title="Help",
            description="Displays The Main Help Command",
            color=0x2f3136
        )
        
        Animeembed = discord.Embed(
            title="Anime",
            description="Anime Commands",
            color=0x2f3136
        )

        Animeembed.add_field(name=f"{self.bot.get_application_command('anisearch').mention}", value="Sends Information About An Anime", inline=False)
        Animeembed.add_field(name=f"{self.bot.get_application_command('watch').mention}", value="Sends Streaming Link Of An Anime", inline=False)
        Animeembed.add_field(name=f"{self.bot.get_application_command('mangasearch').mention}", value="Sends Information About A Manga", inline=False)
        Animeembed.add_field(name=f"{self.bot.get_application_command('topanime').mention}", value="Sends Streaming Link Of A Manga", inline=False)
        Animeembed.add_field(name=f"{self.bot.get_application_command('settings').mention}", value="Enable/Disable Anime Updates", inline=False)
        Animeembed.add_field(name=f"{self.bot.get_application_command('waifu').mention}", value="Sends A Random Waifu", inline=False)
        Animeembed.add_field(name=f"{self.bot.get_application_command('nwaifu').mention}", value="Sends A Random NSFW Waifu", inline=False)

        Emotesembed = discord.Embed(
            title="Emotes",
            description="Simple Emote Commands",
            color=0x2f3136
        )

        Emotesembed.add_field(name=f"{self.bot.get_application_command('emotemenu').mention}", value="Sends The Emotes Menu", inline=False)


        Utilsembed = discord.Embed(
            title="Utility",
            description="Simple Utility Commands",
            color=0x2f3136
        )

        Utilsembed.add_field(name=f"{self.bot.get_application_command('time').mention}", value="Sends Time Of A Particular Timezone", inline=False)
        Utilsembed.add_field(name=f"{self.bot.get_application_command('weather').mention}", value="Sends Weather Information", inline=False)

        Reminderembed = discord.Embed(
            title="Reminder",
            description="Simple Reminder Tool",
            color=0x2f3136
        )

        Reminderembed.add_field(name=f"{self.bot.get_application_command('remind').mention}", value="Sets A Reminder", inline=False)
        Reminderembed.add_field(name=f"{self.bot.get_application_command('reminders').mention}", value="Sends All Your Reminders", inline=False)
        Reminderembed.add_field(name=f"{self.bot.get_application_command('delete_reminder').mention}", value="Deletes A Reminder", inline=False)

        Moderationembed = discord.Embed(
            title="Moderation",
            description="Simple Moderation Commands",
            color=0x2f3136
        )

        Moderationembed.add_field(name=f"{self.bot.get_application_command('kick').mention}", value="Kicks A Member", inline=False)
        Moderationembed.add_field(name=f"{self.bot.get_application_command('ban').mention}", value="Bans A Member", inline=False)
        Moderationembed.add_field(name=f"{self.bot.get_application_command('unban').mention}", value="Unbans A Member", inline=False)
        Moderationembed.add_field(name=f"{self.bot.get_application_command('delete').mention}", value="Deletes Messages", inline=False)
        Moderationembed.add_field(name=f"{self.bot.get_application_command('mute').mention}", value="Mutes A Member", inline=False)
        Moderationembed.add_field(name=f"{self.bot.get_application_command('unmute').mention}", value="Unmutes A Member", inline=False)
        Moderationembed.add_field(name=f"{self.bot.get_application_command('slowmode').mention}", value="Sets Slowmode In A Channel", inline=False)
        Moderationembed.add_field(name=f"{self.bot.get_application_command('nuke').mention}", value="Nukes A Channel", inline=False)
        Moderationembed.add_field(name=f"{self.bot.get_application_command('lock').mention}", value="Locks A Channel", inline=False)
        Moderationembed.add_field(name=f"{self.bot.get_application_command('unlock').mention}", value="Unlocks A Channel", inline=False)
        Moderationembed.add_field(name=f"{self.bot.get_application_command('roleadd').mention}", value="Adds A Role To A Member", inline=False)
        Moderationembed.add_field(name=f"{self.bot.get_application_command('roleremove').mention}", value="Removes A Role From A Member", inline=False)


        Informationembed = discord.Embed(
            title="Information",
            description="Simple Information Commands",
            color=0x2f3136
        )

        Informationembed.add_field(name=f"{self.bot.get_application_command('info').mention}", value="Sends User Information", inline=False)
        Informationembed.add_field(name=f"{self.bot.get_application_command('serverinfo').mention}", value="Sends Server Information", inline=False)
        Informationembed.add_field(name=f"{self.bot.get_application_command('botinfo').mention}", value="Sends Bot Information", inline=False)
        Informationembed.add_field(name=f"{self.bot.get_application_command('avatar').mention}", value="Sends User's Avatar", inline=False)

        Entertainembed = discord.Embed(
            title="Entertainment",
            description="Simple Entertainment Commands",
            color=0x2f3136
        )

        Entertainembed.add_field(name=f"{self.bot.get_application_command('meme').mention}", value="Sends A Random Meme", inline=False)
        Entertainembed.add_field(name=f"{self.bot.get_application_command('quote').mention}", value="Sends A Random Quote", inline=False)
        Entertainembed.add_field(name=f"{self.bot.get_application_command('joke').mention}", value="Sends A Random Joke", inline=False)
        Entertainembed.add_field(name=f"{self.bot.get_application_command('fact').mention}", value="Sends A Random Fact", inline=False)

        Translateembed = discord.Embed(
            title="Translate",
            description="Simple Test Translation Commands",
            color=0x2f3136
        )

        Translateembed.add_field(name=f"{self.bot.get_application_command('translate').mention}", value="Translates Text To Other Language", inline=False)
        Translateembed.add_field(name=f"{self.bot.get_application_command('detect').mention}", value="Detects Language Of Text", inline=False)

    

        if select.values[0] == "AI":
            await interaction.response.send_message(embed=AIembed, ephemeral=True)

        elif select.values[0] == "AFK":
            await interaction.response.send_message(embed=AFKembed, ephemeral=True)

        elif select.values[0] == "Fun":
            await interaction.response.send_message(embed=Funembed, ephemeral=True)

        elif select.values[0] == "Help":
            await interaction.response.send_message(embed=Helpembed, ephemeral=True)

        elif select.values[0] == "Anime":
            await interaction.response.send_message(embed=Animeembed, ephemeral=True)

        elif select.values[0] == "Emotes":
            await interaction.response.send_message(embed=Emotesembed, ephemeral=True)

        elif select.values[0] == "Utility":
            await interaction.response.send_message(embed=Utilsembed, ephemeral=True)

        elif select.values[0] == "Reminder":
            await interaction.response.send_message(embed=Reminderembed, ephemeral=True)

        elif select.values[0] == "Translate":
            await interaction.response.send_message(embed=Translateembed, ephemeral=True)

        elif select.values[0] == "Information":
            await interaction.response.send_message(embed=Informationembed, ephemeral=True)

        elif select.values[0] == "Moderation":
            await interaction.response.send_message(embed=Moderationembed, ephemeral=True)

        elif select.values[0] == "Entertainment":
            await interaction.response.send_message(embed=Entertainembed, ephemeral=True)

        else:
            await interaction.response.send_message("Invalid Option")


def setup(bot):
    bot.add_cog(Help(bot))