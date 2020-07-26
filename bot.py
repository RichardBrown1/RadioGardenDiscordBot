import discord
import sqlite3
import traceback
import os
import asyncio
from usefulFunctions import dubApos
from discord.ext import commands

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

@bot.command(name="sql")
async def sql(ctx, *args):
    sql = " ".join(args)
    print(sql)
    result = ""
    try:
        c.execute(sql)
        rows = c.fetchall()
        for row in rows:
            for column in row:
                result = result + str(column) + " | "
            result = result + "\n"
        await ctx.send(result, delete_after=20)           
    except:
        await ctx.send(traceback.format_exc())
        
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
        sql = sql + "LIMIT 20;"
        print(sql)
        c.execute(sql)
        rows = c.fetchall()
        if len(rows) == 1:
            result = rows[0][0]
            await restartStream(ctx, result)
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


