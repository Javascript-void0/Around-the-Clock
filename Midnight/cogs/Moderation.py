import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='12 ')

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['purge'], help='Clears ceratin number of messages')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'Cleared {amount} messages', delete_after=5)
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify an amount of messages to delete.')
            
    @commands.command(aliases=['user','info'], help='Info about a user')
    @commands.has_permissions(kick_members=True)
    async def whois(self, ctx, member : discord.Member):
        embed = discord.Embed(title = member.name, description = member.mention, color = discord.Color.red())
        embed.add_field(name = "ID", value = member.id, inline = True)
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(help='Kick member from Server')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member} for {reason}')

    @commands.command(help='Ban member from Server')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member} for {reason}')

    @commands.command(help='Unban members')
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @commands.command(help='Mute members')
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member):
        role = get(member.guild.roles, name="Muted")
        await member.add_roles(role)
        await ctx.send(f'Muted {member}')

def setup(client):
    client.add_cog(Moderation(client))