from itertools import cycle
import discord
from discord.ext import commands, tasks
import os

Status_1 = 'IM IN YOUR WALLS IM IN YOUR WALLS IM IN YOUR WALLS'
Status_2 = 'UNGA UNGA BUNGA'
Status_3 = 'crack.exe'
Status_4 = 'with peoples emotions'

status = cycle([Status_1, Status_2, Status_3, Status_4])


class on_ready(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    # Events    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.client.user}')
        self.change_status.start()
        
    
    @tasks.loop(seconds = 10)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(status)))
    
    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')

def setup(client):
    client.add_cog(on_ready(client))
        