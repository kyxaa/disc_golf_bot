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
import re
bot = commands.Bot(command_prefix=INVOCATION)

load_dotenv()
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    print("Connected!")
    git_status = discord.Game(GITHUB_REPO)
    await bot.change_presence(activity=git_status)


class WeatherUpdate(commands.Cog):
    def __init__(self):
        self.index = 0
        self.bot = bot
        self.update.start()

    def cog_unload(self):
        self.update.cancel()

    @tasks.loop(seconds=60.0)
    async def update(self):
        await self.scan_channel_and_update_embeds()

    @update.before_loop
    async def before_update(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    async def scan_channel_and_update_embeds(self):
        channels = bot.get_all_channels()
        for channel in channels:
            if channel.name == "course-info":
                pinned_messages = await channel.pins()
                for message in pinned_messages:
                    coordinates_match = re.search(
                        "\(([0-9.,\s-]*)\)", message.content)
                    coordinates_list = coordinates_match.group(1).split(", ")
                    weather_info = self.weather_lat_long(
                        coordinates_list[0], coordinates_list[1])
                    await self.update_embed(message, weather_info)
                    pass

    async def update_embed(self, message, weather_info):
        with open('embed_json.json', 'r') as infile:
            data = json.load(infile)
        embed = discord.Embed.from_dict(data)
        await message.edit(embed=embed)

    def weather_lat_long(self, lat, lon):
        # r = requests.get(
        #     f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={WEATHER_TOKEN}&units=imperial')
        # if not r.ok:
        #     # return
        #     raise Exception("ERROR: Could not fetch weather")
        # data = r.json()
        # with open('course_data.json', 'w') as outfile:
        #     json.dump(data, outfile)
        ##########Only here during testing##########
        ############################################
        with open('course_data.json', 'r') as infile:
            data = json.load(infile)
        ############################################
        return data


# weather_lat_long(33.044564, -96.691857)
bot.add_cog(WeatherUpdate())
bot.run(DISCORD_TOKEN)

#########Add Park Template#########
# await channel.send(content="**SHAWNEE PARK** (33.044564, -96.691857)\n\
# ===============================\n\
# Google Maps Link: https://goo.gl/maps/n7ThZ1CQeKvJvoDH6\n\
# \n\
# UDisc Link: https://app.udisc.com/applink/course/2307")
