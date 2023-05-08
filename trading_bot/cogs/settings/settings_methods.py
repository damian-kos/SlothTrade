from embed.embed_message import embed_settings_message
from embed.embed_confirmation import Confirmation
from webhook.create_webhook import (
    create_webhook_,
    delete_webhook_,
    channel_updated,
    channel_removed,
)
from webhook.webhook import guild_role_create_log
from ..inventory.add.sell_command import create_sell_app_command
from discord import Embed, Color
from datetime import datetime


async def channel_settings_modify_message(channel, db, ctx, test_view=None):
    guild = db.guild_in_database(guild_id=ctx.guild.id)
    system_channel = guild["guild_system_channel"]
    system_channel_id = (
        f"https://discord.com/channels/{ctx.guild.id}/{system_channel}"
    )
    channels_info = {
        "listing_channel": [
            "Listing Channel",
            "new listings are sent.",
            "Trading Listing",
        ],
        "remove_channel": [
            "Remove Channel",
            f"remove command works. This command will also work on {system_channel_id}.",
        ],
        "search_channel": [
            "Search Channel",
            "search results are sent.",
            "Trading Search",
        ],
        "sell_channel": [
            "Sell Channel",
            "you can post a new item. Once posted it will also be sent on a 'listing_channel'.",
            "Trading Selling",
        ],
        "logging": [
            "Logging Channel",
            "server log messages are sent.",
            "Trading Logging",
        ],
    }

    if test_view is not None:
        last_item_in_message = ctx.message.content.split(" ")[-1]
        if "disable" in last_item_in_message:
            message = f"Are you sure you want to disable the set {channel}?"
        else:
            channel_id = channel_to_set_id(last_item_in_message, ctx=ctx)
            if channel_id is None:
                await ctx.send(
                    f"❌ I couldn't find that channel, are you sure it exists?"
                )
                return
            channel_link = (
                f"https://discord.com/channels/{ctx.guild.id}/{channel_id}"
            )
            message = (
                f"Are you sure you want {channel_link} as the new {channel}?"
            )
        test_view.response = await ctx.send(
            content=message,
            view=test_view,
            delete_after=20,
        )
        await test_view.wait()
        if test_view.value:
            match last_item_in_message:
                case "disable":
                    await disable_webhook(
                        channel=channel,
                        ctx=ctx,
                        channels_info=channels_info,
                        db=db,
                        guild=guild,
                    )

                case other:
                    await create_or_edit_webhook(
                        channel=channel,
                        ctx=ctx,
                        channel_id=channel_id,
                        channels_info=channels_info,
                        channel_link=channel_link,
                        db=db,
                        guild=guild,
                    )

        else:
            print("No")
    else:
        if guild is not None:
            try:
                current_value = f"https://discord.com/channels/{ctx.guild.id}/{guild[channel]}"
            except KeyError:
                current_value = "Not set yet."
        title = f"{channels_info[channel][0]} - Settings"
        description = f"Changes the channel where {channels_info[channel][1]}"
        embed = embed_settings_message(
            msg_title=title,
            msg_desc=description,
            current_value_field=current_value,
            edit_field=f"`/settings {channel} [channel/disable]`",
            accepted_value=f"A channel's name or ID, or `disable`",
            rgb_color=(255, 255, 0),  # yellow,
        )
        await ctx.send(embed=embed)


async def disable_webhook(channel, ctx, channels_info, db, guild):
    if len(channels_info[channel]) == 3:
        await delete_webhook_(
            ctx=ctx,
            webhook_name_to_delete=channels_info[channel][2],
            guild=guild,
        )
    else:
        await channel_removed(
            guild=guild,
            channel=channels_info[channel][0],
            ctx=ctx,
        )
    db.delete_channel(
        guild_id=ctx.guild.id,
        channel_type=channel,
    )
    await ctx.send(f"✅ The {channel} is disabled.")


async def create_or_edit_webhook(
    channel, ctx, channel_id, channels_info, channel_link, db, guild
):

    if len(channels_info[channel]) == 3:
        await create_webhook_(
            ctx=ctx,
            channel_id=channel_id,
            new_webhook_name=channels_info[channel][2],
            guild=guild,
            channel_link=channel_link,
        )
    else:
        await channel_updated(
            guild=guild,
            channel=channels_info[channel][0],
            channel_link=channel_link,
            ctx=ctx,
        )

    await ctx.send(f"✅ {channel_link} will now be used as the {channel}.")
    db.set_channel(
        guild_id=ctx.guild.id,
        channel_id=channel_id,
        channel_type=channel,
    )


