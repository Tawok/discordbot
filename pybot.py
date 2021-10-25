import discord
from discord.embeds import Embed
from discord.flags import Intents
from discord.user import ClientUser
import requests
from env_keys import *
import datetime
from ratings import *

def run():
    intents = discord.Intents().default()
    intents.members = True
    client = discord.Client(intents=intents)

    api_blizz_url = 'https://us.api.blizzard.com'

    #Announcement when bot is active
    @client.event
    async def on_ready():
        general_channel = client.get_channel(848075997949460534)
        await general_channel.send(f'Hello, Femi is online')

    #Command to know the actual price of the wow token
    @client.event
    async def on_message(message):
        split_message = message.content.split('/')
        print(split_message)

         #price of the wow token
        if message.content.lower() == '!wowtoken':
            general_channel = client.get_channel(848075997949460534)
            args = {'namespace':'dynamic-us', 'locale':'en_US','access_token': access_token}
            url = f'{api_blizz_url}/data/wow/token/index'
            r2 = requests.get(url, params=args).json()
            token_price = r2['price']/10000
            token_date = datetime.datetime.now().date()
            await general_channel.send(f'{int(token_price)} :coin: {token_date}')

        #Rbg rating of tawok
        elif split_message[0] == '!rbg':
            name = split_message[1]
            channel_rbg = client.get_channel(851816302786904076)
            try:
                embed_message = discord.Embed()
                embed_message.add_field(name='Rbg Rating', value= Ratings.rating_rbg(Ratings(name)))
                await channel_rbg.send(embed=embed_message)
            except Exception:
                embed_message = discord.Embed()
                embed_message.add_field(name='Rbg Rating', value= 'There is no rating')
                await channel_rbg.send(embed=embed_message)
            

        #2v2 rating of tawok
        elif split_message[0] == '!2v2':
            name = split_message[1]
            channel_2v2 = client.get_channel(851816361042640966)
            try:
                embed_message = discord.Embed()
                embed_message.add_field(name='2v2 Rating', value= Ratings.rating_2v2(Ratings(name)))
                await channel_2v2.send(embed=embed_message)
            except Exception:
                embed_message = discord.Embed()
                embed_message.add_field(name='2v2 Rating', value= 'There is no 2v2 Rating')
                await channel_2v2.send(embed=embed_message)

        #3v3 rating of tawok
        elif split_message[0] == '!3v3':
            name = split_message[1]
            channel_3v3 = client.get_channel(851816395927060511)
            try:
                embed_message = discord.Embed()
                embed_message.add_field(name='3v3 Rating', value= Ratings.rating_3v3(Ratings(name)))
                await channel_3v3.send(embed=embed_message)
            except Exception:
                embed_message = discord.Embed()
                embed_message.add_field(name='3v3 Rating', value= 'There is no 3v3 Rating')
                await channel_3v3.send(embed=embed_message)

    #Greetings to new memebers
    @client.event
    async def on_member_join(member):
        guild = client.get_guild(848075997949460531)
        channel = guild.get_channel(848075997949460534)
        await channel.send(f'Bienvenid@ al canal {member} :space_invader:')
        await member.send(f'Bienvenid@ al canal {member} :space_invader:')


    client.run('ODQ4MDM3NzgzNjc4MzUzNDU5.YLGyuw.3jD_gC5blz-iay2dAoihRkLdVpk')

if __name__ == '__main__':
    run()