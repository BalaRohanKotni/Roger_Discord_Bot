import discord
from datetime import datetime
import time


async def command_user_info(ctx, user, total_user_msg_servers, all_calculations, debugMode):
    if user == ():
        user = ctx.author
    else:
        user = user[0]

    if all_calculations and not debugMode:
        await send_user_info(ctx, user, total_user_msg_servers)
    else:
        if debugMode:
            await ctx.send("Sorry! This command is not available as the bot is in debug mode.")
            print("debug mode")


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(
        now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


async def send_server_info(message, client, total_user_msg_servers):
    await message.send("Roger that! Getting {} info ".format(message.guild))
    embed = discord.Embed(title=message.guild.name, description="")

    owner_id = message.guild.owner_id
    owner = message.guild.get_member(owner_id)

    total_user_msgs = 0

    for member in total_user_msg_servers[message.guild.id]:
        total_user_msgs += total_user_msg_servers[message.guild.id][member]

    embed.set_thumbnail(url=message.guild.icon_url)
    embed.add_field(name="Owner", value=owner.mention)
    embed.add_field(name="Total Members",
                    value=client.get_guild(message.guild.id).member_count, inline=False)
    embed.add_field(name="Total messages sent",
                    value=total_user_msgs, inline=False)

    li_roles = message.guild.roles
    roles = ""
    for i in li_roles:
        if str(i) != "@everyone":
            roles += str(i.mention)+", "
        else:
            roles += str(i)+", "

    if len(roles) > 1018:
        roles = roles[:1018] + " ..."

    embed.add_field(name="Roles[{}]".format(
        len(li_roles)), value=roles)
    await message.send(content=None, embed=embed)


async def send_user_info(message, user, total_user_msg_servers):
    await message.send("Roger that! Getting {} info ".format(user.mention))

    name = user.name
    nick = user.nick
    li_roles = user.roles
    total_messages = total_user_msg_servers[message.guild.id][user.id]

    roles = ""

    for i in li_roles:
        if str(i) != "@everyone":
            roles += str(i.mention)+", "
        else:
            roles += str(i)+", "

    if len(roles) > 1018:
        roles = roles[:1018] + " ..."

    embed = discord.Embed(
        title=name, description=str(user.mention))

    creation = datetime_from_utc_to_local(user.created_at)
    formatted_time = f"""{creation.strftime("%b")} {creation.strftime("%d")} {creation.strftime("%Y")} - {creation.strftime("%H")}:{creation.strftime("%M")} {creation.strftime("%Z")}"""

    embed.add_field(name="Joined Discord at",
                    value=str(formatted_time))
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Nickname", value=nick, inline=False)
    embed.add_field(name="Roles[{}]".format(
        len(li_roles)), value=roles, inline=False)
    embed.add_field(name="Total messages sent", value=total_messages)
    await message.send(content=None, embed=embed)
