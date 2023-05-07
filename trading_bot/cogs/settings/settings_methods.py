from embed.embed_message import embed_settings_message
from embed.embed_confirmation import Confirmation
from webhook.create_webhook import create_webhook_, delete_webhook_
from ..inventory.add.sell_command import create_sell_app_command


async def channel_settings_modify_message(channel, db, ctx, test_view=None):
    channels_info = {
        "listing_channel": [
            "Listing Channel",
            "new listings are sent.",
            "Trading Listing",
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
    guild = db.guild_in_database(guild_id=ctx.guild.id)

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
            print(last_item_in_message)
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
    await delete_webhook_(
        ctx=ctx,
        webhook_name_to_delete=channels_info[channel][2],
        guild=guild,
    )
    db.delete_channel(
        guild_id=ctx.guild.id,
        channel_type=channel,
    )
    await ctx.send(f"✅ The {channel} was disabled.")


async def create_or_edit_webhook(
    channel, ctx, channel_id, channels_info, channel_link, db, guild
):
    await create_webhook_(
        ctx=ctx,
        channel_id=channel_id,
        new_webhook_name=channels_info[channel][2],
        guild=guild,
        channel_link=channel_link,
    )
    db.set_channel(
        guild_id=ctx.guild.id,
        channel_id=channel_id,
        channel_type=channel,
    )
    await ctx.send(f"✅ {channel_link} will now be used as the {channel}.")


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
        current_value = guild["item_properties"]
    except KeyError:
        current_value = "Not set yet."
    embed = embed_settings_message(
        msg_title=title,
        msg_desc=description,
        current_value_field=current_value,
        edit_field=f"`/settings item_properties - [paramater1:description1] - [paramater2:description2]`",
        accepted_value=(
            f"Paramater with it's description: \n `title:What is the title?` or `release:Release date?`.\n"
            "`:` is necessary to run this command. Between `parameter:description` there should be no whitespaces.\n"
            "`-` should be placed after `item_properties` keyword, and after every `parameter:description` pair\n"
            "If you set it like:\n"
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
        await item_properties_settings_embed_message(
            db=db,
            ctx=ctx,
            title_suffix="Modified",
            rgb_color=(102, 255, 51),
        )

        new_command = create_sell_app_command(
            ctx.bot, parameter_names, parameter_descriptions
        )
        guild_to_sync = ctx.guild
        ctx.bot.tree.add_command(new_command, guild=guild_to_sync)
        sync = await ctx.bot.tree.sync(guild=guild_to_sync)
    else:
        await item_properties_settings_embed_message(
            db=db,
            ctx=ctx,
            title_suffix="Settings",
            rgb_color=(255, 255, 0),
        )


async def role_can_embed_message(function, db, ctx, title_suffix, rgb_color):
    function_info = {
        "can_remove": ["Can Remove", "remove listing from database."],
        "can_search": ["Can Search", "search through listings in database."],
        "can_sell": [
            "Can Sell",
            "add new listings to database.",
        ],
    }
    guild = db.guild_in_database(guild_id=ctx.guild.id)
    title = function_info[function][0]
    description = f"Changes the role which can {function_info[function][1]}"
    if guild is not None:
        try:
            current_value = f"{guild[function]}"
        except KeyError:
            current_value = "Not set yet."
    embed = embed_settings_message(
        msg_title=f"{title} - {title_suffix}",
        msg_desc=description,
        current_value_field=current_value,
        edit_field=f"`/settings {function} [role]`",
        accepted_value=f"A role's name or `all`.",
        rgb_color=rgb_color,
    )
    await ctx.send(embed=embed)


async def role_can(ctx, db):
    message = ctx.message.content.split(" ")
    function = message[1]
    guild = db.guild_in_database(guild_id=ctx.guild.id)
    if len(message) == 3:
        role_assigned = message[-1]
        db.allow_role_to(
            guild_id=ctx.guild.id,
            function=function,
            role=role_assigned,
        )
        await role_can_embed_message(
            function=function,
            db=db,
            ctx=ctx,
            title_suffix="Modified",
            rgb_color=(255, 255, 0),  # yellow
        )
    else:
        await role_can_embed_message(
            function=function,
            db=db,
            ctx=ctx,
            title_suffix="Settings",
            rgb_color=(102, 255, 51),
        )
