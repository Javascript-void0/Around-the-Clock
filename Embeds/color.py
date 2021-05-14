import time
import discord
import os
from discord.utils import get
from discord.ext import commands


client = commands.Bot(command_prefix=".")
TOKEN = os.getenv("TOKEN")

originalRoles = '''cozy: #eeadad
sunrise: #d8b2d4
bright: #e9cd87
clover: #89cf95
cloud: #8dbfdb
sunset: #a7a2de
anonymous: #596d90
'''
dreamRoles = '''Dreamscape 1: #c9cca1
Dreamscape 2: #caa05a
Dreamscape 3: #ae6a47
Dreamscape 4: #8b4049
Dreamscape 5: #543344
Dreamscape 6: #515262
Dreamscape 7: #63787d
Dreamscape 8: #8ea091
'''
greenRoles = '''light: #ebff9f
green: #a5c35c
dark: #62811a
'''
blueRoles = '''light: #edffff
blue: #a7bbd7
dark: #667993
'''
pinkRoles = '''light: #ffe3f0
pink: #f5a1aa
dark: #ad5f6a
'''
grayRoles = '''light: #f2f2f2
gray: #acacac
dark: #6c6c6c
'''
orangeRoles = '''light: #ffdc89
orange: #de9848
dark: #955801
'''
purpleRoles = '''light: #fff2ff
purple: #caacf4
dark: #866bad
'''
brownRoles = '''light: #fffccb
brown: #ccb587
dark: #887449
'''

async def role(ctx, line):
    java = ctx.author
    line = line.split(":")
    name = line[0]
    color = discord.Color(int(line[1].replace(" #", "0x"), 16))
    role = await ctx.guild.create_role(name=name, color=color)
    await java.add_roles(role)
    print("Created {}".format(name))

@client.command(pass_context=True, help='Original Colors')
@commands.has_permissions(administrator=True)
async def create(ctx, option):
    if option == 'original':
        for line in originalRoles.splitlines():
            await role(ctx, line)
    if option == 'dream':
        for line in dreamRoles.splitlines():
            await role(ctx, line)
    if option == 'green':
        for line in greenRoles.splitlines():
            await role(ctx, line)
    if option == 'blue':
        for line in blueRoles.splitlines():
            await role(ctx, line)
    if option == 'pink':
        for line in pinkRoles.splitlines():
            await role(ctx, line)
    if option == 'gray':
        for line in grayRoles.splitlines():
            await role(ctx, line)
    if option == 'orange':
        for line in orangeRoles.splitlines():
            await role(ctx, line)
    if option == 'purple':
        for line in purpleRoles.splitlines():
            await role(ctx, line)
    if option == 'brown':
        for line in brownRoles.splitlines():
            await role(ctx, line)
            
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