import discord
import os, os.path
from asyncio import sleep
from discord.errors import DiscordServerError, NotFound
from discord.ext import commands, tasks
from discord.utils import get

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)
TOKEN = os.getenv("TOKEN")

db = None
guild = None
atc = None
log = None
file_log = None
# count = {}
# time = {}

@client.event
async def on_ready():
    global db, guild, atc, log, file_log
    guild = client.get_guild(805299220935999509)
    atc = client.get_guild(802565984602423367)
    db = atc.get_channel(846564411862548490)
    # db = guild.get_channel(834943847602978836)
    log = guild.get_channel(838612591277375518)
    file_log = guild.get_channel(839164203449188372)
    print('[ + ] Started {0.user}'.format(client))
    print(f'[ + ] Connected to database...')
    await log.send('```DATABASE: Started {0.user}```'.format(client))
    await log.send(f'```DATABASE: Connected to database...```')

# Check is member is registered
async def registered(member):
    data = await find_dir_files(member)
    if data:
        return True
    return False

# Adds register member
async def register(member):
    global log
    if not await registered(member) and not member.bot:
        f = open('./DB/data.txt')
        f = f.read()
        lines = f.splitlines(True)
        lines.append(f'{member.id}: 1\n')
        with open(f'./DB/data.txt', 'w') as file:
            file.writelines(lines)
            file.close()
            await log.send(f'```DATABASE: Registered {member}```')

async def unregister(member):
    global log
    f = open(f'./DB/data.txt').read()
    lines = f.splitlines(True)
    with open(f'./DB/data.txt', 'w') as file:
        for i in range(len(lines)):
            if str(member.id) not in lines[i]:
                file.write(lines[i])
    await log.send(f'```DATABASE: Unregistered {member}```')

# Takes files from Database and saves to directory
async def get_db_files():
    global db, log
    messages = await db.history(limit=None, oldest_first=True).flatten()
    if messages:
        file_num = 1
        for msg in messages:
            file = await msg.attachments[0].read()
            with open(f'./DB/data.txt', 'wb') as f:
                f.write(file)
                f.close()
            await log.send(f'```DATABASE: Saved {file_num}.txt to Directory```')
            file_num += 1

# Takes recent file from file log and saves to directory
async def get_log_files():
    global file_log, log
    try:
        message = await file_log.fetch_message(file_log.last_message_id)
    except NotFound:
        await log.send('```DATABASE: Unknown Message```')
    file = await message.attachments[0].read()
    with open(f'./DB/data.txt', 'wb') as f:
        f.write(file)
        f.close()

# Current Directory into Log
async def log_update():
    global file_log, log
    await file_log.send(file=discord.File(f'./DB/data.txt'))

async def db_empty():
    if os.path.exists('./DB/data.txt'):
        return False
    return True

# Searches and Returns Player's Data
async def find_dir_files(member):
    data = None
    # for file in os.listdir('./DB/txt'):
    f = open(f'./DB/data.txt', 'r').read()
    lines = f.splitlines()
    for i in range(len(lines)):
        if str(member.id) in lines[i]:
            data = lines[i][20:]
            return data
    #         break
    if not data:
        return False

# Admin Manual Modify Player Data
async def modify_data(member, action, num):
    global log
    data = None
    # for file in os.listdir('./DB/txt'):
    f = open(f'./DB/data.txt').read()
    lines = f.splitlines(True)
    for i in range(len(lines)):
        if str(member.id) in lines[i]:
            data = lines[i][20:]
            if action == 'add':
                x = int(data) + num
                await log.send(f'```DATABASE: Added {num} to {member}```')
            elif action == 'remove':
                x = int(data) - num
                await log.send(f'```DATABASE: Removed {num} from {member}```')
            elif action == 'reset':
                x = 0
                await log.send(f'```DATABASE: Reset{member} to 0```')
            elif action == 'set':
                x = num
                await log.send(f'```DATABASE: Set {member} to {num}```')
            if x < 0:
                x = 0
            lines[i] = f'{member.id}: {x}\n'
            with open(f'./DB/data.txt', 'w') as file:
                file.writelines(lines)
    #         break
    if not data:
        return False

# Deletes and replaces with Directory Files
async def reload_database():
    global db, file_log
    await db.purge(limit=None)
    messages = await db.history().flatten()
    if messages == []:
    #     for file in os.listdir('./DB/txt'):
        await db.send(file=discord.File(f'./DB/data.txt'))

async def rank(member):
    global log, atc
    data = int(await find_dir_files(member))
    _3 = atc.get_role(846831774968840263)
    _6 = atc.get_role(846831824839245905)
    _9 = atc.get_role(846831895983292488)
    _12 = atc.get_role(846831994607632414)
    if data > 500 and _3 not in member.roles:
        await member.add_roles(_3)
        await log.send(f'```DATABASE: {member} Rank 3```')
    elif data < 500 and _3 in member.roles:
        await member.remove_roles(_3)
    if data > 1500 and _6 not in member.roles:
        await member.add_roles(_6)
        await log.send(f'```DATABASE: {member} Rank 6```')
    elif data < 1500 and _6 in member.roles:
        await member.remove_roles(_6)
    if data > 5000 and _9 not in member.roles:
        await member.add_roles(_9)
        await log.send(f'```DATABASE: {member} Rank 9```')
    elif data < 5000 and _9 in member.roles:
        await member.remove_roles(_9)
    if data > 10000 and _12 not in member.roles:
        await member.add_roles(_12)
        await log.send(f'```DATABASE: {member} Rank 12```')
    elif data < 10000 and _12 in member.roles:
        await member.remove_roles(_12)

