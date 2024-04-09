import json
import asyncio
import datetime

import discord
from discord.ext import commands, tasks


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_reminders.start()

        try:
            with open('Reminders.json', 'r') as f:
                self.reminders = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.reminders = {}

    def cog_unload(self):
        self.check_reminders.cancel()

    def save_reminders(self):
        with open('Reminders.json', 'w') as f:
            json.dump(self.reminders, f, indent=4)

    @tasks.loop(seconds=10)
    async def check_reminders(self):
        to_delete = []
        for user_id, reminders in self.reminders.items():
            for reminder_data in reminders:
                remind_time = datetime.datetime.fromisoformat(reminder_data['remind_time'])
                if remind_time <= datetime.datetime.utcnow():
                    try:
                        user = await self.bot.fetch_user(int(user_id))
                        embed = discord.Embed(
                            title="Reminder", description=reminder_data['reminder'], color=discord.Color.blue())
                        await user.send(embed=embed)
                        to_delete.append((user_id, reminder_data))

                    except discord.Forbidden:
                        embed = discord.Embed(
                            title="Reminder Not Sent", description='Please Enable DMs To Get Reminders', color=discord.Color.red())

                        await user.send(embed=embed, view=Reminder_DM_Error())
                        to_delete.append((user_id, reminder_data))

        for user_id, reminder_data in to_delete:
            self.reminders[user_id].remove(reminder_data)
        self.save_reminders()

    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()

    @commands.slash_command(name='remind', description='Sets A Reminder')
    async def remind(self, ctx, time_str, *, reminder):
        try:
            time = int(time_str[:-1])
            unit = time_str[-1]
        except ValueError:
            await ctx.respond("Reminder Not Set", view=Reminder_Usage())
            return

        if unit == 's':
            delta = datetime.timedelta(seconds=time)
        elif unit == 'm':
            delta = datetime.timedelta(minutes=time)
        elif unit == 'h':
            delta = datetime.timedelta(hours=time)
        elif unit == 'd':
            delta = datetime.timedelta(days=time)
        else:
            await ctx.respond("Reminder Not Set", view=Reminder_Usage())
            return

        remind_time = datetime.datetime.utcnow() + delta
        if str(ctx.author.id) not in self.reminders:
            self.reminders[str(ctx.author.id)] = []
        self.reminders[str(ctx.author.id)].append({
            'start_time': str(datetime.datetime.utcnow()),
            'remind_time': remind_time.isoformat(),
            'reminder': reminder
        })
        self.save_reminders()
        embed = discord.Embed(
            title="Reminder Set", description=f"Reminder Set For {time}{unit} From Now.", color=discord.Color.green())
        await ctx.respond(embed=embed, view=Reminder_List(bot=self.bot, reminders=self.reminders))

    @commands.slash_command(name='reminders', description='Shows All Reminders')
    async def reminders(self, ctx):
        user_id = str(ctx.author.id)
        if user_id in self.reminders and self.reminders[user_id]:
            embed = discord.Embed(title="Your Reminders", color=discord.Color.blue())
            for index, data in enumerate(self.reminders[user_id], start=1):
                embed.add_field(name=f"Reminder {index}: {data['reminder']}", value=f"Remind Time: {data['remind_time']}", inline=False)
            await ctx.respond(embed=embed, view=Reminder_Delete(bot=self.bot,reminders=self.reminders))
        else:
            embed = discord.Embed(
                title="No Reminders", description="You Don't Have Any Reminders Set", color=discord.Color.red())
            await ctx.respond(embed=embed)

    @commands.slash_command(name='delete_reminder', description='Deletes A Reminder')
    async def delete_reminder(self, ctx):
        user_id = str(ctx.author.id)
        if user_id in self.reminders and self.reminders[user_id]:
            del self.reminders[user_id][-1]
            self.save_reminders()
            embed = discord.Embed(
                title="Reminder Deleted", description="Your Reminder Has Been Deleted", color=discord.Color.green())
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(
                title="No Reminders", description="You Don't Have Any Reminders Set", color=discord.Color.red())
            await ctx.respond(embed=embed)

