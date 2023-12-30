import os

import discord
from discord import option
from dotenv import load_dotenv
import requests
import json
import os
import time
import random
from colorthief import ColorThief
from PIL import Image
from html2image import Html2Image
import urllib.request
from io import BytesIO
from bs4 import BeautifulSoup

load_dotenv()
DSTOKEN = os.getenv('DISCORD_TOKEN')
RIOTOKEN = os.getenv('RIOT_TOKEN')
SERVERS = ["BR", "EUNE", "EUW", "JP", "KR", "LAN", "LAS", "NA", "OC", "RU", "TR"]
AMERICAS = ["NA", "BR", "LAN", "LAS", "OCE"]
EUROPE = ["EUNE", "EUW", "TR", "RU"]
ASIA = ["KR", "JP"]
CHAMPS = ['Renata', 'Annie', 'Olaf', 'Galio', 'TwistedFate', 'XinZhao', 'Urgot', 'Leblanc', 'Vladimir', 'FiddleSticks', 'Kayle', 'MasterYi', 'Alistar', 'Ryze', 'Sion', 'Sivir', 'Soraka', 'Teemo', 'Tristana', 'Warwick', 'Nunu', 'MissFortune', 'Ashe', 'Tryndamere', 'Jax', 'Morgana', 'Zilean', 'Singed', 'Evelynn', 'Twitch', 'Karthus', "Chogath", 'Amumu', 'Rammus', 'Anivia', 'Shaco', 'DrMundo', 'Sona', 'Kassadin', 'Irelia', 'Janna', 'Gangplank', 'Corki', 'Karma', 'Taric', 'Veigar', 'Trundle', 'Swain', 'Caitlyn', 'Blitzcrank', 'Malphite', 'Katarina', 'Nocturne', 'Maokai', 'Renekton', 'JarvanIV', 'Elise', 'Orianna', 'MonkeyKing', 'Brand', 'LeeSin', 'Vayne', 'Rumble', 'Cassiopeia', 'Skarner', 'Heimerdinger', 'Nasus', 'Nidalee', 'Udyr', 'Poppy', 'Gragas', 'Pantheon', 'Ezreal', 'Mordekaiser', 'Yorick', 'Akali', 'Kennen', 'Garen', 'Leona', 'Malzahar', 'Talon', 'Riven', "KogMaw", 'Shen', 'Lux', 'Xerath', 'Shyvana', 'Ahri', 'Graves', 'Fizz', 'Volibear', 'Rengar', 'Varus', 'Nautilus', 'Viktor', 'Sejuani', 'Fiora', 'Ziggs', 'Lulu', 'Draven', 'Hecarim', "Khazix", 'Darius', 'Jayce', 'Lissandra', 'Diana', 'Quinn', 'Syndra', 'AurelionSol', 'Kayn', 'Zoe', 'Zyra', "Kaisa", "Seraphine", 'Gnar', 'Zac', 'Yasuo', "Velkoz", 'Taliyah', "Akshan", 'Camille', 'Braum', 'Jhin', 'Kindred', 'Jinx', 'TahmKench', 'Viego', 'Senna', 'Lucian', 'Zed', 'Kled', 'Ekko', 'Qiyana', 'Vi', 'Aatrox', 'Nami', 'Azir', 'Yuumi', 'Samira', 'Thresh', 'Illaoi', "RekSai", 'Ivern', 'Kalista', 'Bard', 'Rakan', 'Xayah', 'Ornn', 'Sylas', 'Rell', 'Neeko', 'Aphelios', 'Pyke', "Sett", "Vex", "Yone", "Gwen", "Lillia", "Zeri", "Belveth"]
REPCHAMPS = []
TIERVALUES = {"IORN": 10000, "BRONZE": 20000, "SILVER": 30000, "GOLD": 40000, "PLATINUM": 50000, "EMERALD": 60000, "DIAMOND": 70000, "MASTER": 80000, "GRANDMASTER": 90000, "CHALLENGER": 100000}
RANKVALUES = {"IV": 1000, "III": 2000, "II": 3000, "I": 4000}
playingids = [] #image guess
playingidss = [] #spell guess

