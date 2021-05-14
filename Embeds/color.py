import time
import discord
import os
from discord.utils import get
from discord.ext import commands


client = commands.Bot(command_prefix=".")
TOKEN = os.getenv("TOKEN")

originalRoles = """cozy: #eeadad
sunrise: #d8b2d4
bright: #e9cd87
clover: #89cf95
cloud: #8dbfdb
sunset: #a7a2de
anonymous: #596d90
"""

dreamRoles = """Dreamscape 1: #c9cca1
Dreamscape 2: #caa05a
Dreamscape 3: #ae6a47
Dreamscape 4: #8b4049
Dreamscape 5: #543344
Dreamscape 6: #515262
Dreamscape 7: #63787d
Dreamscape 8: #8ea091
"""

@client.command(pass_context=True, help='Original Colors')
@commands.has_permissions(administrator=True)
async def create(ctx, option):
    java = ctx.author
    if option == 'original':
        for line in originalRoles.splitlines():
            line = line.split(":")
            name = line[0]
            color = discord.Color(int(line[1].replace(" #", "0x"), 16))
            role = await ctx.guild.create_role(name=name, color=color)
            await java.add_roles(role)
            print("Created {}".format(name))
    elif option == 'dream':
        for line in dreamRoles.splitlines():
            line = line.split(":")
            name = line[0]
            color = discord.Color(int(line[1].replace(" #", "0x"), 16))
            role = await ctx.guild.create_role(name=name, color=color)
            await java.add_roles(role)
            print("Created {}".format(name))

@create.error
async def create_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('```.create <original | dream>```')


@client.command(name='del', pass_context=True, help='Clears Roles')
@commands.has_permissions(administrator=True)
async def _del(ctx):
    for role in ctx.guild.roles:
        try:
            await role.delete()
            print(f'Deleted {role.name}')
        except:
            pass

if __name__ == "__main__":
    client.run(TOKEN)