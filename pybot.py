import discord
from discord.channel import VoiceChannel
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.voice_client import VoiceClient
import youtube_dl
import requests
from env_keys import *
import datetime
from apitoken import access_token
from discord_keys import *

def run():
    intents = discord.Intents().default()
    intents.members = True

    client = commands.Bot(command_prefix= '!', intents=intents)

    #Playlist Queue's
    playlist = {}

    def check_queue(ctx, id):
        if playlist[id] != []:
            voice= ctx.guild.voice_client
            source = playlist[id].pop(0)
            play = voice.play(source)


    api_blizz_url = 'https://us.api.blizzard.com'

    """EVENTS"""
    #Announcement when bot is active
    @client.event
    async def on_ready():
        general_channel = client.get_channel(generalChannel)
        await general_channel.send(f'Hello, Femi is online')
    
    #Welcoming new guild memebers
    @client.event
    async def on_member_join(member):
        guild = client.get_guild(discordId)
        channel = guild.get_channel(generalChannel)
        await channel.send(f'Welcome to the Guild {member} :space_invader:')
        await member.send(f'Welcome to the Guild {member} :space_invader:')

    """COMMANDS"""        
    
    #"!wowtoken" command
    @client.command()
    async def wowtoken(ctx):
        args = {'namespace':'dynamic-us', 'locale':'en_US','access_token': access_token}
        url = f'{api_blizz_url}/data/wow/token/index'
        r2 = requests.get(url, params=args).json()
        token_price = r2['price']/10000
        token_date = datetime.datetime.now().date()
        await ctx.send(f'{int(token_price)} :coin: {token_date}')
    
    #Voice command        
    @client.command(pass_context=True)
    async def join(ctx):
        ctx.author.voice
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("I'm in the channel")

    @client.command(pass_context=True)
    async def youtube(ctx, url):
        FFmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format':'bestaudio', 'noplaylist':'True'}
        voice= ctx.voice_client
        
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFmpeg_options)
            voice.play(source, after=(lambda x=None: check_queue(ctx, ctx.message.guild.id)))
    
    @client.command(pass_context=True)
    async def queue(ctx, url):
        FFmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format':'bestaudio', 'noplaylist':'True'}
        voice= ctx.voice_client
        
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFmpeg_options)
            
            guild_id = ctx.message.guild.id

            if guild_id in playlist:
                playlist[guild_id].append(source)
            else:
                playlist[guild_id] = [source]

            await ctx.send('Added to the playlist')
    
    @client.command(pass_context=True)
    async def leave(ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("Femi leaving the voice channel")
        else:
            await ctx.send("Femi not in the voice channel")

    #Rating command
    @client.command()
    async def pvp2v2(ctx, realm, character):
        realm_name = realm.lower()
        character_name = character.lower()
        args = {'namespace':'profile-us', 'locale':'en_US', 'access_token': access_token}
        url = f'https://us.api.blizzard.com/profile/wow/character/{realm_name}/{character_name}/pvp-bracket/2v2'
        r1 = requests.get(url, params=args).json()
        try:
            r1_rating = r1['rating']
            embed_message = discord.Embed(title= '2v2 Rating', description= r1_rating, color=discord.Color.red())
            await ctx.send(embed=embed_message)
        except Exception:
            embed_message = discord.Embed(title= 'Noob Rating', description= 'There is no 2v2 Rating', color=discord.Color.red())
            await ctx.send(embed=embed_message)

    @client.command()
    async def pvp3v3(ctx, realm, character):
        realm_name = realm.lower()
        character_name = character.lower()
        args = {'namespace':'profile-us', 'locale':'en_US', 'access_token': access_token}
        url = f'https://us.api.blizzard.com/profile/wow/character/{realm_name}/{character_name}/pvp-bracket/3v3'
        r1 = requests.get(url, params=args).json()
        try:
            r1_rating = r1['rating']
            embed_message = discord.Embed(title= '3v3 Rating', description= r1_rating, color=discord.Color.red())
            await ctx.send(embed=embed_message)
        except Exception:
            embed_message = discord.Embed(title='Noob Rating', description= 'There is no 3v3 Rating', color=discord.Color.red())
            await ctx.send(embed=embed_message)

    @client.command()
    async def pvprbg(ctx, realm, character):
        realm_name = realm.lower()
        character_name = character.lower()
        args = {'namespace':'profile-us', 'locale':'en_US', 'access_token': access_token}
        url = f'https://us.api.blizzard.com/profile/wow/character/{realm_name}/{character_name}/pvp-bracket/rbg'
        r1 = requests.get(url, params=args).json()
        try:
            r1_rating = r1['rating']
            embed_message = discord.Embed(title='rbg Rating', description= r1_rating, color=discord.Color.red())
            await ctx.send(embed=embed_message)
        except Exception:
            embed_message = discord.Embed(title='rbg Rating', description= 'There is no rbg Rating', color=discord.Color.red())
            await ctx.send(embed=embed_message)

    #macro commands
    @client.command()
    async def macro(ctx, arg):
        key = arg.lower()
        if arg == 'intervane':
            embed_message = discord.Embed(title='Intervane (warrior) macro', 
                description= '/cast [@mouseover,exists][@target,exists][@help][@focus] Intervene',
                color=discord.Color.red())
            embed_message.add_field(name= "Macro description", 
                value= """This macro only works with "intervane (warrior ability)", can by casted by mousing over a freindy target, targeting the target or focusing the target""")  
            await ctx.send(embed=embed_message)
        
        elif arg == '@player':
            embed_message = discord.Embed(title='@player macro', 
                description= """#showtooltip <Ability name>\n/cast [@player] <Ability name>""",
                color=discord.Color.red())
            embed_message.add_field(name= "Macro description", 
                value= 'This macro can be used to cast any ability that can be casted on your charachter')
            embed_message.add_field(name= "Exmple", 
                value= '#showtooltip Death and Decay\n/cast [@player] Death and Decay', inline=False)              
            await ctx.send(embed=embed_message)
            
    client.run(discordKey)

if __name__ == '__main__':
    run()