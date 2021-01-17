import discord
from discord.ext import commands
from config import INVOCATION, GITHUB_REPO, MESSAGE_DICTIONARY_TEMPLATE
from dotenv import load_dotenv
from os import getenv
import pprint
import re
from disc_golf_park import DiscGolfPark



load_dotenv()
DISCORD_TOKEN = getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=INVOCATION)

@bot.event
async def on_ready():
    print("Connected!")
    git_status = discord.Game(GITHUB_REPO)
    await bot.change_presence(activity=git_status)

class PinScorecards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.channel.name == "scorecards":
            if len(message.attachments) > 0:
                match = re.search("\.(jpe?g|gif|png|tiff)$", message.attachments[0].filename)
                if not match is None:
                    await message.pin()
                    print(f"Pinned a message in scorecards.\n{message}")

async def fetch_park_by_emoji(emoji):
    channels = bot.get_all_channels()
    for channel in channels:
        if channel.name == "course-info":
            pinned_messages = await channel.pins()
            for pinned_message in pinned_messages:
                message = await channel.fetch_message(pinned_message.id)
                if message.reactions[0].emoji == emoji:
                    park = DiscGolfPark(message)
                    await park.fetch_weather_info()
                    await park.fetch_embed()
                    return park                    


@bot.command()
async def new_park(ctx, arg):
    if ctx.message.channel.name == "course-info":
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

        park_emoji = await ctx.guild.fetch_emoji(emoji_resp.content)

        for message in messsages_to_be_deleted:
            await message.delete()
        
        new_park_message = await ctx.send(content=str(dict(message_template)))
        await new_park_message.edit(suppress=True)
        await new_park_message.pin()


        await new_park_message.add_reaction(park_emoji)



async def fetch_context_from_payload(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    ctx = await bot.get_context(message)
    return ctx



@bot.listen()
async def on_raw_reaction_add(payload):
    ctx = await fetch_context_from_payload(payload)
    if not ctx.me.id == payload.user_id:
        error_occurred = False
        park_emoji = discord.Emoji
        try:
            park_emoji = await ctx.guild.fetch_emoji(payload.emoji.id)
        except:
            print(f"Couldn't fetch emoji, don't worry about it: {str(payload.emoji)}")
            error_occurred = True

        if not error_occurred and not park_emoji is None:
            park = await fetch_park_by_emoji(park_emoji)
            if not park is None:
                message = await payload.member.send(content=f"**{park.park_details['name']}**\n\
===============================\n\
Google Maps Link: {park.park_details['gmaps_url']}\n\
\n\
UDisc App Link: {park.park_details['udiscs_urls'][0]}\n\
\n\
UDisc Browser Link: {park.park_details['udiscs_urls'][1]}",embed=park.embed)
                await message.add_reaction(park_emoji)
                await message.add_reaction("🔄")
        elif payload.emoji.name == "🔄" and payload.guild_id == None:
            try:
                guild = await bot.fetch_guild(ctx.message.reactions[0].emoji.guild_id)
                park_emoji = await guild.fetch_emoji(ctx.message.reactions[0].emoji.id)
                        
                park = await fetch_park_by_emoji(park_emoji)

                if not park is None:
                    await ctx.message.edit(embed=park.embed)
            except Exception as ex:
                print(f"Couldn't fetch emoji, don't worry about it: {str(payload.emoji)}\n{ex}")

bot.add_cog(PinScorecards(bot))
bot.run(DISCORD_TOKEN)