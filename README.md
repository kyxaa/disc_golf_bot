# disc_golf_bot

Disc_golf_bot is a Discord bot that provides information about local disc golf courses when the user reacts with a specific emoji that is associated to a disc golf course.

## Motivation

I manage a disc golf Discord server for some friends. There are a handful of courses that we visit. Being able to easily pull up information about course via where we already plan our sessions seemed like a no-brainer.

## Bot Usage

If someone is on the server, they will see that there are custome emojis on the channel that line up with the names of disc golf courses. If they react to a message on the server, the bot will send them a direct message that looks like this:

![Bot Response](/images/disc_golf_bot_response.png)

In addition, if a user posts an image file to a channel of the specific "scorecards" the image will be automatically pinned to the channel.

## How Does It Work?

The bot is written in Python and utilizes the [Discord.py](https://discordpy.readthedocs.io/en/latest/index.html) library. The data for each of the disc golf courses is kept in a channel on the server:

![Data](/images/disc_golf_bot_data.png)

When a user reacts to a message on the server, the bot checks to see if it is a server specific emoji and if it is it loops through the messages on this channel until it finds the right park. The bot then parses out the JSON object that I have as the message's content.

The bot will then reach out to the [OpenWeather API](https://openweathermap.org/api) with the coordinates of the park in order to fetch the weather information.

## Support

As this isn't a public bot, I don't have a support structure in place, but if you have any questions about the bot, please feel free to open an issue and I'll get to it as soon as I can.