import discord
import requests

temp_servers = {}


async def setloc(message, loc, open_weather_api_key):
    global temp_servers

    city_country = loc
    city, country = city_country.split(",")

    if len(country) <= 3:
        country = country.upper()
    else:
        country = country.title()

    city = city.title()
    city_country = city+","+country

    await message.send("Roger that! Trying to set the location.")
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(city_country, open_weather_api_key))

    if response.status_code == 200 or response.status_code == 301:
        temp_servers[message.guild.id] = city_country
        await message.send("Location set! {}".format(city_country))
    else:
        await message.send("Sorry! The location you tried to set doesn't exist.")


async def send_weather_info(message, open_weather_api_key):
    await message.send("Roger that! Trying to get weather info.")
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(temp_servers[message.guild.id], open_weather_api_key))
        if response.status_code == 200 or response.status_code == 301:
            json_response = response.json()

            title = json_response['weather'][0]['main']
            desc = json_response['weather'][0]['description']
            act_temp = json_response['main']['temp']
            feels_like = json_response['main']['feels_like']
            min_temp = json_response['main']['temp_min']
            max_temp = json_response['main']['temp_max']

            embed = discord.Embed(
                title="Weather", description="Location: " + temp_servers[message.guild.id].title())

            embed.add_field(name=title.title(),
                            value=desc.title(), inline=False)
            embed.add_field(name="Actual Temp",
                            value=str(act_temp)+"°C", inline=False)
            embed.add_field(name="Feels like",
                            value=str(feels_like)+"°C", inline=False)
            embed.add_field(name="Minimum Temp",
                            value=str(min_temp)+"°C", inline=False)
            embed.add_field(name="Maximum Temp",
                            value=str(max_temp)+"°C", inline=False)

            await message.send(content=None, embed=embed)

        else:
            await message.send("Sorry! An error occured.")
    except Exception as e:
        print(e)
        await message.send("A location is needed for getting weather info. Set it using the weatherLoc command.\nEx: `.weatherLoc london,england`")
