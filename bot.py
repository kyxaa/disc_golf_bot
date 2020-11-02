import discord
from discord.ext import tasks, commands
from config import INVOCATION, DATETIME_STRING_FORMAT, GITHUB_REPO, SUNNY, FEW_CLOUDS, SCATTERED_CLOUDS, BROKEN_CLOUDS, SHOWER_RAIN, RAIN, THUNDERSTORM, SNOW, FOG
from datetime import datetime
import requests
import os
import json
from dotenv import load_dotenv
import asyncio
import asyncpg
import re
import pandas
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

    def directions_from_degrees(self, degrees_direction):
        if (348.75 <= degrees_direction < 360) or (0 <= degrees_direction < 11.25):
            wind_direction = "N"
        elif (11.25 <= degrees_direction < 33.75):
            wind_direction = "NNE"
        elif (33.75 <= degrees_direction < 56.25):
            wind_direction = "NE"
        elif (56.25 <= degrees_direction < 78.75):
            wind_direction = "ENE"
        elif (78.75 <= degrees_direction < 101.25):
            wind_direction = "E"
        elif (101.25 <= degrees_direction < 123.75):
            wind_direction = "ESE"
        elif (123.75 <= degrees_direction < 146.25):
            wind_direction = "SE"
        elif (146.25 <= degrees_direction < 168.75):
            wind_direction = "SSE"
        elif (168.75 <= degrees_direction < 191.25):
            wind_direction = "S"
        elif (191.25 <= degrees_direction < 213.75):
            wind_direction = "SSW"
        elif (213.75 <= degrees_direction < 236.25):
            wind_direction = "SW"
        elif (236.25 <= degrees_direction < 258.75):
            wind_direction = "WSW"
        elif (258.75 <= degrees_direction < 281.25):
            wind_direction = "W"
        elif (281.25 <= degrees_direction < 303.75):
            wind_direction = "WNW"
        elif (303.75 <= degrees_direction < 326.25):
            wind_direction = "NW"
        elif (326.25 <= degrees_direction < 348.75):
            wind_direction = "NNW"
        return wind_direction

    async def scan_channel_and_update_embeds(self):
        channels = bot.get_all_channels()
        for channel in channels:
            if channel.name == "course-info":
                pinned_messages = await channel.pins()
                for pinned_message in pinned_messages:
                    message = await channel.fetch_message(pinned_message.id)
                    coordinates_match = re.search(
                        "\(([0-9.,\s-]*)\)", message.content)
                    coordinates_list = coordinates_match.group(1).split(", ")
                    weather_info = self.weather_lat_long(
                        coordinates_list[0], coordinates_list[1])
                    await self.update_embed(message, weather_info)
                    pass

    async def update_embed(self, message, weather_info):
        embed = await self.build_embed(weather_info)
        await message.edit(embed=embed)

    async def build_embed(self, weather_info):
        embed_dict = {
            "title": "",
            "type": "rich",
            "color": 1009165,
            "description": ""
        }
        pass
        if weather_info["current"]["weather"][0]["icon"] == "01d":
            current_weather_icon = SUNNY
        elif weather_info["current"]["weather"][0]["icon"] == "02d":
            current_weather_icon = FEW_CLOUDS
        elif weather_info["current"]["weather"][0]["icon"] == "03d":
            current_weather_icon = SCATTERED_CLOUDS
        elif weather_info["current"]["weather"][0]["icon"] == "04d":
            current_weather_icon = BROKEN_CLOUDS
        elif weather_info["current"]["weather"][0]["icon"] == "09d":
            current_weather_icon = SHOWER_RAIN
        elif weather_info["current"]["weather"][0]["icon"] == "10d":
            current_weather_icon = RAIN
        elif weather_info["current"]["weather"][0]["icon"] == "11d":
            current_weather_icon = THUNDERSTORM
        elif weather_info["current"]["weather"][0]["icon"] == "13d":
            current_weather_icon = SNOW
        elif weather_info["current"]["weather"][0]["icon"] == "50n":
            current_weather_icon = FOG
        pass
        current_wind_direction = self.directions_from_degrees(
            weather_info["current"]["wind_deg"])
        current_datetime = datetime.fromtimestamp(
            weather_info["current"]["dt"])
        if current_datetime.minute < 30:
            start_of_hourly_info = 2
        elif current_datetime.minute >= 30:
            start_of_hourly_info = 3

        iterating_hour_value = start_of_hourly_info
        for hour in weather_info["hourly"]:
            if iterating_hour_value > start_of_hourly_info + 16:
                break
            if weather_info["hourly"].index(hour) == iterating_hour_value:
                iterating_hour_value += 2
                pass

        # hourly_dict = {
        #     ""
        # }

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