class Reminder_Delete_Modal(discord.ui.Modal):
    def __init__(self, save_reminders, reminders, **kwargs):
        super().__init__(**kwargs)
        self.reminders = reminders
        self.save_reminders = save_reminders

        self.input = None
        self.add_item(discord.ui.InputText(label="Enter Reminder Number To Delete", placeholder="Enter Reminder Number To Delete"))

    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)

        if user_id in self.reminders and self.reminders[user_id]:
            try:
                index = int(self.children[0].value) - 1
                if index < 0 or index >= len(self.reminders[user_id]):
                    await interaction.response.send_message(
                        "Invalid Index Number. Please Enter A Valid Number.",
                        ephemeral=True
                    )
                    return
                del self.reminders[user_id][index]
                self.save_reminders()
                await interaction.response.send_message("Reminder Deleted", ephemeral=True)

            except asyncio.TimeoutError:
                await interaction.response.send_message("Timeout. Please Try Again.", ephemeral=True)
        
        else:
            await interaction.response.send_message("You Don't Have Any Reminders Set", ephemeral=True)

    async def on_timeout(self) -> None:
        await self.message.edit(view=None)




class Reminder_List(discord.ui.View):

    def __init__(self,bot, reminders):
        super().__init__()
        self.bot = bot
        self.reminders = reminders

    @discord.ui.button(label="Show Reminders", style=discord.ButtonStyle.secondary, emoji="📅")
    async def show_reminders(self, button: discord.ui.Button, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        if user_id in self.reminders and self.reminders[user_id]:
            embed = discord.Embed(title="Your Reminders", color=discord.Color.blue())
            for index, data in enumerate(self.reminders[user_id], start=1):
                embed.add_field(name=f"Reminder {index}: {data['reminder']}", value=f"Remind Time: {data['remind_time']}", inline=False)
            await interaction.response.send_message(embed=embed, view=Reminder_Delete(bot=self.bot, reminders=self.reminders, save_reminders=self.bot.get_cog('Reminder').save_reminders))
        else:
            embed = discord.Embed(
                title="No Reminders", description="You Don't Have Any Reminders Set", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)


class Reminder_Delete(discord.ui.View):

    def __init__(self, bot, reminders, save_reminders):
        super().__init__()
        self.bot = bot
        self.reminders = reminders
        self.save_reminders = save_reminders

    @discord.ui.button(label="Delete All Reminders", style=discord.ButtonStyle.danger, emoji="❎")
    async def delete_all_reminders(self, button: discord.ui.Button, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        if user_id in self.reminders and self.reminders[user_id]:
            del self.reminders[user_id]

            self.bot.get_cog('Reminder').save_reminders()
            embed = discord.Embed(
                title="Reminders Deleted", description="All Your Reminders Have Been Deleted", color=discord.Color.green())
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="No Reminders", description="You Don't Have Any Reminders Set", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Delete Reminder", style=discord.ButtonStyle.danger, emoji="❎")
    async def delete_reminder(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(Reminder_Delete_Modal(reminders=self.reminders,save_reminders=self.save_reminders, title="Delete Reminder"))




class Reminder_Usage(discord.ui.View):

    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Check Usage", style=discord.ButtonStyle.secondary, emoji="❗")
    async def check_usage(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Error",
            description="Wrong Time Unit",
            color=0x2f3136
        )

        embed.add_field(
            name="Example", value="`/remind 10s Do Something`", inline=False)

        embed.add_field(
            name="Unit Format", value="`s` - Seconds \n`m` - Minutes\n`h` - Hours", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


class Reminder_DM_Error(discord.ui.View):

    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Check Usage", style=discord.ButtonStyle.secondary, emoji="❗")
    async def check_usage(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Possible Error : DMs Not Enabled",
            description="Please Enable DMs Form Server Settings / User Settings",
            color=0x2f3136
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Reminder(bot))
