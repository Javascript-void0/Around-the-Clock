import discord
import os
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.')
TOKEN = os.getenv("TOKEN")

@client.event
async def on_ready():
    print('[ + ] Started {0.user}'.format(client))
    print(f'[ + ] Connected to database...')

@client.command(help='Rules Embed')
async def rules(ctx):
    embed = discord.Embed(title='Rules', description='', color=discord.Color(0x2A254A))
    embed.add_field(name='1. Keep All Channels SFW', value='Kepe all topics and images clean. Limit swearing. ', inline=False)
    embed.add_field(name='2. Use channels For Their Proper Use', value="Don't misuse channels. Each of them have their uses. ", inline=False)
    embed.add_field(name="3. Don't Spam / Flood", value='This includes character spam, image spam, copy and pasting large text, etc. ', inline=False)
    embed.add_field(name='4. Respect Everyone', value="Respect all users and their opinions. Please don't insult, bully, or harass anyone. ", inline=False)
    embed.add_field(name="5. Don't advertise", value="Any form of advertising is not allowed. This includes posting invites, sending invites in DMs, advertising social media accounts, etc. ", inline=False)
    embed.add_field(name='6. Have Common Sense', value="If you're not sure something is allowed then please don't post it. Not every rule can be listed so you must have common sense. ", inline=False)
    embed.add_field(name='7. The Staff Team Always Have The Final Say', value="Don't argue with staff members about their modertation activity. If you don't agree with a moderation actions, please discuss with an admin. ", inline=False)
    embed.add_field(name='8. Follow Discord TOS', value="Follow Discord's rules on their pklatform. ", inline=False)
    embed.set_image(url='https://i.pinimg.com/originals/c9/d9/96/c9d996923cc95ef0c010f4dbc7612d50.gif')
    embed.set_footer(text='Follow These Rules to Not Get Banned :D', icon_url='https://media.tenor.com/images/4223cf9120369eea473fcf3565c4e676/tenor.gif')
    await ctx.send(embed=embed)

@client.command(help='Verify Embed')
async def verify(ctx):
    embed = discord.Embed(title='', description='**Verify** - React with 💤 to gain access to the rest of the channels. Make sure to read the rules first!', color=discord.Color(0x84A9C3))
    embed.set_image(url='https://64.media.tumblr.com/dc22e1c917cfe51f4c810a0e6e592915/tumblr_o0n3dvSIRc1qi4ibzo1_500.gif')
    embed.set_footer(text='Not a Robot :D', icon_url='https://i.imgur.com/9vEwlsF.png')
    await ctx.send(embed=embed)

@client.command(help='Study Session Embed')
async def studysession(ctx):
    embed = discord.Embed(title='Study Sesion Ping')
    embed.set_image(url='https://i.pinimg.com/originals/68/ae/bf/68aebf4c71bd1d6090f87237272b01e5.gif')
    await ctx.send(embed=embed)







if __name__ == '__main__':
    client.run(TOKEN)