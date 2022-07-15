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
        await ctx.send("No live matches")
    for i in live:
        ret += f"{i['team1']} VS {i['team2']}  \n VLR: {i['link']} \n"
    await ctx.send(ret)


def getMatchScore(match_data):
    live_dict = {}
    # r = requests.get("https://www.vlr.gg/114530/akrew-vs-knights-nerd-street-summer-championship-2022-open-12-gf")
    r = requests.get(match_data["link"])
    soup = BeautifulSoup(r.content, 'html.parser')
    event = soup.find('div', class_="match-header-super")
    ev_txt = event.findChild('div').findChild('div').text.split()
    str = ""
    for i in ev_txt:
        str += i + " "
    live_dict["event"] = str
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
    # scope=994186669265784922
)
async def live_match_scores(ctx: interactions.CommandContext):
    live = getLiveMatches()
    ret = ""
    if (len(live) == 0):
        await ctx.send("No live matches")
    else:
        msg = await ctx.send("Getting data ...")
        for i in live:
            live_dict = getMatchScore(i)
            ret += f"__**{i['team1']} VS {i['team2']}**__\nEvent: {live_dict['event']}\nMaps: {live_dict['maps'][0]}, {live_dict['maps'][1]}, {live_dict['maps'][2]}\nCurrent Map: {live_dict['cur_map']} \nMap Score: {live_dict['map_score']} \nCurrent Map Score: {live_dict['cur_score']} \n"
        await msg.edit(content=ret)


# {i['team1']} VS {i['team2']} {i['link']}


def getRankings(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    teams = soup.find_all('div', class_='ge-text', limit=5, recursive=True)
    ret = ""
    c = 1
    for i in teams:
        l = i.text.split()
        t = ' '.join(l[:l.index([i for i in l if i.startswith('#')][0])])
        ret += str(c) + ". " + t + "\n"
        c += 1
    return ret


@bot.command(
    name="rankings",
    description="Team Ranking",
    # scope=994186669265784922,
    options=[
        interactions.Option(
            name="region",
            description="Enter region",
            type=interactions.OptionType.STRING,
            required=True
        ),
    ],
)
async def rankings(ctx: interactions.CommandContext, region: str = ""):
    region = region.lower()
    reg = ""
    if region == "na" or region == "north america":
        reg = "/north-america"
    elif region == "eu" or region == "europe" or region == "emea":
        reg = "/europe"
    elif region == "br" or region == "brazil":
        reg = "/brazil"
    elif region == "ap" or region == "asia pacific" or region == "asia":
        reg = "/asia-pacific"
    elif region == "kr" or region == "korea":
        reg = "/korea"
    elif region == "china" or region == "ch":
        reg = "/china"
    elif region == "jp" or region == "japan":
        reg = "/japan"
    elif region == "las" or region == "latin america south" or region == "latin america s":
        reg = "/la-s"
    elif region == "lan" or region == "latin america north" or region == "latin america n":
        reg = "/la-n"
    elif region == "oce" or region == "oceania":
        reg = "/oceania"
    elif region == "gc" or region == "game changers":
        reg = "/gc"
    elif region == "mena":
        reg = "/mena"
    else:
        reg = "invalid"
        await ctx.send("Not a Region")
    if reg != "invalid":
        link = "https://www.vlr.gg/rankings" + reg
        l = await ctx.send("Getting data")
        ranks = getRankings(link)
        await l.edit(content=ranks)


def getTodaymatchs():
    r= requests.get("https://www.vlr.gg/matches")
    soup = BeautifulSoup(r.content, 'html.parser')
    today = soup.find_all('div', class_="wf-card", recursive=True)
    m_divs = today[1].findChildren('div', class_="match-item-vs-team-name", recursive=True)
    todays_matches = []
    for i in range(0, len(m_divs),2):
        match = {}
        eta_div = m_divs[i].parent.parent.parent.findChild('div', class_="ml-eta", recursive=True)

        # match['link'] = "https://www.vlr.gg" + m_divs[i].parent.parent.parent.get('href')
        match['team1'] =' '.join(m_divs[i].findChild('div', class_='text-of').text.split())
        match['team2'] = ' '.join(m_divs[i+1].findChild('div', class_='text-of').text.split())
        if eta_div != None:
            match['eta'] = eta_div.text
        else:
            match['eta'] = "live"
        todays_matches.append(match)
    return todays_matches

@bot.command(
    name="todays_matches",
    description="Get today's matches",
    # scope=994186669265784922,
)
async def todays_matches(ctx: interactions.CommandContext):
    today = getTodaymatchs()
    ret = ""
    if (len(today) == 0):
        await ctx.send("No live matches")
    else:
        msg = await ctx.send("Getting data ...")
        for i in today:
            ret += f"__**{i['team1']} VS {i['team2']}**__\nUpcoming: {i['eta']}\n"
        await msg.edit(content=ret)

@bot.command(
    name= "help",
    description="command usage help",
)
async def help(ctx: interactions.CommandContext):
    ret = f"__**Commands**__\n**/live_matches :** No arguments\n**/live_match_scores :** No arguments\n**/todays_matches :** No arguments" \
          f"\n**/rankings :** Region (Takes abrivations as well as full names like NA or North America) not case sensitive"
    await ctx.send(ret)
bot.start()
