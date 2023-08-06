"""Posting single reddit submission."""
# pylint: disable=duplicate-code
import argparse
import asyncio
import inspect
import logging
import sys

import aiohttp
import asyncpraw
import asyncprawcore
from imgurpython.helpers.error import ImgurClientError

from . import FATAL_TOOTBOT_ERROR
from . import USER_AGENT
from . import __display_name__
from . import __version__
from .collect import LinkedMediaHelper
from .collect import RedditHelper
from .collect import get_secrets
from .control import Configuration
from .publish import MastodonPublisher

logger = logging.getLogger(__display_name__)
logger.setLevel(logging.DEBUG)


async def toot_single_submission() -> None:
    """Post single reddit submission as status."""
    # pylint: disable-msg=too-many-locals
    # pylint: disable-msg=too-many-statements
    parser = argparse.ArgumentParser(description="Post toots from reddit posts.")
    parser.add_argument(
        "-c",
        "--config-dir",
        action="store",
        default=".",
        dest="config_dir",
        help="Name of directory containing configuration files to use",
    )
    parser.add_argument(
        "-l",
        "--debug-log-file",
        action="store",
        default="single-submission-debug.log",
        dest="debug_log_file",
        help="Path of filename to save DEBUG log messages to",
    )
    parser.add_argument(
        "-r",
        "--reddit-submission",
        action="store",
        dest="submission_id",
        help="ID of reddit submission / post",
    )
    args = parser.parse_args()
    config_dir = args.config_dir.rstrip("/")

    config: Configuration = await Configuration.load_config(
        config_dir=config_dir,
        debug_log=args.debug_log_file,
    )

    print(f"Welcome to {__display_name__} ({__version__})")
    logger.debug("Welcome to %s (%s)", __display_name__, __version__)

    try:
        secrets = await get_secrets(config_dir=config_dir)
    except ImgurClientError as imgur_error:
        logger.error("Error on creating ImgurClient: %s", imgur_error)
        logger.error(FATAL_TOOTBOT_ERROR)
        await config.bot.post_recorder.close_db()
        sys.exit(1)
    except asyncprawcore.AsyncPrawcoreException as reddit_exception:
        logger.error("Error while logging into Reddit: %s", reddit_exception)
        logger.error(FATAL_TOOTBOT_ERROR)
        await config.bot.post_recorder.close_db()
        sys.exit(1)

    secrets["mastodon"] = await MastodonPublisher.get_secrets(
        mastodon_domain=config.mastodon_config.domain,
        config_dir=config_dir,
    )

    async with aiohttp.ClientSession() as session:
        mastodon_publisher = await MastodonPublisher.initialise(
            config=config,
            session=session,
            secrets=secrets["mastodon"],
        )

        reddit = RedditHelper(config=config, api_secret=secrets["reddit"])

        try:
            media_helper = LinkedMediaHelper(
                imgur_secrets=secrets["imgur"],
            )
        except ImgurClientError as imgur_error:
            logger.error("Error on creating ImgurClient: %s", imgur_error)
            logger.error(FATAL_TOOTBOT_ERROR)
            await config.bot.post_recorder.close_db()
            sys.exit(1)

        reddit_con = asyncpraw.Reddit(
            user_agent=USER_AGENT,
            client_id=secrets["reddit"].client_id,
            client_secret=secrets["reddit"].client_secret,
        )

        submission = await reddit_con.submission(id=args.submission_id)
        logger.debug(
            "Single Submission retrieved: %s\n%s",
            args.submission_id,
            inspect.getmembers(submission),
        )
        reddit.posts = {submission.subreddit_name_prefixed: {submission.id: submission}}
        reddit.remove_posts_by_ignored_users()

        await mastodon_publisher.make_post(
            posts={submission.subreddit_name_prefixed: {submission.id: submission}},
            reddit_helper=reddit,
            media_helper=media_helper,
            duplicate_checks=False,
        )
        logger.debug("Single Submission posted successfully")

        await reddit_con.close()
        logger.debug("Reddit connection closed successfully")

        await config.bot.post_recorder.close_db()
        logger.debug("Sqlite connection closed successfully")

    logger.debug("aiohttp.Session closed successfully")


def start_debug_single_submission() -> None:
    """Post a single reddit submission for debug purposes.

    No duplicate checks will be performed before posting.
    """
    asyncio.run(toot_single_submission())
