import discord
import os
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

if __name__ == '__main__':
    client.run(TOKEN)