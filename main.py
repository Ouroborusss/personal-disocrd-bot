from discord.ext import commands
import discord
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

AUTO_ROLE = 'Basic-Bitch'
ENTER_CHANNEL = 978748432661504002

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="-", intents=intents)

#discord.opus.load_opus(name='opus')
#if not discord.opus.is_loaded():
#    print("runtime error")

@client.event
async def on_member_join(member):
    #await member.send('Private message')
    print("User " + str(member.display_name) + " Joined")
    role = discord.utils.get(member.guild.roles, name=AUTO_ROLE)
    await member.add_roles(role)
    channel = client.get_channel(ENTER_CHANNEL)
    await channel.send("Welcome " + str(member.display_name) + "!")
    

################# cog func #############

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

################# load cogs #############

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)