import discord
import os
import asyncio
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='::')
TOKEN = os.getenv("TOKEN")

guild = None
db = None

async def getData(member):
    global db
    messages = await db.history(limit=None).flatten()
    for msg in messages:
        m = msg.content.split(": ")
        if str(member.id) in m[0]:
            return m, msg

async def registered(member):
    global db
    messages = await db.history(limit=None).flatten()
    for msg in messages:
        if str(member.id) in msg.content:
            return True
    return False

@client.event
async def on_ready():
    global db, guild
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="#▹💾▹database"))
    guild = client.get_guild(805299220935999509)
    db = guild.get_channel(825053228956647464)
    print('[ + ] Started {0.user}'.format(client))
    print(f'[ + ] Connected to database...')

@client.event
async def on_message(message):
    global db
    if message.author.bot:
        return
    if message.channel.name in ['🌵▹lobby', '🔍▹bump_us', '📚▹resources', '⏰▹sessions', '💪▹motivation', '🌴▹lobby_int', '❓▹hw_help', '📷▹media', '💡▹suggestions', 'general']:
        if await registered(message.author):
            data, msg = await getData(message.author)
            new = int((data[1])[:-3]) + 1
            await msg.edit(content=f'```{message.author} [{message.author.id}]: {new}```')
        else:
            await db.send(f'```{message.author} [{message.author.id}]: 1```')

@client.command(help='Set score for user')
@commands.has_permissions(administrator=True)
async def set(ctx, member : discord.Member, amount : int):
    if member.bot:
        return
    if await registered(member):
        data, msg = await getData(member)
        if amount < 0:
            amount = 0
        embed = discord.Embed(title=f"{member.name}'s Stats", description=f'\n\n**Stats**: {amount} Hours\n**Tasks**: 5')
        await msg.edit(content=f'{data[0]}: {amount}', embed=embed)
        await ctx.send(f'Set hours of {member.mention} to {amount}')
    else:
        await ctx.send(f'{member} has no data')

@client.command(help='Find stats of a user')
async def stats(ctx, member : discord.Member):
    if member.bot:
        return
    if await registered(member):
        data, _ = await getData(member)
        await ctx.send(f'```{member} [{member.id}]: {int((data[1])[:-3])}```')
    else:
        await ctx.send(f'{member} has not data')

@client.command(help='Registers a user')
@commands.has_permissions(administrator=True)
async def register(ctx, member : discord.Member):
    global db
    if member.bot:
        return
    if await registered(member):
        await ctx.send(f'{member} is already registered')
    else:
        await db.send(f'```{member} [{member.id}]: 0```')
        await ctx.send(f'Registered {member.mention}')

if __name__ == '__main__':
    client.run(TOKEN)