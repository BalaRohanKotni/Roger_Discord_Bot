import random
import os
from dotenv import load_dotenv
import time

from json import loads
from discord import activity
from discord.embeds import Embed
from discord.ext.commands.core import check
import requests

import discord.member
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

# import my custom commands
from modules.info import command_user_info, send_server_info
from modules.help import send_help_command
from modules.weather import send_weather_info, setloc
from modules.guess import _guess
from modules.variables import *
from modules.tictactoe import gameplay

load_dotenv()
#  VARIABLES *************************************************************************************

token = os.getenv('GITHUB_TOKEN')
open_weather_api_key = os.getenv('OPENWEATHER_KEY')


# all_calculations = False

total_user_msg_servers = {}
temp_servers = {}

all_calculations_servers = {}

debugMode = False

welcome_words = var_welcome_words
inspire_words = var_inspire_words
eight_ball_replies = var_eight_ball_replies

command_ctx = ""

guild_ids = []

# FUNCTIONS **************************************************************************************

#   0.00018562 secs - 1msg
# 40.403039313 mins - 200000msgs


async def process_all_servers_and_user_info(client, send_message=True):

    global total_user_msg_servers

    global guild_ids

    guild_ids = []

    total_mgs_dict = {}
    tm = 0

    start_time = time.monotonic()

    print("processing")

    for guild in client.guilds:

        all_calculations_servers[guild.id] = False

        guild_ids.append(guild.id)
        total_mgs_dict = {}

        async for member in client.get_guild(guild.id).fetch_members(limit=None):
            total_mgs_dict[member.id] = 0

        for channel in guild.text_channels:
            async for msg in channel.history(limit=None):
                tm += 1
                if msg.author.id in total_mgs_dict:
                    total_mgs_dict[msg.author.id] += 1
        total_user_msg_servers[guild.id] = total_mgs_dict
        all_calculations_servers[guild.id] = True

    print("done")
    print('seconds: ', time.monotonic() - start_time)
    print("Total Msgs of all servers:", tm)


# discord commands


def get_quote():
    quote_qpi = 'http://api.quotable.io/random'
    req = requests.get(quote_qpi)
    parsed = loads(req.text)
    quote = parsed['content']
    author = parsed['author']
    final = quote + " - " + author
    return final


def _8ball():
    a = eight_ball_replies[int(random.randint(0, len(eight_ball_replies)))]
    return a


# MISC *******************************************************************************************
# os.system("clear")
# DISCORD ****************************************************************************************

intents = discord.Intents.all()

client = commands.Bot(command_prefix=".", intents=intents)
slash = SlashCommand(client, sync_commands=True)
client.remove_command('help')

# DISCORD EVENTS ################################################################################


@ client.event
async def on_ready():

    global guild_ids

    for guild in client.guilds:
        guild_ids.append(guild.id)

    await process_all_servers_and_user_info(client) if not debugMode else print("debug mode")
    print('We have logged in as {0.user}'.format(client))
    client.total_msgs_server = total_user_msg_servers


@ client.event
async def on_member_join(member):
    print(member, "joined.")
    total_user_msg_servers[member.guild.id][member.id] = 0
    await member.guild.text_channels[0].send(f"""Welcome {member.mention} to the server! 🎊🎊🎊.\n\n""")


@ client.event
async def on_member_remove(member):
    total_user_msg_servers[member.guild.id][member.id] = 0
    await member.guild.text_channels[0].send(f"""{member.name} got out of the server!.\n\n""")


@ client.event
async def on_guild_join(guild):
    # TODO optimize this
    # await process_all_servers_and_user_info(client, False)

    global total_user_msg_servers
    global all_calculations
    global guild_ids

    all_calculations_servers[guild.id] = False

    print("joined", guild)
    print("Processing the new guild")

    guild_ids.append(guild.id)

    total_mgs_dict = {}

    async for member in client.get_guild(guild.id).fetch_members(limit=None):
        total_mgs_dict[member.id] = 0

    for channel in guild.text_channels:
        async for msg in channel.history(limit=None):
            if msg.author.id in total_mgs_dict:
                total_mgs_dict[msg.author.id] += 1
    total_user_msg_servers[guild.id] = total_mgs_dict

    print("done")

    all_calculations_servers[guild.id] = True


@ client.event
async def on_guild_remove(guild):
    # await process_all_servers_and_user_info(client, False)

    guild_ids.remove(guild.id)

    del total_user_msg_servers[guild.id]
    del all_calculations_servers[guild.id]

    print("got out", guild
          )


@ client.event
async def on_message(message):

    await client.process_commands(message)

    global total_user_msg_servers

    if not debugMode and all_calculations_servers[message.guild.id]:
        total_user_msg_servers[message.guild.id][message.author.id] += 1

    # reply to members when said hello ....
    if message.content.lower() in welcome_words and message.author != client.user:
        await message.reply(welcome_words[random.randint(0, len(welcome_words)-1)])

# DISCORD COMMANDS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# HELP COMMAND


@ client.command(aliases=["help"])
async def _help(ctx):
    await send_help_command(ctx, client)


@ slash.slash(name="help", description="Get all commands for the bot Roger.", guild_ids=guild_ids)
async def _slash_help(ctx):
    print(guild_ids)
    await send_help_command(ctx, client)


# PING COMMAND
@ client.command(aliases=['ping'])
async def _ping(ctx):
    await ctx.send("Pong! {}ms".format(int(client.latency*1000)))


@ slash.slash(name="ping", description="Get the latency(speed) of the bot.", guild_ids=guild_ids)
async def _slash_ping(ctx):
    await ctx.send("Pong! {}ms".format(int(client.latency*1000)))