spells = {}
champs = {}
gamechnl = ""

def regionchange(place):
    global region
    place = place.upper()
    if place in SERVERS:
        if place in EUROPE:
            region = "europe"
            if place == "EUNE":
                place = "EUN1"
            if place == "EUW":
                place = "EUW1"
            if place == "TR":
                place = "TR1"
        if place in AMERICAS:
            region = "americas"
            if place == "LAN":
                place = "LA1"
            if place == "LAS":
                place = "LA2"
            if place == "OCE":
                place = "OC1"
            if place == "BR":
                place = "BR1"
            if place == "NA":
                place = "NA1"
        if place in ASIA:
            region = "asia"
            if place == "JP":
                place = "JP1"
    return place

def portchange(port):
    port = port.upper()
    if port == "NA1":
        portlink = "spectator.na1.lol.riotgames.com:80"
    if port == "EUW1":
        portlink = "spectator.euw1.lol.riotgames.com:80"
    if port == "EUN1":
        portlink = "spectator.eu.lol.riotgames.com:80"
    if port == "BR1":
        portlink = "spectator.br.lol.riotgames.com:80"
    if port == "LA1":
        portlink = "spectator.br.lol.riotgames.com:80"
    if port == "LA2":
        portlink = "spectator.br.lol.riotgames.com:80"
    if port == "RU":
        portlink = "spectator.tr.lol.riotgames.com:80"
    if port == "TR1":
        portlink = "spectator.tr.lol.riotgames.com:80"
    if port == "KR":
        portlink = "QFKR1PROXY.kassad.in:8088"
    if port == "TW":
        portlink = "QFTW1PROXY.kassad.in:8088"
    if port == "TW":
        portlink = "qfsea1proxy.kassad.in:8088"
    return portlink

def getaccbytag(name):
    return requests.get("https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/" + name.split("#")[0] + "/" + name.split("#")[1] + "?api_key=" + RIOTOKEN)

def getaccbypuuid(puuid):
    return requests.get("https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/" + puuid + "?api_key=" + RIOTOKEN)

def find_highest_floor(input_value, tier_values):
    valid_tiers = [tier for tier, value in tier_values.items() if value <= input_value]
    highest_tier = max(valid_tiers, key=lambda tier: tier_values[tier])
    return highest_tier

def rankupdate():
    with open('links.json', 'r') as file:
        data = json.load(file)
        linked_profiles = data.get('linkedProfiles', [])

    for profile in linked_profiles:
        puuid = profile.get('puuid')
        summoner_data = requests.get("https://" + profile.get('leagueServer') + ".api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" + puuid + "?api_key=" + RIOTOKEN).json()
        if summoner_data is not None:
            rank_data = requests.get("https://" + profile.get('leagueServer') + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + summoner_data.get('id') + "?api_key=" + RIOTOKEN).json()
            if len(rank_data) != 0:
                if rank_data[0]['queueType'] == "RANKED_SOLO_5x5":
                    soloq = rank_data[0]
                    profile['soloq'] = TIERVALUES[str(soloq['tier'])] + RANKVALUES[str(soloq['rank'])] + soloq['leaguePoints']
                    profile['flex'] = 0

                elif len(rank_data) > 1 and rank_data[1]['queueType'] == "RANKED_SOLO_5x5":
                    soloq = rank_data[1]
                    flex = rank_data[0]
                    profile['soloq']  = TIERVALUES[str(soloq['tier'])] + RANKVALUES[str(soloq['rank'])] + soloq['leaguePoints']
                    profile['flex'] = TIERVALUES[str(flex['tier'])] + RANKVALUES[str(flex['rank'])] + flex['leaguePoints']

                elif rank_data[0]['queueType'] == "RANKED_FLEX_SR":
                    flex = rank_data[0]
                    profile['soloq'] = 0
                    profile['flex'] = TIERVALUES[str(flex['tier'])] + RANKVALUES[str(flex['rank'])] + flex['leaguePoints']
            else:
                profile['soloq'] = 0
                profile['flex'] = 0
        
    with open('links.json', 'w') as file:
            json.dump(data, file, indent=2)


