from discord.ext import commands
import logging
import logging.handlers
import datetime
from pathlib import Path
import os


log_filename = datetime.datetime.now().strftime("discord_%Y-%m-%d.log")
log_dir = Path(__file__).parent / "logs"
log_path = os.path.join(log_dir, log_filename)
handler = logging.handlers.TimedRotatingFileHandler(
    log_path, when="midnight", backupCount=7, encoding="utf-8"
)

logger = logging.getLogger("discord")
logger.setLevel(logging.ERROR)
# handler = logging.FileHandler(
#     filename="discord.log", encoding="utf-8", mode="w"
# )
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


async def handle_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        error_msg = "You do not have permission to use this command."
        logger.error(
            f"handle_command_error(): {error}, {ctx.message.content},  {ctx.guild.id}: {ctx.guild.name}"
        )

    else:
        error_msg = "An command error occurred while processing your request."
        logger.error(
            f"handle_command_error_else(): {error}, {ctx.message.content},  {ctx.guild.id}: {ctx.guild.name}"
        )


async def handle_error(ctx, error):
    logger.error(
        f"handle_error(): {error}, {ctx.message.content}\n, {ctx.guild.id}: {ctx.guild.name}"
    )
