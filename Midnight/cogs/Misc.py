import discord
import random
from discord.ext import commands

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(help='Latnecy')
    async def ping(self, ctx):
        await ctx.send(f'**Current Ping:** {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['8ball'], help='Tell the future')
    async def _8ball(self, ctx, *, question):
        responses = [
            'It is ceratin.', 'It is decidedly so.', 'Without a doubt.',
            'You may rely on it.', 'As I see it, yes.', 'Most likely.',
            'Outlook good.', 'Yes.', 'Signs point to yes.',
            'Reply hazy, try again.', 'Ask again later.',
            'Better not tell you now.', 'Cannot predict now.',
            'Concentrate and ask again.', "Don't count on it.", 'My reply is no.',
            'My sources say no.', 'Outlook not so good.', 'Very doubtful.'
        ]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(help='Returns the number of members online')
    async def online(self, ctx):
        online = 0
        total = 0
        for member in ctx.guild.members:
            total += 1
            if member.status != discord.Status.offline:
                online += 1
        await ctx.send(f'{online}/{total} Online Members')

    @commands.command(help='Returns the number of bots')
    async def bots(self, ctx):
        bot = 0
        for member in ctx.guild.members:
            if member.bot:
                bot +=1
        await ctx.send(f'{bot} Bots in {ctx.guild.name}')

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

    @commands.command(help='Sever Invite Link')
    async def invite(self, ctx):
        await ctx.send('https://discord.gg/nk69jVbJMP')

def setup(client):
    client.add_cog(Misc(client))