def guessgamef(id):
    global champs
    champs[id] = random.choice(CHAMPS)
    while champs[id] in REPCHAMPS:
        champs[id] = random.choice(CHAMPS)
    REPCHAMPS.append(champs[id])
    if len(REPCHAMPS) > 80:
        REPCHAMPS.pop(0)
    img_data = requests.get("https://ddragon.leagueoflegends.com/cdn/img/champion/tiles/" + champs[id] + "_0.jpg").content
    with open(r"C:\Users\dzelm\Desktop\bots\tristbot\champimg.jpg", 'wb') as handler:
        handler.write(img_data)
    
    image = Image.open(r'C:\Users\dzelm\Desktop\bots\tristbot\champimg.jpg')
    image = image.resize((5, 5))
    image = image.resize((500, 500), resample=Image.BOX)
    image.save(r"C:\Users\dzelm\Desktop\bots\tristbot\champs\\"+str(id)+".jpg")

    color_thief = ColorThief(r"C:\Users\dzelm\Desktop\bots\tristbot\champs\\"+str(id)+".jpg")
    dominant_color = color_thief.get_color(quality=1)
    r, g, b = dominant_color
    embed = discord.Embed(title = "Who is this champion?", color=discord.Color.from_rgb(r, g, b))
    file = discord.File(r"C:\Users\dzelm\Desktop\bots\tristbot\champs\\"+str(id)+".jpg", filename="champimg"+str(id)+".jpg")
    embed.set_image(url="attachment://champimg"+str(id)+".jpg")
    return embed, file


def guessgamefs(id):
    champion = random.choice(CHAMPS)
    spellnum = random.randint(0,3)
    champ_data = requests.get("https://ddragon.leagueoflegends.com/cdn/13.9.1/data/en_US/champion/" + champion + ".json").content

    spells[id] = champion

    return json.loads(champ_data)['data'][str(champion)]['spells'][spellnum]['name']

def changeme(ctx, user):
    if ".me" in user:
        with open(r"C:\Users\dzelm\Desktop\bots\tristbot\links.json", 'r+') as f:
            data = json.load(f)
            for name in data['linkedProfiles']:
                if ctx.author.id == name['discordId']:
                    return name["puuid"]
    else:
        return user
    
def rw(champ):
    return champ.lower().title().replace("'", "").replace(" ", "").replace("wukong", "monkeyking").replace("Glasc", "")

async def log(arr):
    response = f"{arr[0]}"
    arr.pop(0)
    for num in range(1, int(len(arr)/2)+1):
        response += f", {arr[num*2-2]}: {arr[num*2-1]}"
    await bot.get_channel(1098937322881421312).send(response)
    print(response)

