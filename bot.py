import discord
from discord import message
from discord.ext import tasks, commands
from config import INVOCATION, GITHUB_REPO, MESSAGE_DICTIONARY_TEMPLATE
from datetime import datetime
from dotenv import load_dotenv
from os import getenv
import pprint
import re
import sys
# import json
# from bs4 import BeautifulSoup
import asyncio
# import asyncpg
from disc_golf_park import DiscGolfPark
# from disc_golf_park import DiscGolfParkMessageTemplate

import requests

load_dotenv()
DISCORD_TOKEN = getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=INVOCATION)


# r = requests.get('https://udisc.com/courses/b-b-owen-dgc-yS7K')
# # if not r.ok:
# #     # return
# #     raise Exception("ERROR: Could not fetch weather")
# # json_data = r.json()
# # with open('udisc_site_data.json', 'w') as outfile:
# #     json.dump(json_data, outfile)
# soup = BeautifulSoup(r.content, 'html.parser')
# mydivs = soup.findAll('div', {"class": "jss464"})
# pass
# print(soup.prettify())

@bot.event
async def on_ready():
    print("Connected!")
    git_status = discord.Game(GITHUB_REPO)
    await bot.change_presence(activity=git_status)




class ParkWeatherUpdateCog(commands.Cog):
    def __init__(self):
        self.index = 0
        self.bot = bot
        self.update.start()

    def cog_unload(self):
        self.update.cancel()

    @tasks.loop(minutes=60.0)
    async def update(self):
        await self.scan_channel_and_update_embeds()
        pass

    @update.before_loop
    async def before_update(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    async def scan_channel_and_update_embeds(self):
        channels = bot.get_all_channels()
        for channel in channels:
            if channel.name == "course-info":
                # await emoji = 
                # park_template = DiscGolfParkMessageTemplate("BB Owens", ["32.881046", "-96.698731"], "https://goo.gl/maps/99TmQpQVixNcAn8U8", "https://app.udisc.com/applink/course/2225", "")
                pinned_messages = await channel.pins()
                for pinned_message in pinned_messages:
                    message = await channel.fetch_message(pinned_message.id)
                    park = DiscGolfPark(message)
                    await park.fetch_weather_info()
                    # pprint.pp(park.__dict__)
                    await park.update_embed()
                    # emoji = message.reactions[0].emoji
                    # await message.clear_reactions()
                    # await message.add_reaction(emoji)
                    # pprint.pp(message.reactions[0].emoji)
                    # pprint.pp(message)


@bot.command()
async def new_park(ctx, arg):
    messsages_to_be_deleted = [ctx.message]
    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author

    park_name = arg

    gmaps_req = await ctx.send(content=f"What is the Google Maps link for {park_name}?")
    messsages_to_be_deleted.append(gmaps_req)
    gmaps_resp = await bot.wait_for('message', check=check)
    messsages_to_be_deleted.append(gmaps_resp)
    
    udiscs_req = await ctx.send(content=f"What is the UDiscs link for {park_name}?")
    messsages_to_be_deleted.append(udiscs_req)
    udiscs_resp = await bot.wait_for('message', check=check)
    messsages_to_be_deleted.append(udiscs_resp)

    coords_req = await ctx.send(content=f"What are the coordinates for {park_name} in the format *lattitude*,*longitude*?")
    messsages_to_be_deleted.append(coords_req)
    coords_resp = await bot.wait_for('message', check=check)
    messsages_to_be_deleted.append(coords_resp)

    park_coords_list = coords_resp.content.split(",")

    emoji_req = await ctx.send(content=f"What is the ID for the emoji you would like to use for {park_name}?")
    messsages_to_be_deleted.append(emoji_req)
    emoji_resp = await bot.wait_for('message', check=check)
    messsages_to_be_deleted.append(emoji_resp)
    park_details = [park_name, park_coords_list, gmaps_resp.content, udiscs_resp.content, emoji_resp.content]

    message_template = MESSAGE_DICTIONARY_TEMPLATE
    for key,detail in zip(message_template,park_details):
        message_template[key] = detail

    pprint.pp(message_template)


    
    # park_message_template = DiscGolfParkMessageTemplate(message_template)
    # pprint.pp(park_message_template.__dict__)

    park_emoji = await ctx.guild.fetch_emoji(emoji_resp.content)

    for message in messsages_to_be_deleted:
        await message.delete()
    
    new_park_message = await ctx.send(content=str(dict(message_template)))
    await new_park_message.edit(suppress=True)
    await new_park_message.pin()


    await new_park_message.add_reaction(park_emoji)


    # desc_req = await ctx.send(content=f"What can you tell me about >>>{name_resp.content}<<<?")
    # desc_resp = await bot.wait_for('message', check=check)







# weather_lat_long(33.044564, -96.691857)
bot.add_cog(ParkWeatherUpdateCog())
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

#                 await channel.send(content="**TURNER PARK** (32.752835, -96.996896)\n\
# ===============================\n\
# Google Maps Link: https://goo.gl/maps/E7juCzz2mqftQLK29\n\
# \n\
# UDisc Link: https://app.udisc.com/applink/course/2557")

#                 await channel.send(content="**HARRY MYERS** (32.931592, -96.450927)\n\
# ===============================\n\
# Google Maps Link: https://goo.gl/maps/du4nscLcEXdjpvrY6\n\
# \n\
# UDisc Link: https://app.udisc.com/applink/course/2314")

#                 await channel.send(content="**PORTER PARK** (32.827703, -96.605390)\n\
# ===============================\n\
# Google Maps Link: https://goo.gl/maps/zZPYUP6axZwpvABBA\n\
# \n\
# UDisc Link: https://app.udisc.com/applink/course/2295")

#                 await channel.send(content="**AUBUDON PARK** (32.846327, -96.614739)\n\
# ===============================\n\
# Google Maps Link: https://goo.gl/maps/wyu7GWE8mnYSk7Tn8\n\
# \n\
# UDisc Link: https://app.udisc.com/applink/course/2240")

