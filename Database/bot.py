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

async def exists(member):
    await db_files()
    data = await find_dir_files(member)
    if data:
        return True
    return False

async def new(member):
    global db
    await db_files()
    if not await exists(member):
        for file in os.listdir('./Database/data'):
            if os.stat(f'./Database/data/{file}').st_size <= 7800000:
                f = open(f'./Database/data/{file}')
                f = f.read()
                lines = f.splitlines(True)
                print(lines)
                lines[-1] = lines[-1] + '\n'
                lines.append(f'{member.id}: 0\n')
                with open(f'./Database/data/{file}', 'w') as file:
                    file.writelines(lines)
                    file.close()
                    await reload_database()
                    break

@client.command(help='Registers a Member')
async def register(ctx, member : discord.Member):
    await new(member)

async def db_files():
    global db
    messages = await db.history(limit=None, oldest_first=True).flatten()
    if messages == []:
        await ctx.send('```No Files Found```')
    else:
        # Update Files in Directory
        file_num = 1
        for msg in messages:
            file = await msg.attachments[0].read()
            with open(f'./Database/data/{file_num}.txt', 'wb') as f:
                f.write(file)
                f.close()
            file_num += 1

async def find_dir_files(member):
    data = None
    for file in os.listdir('./Database/data'):
        f = open(f'./Database/data/{file}', 'r').read()
        lines = f.splitlines()
        for i in range(len(lines)):
            if str(member.id) in lines[i]:
                data = lines[i][20:]
                return data
                break
    if not data:
        return False

async def add_data(member, num):
    data = None
    for file in os.listdir('./Database/data'):
        f = open(f'./Database/data/{file}')
        f = f.read()
        lines = f.splitlines(True)
        for i in range(len(lines)):
            if str(member.id) in lines[i]:
                data = lines[i][20:]
                lines[i] = f'{member.id}: {int(data) + num}\n'
                with open(f'./Database/data/{file}', 'w') as file:
                    file.writelines(lines)
                break
    if not data:
        return False

async def reload_database():
    global db
    await db.purge(limit=None)
    messages = await db.history().flatten()
    if messages == []:
        for file in os.listdir('./Database/data'):
            await db.send(file=discord.File(f'./Database/data/{file}'))

@client.command(help='Add')
@commands.has_permissions(administrator=True)
async def add(ctx, member : discord.Member, num : int):
    await db_files()
    await add_data(member, num)
    await reload_database()
    await ctx.send(f'```DATABASE: Added {num} to {member}```')

@client.command(aliases=['data'], help='Find Data')
async def find(ctx, member : discord.Member):
    global db
    await db_files()
    data = await find_dir_files(member)
    if data:
        await ctx.send(f'```[{member.id}]\n{member} - {data}```')
    else:
        await ctx.send(f'```DATABASE: No data for {member}```')

@client.command(aliases=['dbclear'], help='Clears the Database')
@commands.has_permissions(administrator=True)
async def databaseclear(ctx):
    global db
    await db.purge(limit=None)
    await ctx.send('```DATABASE: Cleared all files in #db```')

@client.command(aliases=['dbload'], help='Database Load')
@commands.has_permissions(administrator=True)
async def databaseload(ctx):
    global db
    messages = await db.history().flatten()
    if messages == []:
        for file in os.listdir('./Database/data'):
            await db.send(file=discord.File(f'./Database/data/{file}'))

if __name__ == '__main__':
    client.run(TOKEN)