intents = discord.Intents.default()
intents.members = True
intents.messages = True
bot = discord.Bot(owner_id=461859360931315713, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you right now'))
    print(f"current guilds ({len(bot.guilds)}):\r")
    for key, guild in enumerate(bot.guilds):
        print(key+1, guild)
    
    rankupdate()

@bot.event
async def on_message(message):
    if message.author.id == 461859360931315713:
        if message.channel.id == 1098953992735838309:
            response = f"current guilds ({len(bot.guilds)}):\r"
            for key, guild in enumerate(bot.guilds):
                response += f"{key+1}: {guild}\r"
            await message.channel.send(response)


@bot.slash_command(description = "Quickly shows basic stats about summoners last game")
@option("summoner", description="Enter summoner")
@option("server", description="Choose Server (Optional, defaults to EUW)", choices=SERVERS)
async def last(ctx: discord.ApplicationContext, summoner: str, server: str = "EUW"):
    await ctx.defer()
    _ = regionchange(server)
    if changeme(ctx, summoner) == summoner:
        r1 = getaccbytag(summoner)
    else:
        r1 = getaccbypuuid(changeme(ctx, summoner))
                    
    if r1.status_code == 404:
        response = "Summoner not found"
        await ctx.respond(response)
        return

    r2 = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + r1.json()['puuid'] + "/ids?start=0&count=1&api_key=" + RIOTOKEN)
    r3 = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/" + r2.json()[0] + "?api_key=" + RIOTOKEN)
    
    embed = discord.Embed(title = "hm", color=0x3cbc8d)
    for p1 in r3.json()['info']['participants']:
        if p1['summonerName'].lower().strip() == summoner.lower().strip():
            player = p1
            if player['win'] == True:
                embed = discord.Embed(title = p1['summonerName'] + "'s winning " + p1['championName'], color=0x3cbc8d)
            else:
                embed = discord.Embed(title = p1['summonerName'] + "'s losing " + p1['championName'], color=0xe9422e)

    embed.add_field(name = "Gamemode", value = r3.json()['info']['gameMode'], inline = False)
    embed.add_field(name = "Kills", value = player['kills'], inline = True) 
    embed.add_field(name = "Deaths", value = player['deaths'], inline = True)
    embed.add_field(name = "Assists", value = player['assists'], inline = True)
    embed.set_image(url = "https://ddragon.leagueoflegends.com/cdn/img/champion/centered/" + player['championName'] + "_0.jpg")
    await ctx.respond(embed=embed)
    await log(["LAST", "GUILD", ctx.guild, "AUTHOR", ctx.author, "SUMMONER", summoner, "SERVER", server])

@bot.slash_command(description = "Checks the damage your team dealt in the last game")
@option("summoner", description="Enter summoner")
@option("server", description="Choose Server (Optional, defaults to EUW)", choices=SERVERS)
async def dmglast(ctx: discord.ApplicationContext, summoner: str, server: str = "EUW"):
    await ctx.defer()
    summoner = changeme(ctx, summoner)
    place = regionchange(server)

    r1 = requests.get("https://" + place + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner + "?api_key=" + RIOTOKEN)
    if r1.status_code == 404:
        response = "Summoner not found"
        await ctx.respond(response)
        return

    r2 = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + r1.json()['puuid'] + "/ids?start=0&count=1&api_key=" + RIOTOKEN)
    r3 = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/" + r2.json()[0] + "?api_key=" + RIOTOKEN)
    
    embed = discord.Embed(title = "Team DMG distribution", color=0x3cbc8d)
    i = 0
    for p1 in r3.json()['metadata']['participants']:
        i += 1
        if p1 == r1.json()['puuid']:
            if i <= len(r3.json()['metadata']['participants'])/2:
                team = 0
            else:
                team = 1
    
    gamelength = (r3.json()['info']['gameDuration'])/60
    teamdmg = 0
    teamarr = [0, 5]
    isplayer = 0
    isplayerarr = ["", " - "]

    for n in range(5):
        player = r3.json()['info']['participants'][n+teamarr[team]]
        teamdmg += player['totalDamageDealtToChampions']

    for n in range(5):
        player = r3.json()['info']['participants'][n+teamarr[team]]
        if player['summonerName'] == summoner:
            isplayer = 1
        embed.add_field(name = "Summoner", value = (isplayerarr[isplayer] + player['summonerName']), inline = True) 
        embed.add_field(name = "Champion", value = player['championName'], inline = True)
        embed.add_field(name = "dmg;   dmg%;   dmg/m", value = str(player['totalDamageDealtToChampions']) + "; " + str(round(player['totalDamageDealtToChampions']/(teamdmg/100), 2)) + "%; " + str(round(player['totalDamageDealtToChampions']/gamelength)) + "/m", inline = True)
        isplayer = 0
    
    await ctx.respond(embed=embed)
    await log(["DMGLAST", "GUILD", ctx.guild, "AUTHOR", ctx.author, "SUMMONER",summoner, "SERVER", server])

