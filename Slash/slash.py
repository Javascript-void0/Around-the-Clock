from typing import Type
import discord
import os
import random
import asyncio
from discord_slash import SlashCommand, SlashCommandOptionType, SlashContext
from discord.ext import commands
from discord.utils import get
from time import sleep
from random import randint

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix='.', intents=intents)
slash = SlashCommand(client, sync_commands=True)
TOKEN = os.getenv("SLASH")

@client.event
async def on_ready():
    print(f'Started {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with Knives"))

guild_ids = [805299220935999509, 848693031841300491]

options8ball = [
    {
        "name" : "question",
        "description" : "Ask a question. ",
        "required" : True,
        "type" : 3
    }
]

@slash.slash(name='8ball', description='8ball game', guild_ids=guild_ids, options=options8ball)
async def _8ball(ctx : SlashContext, question):
    responses = [
        'It is certain.', 'It is decidedly so.', 'Without a doubt.',
        'You may rely on it.', 'As I see it, yes.', 'Most likely.',
        'Outlook good.', 'Yes.', 'Signs point to yes.',
        'Reply hazy, try again.', 'Ask again later.',
        'Better not tell you now.', 'Cannot predict now.',
        'Concentrate and ask again.', "Don't count on it.", 'My reply is no.',
        'My sources say no.', 'Outlook not so good.', 'Very doubtful.'
    ]
    await ctx.send(f'```Question: {question}\nAnswer: {random.choice(responses)}```')

optionsClear = [
    {
        "name" : "integer",
        "description" : "Number of messages. ",
        "required" : True,
        "type" : 4
    }
]

@slash.slash(name='clear', description='Clears Messages', guild_ids=guild_ids, options=optionsClear)
async def clear(ctx : SlashContext, integer):
    await ctx.channel.purge(limit=integer)
    await ctx.send(f'```Cleared {integer} messages```', delete_after=5)

optionsWhois = [
    {
        "name" : "member",
        "description" : "Choose a member to find the details of. ",
        "required" : True,
        "type" : 6
    }
]

@slash.slash(name='whois', description='Info about a user', guild_ids=guild_ids, options=optionsWhois)
async def whois(ctx : SlashContext, member):
    embed = discord.Embed(title = member.name, description = member.mention)
    embed.add_field(name = "ID", value = member.id, inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

optionsKick = [
    {
        "name" : "member",
        "description" : "Choose a member to kick. ",
        "required" : True,
        "type" : 6
    },
    {
        "name" : "reason",
        "description" : "Reason for kicking. ",
        "required" : True,
        "type" : 3
    }
]

@slash.slash(name='kick', description='Kick member from Server', guild_ids=guild_ids, options=optionsKick)
async def kick(ctx, member, reason):
    await member.kick(reason=reason)
    await ctx.send(f'```Kicked {member} for {reason}```')

optionsBan = [
    {
        "name" : "member",
        "description" : "Choose a member to kick. ",
        "required" : True,
        "type" : 6
    },
    {
        "name" : "reason",
        "description" : "Reason for kicking. ",
        "required" : True,
        "type" : 3
    }
]

@slash.slash(name='ban', description='Ban member from Server', guild_ids=guild_ids, options=optionsBan)
async def ban(ctx, member, reason):
    await member.ban(reason=reason)
    await ctx.send(f'```Banned {member} for {reason}```')

optionsUnban = [
    {
        "name" : "member",
        "description" : "Choose a member to unban. ",
        "required" : True,
        "type" : 6
    }
]

@slash.slash(name='unban', description='Unban members from Server', guild_ids=guild_ids, options=optionsUnban)
async def unban(ctx, member):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.id == member:
            await ctx.guild.unban(user)
            await ctx.send(f'```Unbanned {user}```')
            return

@slash.slash(name='server', description='Server Stats', guild_ids=guild_ids)
async def server(ctx : SlashContext):
    online = 0
    idle = 0
    dnd = 0
    bot = 0
    totalOnline = 0
    for member in ctx.guild.members:
        if member.bot:
            bot += 1
        if member.status != discord.Status.offline:
            totalOnline += 1
        if member.status == discord.Status.online:
            online += 1
        elif member.status == discord.Status.idle:
            idle += 1
        elif member.status == discord.Status.do_not_disturb:
            dnd += 1
    embed = discord.Embed(title=f'Statistics for {ctx.guild.name}', description=f'Owner: {ctx.guild.owner.mention}\nID: {ctx.guild.id}')
    embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
    embed.add_field(name='Channels', value=f'{len(ctx.guild.channels)} Channels', inline=True)
    embed.add_field(name='Bots', value=f'{bot} Bots', inline=True)
    embed.add_field(name='Roles', value=f'{len(ctx.guild.roles)} Roles', inline=True)
    embed.add_field(name='Emoji', value=f'{len(ctx.guild.emojis)} Emojis', inline=True)

    eMember = discord.Embed(title=f'Statistics for {ctx.guild.name}', description=f'Owner: {ctx.guild.owner.mention}\nID: {ctx.guild.id}')
    eMember.set_thumbnail(url=f'{ctx.guild.icon_url}')
    eMember.add_field(name='Members', value=f'{len(ctx.guild.members)} Total Members\n\n**Total Online:** {totalOnline}', inline=False)
    eMember.add_field(name='Online', value=f'{online} Online', inline=True)
    eMember.add_field(name='Idle', value=f'{idle} Idle', inline=True)
    eMember.add_field(name='Do Not Disturb', value=f'{dnd} DND', inline=True)
    
    await ctx.send(embed=embed)
    await ctx.send(embed=eMember)

@slash.slash(name='ping', description='Latnecy', guild_ids=guild_ids)
async def ping(ctx : SlashContext):
    await ctx.send(f'```Current Ping: {round(client.latency * 1000)}ms```')

@slash.slash(name='animation', description='Loading Bar...?', guild_ids=guild_ids)
async def animation(ctx : SlashContext):
    bar = await ctx.send("```[:::::::::::::::::::::::::] 0.0%```")
    sleep(1)
    await bar.edit(content="```[>::::::::::::::::::::::::] 4.0%```")
    sleep(1)
    await bar.edit(content="```[>>:::::::::::::::::::::::] 8.0%```")
    sleep(1)
    await bar.edit(content="```[>>>::::::::::::::::::::::] 12.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>:::::::::::::::::::::] 16.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>::::::::::::::::::::] 20.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>:::::::::::::::::::] 24.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>::::::::::::::::::] 28.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>:::::::::::::::::] 32.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>::::::::::::::::] 36.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>:::::::::::::::] 40.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>::::::::::::::] 44.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>:::::::::::::] 48.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>>::::::::::::] 52.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>>>:::::::::::] 56.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>>>>::::::::::] 60.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>>>>>:::::::::] 64.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>>>>>>::::::::] 68.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>>>>>>>:::::::] 72.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>::::::] 76.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>>:::::] 80.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>>>::::] 84.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>>>>:::] 88.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>>>>>::] 92.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>>>>>>:] 96.0%```")
    sleep(1)
    await bar.edit(content="```[>>>>>>>>>>>>>>>>>>>>>>>>>] 100.0%```")

@slash.slash(name='highlow', description='High-low Game (Dank Memer)', guild_ids=guild_ids)
async def highlow(ctx : SlashContext):
    num = randint(1,100)
    hint = randint(1,100)
    embed = discord.Embed(title=f"{ctx.author.name}'s high-low game", description=f'A number secret between 1-100 has been chosen. Your hint is **{hint}**.\nRespond with "high", "low", or "jackpot".')
    embed.set_footer(text='Choose whether you think the hidden number is higher, lower, or the same number as the hint')
    await ctx.send(embed=embed)

    lEmbed = discord.Embed(title=f"{ctx.author.name}'s losing high-low game\nYou lost!", description=f'Your hint was **{hint}**. The hidden number was **{num}**.', color=discord.Color.red())
    lEmbed.set_footer(text='loser loser')
    wEmbed = discord.Embed(title=f"{ctx.author.name}'s winning high-low game\nYou won!", description=f'Your hint was **{hint}**. The hidden number was **{num}**.', color=discord.Color.green())
    wEmbed.set_footer(text='Multi Bonus: +0% (⏣69)')

    try:
        input = await client.wait_for('message', check=None, timeout=30)

        if input.author.bot:
            pass
        if input.content == "high":
            if num > hint:
                await ctx.send(embed=wEmbed)
            else:
                await ctx.send(embed=lEmbed)
        elif input.content == "low":
            if num < hint:
                await ctx.send(embed=wEmbed)
            else:
                await ctx.send(embed=lEmbed)
        elif input.content == "jackpot":
            if num == hint:
                await ctx.send(embed=wEmbed)
            else:
                await ctx.send(embed=lEmbed)
        else:
            await ctx.send(f'{ctx.author.mention} Hey your options to respond are "high", "low", and "jackpot". Run the command again with more brain cells next time. (Number was {num} btw)')
    except asyncio.TimeoutError:
        await ctx.send('Imagine not answering')

if __name__ == '__main__':
    client.load_extension('cmds')
    client.run(TOKEN)