''' Start Timer in Voice Channel
async def timerStart(member):
    global log
    time[member.id] = 0
    count[member.id] = True
    await log.send(f'```DATABASE: Timer started for {member}```')
    while count[member.id] == True:
        await sleep(60)
        time[member.id] += 1
'''

@client.command(name='register', help='Registers a Member')
@commands.has_permissions(administrator=True)
async def _register(ctx, member : discord.Member):
    await register(member)
    await ctx.send(f'```DATABASE: Registered {member}```')

@client.command(name='unregister', help='Unregisters a Member')
@commands.has_permissions(administrator=True)
async def _unregister(ctx, member : discord.Member):
    await unregister(member)
    await ctx.send(f'```DATABASE: Unregistered {member}```')

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

@client.command(aliases=['self'], help='Shows Your Stats')
async def me(ctx):
    global db
    member = ctx.message.author
    data = await find_dir_files(member)
    if data:
        await ctx.send(f'```[{member.id}]\n{member} - {data}```')
    else:
        await ctx.send(f'```DATABASE: No data for {member}```')

@client.command(aliases=['leaderboard', 'lb'], help='Shows Top Members')
async def top(ctx):
    data = {}
    f = open(f'./DB/data.txt').read()
    lines = f.splitlines()
    lines = lines[2:]
    for i in range(len(lines)):
        member = lines[i].split(': ')
        data[member[0]] = int(member[1])
    top = sorted(data, key=data.get, reverse=True)[:10]
    list = 'Top: '
    for i in range(len(top)):
        member = await client.fetch_user(int(top[i]))
        data = await find_dir_files(member)
        if i == 0:
            list = list + (f'1. {member}: {data}\n')
        elif i == 9:
            list = list + (f'    10. {member}: {data}\n')
        else:
            list = list + (f'     {i+1}. {member}: {data}\n')
    await ctx.send(f'```{list}```')

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
    #     for file in os.listdir('./DB/txt'):
        await db.send(file=discord.File(f'./DB/data.txt'))
        await log.send('```DATABASE: Loaded```', file=discord.File(f'./DB/data.txt'))
    await ctx.send('```DATABASE: Loaded```')

@client.command(aliases=['dbclean', 'databaseclean', 'cleandatabase'], help='Cleans extra data')
@commands.has_permissions(administrator=True)
async def cleandb(ctx):
    global db
    if ctx.guild == atc:
    #     for file in os.listdir('./DB/txt'):
        f = open(f'./DB/data.txt')
        f = f.read()
        lines = f.splitlines(True)
        for i in range(len(lines)-1, -1, -1):
            if ': 0\n' in lines[i]:
                lines.pop(i)
        with open(f'./DB/data.txt', 'w') as file:
            file.writelines(lines)
            file.close()
        await ctx.send('```DATABASE: Cleaned```')
        await log.send('```DATABASE: Cleaned```')

@client.command(help='Send Database File')
async def file(ctx):
    # for file in os.listdir('./DB/txt'):
    await ctx.send(file=discord.File(f'./DB/data.txt'))

# EVENTS TO ADD SCORE

@client.event
async def on_message(message):
    global atc
    if message.guild == atc and not message.author.bot:
        if await registered(message.author):
            if message.channel.id == 805491870183981116 and len(str(message.content)) >= 50: # intros
                await modify_data(message.author, "add", 25)
            elif message.channel.id == 806150413773963275 and len(str(message.conent)) > 50: # todo
                await modify_data(message.author, "add", 10)
            elif message.channel.id == 802577298267963412 and message.content == '!d bump':
                await modify_data(message.author, "add", 5)
            elif message.channel.id == 818507546376798228: # motivation
                await modify_data(message.author, "add", 3)
            elif message.channel.id == 802565985055014953: # welcome
                await modify_data(message.author, "add", 2)
            elif message.channel.id == 802915711122014278: # sessions
                await modify_data(message.author, "add", 3)
            else:
                await modify_data(message.author, "add", 1)
            await rank(message.author)
        else:
            await register(message.author)
    
    await client.process_commands(message)

'''
@client.event
async def on_voice_state_update(member, before, after):
    global db, log
    try:
        if after.channel is None and not member.bot:
            print(f'{member} left #{before.channel.name}')
            await log.send(f'```{member} left #{before.channel.name}```')
            count[member.id] = False
            await modify_data(member, "add", time[member.id])
        if after.channel.guild == atc and not member.bot:
            print(f'{member} joined #{after.channel.name}')
            await log.send(f'```{member} joined #{after.channel.name}```')
            if await registered(member):
                await timerStart(member)
            else:
                await register(member)
                await timerStart(member)
    except AttributeError:
        pass
'''
# LOOP TO RELOAD FILE

@tasks.loop(minutes=1.0)
async def loop_restart():
    if await db_empty():
        await get_log_files()
    else:
        await log_update()
        await get_log_files()
    await reload_database()

@loop_restart.before_loop
async def before_loop_restart():
    print('waiting...')
    await client.wait_until_ready()

loop_restart.start()
if __name__ == '__main__':
    client.run(TOKEN, reconnect=True)