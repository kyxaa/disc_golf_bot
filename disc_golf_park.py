from typing import Dict, OrderedDict
import discord
import requests
from datetime import datetime
import re
import json
from pytz import timezone
from dotenv import load_dotenv
from os import getenv
import pprint
import pandas
from config import DATETIME_STRING_FORMAT, ICON_CODE_TUPLE_LIST, DIRECTION_DEGREES_TUPLE_LIST

load_dotenv()
WEATHER_TOKEN = getenv('WEATHER_TOKEN')


class DiscGolfPark:
    def __init__(self, message: discord.Message):
        self.message = message
        updated_message_content = message.content.replace("\'", "\"")
        self.park_details = json.loads(updated_message_content)
        self.weather_info = {}

    async def fetch_weather_info(self):
        self.weather_info = self.weather_lat_long(
            self.park_details["coords"][0], self.park_details["coords"][1])

    async def fetch_embed(self):
        embed_dict = {
            "title": f"Weather Deatils for {self.park_details['name']}",
            "type": "rich",
            "color": 1009165,
            "description": ""
        }

        current_weather_icon = self.fetch_emoji_with_icon_code(
            self.weather_info["current"]["weather"][0]["icon"][:-1])

        current_temp = self.weather_info["current"]["temp"]

        current_wind_direction = self.fetch_direction_with_degrees(
            self.weather_info["current"]["wind_deg"])

        current_datetime = datetime.fromtimestamp(
            self.weather_info["current"]["dt"], tz=timezone(self.weather_info["timezone"]))
        current_datetime_str = current_datetime.strftime(DATETIME_STRING_FORMAT)

        current_visibility = self.weather_info["current"]["visibility"]

        # if current_datetime.minute < 30:
        #     start_of_hourly_info = 2
        # else:
        #     start_of_hourly_info = 3
        embed_dict["description"] = f"\
**CURRENT WEATHER**:\n\n\
**Weather**: {current_weather_icon}\n\
**Temperature**: {str(current_temp)} F ({str(round(((current_temp - 32) * 5 / 9),2))} C)\n\
**Wind Direction**: {current_wind_direction}\n\
**Visibility**: ~{int(current_visibility*1.09361)} yd (~{current_visibility} m)\n\n\
*Last Updated: {current_datetime_str}*"
        # await self.message.edit(embed=discord.Embed.from_dict(embed_dict))
        self.embed = discord.Embed.from_dict(embed_dict)
        # await self.message.channel.send(content="Joe's Mom is Hoe...This we Know",embed=discord.Embed.from_dict(embed_dict))

    def fetch_direction_with_degrees(self, degrees: int):
        for item in DIRECTION_DEGREES_TUPLE_LIST:
            if item[0] <= degrees < item[1]:
                return item[2]

    def fetch_emoji_with_icon_code(self, icon_code: str):
        for item in ICON_CODE_TUPLE_LIST:
            if item[0] == icon_code:
                return item[1]

    def weather_lat_long(self, lat: str, lon: str):
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={WEATHER_TOKEN}&units=imperial')
        if not r.ok:
            # return
            raise Exception("ERROR: Could not fetch weather")
        data = r.json()
        # with open('course_data.json', 'w') as outfile:
        #     json.dump(data, outfile)
        #########Only here during testing##########
        ###########################################
        # with open('course_data.json', 'r') as infile:
        #     data = json.load(infile)
        ############################################
        return data

# class DiscGolfParkMessageTemplate:
    # def __init__(self, message_dictionary_template):
    #     for key in message_dictionary_template: 
    #         setattr(self, key, message_dictionary_template[key]) 


    # def convert_from_dict(self,dict:dict):