def channel_to_set_id(last_item_of_message, ctx):
    channel_to_set = last_item_of_message
    guild_channels_id = tuple(channel.id for channel in ctx.guild.channels)
    try:
        if channel_to_set.isdigit():
            if int(channel_to_set) in guild_channels_id:
                chosen_channel = int(channel_to_set)
        else:
            for channel in ctx.guild.channels:
                if str(channel) == channel_to_set:
                    chosen_channel = channel.id
                    break
        return chosen_channel
    except UnboundLocalError:
        return None


async def channel_settings(ctx, db):
    channel_to_modify = ctx.message.content.split(" ")[1]
    if len(ctx.message.content.split(" ")) == 3:
        await channel_settings_modify_message(
            channel=channel_to_modify,
            db=db,
            ctx=ctx,
            test_view=Confirmation(),
        )
        return
    await channel_settings_modify_message(
        channel=channel_to_modify,
        db=db,
        ctx=ctx,
    )


async def item_properties_settings_embed_message(
    db, ctx, title_suffix, rgb_color
):
    item_properties_info = {
        "item_properties": [
            "Item Properties",
            (
                "Changes the way your items are stored, "
                "be careful once you setup it you shouldn't change it later.\n "
                "Activates **/sell** command.\n"
                "If so, you need to delete all your items from database.\n"
                "Items will always be having an optional `price` paramater so you don't need to add this.\n"
            ),
        ],
    }
    title = f'{item_properties_info["item_properties"][0]} - {title_suffix}'
    description = item_properties_info["item_properties"][1]
    guild = db.guild_in_database(
        guild_id=ctx.guild.id
    )  # get refreshed collection within same command
    try:
        current_keys = guild["item_properties"]
        current_descriptions = guild["item_params_description"]
        current_value = "\n".join(
            f"`{k}:{v}`" for k, v in zip(current_keys, current_descriptions)
        )
    except KeyError:
        current_value = "Not set yet."
    embed = embed_settings_message(
        msg_title=title,
        msg_desc=description,
        current_value_field=current_value,
        edit_field=f"`/settings item_properties - [paramater1:description1] - [paramater2:description2]`",
        accepted_value=(
            f"Paramater with it's description: \n `title:What is the title?` or `release:Release date?`.\n"
            "\n`:` is necessary to run this command. Between `parameter:description` there should be no whitespaces.\n"
            "\n`-` should be placed after `item_properties` keyword, and after every `parameter:description` pair\n"
            "\nIf you set it like:\n"
            "`/settings item_properties - model:description - color:description`\n"
            "It will automatically add optional `price` paramater at the end.\n"
            "That means when user will be creating a new listing he may add a price or not.\n"
        ),
        rgb_color=rgb_color,  # yellow
    )

    await ctx.send(embed=embed)


async def define_item_properties(ctx, db):
    guild = db.guild_in_database(guild_id=ctx.guild.id)
    parameter_names = {}
    parameter_descriptions = {}
    item_properties = ctx.message.content.split("-")[1:]
    if item_properties != []:
        for count, item in enumerate(item_properties):
            parameter_name, param_description = item.strip().split(":")
            parameter_names[f"param{count}"] = parameter_name
            parameter_descriptions[f"param{count}"] = param_description
            item_properties_to_db = tuple(v for v in parameter_names.values())
            item_params_description_to_db = tuple(
                v for v in parameter_descriptions.values()
            )
        db.define_item_properties(
            guild_id=ctx.guild.id,
            item_properties_tuple=item_properties_to_db,
        )
        db.define_item_properties_descriptions(
            guild_id=ctx.guild.id,
            descriptions_tuple=item_params_description_to_db,
        )
        description = "\n".join(
            f"> `{item.strip()}`" for item in item_properties
        )
        confirmation_message = (
            f"> ‼️ You are about to change item_properties. ‼️\n"
            f"> ‼️ If still have listed items you will need to delete them.\n"
            f"> ‼️ This will also change your **/sell** command.\n"
            f"  {description}\n"
            f"> ‼️ Do you want to continue?"
        )
        confirmation_view = Confirmation()
        confirmation_view.response = await ctx.send(
            content=confirmation_message,
            view=confirmation_view,
            delete_after=20,
        )
        await confirmation_view.wait()
        if confirmation_view.value:
            try:
                logging_webhook_url = guild["logging_webhook"]
                embed = Embed(
                    title="Item properties and it's descpritions updated",
                    description=f"{description}\n You will receive separate message about **/sell** command activation.",
                    color=Color.from_rgb(88, 101, 242),
                    timestamp=datetime.now(),
                )
                embed.set_footer(
                    icon_url=ctx.author.avatar.url,
                    text=f"{ctx.author}",
                )
                await guild_role_create_log(
                    url=logging_webhook_url, embed_message=embed
                )
            except:
                await ctx.send("✅ /sell command updated and available.")

            guild_to_sync = ctx.guild
            sell_command = ctx.bot.tree.get_command("sell", guild=guild_to_sync)
            if sell_command:
                ctx.bot.tree.remove_command("sell", guild=guild_to_sync)
                await ctx.bot.tree.sync(guild=guild_to_sync)
            new_command = create_sell_app_command(
                ctx.bot, parameter_names, parameter_descriptions
            )
            ctx.bot.tree.add_command(new_command, guild=guild_to_sync)
            await ctx.bot.tree.sync(guild=guild_to_sync)
            embed = Embed(
                title="/sell command is active",
                description="Type `/sell` to use it",
                color=Color.from_rgb(88, 101, 242),
                timestamp=datetime.now(),
            )
            embed.set_footer(
                icon_url=ctx.author.avatar.url,
                text=f"{ctx.author}",
            )
            await guild_role_create_log(
                url=logging_webhook_url, embed_message=embed
            )
        else:
            return
    else:
        await item_properties_settings_embed_message(
            db=db,
            ctx=ctx,
            title_suffix="Settings",
            rgb_color=(255, 255, 0),
        )


