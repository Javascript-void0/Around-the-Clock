import asyncio
import random
import discord
from discord.ext import tasks, commands
from discord.utils import get
from datetime import datetime

pomodoro_timer = True

class Study(commands.Cog):

    def __init__(self, client):
        self.client = client
#        self.globalvc.start()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        self.client.get_guild(802565984602423367)
        role = get(member.guild.roles, name="Studying")
        if before.channel is None:
            await member.add_roles(role)
        if after.channel is None:
            await member.remove_roles(role)

    @commands.command(help='Starts Pomodoro timer')
    async def start(self, ctx):
        start_message = [
            "You have **25 minutes** left. Get to studying :D",
            "**25 more minutes** to go!",
            "Get studying, **25 minutes** on the clock."
        ]

        break_message = [
            "BREAK TIME FOR ",
            "I've got a gift: it's a **5 minute** break time for ",
            "Come back in **5 minutes **",
            "25 minutes is up! Take a **5 minute** break :D ",
        ]
        global pomodoro_timer
        pomodoro_timer = True
        global showTimer
        showTimer = False
        global specialBreakTime
        specialBreakTime = False
        
        channel = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice = await channel.connect()

        breakTime = False
        t = 1501

        while pomodoro_timer == True:
            mins, secs = divmod(t, 60) 
            timer = "**{:02d}:{:02d}**".format(mins, secs) 
            await asyncio.sleep(1) 
            t -= 1

            if(showTimer):
                await ctx.send(timer) 
                showTimer = False

            if(specialBreakTime):
                breakTime = True
                t = 0
                specialBreakTime = False

            if(t == 1500):
                response = random.choice(start_message)
                await ctx.send("Hey <@{0}>! {1}".format(ctx.author.id, response))
                voice.play(discord.FFmpegPCMAudio(source="assets/alarm.mp3"))

            elif(t == 600 and breakTime == False):
                breakTime = True
            
            elif(t == 0):
                if(breakTime):
                    response = random.choice(break_message)
                    await ctx.send("{1} <@{0}>!".format(ctx.author.id, response))
                    voice.play(discord.FFmpegPCMAudio(source="assets/alarm.mp3"))
                    t = 301
                    breakTime = False
                else:
                    t = 1501

    @commands.command(aliases=['leave', 'dc', 'disconnect'], help='Stops Pomodoro timer')
    async def stop(self, ctx):
        global pomodoro_timer 
        pomodoro_timer = False
        await ctx.send("Pomodoro stopped!")
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice = await voice.disconnect()

    @commands.command(name='break', help='Starts break timer')
    async def _break(self, ctx):
        global specialBreakTime 
        specialBreakTime = True
        await ctx.send("Starting Break Time now!")
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio(source="assets/alarm.mp3"))

    @commands.command(help='Displays time remaining') 
    async def time(self, ctx):
        global showTimer
        showTimer = True
        await ctx.send("Time remaining:")

    @commands.command(help='Lofi in Voice Channels')
    async def lofi(self, ctx):
        channel = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio(source="assets/lofi.mp3"))

# SESSIONS FORMAT

    @commands.command(help='General Study Session Format')
    async def session(self, ctx, *, message=None):
        mention = discord.utils.get(ctx.guild.roles, name='Study Session')
        if message is None:
            message = 'New Session Started'
        embed = discord.Embed(title = f"⏰ Session Started", description = f"Started by {ctx.author.mention}")
        embed.add_field(name = f"{message}", value = f"`Good Luck ♥`")
        message = await ctx.send(f'{mention.mention} `✔ Session Started', embed=embed)
        embed.set_footer(text=f"End this session with: 12 end {message.id}")
        await message.edit(content=f'{mention.mention} `✔ Session Started`', embed=embed)
        await ctx.message.delete()

    @commands.command(help='Hours.zone Session Format')
    async def hours(self, ctx, link, *, message=None):
        mention = discord.utils.get(ctx.guild.roles, name='Study Session')
        if message is None:
            message = 'New Session Started'
        if "https://hours.zone/invite/" in link:
            embed = discord.Embed(title = f"⏰ Study Session", description = f"Started by {ctx.author.mention}")
            embed.add_field(name = f"{message}", value = f"{link}")
            embed.set_thumbnail(url='https://i.imgur.com/JViNlaE.png')
            message = await ctx.send(f'{mention.mention} `✔ Session Started`', embed=embed)
            embed.set_footer(text=f"End this session with: 12 end {message.id}")
            await message.edit(content=f'{mention.mention} `✔ Session Started`', embed=embed)
            await ctx.message.delete()
        else:
            await ctx.message.delete()
            await ctx.send('Hours Invite Link')

    @commands.command(help='Ends Sessions')
    async def end(self, ctx, msgid : int = None):
        mention = discord.utils.get(ctx.guild.roles, name='Study Session')
        if msgid is None:
            await ctx.send('`12 end <message id>`')
        elif ctx.channel.id == 802915711122014278:
            message = await ctx.fetch_message(msgid)
            embed = message.embeds[0]
            await message.edit(content=f'{mention.mention} `❌ Session Ended`', embed=embed)
        await ctx.message.delete()

def setup(client):
    client.add_cog(Study(client))