import discord
import json
import traceback
import os
import asyncio
import urllib
import requests
#from usefulFunctions import dubApos
from discord.ext import commands

URL_SEARCH = "http://radio.garden/api/search?q="
URL_LISTEN = "https://radio.garden/api/ara/content/listen/"

bot = commands.Bot(command_prefix='`')

gResults = []

def getListenURL(channelID):
    return URL_LISTEN + channelID + "/channel.mp3"

def removeRGQueryString(url):
    # RadioGarden Adds a query string (always?)
    # https://plaza.one/mp3?listening-from-radio-garden=1595772606590
    # screws up some radio stations
    pos = url.find("?listening-from-radio-garden")
    if(pos != -1):
        return url[:pos]
    else:
        return url

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    
@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("hello", delete_after=20)

@bot.command(name="quit")
async def quit(ctx):
    os._exit
    
# TODO do something when places are returned
@bot.command(name="search", aliases=['lookup'])
async def search(ctx, printMsg = True, *args):
    searchTerms = ""
    for keyword in args:
        searchTerms = searchTerms + " " + keyword
    print(searchTerms)
    with urllib.request.urlopen(URL_SEARCH + urllib.parse.quote(searchTerms)) as url:
        apiResults = json.loads(url.read())
        msg = "Showing results for query: " + str(apiResults["query"]) + "\n"
        results = apiResults["hits"]["hits"]
        
        global gResults
        gResults = ['1LLUcpsj'] #nightwaveplaza placeholder since list is going to start from 1
        
        number = 1
        for result in range(len(results)):
            try:
                if(results[result]["_source"]["type"] == "channel"):
                    msg = msg + str(number) + ". " 
                    msg = msg + results[result]["_source"]["title"]
                    msg = msg + "\n\t" + results[result]["_source"]["subtitle"]
                    msg = msg + "\n\n"
                    url = results[result]["_source"]["url"]
                    gResults.append(url[-8:])
                    number = number + 1
            except:
                print(traceback.format_exc())
        print(gResults)
        if printMsg:
            await ctx.send(msg[:2000])     
        
@bot.command(name="play")
async def play(ctx, *args):
    global gResults
    print(gResults)
    firstTerm = args[0]
    isNumber = False
    try: 
        selected = int(firstTerm)
        isNumber = True
    except:
        print("Searching")
    finally:
        if not isNumber:
            await search(ctx, False, *args)
            selected = 1

        print(selected)        
        x = requests.head(getListenURL(gResults[selected]))
        print("headers")
        print(x.headers)
        if(x.status_code == 302):
            url = x.headers['Location']
            await restartStream(ctx, removeRGQueryString(url))
          
    
@bot.command(name="connect", aliases=['join'])
async def connect_(ctx, *, channel: discord.VoiceChannel=None):
    if not channel:
        try:
            channel = ctx.author.voice.channel
        except:
            await ctx.send("Hey buddy, you need to join a voice channel") 
    vc = ctx.voice_client
    if vc:
        if vc.channel.id == channel.id:
            return
        try:
            await vc.move_to(channel)
        except: 
            await ctx.send("Timeout") 
    else:
        try:
            await channel.connect()
        except: 
            await ctx.send("Timeout") 
    await ctx.send(f'Connected to: **{channel}**', delete_after=20)
    
@bot.command(name="stream")
async def stream_(ctx, *args, channel: discord.VoiceChannel=None):
    global player
    if not channel:
        try:
            channel = ctx.author.voice.channel
        except:
            await ctx.send("Hey buddy, you need to join a voice channel") 
    vc = ctx.voice_client
    if vc:
        if vc.channel.id == channel.id:
            return
        try:
            await vc.move_to(channel)
        except: 
            await ctx.send("Timeout") 
    else:
        try:
            player = await channel.connect()
        except: 
            await ctx.send("Timeout") 
    await ctx.send(f'Connected to: **{channel}** \n playing: ' + args[0], delete_after=20)
    stop(ctx)
    player.play(discord.FFmpegPCMAudio(args[0]))

@bot.command(name="pause")
async def pause(ctx):
    player.stop()
    
async def restartStream(ctx, url: str):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    ctx.voice_client.play(discord.FFmpegPCMAudio(url))
        
bot.run('YOUR_TOKEN_HERE')


