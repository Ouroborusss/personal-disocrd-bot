from discord.ext import commands
import discord

test = 'hi'

class embed(commands.Cog):
    def __init__(self, client):
        self.client = client
 
    # Commands
    @commands.command()
    async def testEmbed(self, ctx):
        embed = discord.Embed(title="TEST SONG NAME", 
            url = "https://hambutton.com/", 
            description = test, 
            color = 0xFF5733)
        
        embed.set_author(name="TEST SONG CHANNEL", 
            url = "https://hambutton.com/", 
            icon_url = ctx.author.avatar_url)
        
        embed.add_field(name="Field 2 Title", 
            value = "It is inline with Field 3", 
           
            inline=True)
        
        embed.add_field(name="Field 3 Title", 
            value = "It is inline with Field 2", 
            inline = True)
       
        embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
        
        #embed.set_image(url="https://img.youtube.com/vi/2QMeGkbdIVw/default.jpg")
        
        embed.set_thumbnail(url = "https://img.youtube.com/vi/2QMeGkbdIVw/default.jpg")
        
        await ctx.channel.send(embed=embed)
    
    @commands.command()
    async def serverInfo(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)
        
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)
        
        icon = ctx.guild.icon_url
        
        embed = discord.Embed(
            title = name + " Server Information",
            description = description,
            color = discord.Color.blurple()
        )
        embed.set_thumbnail(url = icon)
        embed.add_field(name = "Owner", value = owner, inline=True)
        embed.add_field(name = "Server ID", value = id, inline=True)
        embed.add_field(name = "Region", value = region, inline=True)
        embed.add_field(name = "Member Count", value = memberCount, inline=True)
    
        await ctx.send(embed = embed)
        
def setup(client):
    client.add_cog(embed(client))