import discord
import requests
from datetime import datetime
import re
from pytz import timezone
from dotenv import load_dotenv
from os import getenv
import pandas
from config import DATETIME_STRING_FORMAT, ICON_CODE_TUPLE_LIST, DIRECTION_DEGREES_TUPLE_LIST

load_dotenv()
WEATHER_TOKEN = getenv('WEATHER_TOKEN')


class DiscGolfPark:
    def __init__(self, message: discord.Message):
        self.message = message
        message_match = re.search(
            "\*\*([A-Za-z\s0-9]*)\*\*\s\(([0-9.,\s-]*)\)", self.message.content)
        self.name = message_match.group(1)
        self.coords = message_match.group(2).split(", ")
        self.weather_info = self.weather_lat_long(
            self.coords[0], self.coords[1])

    async def update_embed(self):
        embed_dict = {
            "title": f"Weather Deatils for {self.name}",
            "type": "rich",
            "color": 1009165,
            "description": ""
        }

        current_weather_icon = self.fetch_emoji_with_icon_code(
            self.weather_info["current"]["weather"][0]["icon"])

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
        await self.message.edit(embed=discord.Embed.from_dict(embed_dict))

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