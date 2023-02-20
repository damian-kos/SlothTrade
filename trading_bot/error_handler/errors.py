from discord.ext import commands


async def handle_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        print(
            f"handle_command_error(): {error}"
            "You do not have permission to use this command. handle_command_error"
        )
        await ctx.send(
            "You do not have permission to use this command. handle_command_error"
        )
    else:
        print(f"handle_command_error_else(): An error occurred: {error}")
        await ctx.send(
            "An error occurred while processing your command. handle_command_error_else{error}"
        )


async def handle_error(ctx, error):
    print(f"An error occurred: {error}", commands.errors.CheckFailure)
    await ctx.send(
        f"handle_error(): An error occurred while processing your command. {error}"
    )
