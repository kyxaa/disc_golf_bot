INVOCATION = "!"
DATETIME_STRING_FORMAT = "%m/%d/%y %H:%M %Z"
GITHUB_REPO = "https://github.com/kyxaa/disc_golf_bot"

# emojis for weather
SUNNY = ":sunny:"
FEW_CLOUDS = ":white_sun_snall_cloud:"
SCATTERED_CLOUDS = ":cloud:"
BROKEN_CLOUDS = ":white_sun_cloud:"
SHOWER_RAIN = ":white_sun_rain_cloud:"
RAIN = ":cloud_rain:"
THUNDERSTORM = ":thunder_cloud_rain:"
SNOW = ":cloud_snow:"
FOG = ":fog:"

# list for converting the Open Weather codes into the above emojis
ICON_CODE_TUPLE_LIST = [
    ("01d", SUNNY),
    ("02d", FEW_CLOUDS),
    ("03d", SCATTERED_CLOUDS),
    ("04d", BROKEN_CLOUDS),
    ("09d", SHOWER_RAIN),
    ("10d", RAIN),
    ("11d", THUNDERSTORM),
    ("13d", SNOW),
    ("50n", FOG)]

# list for converting degrees into directions
DIRECTION_DEGREES_TUPLE_LIST = [
    (348.75, 361, "N"),
    (0, 11.25, "N"),
    (11.25, 33.75, "NNE"),
    (33.75, 56.25, "NE"),
    (56.25, 78.75, "ENE"),
    (78.75, 101.25, "E"),
    (101.25, 123.75, "ESE"),
    (123.75, 146.25, "SE"),
    (146.25, 168.75, "SSE"),
    (168.75, 191.25, "S"),
    (191.25, 213.75, "SSW"),
    (213.75, 236.25, "SW"),
    (236.25, 258.75, "WSW"),
    (258.75, 281.25, "W"),
    (281.25, 303.75, "WNW"),
    (303.75, 326.25, "NW"),
    (326.25, 348.75, "NNW")
]
