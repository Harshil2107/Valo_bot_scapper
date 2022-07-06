# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
import discord
from dotenv import load_dotenv
import os
import random
from discord.ext import commands
# from discord_slash import SlashCommand, SlashContext

client = discord.Bot(command_prefix='!', intents = discord.Intents.all())

# slash = SlashCommand(client)
token = os.getenv('TOKEN')
bot_id = 'OTk0MTg3MjQ5NzExMzI5MzYw.GSGEcI.xDoVsoGFyUL3PBgbFcVua9xMDudjAKU02ZkCXA'
client.run(bot_id)
# @slash.slash(name="test")
# async def _test(ctx: SlashContext):
#     await ctx.send("Hello World!")
@client.command(name="live")
async def livematch(ctx):
    ret ="Live Matchs\n"
    live = getLiveMatches()
    for i in live:
        ret = ret +i["team1"]+" VS "+ i["team2"]+"\nVLR link : "+ i["link"]
    await ctx.send(ret)

@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

# @client.event
# async def on_message(message):
#     username = str(message.author).split("#")[0]
#     channel = str(message.channel.name)
#     user_message = str(message.content)
#
#     print(f'Message {user_message} by {username} on {channel}')
#
#     if message.author == client.user:
#         return
#
#     if True:
#         if user_message.lower() == "hello" or user_message.lower() == "hi":
#             await message.channel.send(f'Hello {username}')
#             return
#         elif user_message.lower() == "bye":
#             await message.channel.send(f'Bye {username}')
#         elif user_message.lower() == "tell me a joke":
#             jokes = [" Can someone please shed more\
#                 light on how my lamp got stolen?",
#                      "Why is she called llene? She\
#                      stands on equal legs.",
#                      "What do you call a gazelle in a \
#                      lions territory? Denzel."]
#             await message.channel.send(random.choice(jokes))




def getLiveMatches():
    r = requests.get('https://www.vlr.gg/matches')

    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find_all('div', class_='ml mod-live')
    live_matchs = []

    for i in s:
        d = i.parent.parent.findChildren('div', class_="match-item-vs-team-name", recursive=True)
        match = {}
        match['link'] = "https://www.vlr.gg" + i.parent.parent.get('href')
        i = 1
        for teams in d:
            match['team' + str(i)] = teams.findChild('div', class_='text-of').text.split()[0]
            i += 1
        live_matchs.append(match)
    print(live_matchs)
    return live_matchs

def getMatchScore(match_data):
    print(match_data)
    r = requests.get(match_data['link'])
    soup = BeautifulSoup(r.content, 'html.parser')
    map_data_div = soup()