# QUOTE COMMAND
@ client.command(aliases=['quote', 'inspire'])
async def _quote(ctx):
    quote = get_quote()
    await ctx.reply(quote)


@ slash.slash(name="quote", description="Replies with a quote(from internet ofc)", guild_ids=guild_ids,)
async def _slash_quote(ctx):
    quote = get_quote()
    await ctx.send(quote)
    # await send_quote(ctx, False)


# 8BALL COMMAND
@ client.command(aliases=['8ball'])
async def _com8ball(ctx, *arg):

    q = ""

    if arg == ():
        await ctx.reply("This command requires a question.")
        return

    for i in range(len(arg)):
        if i == len(arg) - 1:
            q += arg[i]
        else:
            q += arg[i] + ' '

    a = _8ball()
    embed = discord.Embed(title=q+"?", description=a)
    await ctx.reply(content=None, embed=embed)


@ slash.slash(
    name="8ball",
    description="Ask the magic 8ball a question.",
    options=[
        create_option(
            name="question", required=True,
            description="The question u want to ask the magic 8 ball",
            option_type=3
        )
    ],
    guild_ids=guild_ids
)
async def _slash_8ball(ctx, q: str):
    a = _8ball()
    embed = discord.Embed(title=q+"?", description=a)
    await ctx.send(content=None, embed=embed)


# SETLOC COMMAND
@ client.command(aliases=['weatherLoc', 'weatherLocation', 'weatherloc'])
async def _setloc(ctx, loc: str):
    await setloc(ctx, loc, open_weather_api_key)


@ _setloc.error
async def _setloc_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.reply("This command requires a location.")


@ slash.slash(
    name='weatherLocation',
    description="Location for getting the weather info.",
    options=[
        create_option(
            name="location", required=True,
            description="The location u want to set for getting the weather info.",
            option_type=3
        )
    ],
    guild_ids=guild_ids,
)
async def _slash_setloc(ctx, loc: str):
    await setloc(ctx, loc, open_weather_api_key)


# WEATHER INFO
@ client.command(aliases=["weather", "temp"])
async def _weather_info(ctx):
    await send_weather_info(ctx, open_weather_api_key)


@ slash.slash(name="weather", description="Get the weather of set location", guild_ids=guild_ids)
async def _slash_weather_info(ctx):
    await send_weather_info(ctx, open_weather_api_key)


# SERVER INFO COMMAND
@ client.command(name="infoServer")
async def _server_info(ctx):
    if all_calculations_servers[ctx.guild.id] and not debugMode:
        await send_server_info(ctx, client, total_user_msg_servers)
        return
    else:
        if debugMode:
            await ctx.send("Sorry! This command is not available as the bot is in debug mode.")
            print("debug mode")
            return
        await ctx.send("Sorry! I am currently processing this server. You can't use this command right now, try later.")


@ slash.slash(name='infoServer', description="Get info about the server.", guild_ids=guild_ids)
async def _slash_server_info(ctx):
    if all_calculations_servers[ctx.guild.id] and not debugMode:
        await send_server_info(ctx, client, total_user_msg_servers)
        return
    else:
        if debugMode:
            await ctx.send("Sorry! This command is not available as the bot is in debug mode.")
            print("debug mode")
            return
        await ctx.send("Sorry! I am currently processing this server. You can't use this command right now, try later.")


# USERINFO COMMAND
@ client.command(name="info")
async def _user_info(ctx, *user: discord.Member):
    if all_calculations_servers[ctx.guild.id]:
        await command_user_info(ctx, user, total_user_msg_servers, all_calculations_servers[ctx.guild.id], debugMode)
    else:
        await ctx.send("Sorry! I am currently processing this server. You can't use this command right now, try later.")


@ slash.slash(
    name="info",
    description="Get user info",
    guild_ids=guild_ids,
    options=[
        create_option(
            name="user", required=False,
            description="The user",
            option_type=6,
        )
    ],
)
async def _slash_user_info(ctx, *user):
    if all_calculations_servers[ctx.guild.id]:
        await command_user_info(ctx, user, total_user_msg_servers, all_calculations_servers[ctx.guild.id], debugMode)
    else:
        await ctx.send("Sorry! I am currently processing this server. You can't use this command right now, try later.")


# GUESS NUMBER BW 1 AND 10

@ client.command(aliases=['guessnum', 'guessNum'])
async def guess(ctx):
    await _guess(ctx, client)


@ slash.slash(name="GuessNumber", description="Guess a number by checking if you guessed the number by high or low", guild_ids=guild_ids)
async def _slash_guess(ctx):
    await _guess(ctx, client)


# Tic tac toe
@ client.command(name='tictactoe')
async def _tictactoe(ctx, *user):
    if user == ():
        await ctx.send("This game needs a user to play.")
        return
    await gameplay(ctx, client, user)


@ slash.slash(
    name="TicTacToe",
    description="A game in which two players alternately put Xs and Os in a 3x3 board.", guild_ids=guild_ids,
    options=[
        create_option(
            name="user", required=True,
            description="The user",
            option_type=6,
        )
    ],
)
async def _slash_tictactoe(ctx, user):
    await gameplay(ctx, client, user)


@ client.command(name="support")
async def _support(ctx):
    await ctx.send("https://discord.gg/qdvQNwtmn7")


@ slash.slash(name="Support", description="Join the support server of the bot.", guild_ids=guild_ids)
async def _slash_support(ctx):
    await ctx.send("https://discord.gg/qdvQNwtmn7")

client.run(token)
