import discord
import asyncio
from discord.ext import commands
from discord.utils import get

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def updateMemberCount(self):
        guild = self.client.get_guild(802565984602423367)
        category = guild.get_channel(802565985055014952)
        count = 0
        for member in guild.members:
            if not member.bot:
                count += 1
        await category.edit(name=f'﹕{count} Travelers﹕')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.id != 749422471337476107:
            guild = self.client.get_guild(802565984602423367)
            channel = guild.get_channel(802565985055014956)
            print(f'{member} has joined the server.')
            role = get(member.guild.roles, name="☕")
            await member.add_roles(role)

            # Welcome
            verify = guild.get_channel(802566612187349013)
            embed = discord.Embed(title = "Yawn... Oh ~ Welcome!", description = f"Verify : {verify.mention}\n\n[ {member.mention} ] Enjoy Your Stay ☕", color = discord.Color(0xF8F0E3))
            # embed.set_thumbnail(url=member.avatar_url)
            embed.set_thumbnail(url="https://i.imgur.com/7qz95vU.gif")
            await channel.send(embed=embed)

        await self.updateMemberCount()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the server.')
        await self.updateMemberCount()

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