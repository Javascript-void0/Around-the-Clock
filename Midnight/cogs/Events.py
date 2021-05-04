import discord
import asyncio
from discord.ext import commands
from discord.utils import get

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.client.get_guild(802565984602423367)
        channel = guild.get_channel(802565985055014953)
        print(f'{member} has joined the server.')
        role = get(member.guild.roles, name="awake...")
        await member.add_roles(role)

        # Welcome
        verify = ctx.guild.get_channel(802566612187349013)
        lobby = guild.get_channel(802565985055014956)
        roles = ctx.guild.get_channel(802694715019100161)
        embed = discord.Embed(title = f"Yawn... Oh- Welcome! {member}", description = f"First Verify in {verify.mention} :D.\nThen Grab Some {roles.mention}\nor hangout in {lobby.mention}", color = discord.Color.dark_teal())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_image(url="https://64.media.tumblr.com/752e98a41362e1c7e51c7a50a78c179c/f56cd24a7cd794d6-54/s2048x3072_c0,0,100000,85880/782343118d50eddb426ac93204cac586f38469cd.gif")
        embed.set_footer(text="Enjoy Your Stay {}".format(member.name), icon_url = "https://media.tenor.com/images/dae19cf6b07682c4acf67dfc880f11f5/tenor.gif")
        await channel.send(member.mention, embed=embed)

        members = guild.get_channel(802737096640036924)
        count = 0
        for member in guild.members:
            if not member.bot:
                count += 1
        await members.edit(name=f'➥ {count} Travelers')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the server.')
        guild = self.client.get_guild(802565984602423367)
        members = guild.get_channel(802737096640036924)
        count = 0
        for member in guild.members:
            if not member.bot:
                count += 1
        await members.edit(name=f'➥ {count} Travelers')

    @commands.Cog.listener()
    async def on_ready(self):
        print('Started {0.user}'.format(self.client))
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Around the Clock"))

''' Seperate Bot
    @commands.Cog.listener()
    async def on_message(self, message):
        embed = discord.Embed(title = "Disboard is off cooldown!", description  = "Time to bump! 🍌", color = discord.Color.dark_blue())
        embed.set_thumbnail(url="https://i.pinimg.com/originals/ee/b0/e6/eeb0e632af64b76830c5777e07770202.png")
        channel = message.channel
        if message.author.id == 302050872383242240 and 'done' in message.embeds[0].description:
            cd = 7201
            while cd >= 0:
                cd = cd-5
                await asyncio.sleep(5)
                if cd == 0:
                    await channel.send(embed=embed)
        else:
            pass
'''

def setup(client):
    client.add_cog(Events(client))