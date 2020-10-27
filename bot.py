import discord
from discord.ext import commands
from config import INVOCATION, DATETIME_STRING_FORMAT, GITHUB_REPO, SUNNY, FEW_CLOUDS, SCATTERED_CLOUDS, BROKEN_CLOUDS, SHOWER_RAIN, RAIN, THUNDERSTORM, SNOW, MIST
from datetime import datetime
import requests
import os
import json
from dotenv import load_dotenv
bot = commands.Bot(command_prefix=INVOCATION)

load_dotenv()
weather_token = os.getenv('WEATHER_TOKEN')


@bot.event
async def on_ready():
    print("Connected!")
    git_status = discord.Game(GITHUB_REPO)
    await bot.change_presence(activity=git_status)


def weather_lat_long(lat, lon):
    r = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={weather_token}&units=imperial')
    if not r.ok:
        # return
        raise Exception("ERROR: Could not fetch weather")
    data = r.json()
    with open('course_data.txt', 'w') as outfile:
        json.dump(data, outfile)
    pass


weather_lat_long(33.044564, -96.691857)
