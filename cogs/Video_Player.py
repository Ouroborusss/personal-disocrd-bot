from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import youtube_dl
from pydoc import cli
import discord
from discord.ext import commands
import asyncio
import urllib.request
import re

MUSIC_CHANNEL = 979804135698341908

NO_AUDIO_ON_RESUME_MESSAGE = 'Nothing in queue to resume.'
AUDIO_RESUME = 'Audio has been resumed.'

NO_AUDIO_ON_PAUSE_MESSAGE = 'There is no audio to pause.'
AUDIO_PAUSE = 'Audio has been paused.'

NO_AUDIO_ON_SKIP_MESSAGE = 'There is no audio to skip.'
AUDIO_SKIP = 'Audio has been skipped.'

ENTER_CHANNEL_MESSAGE = 'I AM HERE TO PLAY.'
ALREADY_IN_CHANNEL_MESSAGE = 'I am already here.'

EXIT_CHANNEL_MESSAGE = 'I AM BANISHED.'
NOT_IN_CHANNEL_TO_LEAVE = 'Cannot leave since I am not here in the voice channel.'

NO_AUDIO_QUEUE = 'There is no audio in queue.'

NO_AUDIO_QUEUE_CLEAR = 'There is no audio in queue.'
AUDIO_QUEUE_CLEARED = "Queue has been cleared."
SONG_QUEUED = 'Song has been queued.'

UNSUPPORTED_LINK = "Link is not supported."

BOT_AFK_LEAVE = 'I have left for innactivity.'

AFK_TIMEOUT_IN_MINUTES = 10

AFK_TIMEOUT = AFK_TIMEOUT_IN_MINUTES * 12

queue = []

def is_supported(url):
    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(url) and e.IE_NAME != 'generic':
            return True
    return False

def playQueue(self, ctx):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        client = self.client
        voice = get(client.voice_clients, guild=ctx.guild)
        
        if len(queue) != 0:
            with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(queue[0], download=False)
                    URL = info['url']
            if voice == None:
                return
        
            del queue[0]
        
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: playQueue(self, ctx))

