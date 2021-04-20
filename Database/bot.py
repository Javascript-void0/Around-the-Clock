import discord
import os
from asyncio import sleep
from re import findall
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.')
client.remove_command('help')
TOKEN = os.getenv("DB_TOKEN")

ACT_CNL = None
DB_GUILD = None
timing = {}
elapsed_time = {}

async def timerStart(member):
    elapsed_time[member.id] = 0
    timing[member.id] = True
    while timing[member.id]:
        await sleep(1)
        elapsed_time[member.id] += 1

def getData(member):
    global DB_GUILD
    for channel in DB_GUILD.channels:
        if str(member.id) in channel.name:
            stat = channel.channels[1]
            return stat

def registered(member):
    global DB_GUILD
    for channel in DB_GUILD.channels:
        if str(member.id) in channel.name:
            return True
    return False

@client.command()
@commands.is_owner()
async def reset_all_data_in_database(ctx):
    global DB_GUILD
    for channel in DB_GUILD.channels:
        if channel.name == '⎯⎯⎯⎯⎯⎯⎯⎯ important ⎯⎯⎯⎯⎯⎯⎯⎯⎯':
            pass
        elif channel.name == 'info':
            pass
        elif channel.name == 'vc':
            pass
        elif channel.name == 'testing':
            pass
        else:
            await channel.delete()

@client.event
async def on_ready():
    global DB_GUILD, ACT_CNL
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Around the Clock"))
    DB_GUILD = client.get_guild(833853909168160777)
    ACT_CNL = DB_GUILD.get_channel(833893975538401280)
    print('[ + ] Started {0.user}'.format(client))
    print('[ + ] Connected to database...')

@client.event
async def on_voice_state_update(member, before, after):
    global DB_GUILD, ACT_CNL
    if before.channel is None:
        await ACT_CNL.send(f'```{member} joined #{after.channel.name}```')
        if registered(member):
            await timerStart(member)
        else:
            category = await DB_GUILD.create_category_channel(member.id)
            await DB_GUILD.create_voice_channel(member.name + '#' + member.discriminator, category=category)
            await DB_GUILD.create_voice_channel('0 Minutes', category=category)
            await timerStart(member)
    elif after.channel is None:
        timing[member.id] = False
        await ACT_CNL.send(f'```{member} left #{before.channel.name}```')
        stat = getData(member)
        stat_num = findall(r'\d', stat.name)
        total = int(stat_num[0]) + elapsed_time[member.id]
        await stat.edit(name=f'{total} Minutes')
        await ACT_CNL.send(f'```{member} stats updated: {int(stat_num[0])} >> {total}```')
        
if __name__ == '__main__':
    client.run(TOKEN)