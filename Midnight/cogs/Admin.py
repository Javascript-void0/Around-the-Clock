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
        embed = discord.Embed(title = "Yawn... Oh! Welcome :D", description = f"Make sure to verify first... {member.mention}", color = discord.Color.blue())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_image(url="https://media3.giphy.com/media/pVGsAWjzvXcZW4ZBTE/giphy.gif")
        embed.set_footer(text="Enjoy Your Stay", icon_url = member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['testconnect','testcon'], help='Test Join')
    @commands.has_permissions(administrator=True)
    async def testvc(self, ctx):
        channel = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice = await channel.connect()

    @commands.command(help='Test Bump')
    @commands.has_permissions(administrator=True)
    async def testbump(self, ctx):
        embed = discord.Embed(title = "Disboard is off cooldown!", description  = "Time to bump! 🍌", color = discord.Color.dark_blue())
        embed.set_thumbnail(url="https://i.pinimg.com/originals/ee/b0/e6/eeb0e632af64b76830c5777e07770202.png")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Admin(client))