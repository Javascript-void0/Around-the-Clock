import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='12 ', intents=intents)
TOKEN = os.getenv("MID_TOKEN")

@client.command(help='Load Cogs')
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded {extension}')

@client.command(help='Unload Cogs')
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded {extension}')

async def save_audit_logs(guild):
    async for entry in guild.audit_logs(limit=100):
        channel = guild.get_channel(802576537177030686)
        await channel.send('{0.user} did {0.action} to {0.target}'.format(entry))

for filename in os.listdir('./Midnight/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    client.run(TOKEN)
