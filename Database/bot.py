import discord
import os
from discord.ext import commands, tasks
from discord.utils import get

client = commands.Bot(command_prefix='.')
TOKEN = os.getenv("TOKEN")

db = None
guild = None
atc = None

@client.event
async def on_ready():
    global db, guild, atc
    guild = client.get_guild(805299220935999509)
    atc = client.get_guild(802565984602423367)
    db = guild.get_channel(834943847602978836)
    print('[ + ] Started {0.user}'.format(client))
    print(f'[ + ] Connected to database...')
    await db_files()

# Check is member is registered
async def exists(member):
    data = await find_dir_files(member)
    if data:
        return True
    return False

# Adds New member
async def new(member):
    global db
    if not await exists(member):
        for file in os.listdir('./Database/data'):
            if os.stat(f'./Database/data/{file}').st_size <= 7800000:
                f = open(f'./Database/data/{file}')
                f = f.read()
                lines = f.splitlines(True)
                lines[-1] = lines[-1] + '\n'
                lines.append(f'{member.id}: 0\n')
                with open(f'./Database/data/{file}', 'w') as file:
                    file.writelines(lines)
                    file.close()
                    await reload_database()
                    break

# Takes files from Database and saves to directory
async def db_files():
    global db
    messages = await db.history(limit=None, oldest_first=True).flatten()
    if messages:
        file_num = 1
        for msg in messages:
            file = await msg.attachments[0].read()
            with open(f'./Database/data/{file_num}.txt', 'wb') as f:
                f.write(file)
                f.close()
            file_num += 1

# Searches and Returns Player's Data
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

# Admin Manual Modify Player Data
async def modify_data(member, action, num):
    data = None
    for file in os.listdir('./Database/data'):
        f = open(f'./Database/data/{file}')
        f = f.read()
        lines = f.splitlines(True)
        for i in range(len(lines)):
            if str(member.id) in lines[i]:
                data = lines[i][20:]
                if action == 'add':
                    x = int(data) + num
                elif action == 'remove':
                    x = int(data) - num
                elif action == 'reset':
                    x = 0
                elif action == 'set':
                    x = num
                if x < 0:
                    x = 0
                lines[i] = f'{member.id}: {x}\n'
                with open(f'./Database/data/{file}', 'w') as file:
                    file.writelines(lines)
                break
    if not data:
        return False

# Deletes and replaces with Directory Files
async def reload_database():
    global db
    await db.purge(limit=None)
    messages = await db.history().flatten()
    if messages == []:
        for file in os.listdir('./Database/data'):
            await db.send(file=discord.File(f'./Database/data/{file}'))

@client.command(help='Registers a Member')
@commands.has_permissions(administrator=True)
async def register(ctx, member : discord.Member):
    await new(member)

@client.command(help='Add')
@commands.has_permissions(administrator=True)
async def add(ctx, member : discord.Member, num : int):
    if num > 0:
        await modify_data(member, 'add', num)
        await reload_database()
        await ctx.send(f'```DATABASE: Added {num} to {member}```')
    else:
        await ctx.send(f'```DATABASE: Integer must be positive```')

@client.command(help='Remove')
@commands.has_permissions(administrator=True)
async def remove(ctx, member : discord.Member, num : int):
    if num > 0:
        await modify_data(member, 'remove', num)
        await reload_database()
        await ctx.send(f'```DATABASE: Removed {num} from {member}```')
    else:
        await ctx.send(f'```DATABASE: Integer must be positive```')
@client.command(help='Reset Member Data')
@commands.has_permissions(administrator=True)
async def reset(ctx, member : discord.Member):
    await modify_data(member, 'reset', 0)
    await reload_database()
    await ctx.send(f'```DATABASE: Reset {member} to 0```')

@client.command(help='Set Member Data')
@commands.has_permissions(administrator=True)
async def set(ctx, member : discord.Member, num : int):
    if num > 0:
        await modify_data(member, 'set', num)
        await reload_database()
        await ctx.send(f'```DATABASE: Set {member} to {num}```')
    else:
        await ctx.send(f'```DATABASE: Integer must be positive```')

@client.command(aliases=['data', 'search', 'stat', 'stats'], help='Find Data')
async def find(ctx, member : discord.Member):
    global db
    data = await find_dir_files(member)
    if data:
        await ctx.send(f'```[{member.id}]\n{member} - {data}```')
    else:
        await ctx.send(f'```DATABASE: No data for {member}```')

@client.command(aliases=['dbclear', 'cleardatabase', 'cleardb', 'clear_database', 'clear_db'], help='Clears the Database')
@commands.has_permissions(administrator=True)
async def databaseclear(ctx):
    global db
    await db.purge(limit=None)
    await ctx.send('```DATABASE: Cleared all files in #db```')

@client.command(aliases=['dbload', 'loaddatabase', 'loaddb', 'load_database', 'load_db'], help='Database Load')
@commands.has_permissions(administrator=True)
async def databaseload(ctx):
    global db
    messages = await db.history().flatten()
    if messages == []:
        for file in os.listdir('./Database/data'):
            await db.send(file=discord.File(f'./Database/data/{file}'))

@client.event
async def on_message(message):
    global atc
    if message.guild == atc:
        if exists(message.author):
            await modify_data(message.author, "add", 1)
            await reload_database()
        else:
            await new(message.author)
            await modify_data(message.author, "add", 1)
            await reload_database()

if __name__ == '__main__':
    client.run(TOKEN)