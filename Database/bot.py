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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the Database"))
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
            await db.send(f'{member.mention}: 0')
            await timerStart(member)
    elif after.channel is None:
        print(f'{member} left #{before.channel.name}')
        data, msg = await getData(member)
        count[member.id] = False
        addTime = int(data[1]) + time[member.id]
        await msg.edit(content=f'{member.mention}: {addTime}')



if __name__ == '__main__':
    client.run(TOKEN)