@bot.slash_command(description = "Counts the amount of games from the start of the season")
@option("summoner", description="Enter summoner")
@option("server", description="Choose Server (Optional, defaults to EUW)", choices=SERVERS)
async def games(ctx: discord.ApplicationContext, summoner: str, server: str = "EUW"):
    await ctx.defer()
    summoner = changeme(ctx, summoner)
    place = regionchange(server)
    r1 = requests.get("https://" + place + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner + "?api_key=" + RIOTOKEN)

    r2 = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + r1.json()['puuid'] + "/ids?startTime=1673308800&endTime=" + str(int(time.time())) + "&start=0&count=100&api_key=" + RIOTOKEN)
    r2a = r2.json()

    while len(r2a)%100 == 0:
        r2a.extend(requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + r1.json()['puuid'] + "/ids?startTime=1673308800&endTime=" + str(int(time.time())) + "&start=" + str(int(len(r2a)/100)) +"00&count=100&api_key=" + RIOTOKEN).json())
    

    response = summoner + " has played " + str(len(r2a)) + " matches in this season"
    await ctx.respond(response)
    await log(["GAMES", "GUILD", ctx.guild, "AUTHOR", ctx.author, "SUMMONER", summoner, "SERVER", server])


@bot.slash_command(description = "Links your discord id to one league account")
@option("part", description="Choose if you want to start or complete the link process", choices=["start", "complete"])
@option("summoner", description="Enter summoner")
@option("server", description="Choose Server (Optional, defaults to EUW)", choices=SERVERS)
async def link(ctx: discord.ApplicationContext, part: str, summoner: str, server: str = "EUW"):
    await ctx.defer()
    summoner = changeme(ctx, summoner)
    place = regionchange(server)
    if part == "complete":
        r1 = requests.get("https://" + place + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner + "?api_key=" + RIOTOKEN).json()
        if r1['profileIconId'] == 10:
            with open(r"C:\Users\dzelm\Desktop\bots\tristbot\links.json", 'r+') as f:
                data = json.load(f)
                for user in data['linkedProfiles']:
                    if user['puuid'] == r1['puuid']:
                        response = "This account is already linked"
                        await ctx.respond(response)
                        return
                data['linkedProfiles'].append({"discordId":ctx.author.id, "puuid": r1['puuid'], "leagueServer" : place, "soloq": "smth", "flex": "smth"})
                rankupdate()
                response = "You can now use .me instead of summoner your name and are included in the ranking leaderboard"
                await ctx.respond(response)
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
        else:
            response = "Your icon doesnt match the one used for linking"
            await ctx.respond(response)
    elif part == "start":
        with open(r"C:\Users\dzelm\Desktop\bots\tristbot\links.json", 'r+') as f:
                data = json.load(f)
                for user in data['linkedProfiles']:
                    if ctx.author.id == user['discordId']:
                        response = "You already have an account linked"
                        await ctx.respond(response)
                        return
        embed = discord.Embed(title = "Set your profile picture to this one - ", color=0x3cbc8d)
        embed.set_thumbnail(url="https://ddragon.leagueoflegends.com/cdn/13.9.1/img/profileicon/10.png")
        await ctx.respond(embed=embed)
        await log(["LINK", "GUILD", ctx.guild, "AUTHOR", ctx.author, "PART", part, "SUMMONER", summoner, "SERVER", server])

