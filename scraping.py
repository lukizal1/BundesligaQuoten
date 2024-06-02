# scraping.py

import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def scrape_emirbet():
    url = 'https://emirbet.com/de/sports/competition/euro-2024'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    odds = []

    # Konfiguration für den headless Chrome-Browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    # Set path to chromedriver as per your configuration
    webdriver_service = Service(
        r'C:\Users\Anwender\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')  # Use raw string and full path to chromedriver.exe

    # Choose Chrome Browser
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    driver.get(url)

    # Warte, bis die Seite vollständig geladen ist (könnte je nach Verbindungsgeschwindigkeit variieren)
    time.sleep(5)  # Wartezeit in Sekunden anpassen, je nach Ladezeit der Seite

    # Hole den HTML-Inhalt der Seite nach dem Laden
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    # Debug-Ausgabe des HTML-Inhalts
    with open('emir_page.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    # Finde das übergeordnete div mit der Klasse 'SportsCompetitionsEvents-styles-module-competitions-events-block'
    entries_div = soup.find('div', class_='competition-event-list event-list-head-to-head')

    if not entries_div:
        print("Kein Eintrags-Div gefunden")
        return []

    # Finde alle Match-Divs mit der Klasse 't3-list-entry'
    match_divs = entries_div.find_all('div', class_='event-main d-flex align-items-center')

    for match_div in match_divs:
        # Finde das Div mit den Spielernamen
        teams = match_div.find_all('div', class_='event-team')
        if len(teams) < 2:
            print("Unvollständige Team-Informationen gefunden")
            continue

        team1 = teams[0].text.strip()
        team2 = teams[1].text.strip()

        #print(team1, team2)

        # Finde das Div mit den Wettquoten
        bet_group_div = match_div.find('div', class_='main-line-odds d-flex align-items-center')
        #print(bet_group_div)

        odds_team1 = bet_group_div.find('div',
                                        class_='market-column column-home d-flex justify-content-center').text.strip()
        odds_draw = bet_group_div.find('div', class_='market-column d-flex justify-content-center').text.strip()
        odds_team2 = bet_group_div.find('div',
                                        class_='market-column column-away d-flex justify-content-center').text.strip()

        match_info = {
            'team1': team1,
            'team2': team2,
            'odds_team1': odds_team1,
            'odds_draw': odds_draw,
            'odds_team2': odds_team2,
            'source': 'emirbet',
            'link': url  # Hier kannst du den tatsächlichen Wettlink einfügen, wenn verfügbar
        }

        odds.append(match_info)

    return odds


def scrape_win2day():
    url = 'https://www.win2day.at/sport/fussball/international/europameisterschaft-wetten'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    odds = []

    # Finde das übergeordnete div mit der Klasse 't3-list__entries'
    entries_div = soup.find('div', class_='t3-list__entries')

    if not entries_div:
        print("Kein Eintrags-Div gefunden")
        return []

    # Finde alle Match-Divs mit der Klasse 't3-list-entry'
    match_divs = entries_div.find_all('div', class_='t3-list-entry')

    for match_div in match_divs:
        # Finde das Div mit den Spielernamen
        info_div = match_div.find('div', class_='t3-list-entry__info')
        players_div = info_div.find('div', class_='t3-list-entry__players')

        teams = players_div.find_all('a', class_='t3-list-entry__player')
        if len(teams) < 2:
            print("Unvollständige Team-Informationen gefunden")
            continue

        team1 = teams[0].text.strip().split('\n')[0]
        team2 = teams[1].text.strip().split('\n')[0]

        # Finde das Div mit den Wettquoten
        bet_group_div = match_div.find('div', class_='t3-list-entry__bet-group bet-group-column-1')
        bet_divs = bet_group_div.find_all('div', class_='t3-list-entry__bet')

        if len(bet_divs) < 3:
            print("Unvollständige Wettquoten gefunden")
            continue

        odds_team1 = bet_divs[0].find('span', class_='t3-bet-button__text').text.strip()
        odds_draw = bet_divs[1].find('span', class_='t3-bet-button__text').text.strip()
        odds_team2 = bet_divs[2].find('span', class_='t3-bet-button__text').text.strip()

        match_info = {
            'team1': team1,
            'team2': team2,
            'odds_team1': odds_team1,
            'odds_draw': odds_draw,
            'odds_team2': odds_team2,
            'source': 'win2day',
            'link': url  # Hier kannst du den tatsächlichen Wettlink einfügen, wenn verfügbar
        }

        odds.append(match_info)

    return odds


def scrape_tipp3():
    url = 'https://www.tipp3.at/sport/fussball/international/europameisterschaft-wetten?frame'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    odds = []

    entries_div = soup.find('div', class_='t3-list__entries')

    if not entries_div:
        if not entries_div:
            print("Kein Eintrags-Div gefunden")
            return []
        # Finde alle Match-Divs mit der Klasse 't3-list-entry'
    match_divs = entries_div.find_all('div', class_='t3-list-entry')

    for match_div in match_divs:
        # Finde das Div mit den Spielernamen
        info_div = match_div.find('div', class_='t3-list-entry__info')
        players_div = info_div.find('div', class_='t3-list-entry__players')

        teams = players_div.find_all('a', class_='t3-list-entry__player')
        if len(teams) < 2:
            print("Unvollständige Team-Informationen gefunden")
            continue

        team1 = teams[0].text.strip().split('\n')[0]
        team2 = teams[1].text.strip().split('\n')[0]

        # Finde das Div mit den Wettquoten
        bet_group_div = match_div.find('div', class_='t3-list-entry__bet-group bet-group-column-1')
        bet_divs = bet_group_div.find_all('div', class_='t3-list-entry__bet')

        if len(bet_divs) < 3:
            print("Unvollständige Wettquoten gefunden")
            continue

        odds_team1 = bet_divs[0].find('span', class_='t3-bet-button__text').text.strip()
        odds_draw = bet_divs[1].find('span', class_='t3-bet-button__text').text.strip()
        odds_team2 = bet_divs[2].find('span', class_='t3-bet-button__text').text.strip()

        match_info = {
            'team1': team1,
            'team2': team2,
            'odds_team1': odds_team1,
            'odds_draw': odds_draw,
            'odds_team2': odds_team2,
            'source': 'tipp3',
            'link': url
        }

        odds.append(match_info)

    return odds
