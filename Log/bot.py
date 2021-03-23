import discord
import os
import time
import datetime
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')
TOKEN = os.getenv("AUDIT_TOKEN")

def get_dt():
    t = time.localtime()
    t = time.strftime("%I:%M %p", t)
    d = time.strftime("%m/%d/%Y")
    return d,t
    
def nsfw(n):
    if n == True:
        nsfw = 'Marked'
    else:
        nsfw = 'Unmarked'
    return nsfw

def typeRename(channel):
    if channel == discord.ChannelType.text:
        tp = 'Text Channel'
    elif channel == discord.ChannelType.news:
        tp = 'Announcement Channel'
    elif channel == discord.ChannelType.voice:
        tp = 'Voice Channel'
    return tp

def guildCheck(event):
    if event.guild.id == 802565984602423367:
        return True
    else:
        return False

@client.event
async def on_ready():
    print('[ + ] Started {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the Audit Log"))

@client.event
async def on_member_join(member):
    if guildCheck(member) == True:
        log_channel = client.get_channel(802577837365133312)
        created = member.created_at.strftime("%b %d, %Y")
        d,t = get_dt()

        today = datetime.date.today()
        timeAgo = member.created_at.date()
        delta = today - timeAgo

        embed = discord.Embed(title='[ + ] Member Joined', description='{} {}#{}\n`01` - Account Created on **{}**\n`02` - Account Created **{}** Days Ago'.format(member.mention, member.display_name, member.discriminator, created, delta.days))
        embed.set_footer(text=f'{d}, {t} | {member.id}')
        await log_channel.send(embed=embed)

@client.event
async def on_member_remove(member):
    if guildCheck(member) == True:
        log_channel = client.get_channel(802577837365133312)
        d,t = get_dt()
        embed = discord.Embed(title='[ - ] Member Left', description='{} {}#{}'.format(member.mention, member.display_name, member.discriminator))
        embed.set_footer(text=f'{d}, {t} | {member.id}')
        await log_channel.send(embed=embed)

@client.event
async def on_message_delete(message):
    if guildCheck(message) == True:
        log_channel = client.get_channel(802577837365133312)
        d,t = get_dt()
        embed = discord.Embed(title='[ - ] Message Deleted', description='{} deleted a message in {}\n`01` - {}'.format(message.author.mention, message.channel.mention, message.content))
        embed.set_footer(text=f'{d}, {t}')
        await log_channel.send(embed=embed)

@client.event
async def on_message_edit(before, after):
    if guildCheck(before) == True:
        log_channel = client.get_channel(802577837365133312)
        d,t = get_dt()

        if before.author.bot:
            pass
        elif before.channel == log_channel:
            pass
        elif before.channel.id == 806150413773963275:
            pass
        else:
            embed = discord.Embed(title='[ + ] Message Edited', description='{} edited a [message]({}) in {}\n`01` - From **{}**\n`02` - To **{}**'.format(before.author.mention, before.jump_url, before.channel.mention, before.content, after.content))
            embed.set_footer(text=f'{d}, {t}')
            await log_channel.send(embed=embed)

@client.event
async def on_guild_channel_delete(channel):
    if guildCheck(channel) == True:
        log_channel = client.get_channel(802577837365133312)
        entry = await channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1).get()
        d,t = get_dt()
        embed = discord.Embed(title='[ - ] Channel Deleted', description='{} removed #{}'.format(entry.user.mention, channel.name))
        embed.set_footer(text=f'{d}, {t}')
        await log_channel.send(embed=embed)