@bot.slash_command(description = "Generates a batch file for spectating a summoner")
@option("summoner", description="Enter summoner")
@option("server", description="Choose Server (Optional, defaults to EUW)", choices=SERVERS)
async def spectate(ctx: discord.ApplicationContext, summoner: str, server: str = "EUW"):
    await ctx.defer()
    summoner = changeme(ctx, summoner)
    place = regionchange(server)

    r1 = requests.get("https://" + place + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner + "?api_key=" + RIOTOKEN)
    r2 = requests.get("https://" + place + ".api.riotgames.com/lol/spectator/v4/active-games/by-summoner/" + r1.json()['id'] + "?api_key=" + RIOTOKEN)

    if r2.status_code == 404:
        response = "Summoner not playing"
        await ctx.send(response)
        return
    with open(r'C:\Users\dzelm\Desktop\bots\tristbot\spectate.bat', 'w') as fp:
        pass
        f = open(r"C:\Users\dzelm\Desktop\bots\tristbot\templatespec.txt", "r")
        text = f.read()
        text = text.replace("<portlink>", portchange(place))
        text = text.replace("<encryptkey>", str(r2.json()['observers']['encryptionKey']))
        text = text.replace("<gameid>", str(r2.json()['gameId']))
        text = text.replace("<regionid>", place)
        fp.write(text)
    batfile = discord.File(r'C:\Users\dzelm\Desktop\bots\tristbot\spectate.bat')
    response = "Here is a file to spectate your selected summoner"
    await ctx.respond(response, file=batfile)

    response = "this batch file isn't dangerous to your pc so click 'save' in discord and on running the file click 'more info' and 'run anyway'"
    await ctx.respond(response)
    await log(["SPECTATE", "GUILD", ctx.guild, "AUTHOR", ctx.author, "SUMMONER", summoner, "SERVER", server])

@bot.slash_command(description = "Sets up a guessgame")
@option("option", description="Option to start/skip/end the guessgame", choices=["start", "skip", "end"])
async def guessgame(ctx: discord.ApplicationContext, option: str):
    global playing, gamechnl, playingids
    gamechnl = str(ctx.channel.id)
    if option == "start" and gamechnl not in playingids:
        playingids += [gamechnl]
        await ctx.respond("The guessing game has started in : <#" + gamechnl + ">")

    if option == "skip" and gamechnl in playingids:
        embed, file = guessgamef(gamechnl)
        await ctx.respond(file=file, embed=embed)
        return

    if option == "end" and gamechnl in playingids:
        playingids.remove(gamechnl)
        await ctx.respond("The guessing game has been ended")

    if gamechnl in playingids:
        embed, file = guessgamef(gamechnl)
        await ctx.respond(file=file, embed=embed)
    await log(["GUESSGAME", "GUILD", ctx.guild, "AUTHOR", ctx.author, "OPTION", option])

@bot.slash_command(description = "Function for guessing a champion in the guessing game")
@option("champion", description="a champion you want to guess")
async def g(ctx: discord.ApplicationContext, champion: str):
    global playingids, gamechnl, playingids, champs
    gamechnl = str(ctx.channel.id)
    if champs[gamechnl].lower().title() == rw(champion) and gamechnl in playingids:
        await ctx.respond("Correct the champion was " + champs[gamechnl].replace("MonkeyKing", "wukong").capitalize())
        embed, file = guessgamef(gamechnl)
        await ctx.respond(file=file, embed=embed)
    elif gamechnl not in playingids:
        await ctx.respond(content="no game running", ephemeral=True)
    else:
        await ctx.respond(content="no", ephemeral=True)
    await log(["GUESS", "GUILD", ctx.guild, "AUTHOR", ctx.author, "CHAMPION", champion, "TRUECHAMPION", champs[gamechnl]])

