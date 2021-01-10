import discord
from discord import message
from discord.ext import tasks, commands
from config import INVOCATION, DATETIME_STRING_FORMAT, GITHUB_REPO, SUNNY, FEW_CLOUDS, SCATTERED_CLOUDS, BROKEN_CLOUDS, SHOWER_RAIN, RAIN, THUNDERSTORM, SNOW, FOG, ICON_CODE_TUPLE_LIST, DIRECTION_DEGREES_TUPLE_LIST
from datetime import datetime
import requests
import os
import json
from dotenv import load_dotenv
import asyncio
# import asyncpg
import re
import pandas
from pytz import timezone
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

    # def directions_from_degrees(self, degrees_direction):
    #     if (348.75 <= degrees_direction < 360) or (0 <= degrees_direction < 11.25):
    #         wind_direction = "N"
    #     elif (11.25 <= degrees_direction < 33.75):
    #         wind_direction = "NNE"
    #     elif (33.75 <= degrees_direction < 56.25):
    #         wind_direction = "NE"
    #     elif (56.25 <= degrees_direction < 78.75):
    #         wind_direction = "ENE"
    #     elif (78.75 <= degrees_direction < 101.25):
    #         wind_direction = "E"
    #     elif (101.25 <= degrees_direction < 123.75):
    #         wind_direction = "ESE"
    #     elif (123.75 <= degrees_direction < 146.25):
    #         wind_direction = "SE"
    #     elif (146.25 <= degrees_direction < 168.75):
    #         wind_direction = "SSE"
    #     elif (168.75 <= degrees_direction < 191.25):
    #         wind_direction = "S"
    #     elif (191.25 <= degrees_direction < 213.75):
    #         wind_direction = "SSW"
    #     elif (213.75 <= degrees_direction < 236.25):
    #         wind_direction = "SW"
    #     elif (236.25 <= degrees_direction < 258.75):
    #         wind_direction = "WSW"
    #     elif (258.75 <= degrees_direction < 281.25):
    #         wind_direction = "W"
    #     elif (281.25 <= degrees_direction < 303.75):
    #         wind_direction = "WNW"
    #     elif (303.75 <= degrees_direction < 326.25):
    #         wind_direction = "NW"
    #     elif (326.25 <= degrees_direction < 348.75):
    #         wind_direction = "NNW"
    #     return wind_direction
    class DiscGolfPark:
        def __init__(self, name: str, messageID: str, coords: list, weather_info: dict):
            self.name = name
            self.messageID = messageID
            self.coords = coords
            self.weather_info = weather_info  

    def fetch_direction_with_degrees(self, degrees: int):
        for item in DIRECTION_DEGREES_TUPLE_LIST:
            if item[0] <= degrees < item[1]:
                return item[2]

    def fetch_emoji_with_icon_code(self, icon_code: str):
        for item in ICON_CODE_TUPLE_LIST:
            if item[0] == icon_code:
                return item[1]

    async def scan_channel_and_update_embeds(self):
        channels = bot.get_all_channels()
        for channel in channels:
            if channel.name == "course-info":
                pinned_messages = await channel.pins()
                for pinned_message in pinned_messages:
                    message = await channel.fetch_message(pinned_message.id)
                    message_match = re.search(
                        "\*\*([A-Za-z\s0-9]*)\*\*\s\(([0-9.,\s-]*)\)", message.content)
                    park_name = message_match.group(1)
                    coordinates_list = message_match.group(2).split(", ")
                    weather_info = self.weather_lat_long(
                        park_name, coordinates_list[0], coordinates_list[1])
                    park = self.DiscGolfPark(park_name, message.id, coordinates_list, weather_info)
                    await self.update_embed(message, park)

    async def update_embed(self, message: discord.Message, park: DiscGolfPark):
        embed = await self.build_embed(park)
        await message.edit(embed=embed)

    async def build_embed(self, park: DiscGolfPark):
        embed_dict = {
            "title": "Weather Details",
            "type": "rich",
            "color": 1009165,
            "description": ""
        }
        pass
        current_weather_icon = self.fetch_emoji_with_icon_code(
            park.weather_info["current"]["weather"][0]["icon"])
        pass
        current_wind_direction = self.fetch_direction_with_degrees(
            park.weather_info["current"]["wind_deg"])
        current_datetime = datetime.fromtimestamp(
            park.weather_info["current"]["dt"], tz=timezone(park.weather_info["timezone"]))
        # if current_datetime.minute < 30:
        #     start_of_hourly_info = 2
        # else:
        #     start_of_hourly_info = 3
        embed_dict["description"] = f"\
Weather: {current_weather_icon}\n\
Wind Direction: {current_wind_direction}\n\
Last Updated: {current_datetime}"
        return discord.Embed.from_dict(embed_dict)

        

        # iterating_hour_value = start_of_hourly_info
        # for hour in park.weather_info["hourly"]:
        #     if iterating_hour_value > start_of_hourly_info + 16:
        #         break
        #     if park.weather_info["hourly"].index(hour) == iterating_hour_value:
        #         hour_datetime = datetime.fromtimestamp(hour["dt"])

        #     iterating_hour_value += 2

        # hourly_dict = {
        #     ""
        # }

    def weather_lat_long(self, park_name, lat: str, lon: str):
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={WEATHER_TOKEN}&units=imperial')
        if not r.ok:
            # return
            raise Exception("ERROR: Could not fetch weather")
        data = r.json()
        with open('course_data.json', 'w') as outfile:
            json.dump(data, outfile)
        #########Only here during testing##########
        ###########################################
        with open('course_data.json', 'r') as infile:
            data = json.load(infile)
        ############################################
        return data


# weather_lat_long(33.044564, -96.691857)
bot.add_cog(WeatherUpdate())
bot.run(DISCORD_TOKEN)


                

                # 32.881046750179046, -96.69873166266753
#########Add Park Template#########
#                 await channel.send(content="**SHAWNEE PARK** (33.044564, -96.691857)\n\
# # ===============================\n\
# # Google Maps Link: https://goo.gl/maps/n7ThZ1CQeKvJvoDH6\n\
# # \n\
# # UDisc Link: https://app.udisc.com/applink/course/2307")

#                 await channel.send(content="**BB OWENS** (32.881046, -96.698731)\n\
# ===============================\n\
# Google Maps Link: https://goo.gl/maps/99TmQpQVixNcAn8U8\n\
# \n\
# UDisc Link: https://app.udisc.com/applink/course/2225")