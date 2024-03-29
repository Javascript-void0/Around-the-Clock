import discord
import asyncio
import datetime
from discord.ext import tasks, commands
from discord.utils import get

def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]

client = commands.Bot(command_prefix='::')

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['cl'], help='Input for Changlogs')
    @commands.has_permissions(administrator=True)
    async def changelog(self, ctx, *, change):
        channel = ctx.guild.get_channel(802571459712516156)
        d = datetime.date.today().strftime("%b %d")
        embed = discord.Embed(title = "Change Log")
        embed.add_field(name = "Date:", value = f'{d}')
        embed.add_field(name = "<:down1:823376679128268850> Changes:", value = f"{change}\n<:down1:823376679128268850> No changes to having a great day :D")
        await channel.send(embed=embed)
        await ctx.send('Created New Changelog')

    @commands.command(aliases=['testwel','testjoin'], help='Test Welcome')
    @commands.has_permissions(administrator=True)
    async def testwelcome(self, ctx):
        member = ctx.author
        verify = ctx.guild.get_channel(802566612187349013)
        lobby = ctx.guild.get_channel(802565985055014956)
        roles = ctx.guild.get_channel(802694715019100161)
        embed = discord.Embed(title = f"Yawn... Oh- Welcome! {member}", description = f"First Verify in {verify.mention} :D.\nThen Grab Some {roles.mention}\nor hangout in {lobby.mention}", color = discord.Color.dark_teal())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_image(url="https://64.media.tumblr.com/752e98a41362e1c7e51c7a50a78c179c/f56cd24a7cd794d6-54/s2048x3072_c0,0,100000,85880/782343118d50eddb426ac93204cac586f38469cd.gif")
        embed.set_footer(text="Enjoy Your Stay {}".format(member.name), icon_url = "https://media.tenor.com/images/dae19cf6b07682c4acf67dfc880f11f5/tenor.gif")
        await ctx.send(member.mention, embed=embed)

    @commands.command(aliases=['testconnect','testcon'], help='Test Join')
    @commands.has_permissions(administrator=True)
    async def testvc(self, ctx):
        channel = ctx.author.voice.channel
        get(self.client.voice_clients, guild=ctx.guild)
        await channel.connect()

    @commands.command(help='Test Bump')
    @commands.has_permissions(administrator=True)
    async def testbump(self, ctx):
        embed = discord.Embed(title = "Disboard is off cooldown!", description  = "Time to bump! 🍌", color = discord.Color.dark_blue())
        embed.set_thumbnail(url="https://i.pinimg.com/originals/ee/b0/e6/eeb0e632af64b76830c5777e07770202.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=['testcl'], help='Test Changlogs')
    @commands.has_permissions(administrator=True)
    async def testchangelog(self, ctx, *, change):
        d = datetime.date.today().strftime("%b %d")
        embed = discord.Embed(title = "Change Log")
        embed.add_field(name = "Date:", value = f'{d}')
        embed.add_field(name = "<:down1:823376679128268850> Changes:", value = f"{change}\n<:down1:823376679128268850> No changes to having a great day :D")
        await ctx.send(embed=embed)

    @commands.command(help='Test sessions format')
    @commands.has_permissions(administrator=True)
    async def testsession(self, ctx, *, message=None):
        mention = discord.utils.get(ctx.guild.roles, name='Study Session')
        if message is None:
            message = 'New Session Started'
        embed = discord.Embed(title = f"⏰ Session Started", description = f"Started by {ctx.author.mention}")
        embed.add_field(name = f"{message}", value = f"`Good Luck ♥`")
        message = await ctx.send(f'{mention.mention} `✔ Session Started', embed=embed)
        embed.set_footer(text=f"End this session with: 12 end {message.id}")
        await message.edit(content=f'{mention.mention} `✔ Session Started`', embed=embed)
        await ctx.message.delete()

    @commands.command(help='Test sessions format')
    @commands.has_permissions(administrator=True)
    async def testhours(self, ctx, link, *, message=None):
        mention = discord.utils.get(ctx.guild.roles, name='Study Session')
        if message is None:
            message = 'New Session Started'
        if "https://hours.zone/invite/" in link:
            embed = discord.Embed(title = f"⏰ Study Session", description = f"Started by {ctx.author.mention}")
            embed.add_field(name = f"{message}", value = f"{link}")
            embed.set_thumbnail(url='https://i.imgur.com/JViNlaE.png')
            message = await ctx.send(f'{mention.mention} `✔ Session Started`', embed=embed)
            embed.set_footer(text=f"End this session with: 12 end {message.id}")
            await message.edit(content=f'{mention.mention} `✔ Session Started`', embed=embed)
            await ctx.message.delete()
        else:
            await ctx.message.delete()
            await ctx.send('Hours Invite Link')

    @commands.command(help='Ends Sessions')
    @commands.has_permissions(administrator=True)
    async def testend(self, ctx, msgid : int = None):
        mention = discord.utils.get(ctx.guild.roles, name='Study Session')
        if msgid is None:
            await ctx.send('`12 end <message id>`')
        elif ctx.channel.id == 802915711122014278:
            message = await ctx.fetch_message(msgid)
            embed = message.embeds[0]
            await message.edit(content=f'{mention.mention} `❌ Session Ended`', embed=embed)
        await ctx.message.delete()

    @commands.command(aliases=['traveler_update', 'mu', 'tu'], help='update member count')
    @commands.has_permissions(administrator=True)
    async def member_update(self, ctx):
        guild = self.client.get_guild(802565984602423367)
        members = guild.get_channel(802737096640036924)
        count = 0
        for member in guild.members:
            if not member.bot:
                count += 1
        await members.edit(name=f'➥ {count} Travelers')
        await ctx.send('Traveler count updated')

def setup(client):
    client.add_cog(Admin(client))