@bot.slash_command(description = "Function to show everything about a champ on a specific role")
@option("champion", description="Pick your champion")
@option("role", description="Specify a role for your champion (optional, defaults to what op.gg thinks is best)", choices=["top", "jungle", "mid", "adc", "support"])
async def champ(ctx: discord.ApplicationContext, champion: str, role: str = ""):
    await ctx.defer()

    hi = Html2Image(custom_flags=['--hide-scrollbars'])
    champion1 = rw(champion)
    if role != "":
        htmlres = urllib.request.urlopen("https://www.op.gg/champions/" + champion1 + "/build/" + role + "?region=global&tier=diamond_plus")
    else:
        htmlres = urllib.request.urlopen("https://www.op.gg/champions/" + champion1 + "/build?region=global&tier=diamond_plus")
    html = htmlres.read().decode(htmlres.headers.get_content_charset())

    soup = BeautifulSoup(html, 'html.parser')

    site = soup.find_all("div", {"e12xxeqe0"})[0]


    with open(r'C:\Users\dzelm\Desktop\bots\tristbot\champ.css', 'r') as file:
        css = file.read().replace('\n', '')
    hi.screenshot(html_str=str(site), css_str=css, save_as='build.png', size=(1100, 900))

    cat = requests.get("https://api.thecatapi.com/v1/images/search").json()[0]['url']
    im1 = Image.open(requests.get(cat, stream = True).raw).resize((350, 350))
    im2 = Image.open(r"build.png")

    back_im = im2.copy()
    back_im.paste(im1, (750, 550))
    back_im.save(r'catbuild.png')

    file = discord.File(r"C:\Users\dzelm\Desktop\bots\tristbot\catbuild.png", filename="catbuild.png")

    embed = discord.Embed(title = (champion + role).title(), color=0x3cbc8d)
    embed.set_image(url="attachment://catbuild.png")

    await ctx.respond(embed=embed, file=file)
    await log(["CHAMP", "GUILD", ctx.guild, "AUTHOR", ctx.author, "CHAMPION", champion, "ROLE", role])

@bot.slash_command(description = "Function to create images for a comp")
@option("top", description="Pick a champion for top")
@option("jgl", description="Pick a champion for jgl")
@option("mid", description="Pick a champion for mid")
@option("adc", description="Pick a champion for adc")
@option("sup", description="Pick a champion for sup")
async def comp(ctx: discord.ApplicationContext, top: str, jgl: str, mid: str, adc: str, sup: str):
    await ctx.defer()
    champs = [top, jgl, mid, adc, sup]
    comp = Image.open(r"C:\Users\dzelm\Desktop\bots\tristbot\compbg.png")
    for key, champ in enumerate(champs):
        champs[key] = rw(champ)
        if champ == "ksante":
            champs[key] = Image.open(r"C:\Users\dzelm\Desktop\bots\tristbot\ksante.jpg").resize((200, 200))
        elif champ == "nilah":
            champs[key] = Image.open(r"C:\Users\dzelm\Desktop\bots\tristbot\nilah.jpg").resize((200, 200))
        else:
            champs[key] = requests.get("https://ddragon.leagueoflegends.com/cdn/img/champion/tiles/" + champs[key] + "_0.jpg")
            champs[key] = Image.open(BytesIO(champs[key].content)).resize((200, 200))
        comp.paste(champs[key], (50+(250*key), 150))
    comp.save(r"C:\Users\dzelm\Desktop\bots\tristbot\comp.png")

    file = discord.File(r"C:\Users\dzelm\Desktop\bots\tristbot\comp.png", filename="comp.png")

    embed = discord.Embed(title = f"{top},          {jgl},          {mid},          {adc},          {sup}", color=0x3cbc8d)
    embed.set_image(url="attachment://comp.png")

    await ctx.respond(embed=embed, file=file)
    await log(["COMP", "GUILD", ctx.guild, "AUTHOR", ctx.author, "TOP", top, "JGL", jgl, "MID", mid, "ADC", adc, "SUP", sup])

