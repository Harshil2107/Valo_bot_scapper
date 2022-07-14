import requests
from bs4 import BeautifulSoup

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
        map_score+= i.text.split()[0] + " "
    maps_divs = soup.find_all('div', class_="js-map-switch", recursive=True)
    maps = []
    for i in maps_divs:
        for j in i.findChildren('div', recursive=True):
            maps.append(j.text.split()[1])
    live_map = soup.find('div', class_="map", recursive=True).text.split()[0]
    live_dict["maps"] = maps
    live_dict["map_score"] = map_score
    live_dict["cur_map"] = live_map
    score = soup.find_all('div', class_= "score", recursive=True)
    i = maps.index(live_map)*2
    cur_score = score[i].text.split()[0] + " : " + score[i+1].text.split()[0]
    live_dict["cur_score"] = cur_score
    print(live_dict)
    return live_dict

l = getLiveMatches()
getMatchScore(l)