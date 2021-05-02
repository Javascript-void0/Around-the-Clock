import discord
import os
import asyncio
import time
from discord.ext import tasks, commands
from discord.utils import get

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)
TOKEN = os.getenv("SS_TOKEN")

@client.event
async def on_ready():
    print('Started {0.user}'.format(client))

@tasks.loop(seconds=1.0)
async def timer_start():

    guild = client.get_guild(802565984602423367)
    guild2 = client.get_guild(805299220935999509)
    channel = guild2.get_channel(838431117006340106)
    member = guild.me

    shortBreak = False
    longBreak = False
    t = 1500
    r = 1

    while True:
        await asyncio.sleep(5) 
        t -= 5
        print(t)
        m, s = divmod(t,60)

        if t == 0:
            if r == 0:
                shortBreak = False
                longBreak = False
            elif r == 1:
                shortBreak = True
                longBreak = False
            elif r == 9:
                shortBreak = False
                longBreak = True
            elif r % 2 == 0:
                shortBreak = False
                longBreak = False
            elif r % 2 == 1:
                shortBreak = True
                longBreak = False
            r += 1
            if r == 10:
                r = 0
            messages = await channel.history(limit=None).flatten()
            if shortBreak == True:
                t = 300
                for msg in messages:
                    user = guild.get_member(int(msg.content))
                    await user.send('```Study Time over, take a 5 minute break.```')
            elif longBreak == True:
                t = 900
                for msg in messages:
                    user = guild.get_member(int(msg.content))
                    await user.send('```Study Time over, take a 15 minute break.```')
            else:
                t = 1500
                for msg in messages:
                    user = guild.get_member(int(msg.content))
                    await user.send('```Break Time over, time to study for 25 minutes!```')

        if longBreak == True:
            await member.edit(nick='Long Break:')
        elif shortBreak == True:
            await member.edit(nick='Short Break:')    
        else:
            await member.edit(nick='Time Left:')
        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name='{:02}m {:02}s | .toggle'.format(m,s)))

@client.command(help='Tune into DM notifications')
async def toggle(ctx):
    guild = client.get_guild(805299220935999509)
    channel = guild.get_channel(838431117006340106)
    messages = await channel.history(limit=None).flatten()
    on = True
    for msg in messages:
        if str(ctx.message.author.id) in msg.content:
            await msg.delete()
            on = False
            await ctx.send('```Notifications Turned OFF```')
            break
    if on:
        await channel.send(ctx.message.author.id)
        await ctx.send('```Notifications Turned ON```')

@timer_start.before_loop
async def before_timer_start():
    print('waiting...')
    await client.wait_until_ready()

timer_start.start()
client.remove_command('help')
if __name__ == '__main__':
    client.run(TOKEN)