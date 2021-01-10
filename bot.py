import discord
from discord import message
from discord.ext import tasks, commands
from config import INVOCATION, GITHUB_REPO
from datetime import datetime
from dotenv import load_dotenv
from os import getenv
import json
import asyncio
# import asyncpg
from disc_golf_park import DiscGolfPark

load_dotenv()
DISCORD_TOKEN = getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=INVOCATION)




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
                for pinned_message in pinned_messages:
                    message = await channel.fetch_message(pinned_message.id)
                    park = DiscGolfPark(message)
                    await park.update_embed()



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