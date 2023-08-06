from typing import Optional

from discord_logger import DiscordLogger

from sallron.util import settings


def send_message(
    message: str,
    level="error",
    title="Exception raised",
    description="",
    metadata: Optional[dict] = None,
):
    """
    Sends a message to a discord channel.

    Args:
        message (string): the message to be sent. Max length is 1000 (auto truncate).
        level (string): The level of the information being sent. Default is "error". Possibilities: error, warn, info, verbose, debug, success.
        title (string): Title of the message.
        description (string): Description of the message.
        metadata (dict): Metadata of the message.
    """
    webhook_url = settings.DISCORD_WEBHOOK

    options = {
        "application_name": "Sallron",
        "service_name": f"{settings.INTERFACE_NAME}",
        "service_environment": "Production",
        "default_level": "info",
    }

    logger = DiscordLogger(webhook_url=webhook_url, **options)

    if message and len(message) > 1000:
        message = message[-1000:]

    if level == "error":
        logger.construct(
            title=f"{title}",
            level=f"{level}",
            description=f"{description}",
            error=message,
            metadata=metadata,
        )
    else:
        logger.construct(
            title=f"{title}",
            level=f"{level}",
            description=f"{description}\n{message}",
            metadata=metadata,
        )

    logger.send()
