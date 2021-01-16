import discord
from discord.ext import commands
from config import INVOCATION, GITHUB_REPO, MESSAGE_DICTIONARY_TEMPLATE
from dotenv import load_dotenv
from os import getenv
import pprint

# import json
# from bs4 import BeautifulSoup

# import asyncpg
from disc_golf_park import DiscGolfPark
# from disc_golf_park import DiscGolfParkMessageTemplate



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




# class ParkInformationFetching(commands.Cog):
#     def __init__(self):
#         self.bot = bot

#     async def fetch_park_by_emoji(self, emoji):
#         channels = bot.get_all_channels()
#         for channel in channels:
#             if channel.name == "course-info":
#                 # await emoji = 
#                 # park_template = DiscGolfParkMessageTemplate("BB Owens", ["32.881046", "-96.698731"], "https://goo.gl/maps/99TmQpQVixNcAn8U8", "https://app.udisc.com/applink/course/2225", "")
#                 pinned_messages = await channel.pins()
#                 for pinned_message in pinned_messages:
#                     if pinned_message.reaction[0] == emoji:


#                         message = await channel.fetch_message(pinned_message.id)
#                         park = DiscGolfPark(message)
#                         await park.fetch_weather_info()
#                     # pprint.pp(park.__dict__)
#                         await park.fetch_embed()
#                         return park
#                     else:
#                         return None
#                     # emoji = message.reactions[0].emoji
#                     # await message.clear_reactions()
#                     # await message.add_reaction(emoji)
#                     # pprint.pp(message.reactions[0].emoji)
#                     # pprint.pp(message)

async def fetch_park_by_emoji(emoji):
    channels = bot.get_all_channels()
    for channel in channels:
        if channel.name == "course-info":
            # await emoji = 
            # park_template = DiscGolfParkMessageTemplate("BB Owens", ["32.881046", "-96.698731"], "https://goo.gl/maps/99TmQpQVixNcAn8U8", "https://app.udisc.com/applink/course/2225", "")
            pinned_messages = await channel.pins()
            for pinned_message in pinned_messages:
                message = await channel.fetch_message(pinned_message.id)
                if message.reactions[0].emoji == emoji:
                    park = DiscGolfPark(message)
                    await park.fetch_weather_info()
                # pprint.pp(park.__dict__)
                    await park.fetch_embed()
                    return park                    

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
    
    udiscs_req = await ctx.send(content=f"What is the UDiscs link for {park_name} in the format *mobileLink* *browserLink*?")
    messsages_to_be_deleted.append(udiscs_req)
    udiscs_resp = await bot.wait_for('message', check=check)
    messsages_to_be_deleted.append(udiscs_resp)

    udiscs_urls = udiscs_resp.content.split(" ")

    coords_req = await ctx.send(content=f"What are the coordinates for {park_name} in the format *lattitude*,*longitude*?")
    messsages_to_be_deleted.append(coords_req)
    coords_resp = await bot.wait_for('message', check=check)
    messsages_to_be_deleted.append(coords_resp)

    park_coords_list = coords_resp.content.split(",")

    emoji_req = await ctx.send(content=f"What is the ID for the emoji you would like to use for {park_name}?")
    messsages_to_be_deleted.append(emoji_req)
    emoji_resp = await bot.wait_for('message', check=check)
    messsages_to_be_deleted.append(emoji_resp)
    park_details = [park_name, park_coords_list, gmaps_resp.content, udiscs_urls, emoji_resp.content]

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

async def fetch_context_from_payload(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    ctx = await bot.get_context(message)
    return ctx

@bot.listen()
async def on_raw_reaction_add(payload):
    ctx = await fetch_context_from_payload(payload)


    if not payload.member == ctx.me:
        error_occurred = False
        park_emoji = discord.Emoji
        try:
            park_emoji = await ctx.guild.fetch_emoji(payload.emoji.id)
        except:
            print("Emoji from another server, do nothing")
            error_occurred = True

        if not error_occurred:
            park = await fetch_park_by_emoji(park_emoji)
            if not park is None:
                message = await payload.member.send(content=f"**{park.park_details['name']}**\n\
===============================\n\
Google Maps Link: {park.park_details['gmaps_url']}\n\
\n\
UDisc App Link: {park.park_details['udiscs_urls'][0]}\n\
\n\
UDisc Browser Link: {park.park_details['udiscs_urls'][1]}",embed=park.embed)
                pass
            

        

        
        




# weather_lat_long(33.044564, -96.691857)
# bot.add_cog(ParkInformationFetching())
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

