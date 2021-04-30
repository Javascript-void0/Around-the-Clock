import discord
import os
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.')
TOKEN = os.getenv("TOKEN")

db = None
guild = None

@client.event
async def on_ready():
    global db, guild
    guild = client.get_guild(805299220935999509)
    db = guild.get_channel(834943847602978836)
    print('[ + ] Started {0.user}'.format(client))
    print(f'[ + ] Connected to database...')

@client.command(help='test')
async def file(ctx):
    global db
    messages = await db.history(limit=None, oldest_first=True).flatten()
    if messages == []:
        await ctx.send('```No Files Found```')
    else:
        # Update Files
        file_num = 1
        for msg in messages:
            file = await msg.attachments[0].read()
            with open(f'./Database/data/{file_num}.txt', 'wb') as f:
                f.write(file)
            file_num += 1

if __name__ == '__main__':
    client.run(TOKEN)