async def role_can_embed_message(function, db, ctx, title_suffix, rgb_color):
    roles = {
        "can_remove": ["Can Remove", "remove listing from database."],
        "can_search": ["Can Search", "search through listings in database."],
        "can_sell": [
            "Can Sell",
            "add new listings to database.",
        ],
    }
    guild = db.guild_in_database(guild_id=ctx.guild.id)
    title = roles[function][0]
    description = f"Changes the role which can {roles[function][1]}"
    if guild is not None:
        try:
            current_value = f"{guild[function]}"
        except KeyError:
            current_value = "Not set yet."
    embed = embed_settings_message(
        msg_title=f"{title} - {title_suffix}",
        msg_desc=description,
        current_value_field=current_value,
        edit_field=f"`/settings {function} [role/everyone]`",
        accepted_value=f"A role's name or `everyone`.",
        rgb_color=rgb_color,
    )
    await ctx.send(embed=embed)


async def role_can(ctx, db):
    message = ctx.message.content.split(" ")
    function = message[1]
    guild = db.guild_in_database(guild_id=ctx.guild.id)
    if len(message) == 3:
        role_assigned = message[-1]
        if role_assigned == "everyone":
            confirmation_message = (
                f"Are you sure you want that `{role_assigned}` {function}?"
            )
        else:
            guild_roles = tuple(role.name for role in ctx.guild.roles)
            if role_assigned not in guild_roles:
                await ctx.send(
                    f"❌ I couldn't find that role, are you sure it exists."
                )
                return
            role_index = next(
                count
                for count, role in enumerate(ctx.guild.roles)
                if role.name == role_assigned
            )
            role = ctx.guild.roles[role_index]
            confirmation_message = (
                f"Are you sure you want that {role.mention} role {function}"
            )
        confirmation_view = Confirmation()
        confirmation_view.response = await ctx.send(
            content=confirmation_message,
            view=confirmation_view,
            delete_after=20,
        )
        await confirmation_view.wait()
        if confirmation_view.value:
            db.allow_role_to(
                guild_id=ctx.guild.id,
                function=function,
                role=role_assigned,
            )
            if role_assigned:
                await ctx.send(f"✅ The {role_assigned} from now {function}")
                description = f"{role_assigned} {function} from now on."
            else:
                await ctx.send(f"✅ The {role.mention} from now {function}")
                description = (
                    f"{role.mention} is changed to a role which {function}."
                )
            try:
                logging_webhook_url = guild["logging_webhook"]
                embed = Embed(
                    title=f"{function.capitalize()} role updated",
                    description=description,
                    color=Color.from_rgb(88, 101, 242),
                    timestamp=datetime.now(),
                )
                embed.set_footer(
                    icon_url=ctx.author.avatar.url,
                    text=f"{ctx.author}",
                )
                await guild_role_create_log(
                    url=logging_webhook_url,
                    embed_message=embed,
                )
            except:
                return
        else:
            return
    else:
        await role_can_embed_message(
            function=function,
            db=db,
            ctx=ctx,
            title_suffix="Settings",
            rgb_color=(102, 255, 51),
        )
