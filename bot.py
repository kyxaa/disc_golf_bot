import discord
from discord.ext import tasks, commands
from config import INVOCATION, DATETIME_STRING_FORMAT, GITHUB_REPO, SUNNY, FEW_CLOUDS, SCATTERED_CLOUDS, BROKEN_CLOUDS, SHOWER_RAIN, RAIN, THUNDERSTORM, SNOW, MIST
from datetime import datetime
import requests
import os
import json
from dotenv import load_dotenv
import asyncio
import asyncpg
bot = commands.Bot(command_prefix=INVOCATION)

load_dotenv()
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


#######################################################################
# Discord Stuff
# TODO: Create an update system that has properly handling...lets not make this another Calendra fiasco
# TODO: Create information scrapping from messages in specific channel.
# TODO: I would like the bot to create a "global" variable that is the channel that we are updating course info. I would like to this to be based on channel name.
# TODO: Test Github webhooks ROUND 4
#######################################################################

@bot.event
async def on_ready():
    print("Connected!")
    git_status = discord.Game(GITHUB_REPO)
    await bot.change_presence(activity=git_status)


class HourlyUpdate(commands.Cog):
    def __init__(self):
        self.index = 0
        self.bot = bot
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=5.0)
    async def printer(self):
        await self.scan_channel()

    @printer.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    async def scan_channel(self):
        channels = bot.get_all_channels()
        for channel in channels:
            if channel.name == "course-info":
                pinned_messages = await channel.pins()
                for messages in pinned_messages:
                    pass


#######################################################################
# Weather Stuff
# TODO: Create "data presentation" functionality.
# TODO: Create ways to force an update
#######################################################################

def weather_lat_long(lat, lon):
    r = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={WEATHER_TOKEN}&units=imperial')
    if not r.ok:
        # return
        raise Exception("ERROR: Could not fetch weather")
    data = r.json()
    with open('course_data.txt', 'w') as outfile:
        json.dump(data, outfile)
    pass

# weather_lat_long(33.044564, -96.691857)


bot.add_cog(HourlyUpdate())
bot.run(DISCORD_TOKEN)
