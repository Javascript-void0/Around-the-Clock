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
        embed = discord.Embed(title = "Yawn... Oh! Welcome :D", description = f"Make sure to verify first... {member.mention}", color = discord.Color.blue())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_image(url="https://media3.giphy.com/media/pVGsAWjzvXcZW4ZBTE/giphy.gif")
        embed.set_footer(text="Enjoy Your Stay", icon_url = member.avatar_url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the server.')

    @commands.Cog.listener()
    async def on_ready(self):
        print('Started {0.user}'.format(self.client))
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Around the Clock"))

    @commands.Cog.listener()
    async def on_message(self, ctx, message):
        embed = discord.Embed(title = "Disboard is off cooldown!", description  = "Time to bump! 🍌", color = discord.Color.dark_blue())
        embed.set_thumbnail(url="https://i.pinimg.com/originals/ee/b0/e6/eeb0e632af64b76830c5777e07770202.png")
        if message.author.id == 302050872383242240 and 'done' in message.embeds[0].description:
            cd = 7201
            while cd >= 0:
                cd = cd-5
                await asyncio.sleep(5)
                if cd == 0:
                    await ctx.send(embed=embed)
        else:
            pass

def setup(client):
    client.add_cog(Events(client))