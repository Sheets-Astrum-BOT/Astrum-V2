import discord
from discord.ext import commands

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def info(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author

        embed = discord.Embed(title="User Information", color=member.color)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Name", value=member.display_name)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="Joined At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="Bot", value=member.bot, inline=False)

        roles = [f"<@&{role.id}>" for role in member.roles if role.name != "@everyone"]

        if roles:
            embed.add_field(name="Roles", value=", ".join(roles), inline=False)

        embed.set_footer(text=f"Requested By {ctx.author.display_name}")

        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        if not isinstance(member, discord.Member):
            await ctx.send("Invalid Member Specified")
            return
        
        embed = discord.Embed(title=f"{member}'s Avatar", color=discord.Color.blue())
        embed.set_image(url=member.avatar.url)
        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def serverinfo(self, ctx):
        guild = ctx.guild

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)

        channels = text_channels + voice_channels

        embed = discord.Embed(title="Server Information", color=discord.Color.blurple())
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Name", value=guild.name)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Owner", value=guild.owner.display_name)
        embed.add_field(name="Members", value=guild.member_count, inline=False)
        embed.add_field(name="Channels", value=channels, inline=False)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Information(bot))
