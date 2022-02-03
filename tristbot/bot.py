import os

import discord
from dotenv import load_dotenv
import requests
import shlex
import json
import os
import time

load_dotenv()
DSTOKEN = os.getenv('DISCORD_TOKEN')
RIOTOKEN = os.getenv('RIOT_TOKEN')
file1 = open(r"C:\Users\PcPraha\Desktop\tristbot\prefix.txt", "r")
PREFIX = file1.read()
SERVERS = ["BR", "EUNE", "EUW", "JP", "KR", "LAN", "LAS", "NA", "OC", "RU", "TR"]
AMERICAS = ["NA", "BR", "LAN", "LAS", "OCE"]
EUROPE = ["EUNE", "EUW", "TR", "RU"]
ASIA = ["KR", "JP"]
print("current prefix is " + PREFIX)

client = discord.Client()

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

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    global PREFIX, response, embed, region, author
    author = False

    if ".me" in message.content:
        with open('links.json', 'r+') as f:
            data = json.load(f)
            for name in data['linkedProfiles']:
                if message.author.id == name['discordId']:
                    message.content = message.content.replace(".me", '"' + name['summonerName'] + '"')
                    author = True
            print(message.content)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()


    if message.author == client.user:
        return

    if message.content == PREFIX + 'ping':
        response = 'pong'
        await message.channel.send(response)

    if (PREFIX + 'prefix') in message.content[0:7]:
        PREFIX = message.content[8:9]
        if PREFIX == " " or PREFIX == "":
            response = 'The prefix has not been set'
            await message.channel.send(response)
            return
        file1 = open(r"C:\Users\PcPraha\Desktop\tristbot\prefix.txt", "w")
        file1.write(PREFIX)
        file1.close()
        response = 'The prefix has been set to ' + PREFIX
        print("The prefix has been set to " + PREFIX)
        await message.channel.send(response)

    if (PREFIX + 'last') in message.content[0:5]:
        args = shlex.split(message.content[6:None])
        if len(args) > 1:
            args[1] = regionchange(args[1])
        else:
            args.append("EUN1")
            region = "europe"

                    
        r1 = requests.get("https://" + args[1] + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + args[0] + "?api_key=" + RIOTOKEN)
        if r1.status_code == 404:
            response = "Summoner not found"
            await message.channel.send(response)
            return

        r2 = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + r1.json()['puuid'] + "/ids?start=0&count=1&api_key=" + RIOTOKEN)
        r3 = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/" + r2.json()[0] + "?api_key=" + RIOTOKEN)
        
        embed = discord.Embed(title = "hm", color=0x3cbc8d)
        for p1 in r3.json()['info']['participants']:
            if p1['summonerName'].lower() == args[0].lower():
                player = p1
                if player['win'] == True:
                    embed = discord.Embed(title = p1['summonerName'] + "'s winning " + p1['championName'], color=0x3cbc8d)
                else:
                    embed = discord.Embed(title = p1['summonerName'] + "'s losing " + p1['championName'], color=0xe9422e)

        embed.add_field(name = "Kills", value = player['kills'], inline = True) 
        embed.add_field(name = "Deaths", value = player['deaths'], inline = True)
        embed.add_field(name = "Assists", value = player['assists'], inline = True)
        embed.set_image(url = "https://ddragon.canisback.com/img/champion/centered/" + player['championName'] + "_0.jpg")
        await message.channel.send(embed=embed)
        print(message.author,player['summonerName'], args[1], player['championName'], player["win"])

    if (PREFIX + 'stats') in message.content[0:6]:
        args = shlex.split(message.content[7:None])
        if len(args) > 1:
            args[1] = regionchange(args[1])
        else:
            args.append("EUN1")
            region = "europe"

                    
        r1 = requests.get("https://" + args[1] + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + args[0] + "?api_key=" + RIOTOKEN)
        if r1.status_code == 404:
            response = "Summoner not found"
            await message.channel.send(response)
            return
        print(r1.json())

        r2 = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + r1.json()['puuid'] + "/ids?startTime=1641513600&endTime=" + str(int(time.time())) + "&start=0&count=100&api_key=" + RIOTOKEN)
        r2a = r2.json()

        while len(r2a)%100 == 0:
            r2a.extend(requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + r1.json()['puuid'] + "/ids?startTime=1641513600&endTime=" + str(int(time.time())) + "&start=" + str(int(len(r2.json())/100)) +"00&count=100&api_key=" + RIOTOKEN).json())
            print(len(r2a))
        print(len(r2a))
        if author:
            response = "You have played " + str(len(r2a)) + " matches in this season"
        else:
            response = "They have played " + str(len(r2a)) + " matches in this season"
        print(r2a)
        await message.channel.send(response)

    if (PREFIX + 'link') in message.content[0:5]:
        args = shlex.split(message.content[6:None])

        if len(args) > 2:
            args[2] = regionchange(args[2])
        else:
            args.append("EUN1")
            region = "europe"

        if len(args) > 1:
            if args[1] == "done":
                r1 = requests.get("https://" + args[2] + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + args[0] + "?api_key=" + RIOTOKEN)
                if r1.json()['profileIconId'] == 10:
                    with open('links.json', 'r+') as f:
                        data = json.load(f)
                        for name in data['linkedProfiles']:
                            if message.author.id == name['discordId']:
                                response = "You already have a account linked"
                                await message.channel.send(response)
                                return
                        data['linkedProfiles'].append({"discordId":message.author.id, "summonerName": args[0], "leagueServer" : args[2]})
                        response = "You can now use .me instead of your name"
                        await message.channel.send(response)
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()
                    return

        embed = discord.Embed(title = "Set your profile picture to this one - ", color=0x3cbc8d)
        embed.set_thumbnail(url="https://ddragon.canisback.com/latest/img/profileicon/10.png")
        await message.channel.send(embed=embed)

    if (PREFIX + 'spectate') in message.content[0:9]:
        args = shlex.split(message.content[10:None])
        if len(args) > 1:
            args[1] = regionchange(args[1])
        else:
            args.append("EUN1")
            region = "europe"

        r1 = requests.get("https://" + args[1] + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + args[0] + "?api_key=" + RIOTOKEN)
    
        if r1.status_code == 404:
            response = "Summoner not found"
            await message.channel.send(response)
            return

        r2 = requests.get("https://" + args[1] + ".api.riotgames.com/lol/spectator/v4/active-games/by-summoner/" + r1.json()['id'] + "?api_key=" + RIOTOKEN)

        if r2.status_code == 404:
            response = "Summoner not playing"
            await message.channel.send(response)
            return
        print(r2.status_code, message.author, args[0])
        with open('spectate.bat', 'w') as fp:
            pass
            f = open("templatespec.txt", "r")
            text = f.read()
            text = text.replace("<portlink>", portchange(args[1]))
            text = text.replace("<encryptkey>", str(r2.json()['observers']['encryptionKey']))
            text = text.replace("<gameid>", str(r2.json()['gameId']))
            text = text.replace("<regionid>", args[1])
            fp.write(text)
        batfile = discord.File(r'spectate.bat')
        response = "Here is a file to spectate your selected summoner"
        await message.channel.send(response, file=batfile)

        response = "this batch file isn't dangerous to your pc so click 'save' in your internet browser and on running the file click 'more info' and 'run anyway'"
        await message.channel.send(response)
    
    if "Ondra gaming?" in message.content[0:13]:
        await message.channel.send("Zuzka time")
    
    if "niger" in message.content or "nigger" in message.content or "nigga" in message.content:
        await message.channel.send("fuck em")

client.run(DSTOKEN)