import discord
import traceback
import os
import asyncio
from usefulFunctions import dubApos
from discord.ext import commands

URL_SEARCH = "http://radio.garden/api/search?q="

conn = sqlite3.connect('radioGarden.db')
c = conn.cursor()

bot = commands.Bot(command_prefix='`')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    
@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("hello", delete_after=20)

@bot.command(name="quit")
async def quit(ctx):
    os._exit
    
@bot.command(name="search", aliases=['lookup'])
async def search(ctx, *args):
    searchTerms = ""
    for keyword in args:
        searchTerms = searchTerms + " " + keyword
    print(searchTerms)
    with urllib.request.urlopen(URL_SEARCH + urllib.parse.quote(searchTerms)) as url:
        places = json.loads(url.read())
        placesList = places["data"]["list"]
        print(json.dumps(places["data"]["list"][0], indent=4))       
    
        
@bot.command(name="play")
async def play(ctx, *args):
    sql = 'SELECT mp3, Name, PlaceName, CountryName FROM RadioStations WHERE 1 = 1 '
    try:
        for keyword in args:
            print(keyword)
            cleanKeyword = dubApos(keyword)
            sql = sql + "AND ( Name LIKE '%" + cleanKeyword + "%' "
            sql = sql + "OR PlaceName LIKE '%" + cleanKeyword + "%' "
            sql = sql + "OR CountryName LIKE '%" + cleanKeyword + "%' ) "
        sql = sql + "LIMIT 15;"
        print(sql)
        c.execute(sql)
        rows = c.fetchall()
        result = ""
        if len(rows) == 1:
            await restartStream(ctx, rows[0][0])
        elif len(rows) == 0:
            result = "No results found"
        else: 
            result = "Multiple Radio Channels returned: \n"
        for row in rows:
            print(row)
            for column in row:
                result = result + column + " | "
                result = result + "\n"  
        await ctx.send(result) 
    except:
        await ctx.send(traceback.format_exc()) 
    
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
async def stream_(self, ctx, *args, channel: discord.VoiceChannel=None):
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
    try:
        stop(ctx)
        player.play(discord.FFmpegPCMAudio(args[0]))
    except Exception as e:
        ctx.send(print(e))

@bot.command(name="pause")
async def pause(ctx):
    ctx.voice_client.pause
    
@bot.command(name="stop")
async def stop(ctx):
    ctx.voice_client.stop()

@bot.command(name="resume")
async def stop(ctx):
    ctx.voice_client.resume()

    
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
        
bot.run('MjAyMzk5MDU1MzQxNTUxNjE2.XxBTAQ.8dsmBJLfQb9Ju3zf5AlD0h6K5bg')