@bot.slash_command(description = "Sets up a spellguess game")
@option("option", description="Option to start/skip/end the spellguess game", choices=["start", "skip", "end"])
async def spellguess(ctx: discord.ApplicationContext, option: str):
    global playingidss
    gamechnl = str(ctx.channel.id)
    if option == "start":
        playingidss += [gamechnl]
        await ctx.respond("The spellguessing game has started in : <#" + gamechnl + ">")

    if option == "skip":
        spell = guessgamefs(gamechnl)
        await ctx.respond(f"Spell name: {spell}")
        return

    if option == "end":
        playingidss.remove(gamechnl)
        await ctx.respond("The spellguessing game has been ended")

    if gamechnl in playingidss:
        spell = guessgamefs(gamechnl)
        await ctx.respond(f"Spell name: {spell}")
    await log(["SPELLGUESSGAME", "GUILD", ctx.guild, "AUTHOR", ctx.author, "OPTION", option])

@bot.slash_command(description = "Function for guessing a champion in the guessing spell game")
@option("champion", description="a champion you want to guess")
async def sg(ctx: discord.ApplicationContext, champion: str):
    global spells, gamechnl, playingids, champs
    gamechnl = str(ctx.channel.id)
    print(rw(spells[gamechnl]), rw(champion), rw(spells[gamechnl]) == rw(champion))
    if rw(spells[gamechnl]) == rw(champion):
        await ctx.respond("Correct the champion was " + spells[gamechnl].replace("MonkeyKing", "wukong").capitalize())
        spell = guessgamefs(gamechnl)
        await ctx.respond(f"Spell name: {spell}")
    else:
        await ctx.respond(content="no", ephemeral=True)
    await log(["SPELLGUESS", "GUILD", ctx.guild, "AUTHOR", ctx.author, "CHAMPION", champion, "TRUECHAMPION", spells[gamechnl]])


@bot.slash_command(description = "Shows the ranking of everyone in this server")
@option("server", description="Choose Server (Optional, defaults to EUW)", choices=["ALL", "EUW", "EUNE", "JP", "KR", "LAN", "LAS", "NA", "OC", "RU", "TR", "BR"])
@option("queuetype", description="Choose type of queue (Optional, defaults to SOLOQ)", choices=["SOLOQ", "FLEX"])
async def ranking(ctx: discord.ApplicationContext, server: str = "EUW", queuetype: str = "SOLOQ"):
    await ctx.defer()
    rankupdate()

    embed = discord.Embed(title=f"Top {queuetype} Players", color=discord.Color.gold())
    if server != "ALL":
        place = regionchange(server)
    else:
        place = None

    rankedarray = []

    with open('links.json', 'r') as file:
        data = json.load(file)
        linked_profiles = data.get('linkedProfiles', [])

    for profile in linked_profiles:
        guild = ctx.guild

        user = guild.get_member(profile.get('discordId'))
        if user:
            if profile.get('leagueServer') == place or server == "ALL":
                rankedarray.append(profile)
    
    sortedrankedarray = sorted(rankedarray, key=lambda x: x[str(queuetype).lower()], reverse=True)
    text = ""
    for key, elem in enumerate(sortedrankedarray):
        summonername = requests.get("https://" + elem.get('leagueServer') + ".api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" + elem['puuid'] + "?api_key=" + RIOTOKEN).json()["name"]

        elo = elem[str(queuetype).lower()]
        if elo != 0:
            highest_tier = find_highest_floor(elo, TIERVALUES)
            remainder = elo - TIERVALUES[str(highest_tier)]
            highest_rank = find_highest_floor(remainder, RANKVALUES)
            lp = remainder - RANKVALUES[str(highest_rank)]

            text = text + f"#{key+1}| <@{elem['discordId']}> - {summonername} - {highest_tier} {highest_rank} {lp} LP \n"
        else:
            text = text + f"#{key+1}| <@{elem['discordId']}> - {summonername} - Unranked \n"

    embed.add_field(name=f"server - {server}", value=text, inline=False)

    await ctx.respond(embed=embed)
    await log(["RANKING", "GUILD", ctx.guild, "AUTHOR", ctx.author, "SERVER", server, "QUEUETYPE", queuetype])


bot.run(DSTOKEN)