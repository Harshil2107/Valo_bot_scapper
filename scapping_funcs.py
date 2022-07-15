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
            match['team' + str(i)] =' '.join(teams.findChild('div', class_='text-of').text.split())
            i += 1
        live_matchs.append(match)
    return live_matchs

def getMatchScore(match_data):
    live_dict = {}
    r = requests.get("https://www.vlr.gg/112286/kr-esports-vs-optic-gaming-valorant-champions-tour-stage-2-masters-copenhagen-decider-a")
    # r = requests.get(match_data["link"])
    soup = BeautifulSoup(r.content, 'html.parser')
    event = soup.find('div', class_="match-header-super")
    ev_txt = event.findChild('div').findChild('div').text.split()
    str = ""
    for i in ev_txt:
        str += i +" "
    live_dict["event"] = str
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

def getRankings(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    teams = soup.find_all('div', class_='ge-text',limit=5, recursive=True)
    ret = ""
    c = 1
    print(len(teams))
    for i in teams:
        l = i.text.split()
        t = ' '.join(l[:l.index([i for i in l if i.startswith('#')][0])])
        ret += str(c)+". "+ t + "\n"
        c +=1
    print(ret)
    return ret


def getTodaymatchs():
    r= requests.get("https://www.vlr.gg/matches")
    soup = BeautifulSoup(r.content, 'html.parser')
    today = soup.find_all('div', class_="wf-card", recursive=True)
    m_divs = today[1].findChildren('div', class_="match-item-vs-team-name", recursive=True)
    todays_matches = []
    for i in range(0, len(m_divs),2):
        match = {}
        eta_div = m_divs[i].parent.parent.parent.findChild('div', class_="ml-eta", recursive=True)

        match['link'] = "https://www.vlr.gg" + m_divs[i].parent.parent.parent.get('href')
        match['team1'] =' '.join(m_divs[i].findChild('div', class_='text-of').text.split())
        match['team2'] = ' '.join(m_divs[i+1].findChild('div', class_='text-of').text.split())
        match['eta'] = eta_div.text
        todays_matches.append(match)
    print(todays_matches)
getRankings("https://www.vlr.gg/rankings/north-america")