class Music_Bot(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context = True)
    async def play(self, ctx, searchterm):
        client = self.client
        voice = get(client.voice_clients, guild=ctx.guild)
        textChannel = client.get_channel(MUSIC_CHANNEL)
        
        #checks if is link if not searches youtube for link
        if 'www.youtube.com/watch?v=' in searchterm:
            print('already link')
            url = searchterm
        else:
            print("Origional Wording: " + searchterm.replace(" ","-"))
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + str(searchterm.replace(" ","-")))
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            url = 'https://www.youtube.com/watch?v='+video_ids[0]
            print("Final Link" + 'https://www.youtube.com/watch?v='+video_ids[0])
        
        #checks if voice is not connects if no then connect
        if voice == None:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await textChannel.send(ENTER_CHANNEL_MESSAGE)
        
        print("play")
        
        #checks if first song play if yes play song and enter play next recursion if no add song to queue
        voice = get(client.voice_clients, guild=ctx.guild)
        if len(queue) == 0 and voice.is_playing() == False:
            queue.append(url)
            playQueue(self, ctx)
        else:
            queue.append(url)
    
    @commands.command(pass_context = True)
    async def join(self, ctx):
        client = self.client
        voice = get(client.voice_clients, guild=ctx.guild)
        textChannel = client.get_channel(MUSIC_CHANNEL)
        if voice == None:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await textChannel.send(ENTER_CHANNEL_MESSAGE)
        else:
            await textChannel.send(ALREADY_IN_CHANNEL_MESSAGE)
        print("join")
    
    @commands.command(pass_context = True)
    async def leave(self, ctx):
        client = self.client
        voice = get(client.voice_clients, guild=ctx.guild)
        textChannel = client.get_channel(MUSIC_CHANNEL)
        if voice != None:
            voice_client = ctx.guild.voice_client
            await voice_client.disconnect()
            await textChannel.send(EXIT_CHANNEL_MESSAGE)
        else:
            await textChannel.send(NOT_IN_CHANNEL_TO_LEAVE)
        print("leave")
        queue.clear()
        
        
    @commands.command(pass_context = True)
    async def pause(self,ctx):
        client = self.client
        voice = get(client.voice_clients, guild=ctx.guild)
        channel = client.get_channel(MUSIC_CHANNEL)
        if voice.is_playing():
            voice.pause()
            await channel.send(AUDIO_PAUSE)
        else:
            await channel.send(NO_AUDIO_ON_PAUSE_MESSAGE)
        print("pause")
    
    @commands.command(pass_context = True)
    async def resume(self, ctx):
        client = self.client
        voice = get(client.voice_clients, guild=ctx.guild)
        channel = client.get_channel(MUSIC_CHANNEL)
        if voice.is_paused():
            voice.resume()
            await channel.send(AUDIO_RESUME)
        else:
            await channel.send(NO_AUDIO_ON_RESUME_MESSAGE)
        print("resume")
            
    @commands.command(pass_context = True)
    async def skip(self, ctx):
        client = self.client
        voice = get(client.voice_clients, guild=ctx.guild)
        channel = client.get_channel(MUSIC_CHANNEL)
        if voice.is_playing() and len(queue) == 0:
            queue.clear()
            voice.stop()
            await channel.send(AUDIO_SKIP)
        elif voice.is_playing():
            voice.stop()
            #play_next(self, ctx)
            await channel.send(AUDIO_SKIP)
        else:
            await channel.send(NO_AUDIO_ON_SKIP_MESSAGE)
        print("skip")
        
    
    @commands.command(pass_context = True)
    async def pop(self):
        client = self.client
        channel = client.get_channel(MUSIC_CHANNEL)
        if len(queue) == 0:
            await channel.send('No Audio to pop.')
            return
        else:
            await channel.send('Audio has been popped.')
            queue.pop()
            
    
    @commands.command(pass_context = True)
    async def showq(self, ctx):
        client = self.client
        channel = client.get_channel(MUSIC_CHANNEL)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        index = 0
        if len(queue) == 0:
             await channel.send(NO_AUDIO_QUEUE)
        else:    
            for i in queue:
                with YoutubeDL(ydl_opts) as ydl:
                    #info = ydl.extract_info(i, download=False)
                    #URL = info['url']
                    info_dict = ydl.extract_info(i, download=False)
                    
                    video_url = info_dict.get("url", None)
                    video_id = info_dict.get("id", None)
                    video_title = info_dict.get('title', None)
                    video_creator = info_dict.get('channel', None)
                
                embed = discord.Embed(title=video_title,  url = video_url, 
                    description = 'This is song number ' + str(index + 1) + ' in queue.',  
                    color = 0xFF5733)
                
                embed.set_author(name=video_creator, 
                    icon_url = ctx.author.avatar_url)
                
                embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
                
                embed.set_thumbnail(url = 'http://img.youtube.com/vi/' + str(video_id) + '/default.jpg')
                
                index = index + 1
                
                await ctx.channel.send(embed=embed)
            
        
        print("show queue")
    
    @commands.command(pass_context = True)
    async def clearq(self, ctx):
        client = self.client
        channel = client.get_channel(MUSIC_CHANNEL)
        if len(queue) == 0:
            await channel.send(NO_AUDIO_QUEUE_CLEAR)
        else:    
            queue.clear()
            await channel.send(AUDIO_QUEUE_CLEARED)
        print("clear queue")
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        if not member.id == self.client.user.id:
            return

        elif before.channel is None:
            voice = after.channel.guild.voice_client
            time = 0
            while True:
                await asyncio.sleep(5)
                time = time + 1
                if voice.is_playing() and not voice.is_paused():
                    time = 0
                if time == AFK_TIMEOUT:
                    await voice.disconnect()
                    channel = self.client.get_channel(MUSIC_CHANNEL)
                    await channel.send(BOT_AFK_LEAVE)
                if not voice.is_connected():
                    break

 

def setup(client):
    client.add_cog(Music_Bot(client))