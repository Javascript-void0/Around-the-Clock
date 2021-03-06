import discord
import asyncio
from datetime import datetime
from discord.ext import tasks, commands
from discord.utils import get

def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]

client = commands.Bot(command_prefix='12 ')

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['cl'], help='Input for Changlogs')
    @commands.has_role("Admin")
    async def changelog(self, ctx, date, message):
        guild = self.client.get_guild(802565984602423367)
        channel = guild.get_channel(802571459712516156)
        embed = discord.Embed(title = "Change Log", color = discord.Color.green())
        embed.add_field(name = "Date:", value = date)
        embed.add_field(name = "Changes:", value = message)
        embed.set_thumbnail(url="https://media2.giphy.com/media/2ceckIBeAIKqw7awPO/giphy.gif")
        await channel.send(embed=embed)
        await ctx.send('Created New Changelog')

    @commands.command(aliases=['testwel','testjoin'], help='Test Welcome')
    @commands.has_permissions(administrator=True)
    async def testwelcome(self, ctx):
        member = ctx.author
        guild = self.client.get_guild(802565984602423367)
        role = guild.get_channel(802581706816487474)
        lobby = guild.get_channel(802565985055014956)
        embed = discord.Embed(title = "Yawn... Oh! Welcome :D", description = f"Welcome to Around the Clock {member.mention}!\nFirst Verify in {role.mention} :D\nThen Grab Some Roles, or hangout in {lobby.mention}", color = discord.Color.dark_teal())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_image(url="https://64.media.tumblr.com/752e98a41362e1c7e51c7a50a78c179c/f56cd24a7cd794d6-54/s2048x3072_c0,0,100000,85880/782343118d50eddb426ac93204cac586f38469cd.gif")
        embed.set_footer(text="Enjoy Your Stay", icon_url = "https://media.tenor.com/images/dae19cf6b07682c4acf67dfc880f11f5/tenor.gif")
        await ctx.send(embed=embed)

    @commands.command(aliases=['testconnect','testcon'], help='Test Join')
    @commands.has_permissions(administrator=True)
    async def testvc(self, ctx):
        channel = ctx.author.voice.channel
        get(self.client.voice_clients, guild=ctx.guild)
        await channel.connect()

    @commands.command(help='Test Bump')
    @commands.has_permissions(administrator=True)
    async def testbump(self, ctx):
        embed = discord.Embed(title = "Disboard is off cooldown!", description  = "Time to bump! ????", color = discord.Color.dark_blue())
        embed.set_thumbnail(url="https://i.pinimg.com/originals/ee/b0/e6/eeb0e632af64b76830c5777e07770202.png")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Admin(client))