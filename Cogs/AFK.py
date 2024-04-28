import json

import discord
from discord.ext import commands


class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            with open('AFK.json', 'r') as f:
                self.afk_data = json.load(f)
        except FileNotFoundError:
            self.afk_data = {}

    def save_afk_data(self):
        with open('AFK.json', 'w') as f:
            json.dump(self.afk_data, f, indent=4)

    @commands.slash_command()
    async def afk(self, ctx, *, message: str = None):
        original_name = ctx.author.display_name
        self.afk_data[str(ctx.author.id)] = {
            "message": message or "AFK",
            "original_name": original_name
        }
        self.save_afk_data()
        embed = discord.Embed(
            title="AFK Status", description=f"{ctx.author.mention} Is Now AFK", color=discord.Color.blue())
        await ctx.respond(embed=embed)
        try:
            await ctx.author.edit(nick="[ AFK ] " + original_name)
        except discord.Forbidden:
            pass

    @commands.slash_command()
    async def unafk(self, ctx):
        if str(ctx.author.id) in self.afk_data:
            original_name = self.afk_data[str(ctx.author.id)]["original_name"]
            del self.afk_data[str(ctx.author.id)]
            self.save_afk_data()
            try:
                await ctx.author.edit(nick=original_name)
            except discord.Forbidden:
                pass
            embed = discord.Embed(
                title="AFK Removed", description=f"{ctx.author.mention} Is No Longer AFK", color=discord.Color.green())
            await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        for user_id in [user.id for user in message.mentions]:
            user = message.guild.get_member(user_id)
            if user is None:
                continue

            if str(user_id) in self.afk_data:
                afk_message = self.afk_data[str(user_id)]["message"]
                original_name = self.afk_data[str(user_id)]["original_name"]
                del self.afk_data[str(user_id)]
                self.save_afk_data()

                try:
                    await user.edit(nick=original_name)
                except discord.Forbidden:
                    pass

                embed = discord.Embed(
                    title="User Is AFK", description=f"{user.display_name} Is Currently AFK", color=discord.Color.green())
                
                if afk_message:
                    embed.add_field(name="AFK Message", value=afk_message, inline=False)

                await message.channel.send(embed=embed)

                await user.send(f"You Were Mentioned By {message.author.display_name} In {message.channel.mention}")

        if str(message.author.id) in self.afk_data:
            original_name = self.afk_data[str(message.author.id)]["original_name"]
            del self.afk_data[str(message.author.id)]
            self.save_afk_data()

            try:
                await message.author.edit(nick=original_name)
            except discord.Forbidden:
                pass

            embed = discord.Embed(
                title="AFK Removed", description=f"{message.author.display_name} Is No Longer AFK", color=discord.Color.green())
            await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(AFK(bot))
