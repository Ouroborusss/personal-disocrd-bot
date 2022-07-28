from discord.ext import commands

class clear(commands.Cog):
    
    def __init__(self, client):
        self.client = client
 
    # Commands
    @commands.command()
    async def clear(self, ctx, amount = 1000):
        await ctx.channel.purge(limit = amount)
    
def setup(client):
    client.add_cog(clear(client))