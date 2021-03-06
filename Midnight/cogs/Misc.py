import discord
import random
from discord.ext import commands

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(help='Latnecy')
    async def ping(self, ctx):
        await ctx.send(f'**Current Ping:** {round(self.client.latency * 1000)}ms')

'''
    @commands.command(aliases=['8ball'], help='Tell the future')
    async def _8ball(self, ctx, *, question):
        responses = [
            'It is ceratin.', 'It is decidedly so.', 'Without a doubt.',
            'You may rely on it.', 'As I see it, yes.', 'Most likely.',
            'Outlook good.', 'Yes.', 'Signs point to yes.',
            'Reply hazy, try again.', 'Ask again later.',
            'Better not tell you now.', 'Cannot predict now.',
            'Concentrate and ask again.', "Don't count on it.", 'My reply is no.',
            'My sources say no.', 'Outlook not so good.', 'Very doubtful.'
        ]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
'''

def setup(client):
    client.add_cog(Misc(client))