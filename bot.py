import discord
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

TOKEN = ''

client = discord.Client()


def getSoup():
    driver = webdriver.Firefox()
    driver.get("https://www.flashscore.pt/")
    driver.implicitly_wait(10)

    live_tab = driver.find_element(by=By.XPATH,
                                   value="/html/body/div[6]/div[1]/div/div[1]/div[2]/div[4]/div[2]"
                                         "/div/div[1]/div[1]/div[2]")
    live_tab.click()

    scores_div = driver.find_element(by=By.XPATH, value="/html/body/div[6]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div")
    html_content = scores_div.get_attribute('outerHTML')

    return BeautifulSoup(html_content, 'html.parser')


def extractTeamName(msg):
    split_msg = msg.split(" ", 1)
    team_name = split_msg[1].strip()
    print(team_name)
    return team_name


def getScore(team):
    soup = getSoup()
    home_team = soup.find_all('div', class_='event__participant--home')
    home_score = soup.find_all('div', class_='event__score--home')
    away_team = soup.find_all('div', class_='event__participant--away')
    away_score = soup.find_all('div', class_='event__score--away')

    #score_str = home_team[0].get_text() + ' ' + home_score[0].get_text() + ' - ' + \
    #            away_score[0].get_text() + ' ' + away_team[0].get_text()
    #print(score_str)

    for item in home_team:
        item_team = item.get_text().lower()
        if team in item_team:
            print(item.get_text())

    return team


def requestType(msg):
    if msg.startswith('!score'):
        return 'score'
    else:
        return False


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content).lower()
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    if message.channel.name == 'testing':
        if requestType(user_message) == 'score':
            team = extractTeamName(user_message)
            await message.channel.send(getScore(team))
            return
        elif requestType(user_message) == 'lolgame':
            await message.channel.send("Hi2")
            return
        elif requestType(user_message) == 'help':
            await message.channel.send('!lol [username] - para veres o teu perfil\n'
                                       '!lolgame [username] - para ver informação ingame')
            return


client.run(TOKEN)
