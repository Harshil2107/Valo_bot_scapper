# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
import discord
import interactions
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = interactions.Client(token=token)


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
    return live_matchs


@bot.command(
    name="live_matches",
    description="Get live valorant matches",
)
async def live_matches(ctx: interactions.CommandContext):
    live = getLiveMatches()
    ret = ""
    if (len(live) == 0):
        await ctx.send("No live matchs")
    for i in live:
        ret += f"{i['team1']} VS {i['team2']}  \n VLR: {i['link']} \n"
    await ctx.send(ret)


def getMatchScore(match_data):
    live_dict = {}
    r = requests.get("https://www.vlr.gg/114530/akrew-vs-knights-nerd-street-summer-championship-2022-open-12-gf")
    # r = requests.get(match_data["link"])
    soup = BeautifulSoup(r.content, 'html.parser')
    map_data_div = soup.find('div', class_="js-spoiler")
    # print(map_data_div)
    children = map_data_div.findChildren('span')
    map_score = ""
    for i in children:
        map_score += i.text.split()[0] + " "
    maps_divs = soup.find_all('div', class_="js-map-switch", recursive=True)
    maps = []
    for i in maps_divs:
        for j in i.findChildren('div', recursive=True):
            maps.append(j.text.split()[1])
    live_map = soup.find('div', class_="map", recursive=True).text.split()[0]
    live_dict["maps"] = maps
    live_dict["map_score"] = map_score
    live_dict["cur_map"] = live_map
    score = soup.find_all('div', class_="score", recursive=True)
    i = maps.index(live_map) * 2
    cur_score = score[i].text.split()[0] + " : " + score[i + 1].text.split()[0]
    live_dict["cur_score"] = cur_score

    return live_dict


@bot.command(
    name="live_match_scores",
    description="Get current scores of all live matches",
    scope=994186669265784922
)
async def live_match_scores(ctx: interactions.CommandContext):
    live = getLiveMatches()
    ret = ""
    if (len(live) == 0):
        await ctx.send("No live matches")
    for i in live:
        live_dict = getMatchScore(i)
        ret += f"__**{i['team1']} VS {i['team2']}**__\n Maps: {live_dict['maps'][0]}, {live_dict['maps'][1]}, {live_dict['maps'][2]} \n Current Map: {live_dict['cur_map']} \n Map Score: {live_dict['map_score']} \n Current Map Score: {live_dict['cur_score']} \n VLR: {i['link']} \n"
    await ctx.send(ret)


bot.start()
