import discord
import os
import asyncio
from discord.ext import tasks, commands
from discord.utils import get

client = commands.Bot(command_prefix='63 ')
run = False
show = False
TOKEN = os.getenv("6030_TOKEN")

@client.event
async def on_ready():
    print('Started {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Around the Clock"))

@client.command(aliases=['start', 'pomo', 'pomodoro'], help='Starts the Timer')
async def _start(ctx):
    global run, show

    channel = ctx.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)    
    if ctx.author.voice.channel:
        voice = await channel.connect()
    else:
        await ctx.send('You need to join a voice channel first')

    Break = False
    t = 3601
    r = 0
    run = True

    while run == True:
        mins, secs = divmod(t, 60) 
        timer = "**{:02d}:{:02d}**".format(mins, secs) 
        await asyncio.sleep(1) 
        t -= 1

        if show == True:
            await ctx.send(timer) 
            show = False

        if t == 3600:
            voice.play(discord.FFmpegPCMAudio(source="alarm.mp3"))
            await ctx.send("<@{0}>! Study Time!".format(ctx.author.id))

        elif t == 10:
            if r == 0:
                Break = False
            elif r == 1:
                Break = True
            elif r % 2 == 0:
                Break = False
            elif r % 2 == 1:
                Break = True

        elif t == 0:
            r += 1
            if Break == True:
                t = 1801
                await ctx.send("<@{0}> Break Time!".format(ctx.author.id))
                voice.play(discord.FFmpegPCMAudio(source="alarm.mp3"))
            else:
                t = 3601

@client.command(aliases=['leave', 'stop', 'pause'], help='Stops the Timer')
async def _stop(ctx):
    global run
    if run == True:
        run = False
        await ctx.send('Timer Stopped')
        voice = get(client.voice_clients, guild=ctx.guild)
        voice = await voice.disconnect()
    else:
        await ctx.send('No Timer Running')

@client.command(aliases=['join'], help='Use if Bot disconnects, idk')
async def rejoin(ctx):
    global run
    channel = ctx.author.voice.channel
    get(client.voice_clients, guild=ctx.guild)
    
    if ctx.author.voice.channel:
        if run == True:
            await channel.connect()
        else:
            await ctx.send('You need to start a timer first `63 start`')
    else:
        await ctx.send('You need to join a voice channel first')


@client.command(aliases=['timer', 'time'], help='Shows the time remaining')
async def _time(ctx):
    global show
    if run == True:
        show = True
        await ctx.send("Time remaining:")
    else:
        await ctx.send('No Timer Running')

if __name__ == '__main__':
    client.run(TOKEN)