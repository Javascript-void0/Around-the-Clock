import discord
import os
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.')
TOKEN = os.getenv("TOKEN")

@client.event
async def on_ready():
    print('[ + ] Started {0.user}'.format(client))

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
    channel = ctx.guild.get_channel(802566612187349013)
    embed = discord.Embed(title='', description='**Verify** - React with 💤 to gain access to the rest of the channels. Make sure to read {} first!'.format(channel.mention), color=discord.Color(0x84A9C3))
    embed.set_image(url='https://64.media.tumblr.com/dc22e1c917cfe51f4c810a0e6e592915/tumblr_o0n3dvSIRc1qi4ibzo1_500.gif')
    embed.set_footer(text='Not a Robot :D', icon_url='https://i.imgur.com/9vEwlsF.png')
    await ctx.send(embed=embed)

@client.command(help='Study Session Embed')
async def studysession(ctx):
    await ctx.send(file=discord.File('assets/pings.png'))
    channel = ctx.guild.get_channel(802915711122014278)
    embed = discord.Embed(title='<:down4:823376678838861855> Study Session Ping', description='Pingable by all members to start a study session in {}'.format(channel.mention), color=discord.Color(0x5D7388))
    embed.set_image(url='https://i.pinimg.com/originals/68/ae/bf/68aebf4c71bd1d6090f87237272b01e5.gif')
    embed.set_footer(text='Un-React to turn of Pings')
    await ctx.send(embed=embed)

@client.command(help='Study Help Embed')
async def studyhelp(ctx):
    english = ctx.guild.get_role(842209843275235378).mention
    biology = ctx.guild.get_role(842209456850337812).mention
    math = ctx.guild.get_role(842210482718244885).mention
    language = ctx.guild.get_role(842211473932681266).mention
    social = ctx.guild.get_role(842210564972609615).mention
    chemistry = ctx.guild.get_role(842209762853912627).mention
    programming = ctx.guild.get_role(842213186413527063).mention
    other = ctx.guild.get_role(805251882820829256).mention
    channel = ctx.guild.get_channel(802565985055014957)
    embed = discord.Embed(title='<:down4:823376678838861855> Study Help Ping(s)', description=f'Pingable by all members to get help in {channel.mention}\n\n`:book:` {english}. . . . . . . .`:seed:` {biology}\n`:infi:` {math}. . . . . . . . . `:talk:` {language}\n`:pepl:` {social}. `:tube:` {chemistry}\n`:comp:` {programming} . `:ques:` {other}', color=discord.Color(0x5D7388))
    embed.set_image(url='https://i.pinimg.com/originals/7a/e3/c7/7ae3c7ad104a968dc735871c0bf17608.gif')
    embed.set_footer(text='Un-React to turn of Pings')
    await ctx.send(embed=embed)

@client.command(help='Continents Embed')
async def continents(ctx):
    await ctx.send(file=discord.File('assets/roles.png'))
    embed = discord.Embed(title='<:down2:823376679166541834> Continent Roles', description='` North America: ` `1` ` South America: ` `2`\n`        Europe: ` `3` `          Asia: ` `4`\n`        Africa: ` `5` `     Australia: ` `6`', color=discord.Color(0x447352))
    embed.set_image(url='https://i.pinimg.com/originals/68/3f/3f/683f3ff4910420e826aa5b3318ff52c8.gif')
    await ctx.send(embed=embed)

@client.command(help='Pronouns Embed')
async def pronouns(ctx):
    embed = discord.Embed(title='<:down2:823376679166541834> Pronoun Role(s)', description='```he/him   |   she/her   |   they/them```', color=discord.Color(0x447352))
    # embed = discord.Embed(title='<:down2:823376679166541834> Pronoun Role(s)', description='`he/him` `she/her` `they/them`', color=discord.Color(0x447352))
    embed.set_image(url='https://64.media.tumblr.com/cc2e727667a023f6a89e80513c4d8649/tumblr_pdk42eWuKq1rnbw6mo1_1280.gifv')
    await ctx.send(embed=embed)

@client.command(help='DMs Embed')
async def dms(ctx):
    embed = discord.Embed(title='<:down2:823376679166541834> DMs Roles', description="```🔴: dm's open | 🟡: ask to dm | 🟢: dm's closed```", color=discord.Color(0x447352))
    embed.set_image(url='https://data.whicdn.com/images/305888882/original.gif')
    await ctx.send(embed=embed)

@client.command(help='Original Colors Embed')
async def colors(ctx):
    cozy = ctx.guild.get_role(802745474742091826)
    bright = ctx.guild.get_role(802745469407199232)
    sunrise = ctx.guild.get_role(802745476490330122)
    clover = ctx.guild.get_role(802745467251195924)
    cloud = ctx.guild.get_role(802745472263389195)
    sunset = ctx.guild.get_role(802745470988058665)
    anonymous = ctx.guild.get_role(802744112821960724)
    embed = discord.Embed(title='<:down3:823376679463419935> Color Roles', description=f"{cozy.mention}{sunrise.mention}{bright.mention}{clover.mention}{cloud.mention}{sunset.mention}{anonymous.mention}", color=discord.Color(0xFEFDD1))
    # embed = discord.Embed(title='<:down3:823376679463419935> Color Roles', color=discord.Color(0xFEFDD1))
    embed.set_image(url='https://i.pinimg.com/originals/51/45/23/5145235480824587a34264859401580e.gif')
    await ctx.send(embed=embed)

@client.command(name='3colors', help='3x Colors Embed')
async def _3colors(ctx):
    lp = ctx.guild.get_role(842812625946935306).mention
    p = ctx.guild.get_role(842812626584600639).mention
    dp = ctx.guild.get_role(842812628220903474).mention
    lo = ctx.guild.get_role(842812649275523123).mention
    o = ctx.guild.get_role(842812649929441321).mention
    do = ctx.guild.get_role(842812651297570816).mention
    lb = ctx.guild.get_role(842812660671184957).mention
    b = ctx.guild.get_role(842812661779136542).mention
    db = ctx.guild.get_role(842812662567665736).mention
    lg = ctx.guild.get_role(842812671267307552).mention
    g = ctx.guild.get_role(842812672239992872).mention
    dg = ctx.guild.get_role(842812673204944896).mention
    lbl = ctx.guild.get_role(842812688866607105).mention
    bl = ctx.guild.get_role(842812689742299168).mention
    dbl = ctx.guild.get_role(842812691072155678).mention
    lpu = ctx.guild.get_role(842812703399346308).mention
    pu = ctx.guild.get_role(842812704795787325).mention
    dpu = ctx.guild.get_role(842812705764671529).mention
    lgr = ctx.guild.get_role(842812734634328065).mention
    gr = ctx.guild.get_role(842812735863652402).mention
    dgr = ctx.guild.get_role(842812736772505621).mention
    embed = discord.Embed(title='Color Roles', description=f"{lp}{p}{dp}\n\n{lo}{o}{do}\n\n{lb}{b}{db}\n\n{lg}{g}{dg}\n\n{lbl}{bl}{dbl}\n\n{lpu}{pu}{dpu}\n\n{lgr}{gr}{dgr}")
    await ctx.send(embed=embed)

if __name__ == '__main__':
    client.run(TOKEN)