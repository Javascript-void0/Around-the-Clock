import discord
import asyncio
from discord.utils import get
from discord.ext import commands
from time import sleep
from random import randint

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['purge'], help='Clears certin number of messages')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'Cleared {amount} messages', delete_after=5)
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify an amount of messages to delete.')
            
    @commands.command(aliases=['user','info'], help='Info about a user')
    @commands.has_permissions(kick_members=True)
    async def whois(self, ctx, member : discord.Member):
        embed = discord.Embed(title = member.name, description = member.mention)
        embed.add_field(name = "ID", value = member.id, inline = True)
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(help='Kick member from Server')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member} for {reason}')

    @commands.command(help='Ban member from Server')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member} for {reason}')

    @commands.command(help='Unban members from Server')
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @commands.command(aliases=['guild'], help='Server Stats')
    async def server(self, ctx):
        online = 0
        idle = 0
        dnd = 0
        bot = 0
        totalOnline = 0
        for member in ctx.guild.members:
            if member.bot:
                bot += 1
            if member.status != discord.Status.offline:
                totalOnline += 1
            if member.status == discord.Status.online:
                online += 1
            elif member.status == discord.Status.idle:
                idle += 1
            elif member.status == discord.Status.do_not_disturb:
                dnd += 1
        embed = discord.Embed(title=f'Statistics for {ctx.guild.name}', description=f'Owner: {ctx.guild.owner.mention}\nID: {ctx.guild.id}')
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.add_field(name='Channels', value=f'{len(ctx.guild.channels)} Channels', inline=True)
        embed.add_field(name='Bots', value=f'{bot} Bots', inline=True)
        embed.add_field(name='Roles', value=f'{len(ctx.guild.roles)} Roles', inline=True)
        embed.add_field(name='Emoji', value=f'{len(ctx.guild.emojis)} Emojis', inline=True)

        eMember = discord.Embed(title=f'Statistics for {ctx.guild.name}', description=f'Owner: {ctx.guild.owner.mention}\nID: {ctx.guild.id}')
        eMember.set_thumbnail(url=f'{ctx.guild.icon_url}')
        eMember.add_field(name='Members', value=f'{len(ctx.guild.members)} Total Members\n\n**Total Online:** {totalOnline}', inline=False)
        eMember.add_field(name='Online', value=f'{online} Online', inline=True)
        eMember.add_field(name='Idle', value=f'{idle} Idle', inline=True)
        eMember.add_field(name='Do Not Disturb', value=f'{dnd} DND', inline=True)
        
        await ctx.send(embed=embed)
        await ctx.send(embed=eMember)

    @commands.command(help='Latnecy')
    async def ping(self, ctx):
        await ctx.send(f'**Current Ping:** {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['ani'], help='Loading Bar...?')
    async def animation(self, ctx):
        bar = await ctx.send("```[:::::::::::::::::::::::::] 0.0%```")
        sleep(1)
        await bar.edit(content="```[>::::::::::::::::::::::::] 4.0%```")
        sleep(1)
        await bar.edit(content="```[>>:::::::::::::::::::::::] 8.0%```")
        sleep(1)
        await bar.edit(content="```[>>>::::::::::::::::::::::] 12.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>:::::::::::::::::::::] 16.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>::::::::::::::::::::] 20.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>:::::::::::::::::::] 24.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>::::::::::::::::::] 28.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>:::::::::::::::::] 32.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>::::::::::::::::] 36.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>:::::::::::::::] 40.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>::::::::::::::] 44.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>:::::::::::::] 48.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>>::::::::::::] 52.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>>>:::::::::::] 56.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>>>>::::::::::] 60.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>>>>>:::::::::] 64.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>>>>>>::::::::] 68.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>>>>>>>:::::::] 72.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>::::::] 76.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>>:::::] 80.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>>>::::] 84.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>>>>:::] 88.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>>>>>::] 92.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>>>>>>:] 96.0%```")
        sleep(1)
        await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>>>>>>>] 100.0%```")

    @commands.command(help='High-low Game (Dank Memer)')
    async def highlow(self, ctx):
        num = randint(1,100)
        hint = randint(1,100)
        embed = discord.Embed(title=f"{ctx.author.name}'s high-low game", description=f'A number secret between 1-100 has been chosen. Your hint is **{hint}**.\nRespond with "high", "low", or "jackpot".')
        embed.set_footer(text='Choose whether you think the hidden number is higher, lower, or the same number as the hint')
        await ctx.send(embed=embed)

        lEmbed = discord.Embed(title=f"{ctx.author.name}'s losing high-low game\nYou lost!", description=f'Your hint was **{hint}**. The hidden number was **{num}**.', color=discord.Color.red())
        lEmbed.set_footer(text='loser loser')
        wEmbed = discord.Embed(title=f"{ctx.author.name}'s winning high-low game\nYou won!", description=f'Your hint was **{hint}**. The hidden number was **{num}**.', color=discord.Color.green())
        wEmbed.set_footer(text='Multi Bonus: +0% (⏣69)')

        try:
            input = await self.client.wait_for('message', check=None, timeout=30)

            if input.author.bot:
                pass
            if input.content == "high":
                if num > hint:
                    await ctx.send(embed=wEmbed)
                else:
                    await ctx.send(embed=lEmbed)
            elif input.content == "low":
                if num < hint:
                    await ctx.send(embed=wEmbed)
                else:
                    await ctx.send(embed=lEmbed)
            elif input.content == "jackpot":
                if num == hint:
                    await ctx.send(embed=wEmbed)
                else:
                    await ctx.send(embed=lEmbed)
            else:
                await ctx.send(f'{ctx.author.mention} Hey your options to respond are "high", "low", and "jackpot". Run the command again with more brain cells next time. (Number was {num} btw)')
        except asyncio.TimeoutError:
            await ctx.send('Imagine not answering')

def setup(client):
    client.add_cog(Commands(client))