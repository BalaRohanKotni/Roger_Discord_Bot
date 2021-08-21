import discord


async def send_help_command(message, client):

    await message.send("Roger that! Getting help info.")

    help_embed = discord.Embed(title="Roger")

    help_embed.set_thumbnail(url=client.user.avatar_url)

    help_embed.add_field(
        name=".help", value="Get all commands and their usages of this bot.", inline=False)

    help_embed.add_field(name=".infoServer",
                         value=f'Get {message.guild.name} info.', inline=False)

    help_embed.add_field(
        name=".info user", value=f'Get user info\nExample: `.info @{client.user}`', inline=False)

    help_embed.add_field(name=".quote or .inspire",
                         value=f'Get a quote(from internet ofc).', inline=False)

    help_embed.add_field(name=".weather |or| .temp",
                         value="Get weather info/details. \n**Note**: For this command to work, You need to set the location for this command to work, for more info continue to read this embed.", inline=False)

    help_embed.add_field(
        name=".weatherLoc or .weatherLocation", value="Sets the location for getting the info of weather.\n**Note: The location should consist of city and country seperated only by comma(,).**\nEx: `.weatherLoc london,england`", inline=False)

    help_embed.add_field(
        name=".8ball", value="Ask the magic 8ball a question.\nExample: `.8ball Am I a lazy person`", inline=False)

    help_embed.add_field(
        name=".ping", value="Get the latency(speed) of the bot.", inline=False)

    help_embed.add_field(name=".guess |or| .guessnum",
                         value="Guess a number by checking if it's smaller or greater than your guess.", inline=False)

    help_embed.add_field(
        name=".tictactoe", value="Play tictactoe.", inline=False)

    help_embed.add_field(name=".support", value="Join the support server of the bot.", inline=False)

    help_embed.add_field(
        name="You can also use slash commands for this bot.", value='\u200b', inline=False)

    await message.send(content=None, embed=help_embed)
