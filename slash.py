import discord
import os
import random
from discord_slash import SlashCommand, SlashCommandOptionType, SlashContext
from discord.ext import commands

client = commands.Bot(command_prefix='.')
slash = SlashCommand(client, sync_commands=True)
TOKEN = os.getenv("TOKEN")

@client.event
async def on_ready():
    print('Bot Ready')

options = [
    {
        "name" : "question",
        "description" : "Ask a question. ",
        "required" : True,
        "type" : 3
    }

]

@slash.slash(name='8ball', description='8ball game', options=options)
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
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

client.run(TOKEN)