@client.event
async def on_guild_channel_create(channel):
    if guildCheck(channel) == True:
        log_channel = client.get_channel(802577837365133312)
        entry = await channel.guild.audit_logs(action=discord.AuditLogAction.channel_create, limit=1).get()

        if channel.type == discord.ChannelType.text:
            tp = 'Text Channel'
            slow = channel.slowmode_delay
            n = nsfw(channel.nsfw)
            if slow == 0:
                slow = 'disabled'

        elif channel.type == discord.ChannelType.news:
            tp = 'Announcement Channel'
            n = nsfw(channel.nsfw)

        elif channel.type == discord.ChannelType.voice:
            tp = 'Voice Channel'

        if tp == 'Voice Channel':
            embed = discord.Embed(title='[ + ] Channel Created', description='{} created a voice channel **{}**\n`01` - Set the name to **{}**\n`02` - Set the type to **{}**\n`03` - Set the bitrate of **{}**\n`04` - Set the user limit of **{}**'.format(entry.user.mention, channel.name, channel.name, tp, channel.bitrate//1000, channel.user_limit))
        else:
            embed = discord.Embed(title='[ + ] Channel Created', description='{} created a text channel **#{}**\n`01` - Set the name to **{}**\n`02` - Set the type to **{}**\n`03` - {} the channel as NSFW\n`04` - Set slowmode {}'.format(entry.user.mention, channel.name, channel.name, tp, n, slow))
        
        d,t = get_dt()
        embed.set_footer(text=f'{d}, {t}')
        await log_channel.send(embed=embed)

@client.event
async def on_guild_channel_update(before, after):
    if guildCheck(before) == True:

        if before.type == discord.ChannelType.voice:
            x = '`01` - Changed the name from **{}** to **{}**'.format(before.name, after.name)
        else:
            if before.topic != after.topic:
                x = '`01` - Changed the topic to **{}**'.format(after.topic)
            if before.nsfw != after.nsfw:
                n = nsfw(after.nsfw)
                x = '`01` - {} the channel as NSFW'.format(n)
            if before.slowmode_delay != after.slowmode_delay:
                x = '`01` - Set slowmode to **{}**'.format(after.slowmode_delay//1000)
            if before.type != after.type:
                b = typeRename(before.type)
                a = typeRename(after.type)
                x = '`01` - Changed the type from **{}** to **{}**'.format(b, a)
            if before.name != after.name:
                x = '`01` - Changed the name from **{}** to **{}**'.format(before.name, after.name)
            
        log_channel = client.get_channel(802577837365133312)
        guild = client.get_guild(802565984602423367)
        entry = await guild.audit_logs(action=discord.AuditLogAction.channel_update, limit=1).get()
        embed = discord.Embed(title='[ + ] Channel Updated', description='{} made changes to **#{}**\n{}'.format(entry.user.mention, before, x))
        d,t = get_dt()
        embed.set_footer(text=f'{d}, {t}')
        await log_channel.send(embed=embed)

'''
@client.event
async def on_member_update(before, after):
    log_channel = client.get_channel(802577837365133312)

    async for entry in before.guild.audit_logs(action=discord.AuditLogAction.member_update, limit=100):
        if entry.user.discriminator == '4774':
            pass
        else:
            entry = entry.id
            if len(before.roles) < len(after.roles):
                n = next(role for role in after.roles if role not in before.roles)
                x = '`01` - **Added** a role\n{}'.format(n)
                embed = discord.Embed(title='[ + ] Member Updated', description='{} updated roles for **{}**\n{}'.format(entry.user.mention, before.mention, x))
            if len(before.roles) > len(after.roles):
                n = next(role for role in before.roles if role not in after.roles)
                x = '`01` - **Removed** a role\n{}'.format(n)
                embed = discord.Embed(title='[ - ] Member Updated', description='{} updated roles for **{}**\n{}'.format(entry.user.mention, before.mention, x))
            break
    
    d,t = get_dt()
    try:
        embed.set_footer(text=f'{d}, {t}')
    except UnboundLocalError:
        pass
    else:
        await log_channel.send(embed=embed)
'''
'''
    if before.nick != after.nick:
        if after.nick:
            x = '`01` - Set their nickname to **{}**'.format(after.nick)
            embed = discord.Embed(title='[ + ] Member Updated', description='{} updated **{}**\n{}'.format(entry.user.mention, before.mention, x))
        else:
            x = '`01` - **Removed** their nickname of **{}**'.format(before.nick)
            embed = discord.Embed(title='[ - ] Member Updated', description='{} updated **{}**\n{}'.format(entry.user.mention, before.mention, x))
'''

@client.event
async def on_message(message):
    if message.guild:
        pass
    elif message.author.id == 804094737321164800:
        g = client.get_guild(805299220935999509)
        log_channel = g.get_channel(802577837365133312)
        await log_channel.send(message.content)
    else:
        pass

if __name__ == '__main__':
    client.run(TOKEN)