import discord
import os
from asyncio import sleep
from discord.ext import commands, tasks
from discord.utils import get

client = commands.Bot(command_prefix='.')
TOKEN = os.getenv("TOKEN")

db = None
guild = None
atc = None
count = {}
time = {}

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
async def registered(member):
    data = await find_dir_files(member)
    if data:
        return True
    return False

# Adds register member
async def register(member):
    global db
    if not await registered(member):
        for file in os.listdir('./Database/data'):
            if os.stat(f'./Database/data/{file}').st_size <= 7800000:
                f = open(f'./Database/data/{file}')
                f = f.read()
                lines = f.splitlines(True)
                lines.append(f'{member.id}: 1\n')
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

# Start Timer in Voice Channel
async def timerStart(member):
    time[member.id] = 0
    count[member.id] = True
    while count[member.id] == True:
        await sleep(1)
        time[member.id] += 1

@client.command(name='register', help='Registers a Member')
@commands.has_permissions(administrator=True)
async def _register(ctx, member : discord.Member):
    await register(member)
    await ctx.send(f'```DATABASE: Registered {member}```')

@client.command(help='Add')
@commands.has_permissions(administrator=True)
async def add(ctx, member : discord.Member, num : int):
    if num > 0:
        await modify_data(member, 'add', num)
        await ctx.send(f'```DATABASE: Added {num} to {member}```')
    else:
        await ctx.send(f'```DATABASE: Integer must be positive```')

@client.command(help='Remove')
@commands.has_permissions(administrator=True)
async def remove(ctx, member : discord.Member, num : int):
    if num > 0:
        await modify_data(member, 'remove', num)
        await ctx.send(f'```DATABASE: Removed {num} from {member}```')
    else:
        await ctx.send(f'```DATABASE: Integer must be positive```')
        
@client.command(help='Reset Member Data')
@commands.has_permissions(administrator=True)
async def reset(ctx, member : discord.Member):
    await modify_data(member, 'reset', 0)
    await ctx.send(f'```DATABASE: Reset {member} to 0```')

@client.command(help='Set Member Data')
@commands.has_permissions(administrator=True)
async def set(ctx, member : discord.Member, num : int):
    if num > 0:
        await modify_data(member, 'set', num)
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
        if await registered(message.author):
            await modify_data(message.author, "add", 1)
        else:
            await register(message.author)
    
    await client.process_commands(message)

@client.event
async def on_voice_state_update(member, before, after):
    global db
    if before.channel is None:
        print(f'{member} joined #{after.channel.name}')
        if await registered(member):
            await timerStart(member)
        else:
            await register(member)
            await timerStart(member)
    elif after.channel is None:
        print(f'{member} left #{before.channel.name}')
        count[member.id] = False
        await modify_data(member, "add", time[member.id])

@tasks.loop(minutes=1.0)
async def loop_restart():
    await reload_database()

@loop_restart.before_loop
async def before_loop_restart():
    print('waiting...')
    await client.wait_until_ready()

loop_restart.start()
if __name__ == '__main__':
    client.run(TOKEN)