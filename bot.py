import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import time
import requests
import asyncio
import math
import json

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

TOKEN = config['token']
url = config['url']
waitTime = config['waitTime']
version = config['version']
command_prefix = config['command_prefix']
required_role_id = config['required_role_id']

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

bot = commands.Bot(command_prefix=command_prefix, intents=intents)

watching = False

def truncate(number, decimal_places):
    factor = 10.0 ** decimal_places
    return math.trunc(number * factor) / factor

def getPlatformLatency():
    begin = time.time()
    response = requests.get(url)
    end = time.time()
    total = truncate(((end - begin) * 1000), 2)
    return total

def getPlatformStatus():
    response = requests.get(url)
    return response.status_code

def statusColor():
    latency = getPlatformLatency()
    if getPlatformStatus() == 200:
        if latency < 16:
            return discord.Color.magenta()
        elif latency >= 16 and latency < 180:
            return discord.Color.blue()
        elif latency >= 180 and latency < 360:
            return discord.Color.green()
        elif latency >= 360 and latency < 580:
            return discord.Color.yellow()
        else:
            return discord.Color.red()
    else:
        return discord.Color.dark_red()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="stop")
async def stop(ctx):
    required_role = discord.utils.get(ctx.guild.roles, id=required_role_id)
    if required_role in ctx.author.roles:
        global watching
        watching = False
        print(f"API monitoring stopped by {ctx.author.name} / {ctx.author.mention}")
        await ctx.send("Stopped API uptime monitoring.")
        await ctx.message.delete()
    else:
        await ctx.reply("❌ You're not allowed to do that.")

@bot.command(name="waittime")
async def awt(ctx, arg: int):
    required_role = discord.utils.get(ctx.guild.roles, id=required_role_id)
    if required_role in ctx.author.roles:
        global waitTime
        waitTime = arg
        print(f"Wait Time set to {waitTime} by {ctx.author.name} / {ctx.author.mention}")
        await ctx.send(f"Updated API ping time to {arg} seconds")
        await ctx.message.delete()
    else:
        await ctx.reply("❌ You're not allowed to do that.")

@bot.command(name="begin")
async def beginwatch(ctx):
    global watching, url, waitTime
    required_role = discord.utils.get(ctx.guild.roles, id=required_role_id)
    if required_role in ctx.author.roles:
        if not watching:
            watching = True
            channel = ctx.message.channel
            await ctx.message.delete()
            
            latency = getPlatformLatency()
            status_code = getPlatformStatus()

            if status_code == 200:
                status = "UP"
            else:
                status = "DOWN"

            beginEmbed = discord.Embed(
                title="Begun monitoring API",
                description=f"Current status: **{status}**\nStatus code: **{status_code}**\nAPI latency: **{latency}** ms\nBot latency: **{round(bot.latency*1000)}** ms\nUpdating every **{waitTime} seconds**.",
                color = statusColor()
            )
            beginEmbed.set_footer(text=f"WatchBot {version}")
            await channel.send(embed=beginEmbed)

            status_old = " "

            while watching:
                await asyncio.sleep(waitTime)

                latency = getPlatformLatency()
                status_code = getPlatformStatus()
                
                if status_code == 200:
                    status = "UP"
                else:
                    status = "DOWN"
                
                print("WatchBot: | " + str(time.time()) + " | " + status)
                
                if status_old != status:
                    if status_code == 200:
                        embed = discord.Embed(
                            title=f"✅ {url} is UP",
                            description=f"Request to {url} succeeded with status code {status_code}.",
                            color=discord.Color.green()
                        )
                        embed.set_footer(text=f"Response time: {latency} ms | Bot ping: {round(bot.latency*1000)} ms | WatchBot {version}")
                        await channel.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title=f"❌ {url} is DOWN",
                            description=f"Request to {url} FAILED ({status_code}).",
                            color=discord.Color.red()
                        )
                        embed.set_footer(text=f"Request latency : {latency} ms | Bot ping: {round(bot.latency*1000)} ms | WatchBot {version}")
                        await channel.send(embed=embed)
                status_old = status
        else:
            await ctx.send("❌ I'm already doing that")
            await ctx.message.delete()
    else:
        await ctx.reply("❌ You're not allowed to do that.")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Bot latency: `{round(bot.latency*1000)}` ms\nPlatform latency: `" + getPlatformLatency + "` ms")
    await ctx.message.delete()

bot.run(TOKEN)