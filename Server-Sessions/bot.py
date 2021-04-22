import discord
import os
import asyncio
from discord.ext import tasks, commands
from discord.utils import get

client = commands.Bot(command_prefix='.')
TOKEN = os.getenv("SS_TOKEN")

@client.event
async def on_ready():
    print('Started {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="#▹fireplace_study"))

@tasks.loop(minutes=1.0)
async def timer_start():

    guild = client.get_guild(802565984602423367)
#    channel = guild.get_channel(802567364658855976)
#    voice = get(client.voice_clients, guild=guild)
#    voice = await channel.connect()
    member = guild.me

    shortBreak = False
    longBreak = False
    t = 1501
    r = 1

    while True:
        await asyncio.sleep(1) 
        t -= 1
        print(t)

        if t == 1500:
            await member.edit(nick='Time Left: 25m 0s')
#            voice.play(discord.FFmpegPCMAudio(source="assets/alarm.mp3"))

        elif t == 10:
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

        elif t == 0:
            r += 1
            if r == 10:
                r = 0
            if shortBreak == True:
                t = 301
#                voice.play(discord.FFmpegPCMAudio(source="assets/alarm.mp3"))
            elif longBreak == True:
                t = 901
#                voice.play(discord.FFmpegPCMAudio(source="assets/alarm.mp3"))
            else:
                t = 1501

        elif t % 30 == 0:
            if t % 60 == 0:
                m = t // 60
                s = 0
            else:
                m = t // 30
                m -= 1
                m = m // 2
                s = 30
            if longBreak == True:
                await member.edit(nick='Long Break: {}m {}s'.format(m,s))
            elif shortBreak == True:
                await member.edit(nick='Short Break: {}m {}s'.format(m,s))    
            else:
                await member.edit(nick='Time Left: {}m {}s'.format(m,s))

@timer_start.before_loop
async def before_timer_start():
    print('waiting...')
    await client.wait_until_ready()

timer_start.start()
client.remove_command('help')
if __name__ == '__main__':
    client.run(TOKEN)