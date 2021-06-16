import discord
import os
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.')
TOKEN = os.getenv("TOKEN")

@client.event
async def on_ready():
    print('[ + ] Started {0.user}'.format(client))

@client.command(aliases=['i'], help='Rules Embed')
async def info(ctx):
    music = ctx.guild.get_channel(802572909746323466).mention
    pomo = ctx.guild.get_channel(802925058595094559).mention
    bot = ctx.guild.get_channel(802947754467917834).mention
    embed = discord.Embed(title='🔑 Information', description=f'These are the commonly used commands on the server. Music commands are used in {music} Pomodoro commands in {pomo}. Other commands go to {bot}. \n\n`                       📻 Jukebox                          `\n`🔊` Join a voice channel, then use Rythm bot in {music}. \n- `!play <link>`: Play a Youtube, Spotify, or Soundcloud Link\n- `!skip`: Skips the current song\n- `!queue`: Shows the queue\n\n`                      🍅 Pomodoro                          `\n`🔊` Join a voice channel, then use Pomomo bot in {pomo}. \n- `pom!start [work] [short] [long]`: Start a Pomodoro timer. Default values for [work], [short], and [long] are `25`, `5`, and `15`. \n- `pom!end`: Ends the Pomodoro timer. \n- `pom!time`: Displays the time remaining in the interval. ')
    embed.add_field(name='`                      📈 Statistics                        `', value='- `.me`\n- `.top`', inline=False)
    embed.add_field(name='`                     ⭐ Miscellaneous                      `', value='- `.toggle`', inline=False)
    embed.set_thumbnail(url='https://i.imgur.com/3pI4TnZ.jpg')
    await ctx.send(embed=embed)

if __name__ == '__main__':
    client.run(TOKEN)