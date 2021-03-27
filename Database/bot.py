import discord
import os
import asyncio
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.')
client.remove_command('help')
TOKEN = os.getenv("DB_TOKEN")

guild = None
db = None
count = {}
time = {}

async def timerStart(member):
    time[member.id] = 0
    count[member.id] = True
    while count[member.id] == True:
        await asyncio.sleep(1)
        time[member.id] += 1

async def getData(member):
    global db
    id = member.id
    messages = await db.history(limit=None).flatten()
    for msg in messages:
        m = msg.content.split(": ")
        if str(id) in m[0]:
            return m, msg

async def registered(member):
    global db
    id = member.id
    messages = await db.history(limit=None).flatten()
    for msg in messages:
        m = msg.content.split(": ")
        if str(id) in m[0]:
            return True
    return False

@client.event
async def on_ready():
    global db, guild
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="#▹💾▹database"))
    guild = client.get_guild(805299220935999509)
    db = guild.get_channel(825053228956647464)
    print('[ + ] Started {0.user}'.format(client))
    print(f'[ + ] #{db} Connected to database... :P')

@client.event
async def on_voice_state_update(member, before, after):
    global db
    if before.channel is None:
        print(f'{member} joined #{after.channel.name}')
        if await registered(member):
            data, msg = await getData(member)
            await timerStart(member)
        else:
            embed = discord.Embed(title=f"{member.name}'s Stats", description=f'\n\n**Stats**: 0 Hours')
            await db.send(f'{member.mention}: 0')
            await timerStart(member)
    elif after.channel is None:
        print(f'{member} left #{before.channel.name}')
        data, msg = await getData(member)
        count[member.id] = False
        addTime = int(data[1]) + time[member.id]
        embed = discord.Embed(title=f"{member.name}'s Stats", description=f'\n\n**Stats**: {addTime} Hours')
        await msg.edit(content=f'{member.mention}: {addTime}', embed=embed)

@client.command(help='Add score to user')
@commands.has_permissions(administrator=True)
async def add(ctx, member : discord.Member, amount : int):
    if await registered(member):
        data, msg = await getData(member)
        newTime = amount + int(data[1])
        embed = discord.Embed(title=f"{member.name}'s Stats", description=f'\n\n**Stats**: {newTime} Hours')
        await msg.edit(content=f'{data[0]}: {newTime}', embed=embed)
        await ctx.send(f'Added {amount} hours to {member.mention}')
    else:
        await ctx.send(f'{member} has no data')

@client.command(aliases=['subtract'], help='Remove score from user')
@commands.has_permissions(administrator=True)
async def remove(ctx, member : discord.Member, amount : int):
    if await registered(member):
        data, msg = await getData(member)
        newTime = int(data[1]) - amount
        if newTime < 0:
            newTime = 0
        embed = discord.Embed(title=f"{member.name}'s Stats", description=f'\n\n**Stats**: {newTime} Hours')
        await msg.edit(content=f'{data[0]}: {newTime}', embed=embed)
        await ctx.send(f'Removed {amount} hours from {member.mention}')
    else:
        await ctx.send(f'{member} has no data')

@client.command(help='Set score for user')
@commands.has_permissions(administrator=True)
async def set(ctx, member : discord.Member, amount : int):
    if await registered(member):
        data, msg = await getData(member)
        if amount < 0:
            amount = 0
        embed = discord.Embed(title=f"{member.name}'s Stats", description=f'\n\n**Stats**: {amount} Hours')
        await msg.edit(content=f'{data[0]}: {amount}', embed=embed)
        await ctx.send(f'Set hours of {member.mention} to {amount}')
    else:
        await ctx.send(f'{member} has no data')

@client.command(help='Find stats of a user')
async def stats(ctx, member : discord.Member):
    if await registered(member):
        data, _ = await getData(member)
        embed = discord.Embed(title=f"{member.name}'s Stats", description=f'\n\n**Stats**: {int(data[1])} Hours')
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'{member} has not data')

@client.command(help='Registers a user')
@commands.has_permissions(administrator=True)
async def register(ctx, member : discord.Member):
    global db
    if await registered(member):
        await ctx.send(f'{member.mention} is already registered')
    else:
        embed = discord.Embed(title=f"{member.name}'s Stats", description=f'\n\n**Stats**: 0 Hours')
        await db.send(f'{member.mention}: 0', embed=embed)
        await ctx.send(f'Registered {member.mention}')
if __name__ == '__main__':
    client.run(TOKEN)