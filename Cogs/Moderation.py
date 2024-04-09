import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='kick',
        description='Kicks a Member',
    )
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if not await self.check_permissions(ctx, member):
            return await ctx.respond('You Dont Have Permission To Kick This')

        await member.kick(reason=reason)
        embed = discord.Embed(
            title='Member Kicked', description=f'{member.mention} Has Been Kicked', color=discord.Color.red())
        embed.add_field(name='Reason', value=reason or 'No Reason Provided')
        await ctx.respond(embed=embed)

    @commands.slash_command(
        name='ban',
        description='Bans a Member',
        
    )
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if not await self.check_permissions(ctx, member):
            return await ctx.respond('You Do Not Have Permission To Ban This Member.')

        await member.ban(reason=reason)
        embed = discord.Embed(
            title='Member Banned', description=f'{member.mention} Has Been Banned.', color=discord.Color.red())
        embed.add_field(name='Reason', value=reason or 'No reason provided')
        await ctx.respond(embed=embed)

    @commands.slash_command(
        name='unban',
        description='Unbans a Member',
        
    )
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    title='Member Unbanned', description=f'{user.mention} Has Been Unbanned.', color=discord.Color.green())
                await ctx.respond(embed=embed)
                return
            
        await ctx.respond('Member Not Found')

    @commands.slash_command(name = 'delete', description = 'Deletes Messages')
    async def delete(self, ctx, amount: int):
        if not await self.check_permissions(ctx, ctx.author):
            return await ctx.respond('You Do Not Have Permission To Delete Messages')

        await ctx.channel.purge(limit = amount + 1)
        embed = discord.Embed(title = 'Messages Deleted', description = f'{amount} Messages Have Been Deleted', color = discord.Color.red())
        await ctx.respond(embed = embed)

    @commands.slash_command(name = 'nuke', description = 'Nukes The Channel')
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        if not await self.check_permissions(ctx, ctx.author):
            return await ctx.respond('You Do Not Have Permission To Nuke This Channel')

        channel = channel or ctx.channel
        position = channel.position
        new_channel = await channel.clone()
        await channel.delete()
        await new_channel.edit(position = position)
        embed = discord.Embed(title = 'Channel Nuked', description = f'{channel.mention} Has Been Nuked', color = discord.Color.red())
        await new_channel.send(embed = embed)


    async def check_permissions(self, ctx, member):
        author_permissions = ctx.channel.permissions_for(ctx.author)
        target_permissions = ctx.channel.permissions_for(member)

        return author_permissions.kick_members and author_permissions.ban_members and author_permissions.administrator


    @commands.slash_command(name = 'mute', description = 'Mutes A Member')
    async def mute(self, ctx, member: discord.Member, *, reason = None):
        if not await self.check_permissions(ctx, member):
            return await ctx.respond('You Do Not Have Permission To Mute This Member')

        role = discord.utils.get(ctx.guild.roles, name = 'Muted')

        if role is None:
            role = await ctx.guild.create_role(name = 'Muted')

            for channel in ctx.guild.text_channels:
                await channel.set_permissions(role, send_messages = False)

        await member.add_roles(role, reason = reason)
        embed = discord.Embed(title = 'Member Muted', description = f'{member.mention} Has Been Muted', color = discord.Color.red())
        embed.add_field(name = 'Reason', value = reason or 'No Reason Provided')
        await ctx.respond(embed = embed)

    @commands.slash_command(name = 'unmute', description = 'Unmutes A Member')
    async def unmute(self, ctx, member: discord.Member):
        if not await self.check_permissions(ctx, member):
            return await ctx.respond('You Do Not Have Permission To Unmute This Member')

        role = discord.utils.get(ctx.guild.roles, name = 'Muted')

        if role is None:
            return await ctx.respond('Member Is Not Muted')

        await member.remove_roles(role)
        embed = discord.Embed(title = 'Member Unmuted', description = f'{member.mention} Has Been Unmuted', color = discord.Color.green())
        await ctx.respond(embed = embed)


    @commands.slash_command(name = 'slowmode', description = 'Sets Slowmode In A Channel')
    async def slowmode(self, ctx, time: int):
        if not await self.check_permissions(ctx, ctx.author):
            return await ctx.respond('You Do Not Have Permission To Set Slowmode')

        await ctx.channel.edit(slowmode_delay = time)
        embed = discord.Embed(title = 'Slowmode Set', description = f'Slowmode Set To {time} Seconds', color = discord.Color.green())
        await ctx.respond(embed = embed)

    @commands.slash_command(name = 'lock', description = 'Locks A Channel')
    async def lock(self, ctx):
        if not await self.check_permissions(ctx, ctx.author):
            return await ctx.respond('You Do Not Have Permission To Lock This Channel')

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
        embed = discord.Embed(title = 'Channel Locked', description = f'{ctx.channel.mention} Has Been Locked', color = discord.Color.red())
        await ctx.respond(embed = embed)

    @commands.slash_command(name = 'unlock', description = 'Unlocks A Channel')
    async def unlock(self, ctx):
        if not await self.check_permissions(ctx, ctx.author):
            return await ctx.respond('You Do Not Have Permission To Unlock This Channel')

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = True)
        embed = discord.Embed(title = 'Channel Unlocked', description = f'{ctx.channel.mention} Has Been Unlocked', color = discord.Color.green())
        await ctx.respond(embed = embed)

    @commands.slash_command(name = 'roleadd', description = 'Adds A Role To A Member')
    async def roleadd(self, ctx, member: discord.Member, role: discord.Role):
        if not await self.check_permissions(ctx, member):
            return await ctx.respond('You Do Not Have Permission To Add Role To This Member')

        await member.add_roles(role)
        embed = discord.Embed(title = 'Role Added', description = f'{role.mention} Has Been Added To {member.mention}', color = discord.Color.green())
        await ctx.respond(embed = embed)

    @commands.slash_command(name = 'roleremove', description = 'Removes A Role From A Member')
    async def roleremove(self, ctx, member: discord.Member, role: discord.Role):
        if not await self.check_permissions(ctx, member):
            return await ctx.respond('You Do Not Have Permission To Remove Role From This Member')

        await member.remove_roles(role)
        embed = discord.Embed(title = 'Role Removed', description = f'{role.mention} Has Been Removed From {member.mention}', color = discord.Color.red())
        await ctx.respond(embed = embed)

    @commands.slash_command(name = 'rolecreate', description = 'Creates A Role')
    async def rolecreate(self, ctx, name: str, color: discord.Color):
        if not await self.check_permissions(ctx, ctx.author):
            return await ctx.respond('You Do Not Have Permission To Create Role')

        await ctx.guild.create_role(name = name, color = color)
        embed = discord.Embed(title = 'Role Created', description = f'Role {name} Has Been Created', color = discord.Color.green())
        await ctx.respond(embed = embed)

    @commands.slash_command(name = 'roledelete', description = 'Deletes A Role')
    async def roledelete(self, ctx, role: discord.Role):
        if not await self.check_permissions(ctx, ctx.author):
            return await ctx.respond('You Do Not Have Permission To Delete Role')

        await role.delete()
        embed = discord.Embed(title = 'Role Deleted', description = f'Role {role.name} Has Been Deleted', color = discord.Color.red())
        await ctx.respond(embed = embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
