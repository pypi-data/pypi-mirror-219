"""Helper classes and methods to assist with determining if a reddit post should be published on Mastodon."""
import configparser
import sys
from dataclasses import dataclass
from logging import DEBUG
from logging import Formatter
from logging import StreamHandler
from logging import getLogger
from logging.handlers import TimedRotatingFileHandler
from sqlite3 import OperationalError
from typing import Any
from typing import Final
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import aiosqlite
import arrow
from minimal_activitypub import __display_name__ as minimal_activitypub_logger

from . import POST_RECORDER_HISTORY_RETENTION_DAYS
from . import POST_RECORDER_SQLITE_DB
from . import __display_name__

PR = TypeVar("PR", bound="PostRecorder")
ConfigClass = TypeVar("ConfigClass", bound="Configuration")

logger = getLogger(__display_name__)


class PostRecorder:
    """Implements logging of reddit posts published to Mastodon and also
    checking against the log of published content to determine if a post would
    be a duplicate.
    """

    LAST_POST_TS: Final[str] = "last-post-timestamp"

    def __init__(self: PR, history_db_dir: str = ".") -> None:
        """Initialise PostRecord instance.

        :param history_db_dir: Location where history db should be stored. Default to current directory (.)
        """
        self.history_db_file = f"{history_db_dir.rstrip('/')}/{POST_RECORDER_SQLITE_DB}"
        self.history_db: Optional[aiosqlite.Connection] = None

    async def db_init(self: PR) -> None:
        """Initialise DB connection and tables if necessary."""
        self.history_db = await aiosqlite.connect(database=self.history_db_file)
        # Make sure DB tables exist
        await self.history_db.execute(
            "CREATE TABLE IF NOT EXISTS history (created_at FLOAT NOT NULL PRIMARY KEY, "
            "id TEXT, url TEXT, checksum TEXT)"
        )
        await self.history_db.execute(
            "CREATE TABLE IF NOT EXISTS settings "
            "(key TEXT PRIMARY KEY, value) "
            "WITHOUT ROWID"
        )

        # Create indexes
        await self.history_db.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS created_at_index ON history (created_at)"
        )
        await self.history_db.execute(
            "CREATE INDEX IF NOT EXISTS id_index ON history (id)"
        )
        await self.history_db.execute(
            "CREATE INDEX IF NOT EXISTS url_index ON history (url)"
        )
        await self.history_db.execute(
            "CREATE INDEX IF NOT EXISTS checksum_index ON history (checksum)"
        )

        # Create default entries
        await self.history_db.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (:key, :value)",
            {"key": PostRecorder.LAST_POST_TS, "value": 0},
        )

        await self.history_db.commit()

        # Migrate data from old tables to new table
        try:
            async with self.history_db.execute("SELECT id FROM post") as cursor:
                async for row in cursor:
                    now_ts = arrow.now(tz="UTC").timestamp()
                    await self.history_db.execute(
                        "INSERT INTO history (created_at, id) VALUES (:ts, :id)",
                        {"ts": now_ts, "id": row[0]},
                    )
            await self.history_db.execute("DROP TABLE post")
            await self.history_db.commit()
        except OperationalError:
            # Skipping this error as it probably means that the old table post doesn't exist anymore
            pass

        try:
            async with self.history_db.execute("SELECT url FROM share") as cursor:
                async for row in cursor:
                    now_ts = arrow.now(tz="UTC").timestamp()
                    await self.history_db.execute(
                        "INSERT INTO history (created_at, url) VALUES (:ts, :url)",
                        {"ts": now_ts, "url": row[0]},
                    )
            await self.history_db.execute("DROP TABLE share")
            await self.history_db.commit()
        except OperationalError:
            # Skipping this error as it probably means that the old table 'share' doesn't exist anymore
            pass

        try:
            async with self.history_db.execute("SELECT checksum FROM hash") as cursor:
                async for row in cursor:
                    now_ts = arrow.now(tz="UTC").timestamp()
                    await self.history_db.execute(
                        "INSERT INTO history (created_at, checksum) VALUES (:ts, :checksum)",
                        {"ts": now_ts, "checksum": row[0]},
                    )
            await self.history_db.execute("DROP TABLE hash")
            await self.history_db.commit()
        except OperationalError:
            # Skipping this error as it probably means that the old table 'hash' doesn't exist anymore
            pass

    async def duplicate_check(self: PR, identifier: str) -> bool:
        """Check identifier can be found in log file of content posted to
        Mastodon.

        :param identifier:
                Any identifier we want to make sure has not already been posted.
                This can be id of reddit post, url of media attachment file to be
                posted, or checksum of media attachment file.

        :returns:
                False if "identifier" is not in log of content already posted to
                Mastodon
                True if "identifier" has been found in log of content.
        """
        logger.debug("PostRecorder.duplicate_check(identifier=%s)", identifier)

        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        # check for reddit_id
        cursor = await self.history_db.execute(
            "SELECT * FROM history WHERE id=:id OR url=:url OR checksum=:checksum",
            {"id": identifier, "url": identifier, "checksum": identifier},
        )
        if await cursor.fetchone():
            logger.debug("PostRecorder.duplicate_check(...) -> True")
            return True

        logger.debug("PostRecorder.duplicate_check(...) -> False")
        return False

    async def log_post(
        self: PR,
        reddit_id: Optional[str] = None,
        shared_url: Optional[str] = None,
        check_sum: Optional[str] = None,
    ) -> None:
        """Log details about reddit posts that have been published.

        :param reddit_id:
                Id of post on reddit that was published to Mastodon
        :param shared_url:
                URL of media attachment that was shared on Mastodon
        :param check_sum:
                Checksum of media attachment that was shared on Mastodon.
                This enables checking for duplicate media even if file has been renamed.
        """
        logger.debug(
            "PostRecorder.log_post(reddit_id=%s ,shared_url= %s, checksum= %s)",
            reddit_id,
            shared_url,
            check_sum,
        )

        now_ts = arrow.now(tz="UTC").timestamp()
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        await self.history_db.execute(
            "INSERT INTO history (created_at, id, url, checksum) VALUES (:ts, :id, :url, :checksum)",
            {"ts": now_ts, "id": reddit_id, "url": shared_url, "checksum": check_sum},
        )
        await self.history_db.commit()

    async def get_setting(
        self: PR,
        key: str,
    ) -> Any:
        """Retrieve a setting from database.

        :param self: Post Recorded instance
        :param key: Key to setting stored in DB
        :type key: str

        :return: Value of setting. This could be an int, str, or float
        """
        logger.debug("PostRecorder.get_settings(key=%s)", key)
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        cursor = await self.history_db.execute(
            "SELECT value FROM settings WHERE key=:key", {"key": key}
        )
        row = await cursor.fetchone()
        if row is None:
            return None

        logger.debug("PostRecorder.get_settings(...) returns: %s", row[0])
        return row[0]

    async def save_setting(
        self: PR,
        key: str,
        value: Union[int, str, float],
    ) -> None:
        """Save a setting to database.

        :param self: Post Recorded instance
        :param key: Key to setting stored in DB
        :type key: str
        :param value: Value to store as a setting
        :type key: Union[int, str, float]

        :return: None
        """
        logger.debug("PostRecorder.save_settings(key=%s, value=%s)", key, value)
        if self.history_db is None:
            raise AssertionError("Have you called db_init() first?")

        await self.history_db.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (:key, :value)",
            {"key": key, "value": value},
        )

        await self.history_db.commit()

    async def close_db(self: PR) -> None:
        """Close db connection."""
        logger.debug("PostRecorder.close_db()")

        delete_earlier_than_ts = (
            arrow.now(tz="UTC")
            .shift(days=-POST_RECORDER_HISTORY_RETENTION_DAYS)
            .timestamp()
        )
        logger.debug(
            "PostRecorder.close_db() - removing history prior to TS=%s",
            delete_earlier_than_ts,
        )

        if self.history_db:
            await self.history_db.execute(
                "DELETE FROM history WHERE created_at < :ts",
                {"ts": delete_earlier_than_ts},
            )
            await self.history_db.commit()
            await self.history_db.close()


@dataclass
class Secret:
    """Dataclass for API login secrets."""

    client_id: Optional[str]
    client_secret: str


@dataclass
class BotConfig:
    """Dataclass holding configuration values for general behaviour of tootbot."""

    post_recorder: PostRecorder
    delay_between_posts: int
    run_once_only: bool
    hash_tags: List[str]
    log_level: str


@dataclass
class RedditReaderConfig:
    """Dataclass holding configuration values related to Reddit."""

    post_limit: int
    nsfw_allowed: bool
    nsfw_marked: bool
    spoilers: bool
    self_posts: bool
    stickied_allowed: bool


@dataclass
class PromoConfig:
    """Dataclass holding configuration values related to Promotional message settings."""

    every: int
    message: str


@dataclass
class HealthCheckConfig:
    """Dataclass holding configuration values around Healthchecks monitoring."""

    enabled: bool
    base_url: str
    uuid: str


@dataclass
class MediaConfig:
    """Dataclass holding configuration values around attached media."""

    folder: str
    media_only: bool


@dataclass
class MastodonConfig:
    """Dataclass holding configuration values for Mastodon settings.

    This also stores the number of times the mastodon API has returned
    an error to allow throttling of posting toots in a controlled manner
    """

    # pylint: disable=too-many-instance-attributes

    domain: str
    media_always_sensitive: bool
    post_visibility: str
    throttling_enabled: bool
    throttling_max_delay: int
    number_of_errors: int
    use_caption: bool
    use_tags: bool
    use_backlink: bool
    link_to_media: bool
    use_redditor_tag: bool


@dataclass
class SubredditConfig:
    """Dataclass to hold configuration settings about the subreddits to be monitored."""

    name: str
    tags: str


@dataclass
class Configuration:
    """Dataclass to hold all settings for tootbot."""

    # pylint: disable-msg=too-many-locals
    bot: BotConfig
    subreddits: List[SubredditConfig]
    promo: PromoConfig
    health: HealthCheckConfig
    media: MediaConfig
    mastodon_config: MastodonConfig
    reddit: RedditReaderConfig
    ignore_users_list: List[str]

    @classmethod
    async def load_config(
        cls: Type[ConfigClass],
        config_dir: str,
        debug_log: str,
    ) -> ConfigClass:
        """Load config parameters from user, as necessary.

        :param config_dir: directory to load config.ini file from.
        :param debug_log: full path including filename to save debug log messages to

        :returns:
        Configuration data class with config settings
        """
        if debug_log:
            file_log_formatter = Formatter(
                "%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s",
                datefmt="%H:%M:%S",
            )
            file_handler = TimedRotatingFileHandler(
                filename=debug_log,
                backupCount=7,
                when="midnight",
            )
            file_handler.setFormatter(file_log_formatter)
            file_handler.setLevel(DEBUG)
            logger.addHandler(file_handler)
            mal = getLogger(minimal_activitypub_logger)
            mal.setLevel(DEBUG)
            mal.addHandler(file_handler)

        # Make sure config file exists
        try:
            config = configparser.ConfigParser()
            # This next lines makes ConfigParser have case-sensitive settings keys which we need
            # for dealing with reddit usernames in the config
            config.optionxform = str  # type: ignore[method-assign, assignment]
            config.read(f"{config_dir}/config.ini")
        except configparser.Error as config_error:
            print("[ERROR] Error while reading config file: %s", config_error)
            sys.exit(1)

        await cls._set_up_logging(config)
        bot = await Configuration._load_bot_settings(
            config=config,
            config_dir=config_dir,
        )
        reddit = RedditReaderConfig(
            post_limit=int(config["BotSettings"]["PostLimit"]),
            nsfw_allowed=str_to_bool(config["BotSettings"]["NSFWPostsAllowed"]),
            nsfw_marked=str_to_bool(config["BotSettings"]["NSFWPostsMarked"]),
            spoilers=str_to_bool(config["BotSettings"]["SpoilersAllowed"]),
            self_posts=str_to_bool(config["BotSettings"]["SelfPostsAllowed"]),
            stickied_allowed=str_to_bool(config["BotSettings"]["StickiedPostsAllowed"]),
        )
        promo = PromoConfig(
            every=int(config["PromoSettings"]["PromoEvery"]),
            message=config["PromoSettings"]["PromoMessage"],
        )
        health = await Configuration._load_healthchecks_settings(config)
        media = MediaConfig(
            folder=config["MediaSettings"]["MediaFolder"],
            media_only=str_to_bool(config["MediaSettings"]["MediaPostsOnly"]),
        )
        mastodon_config = MastodonConfig(
            domain=config["Mastodon"]["InstanceDomain"],
            media_always_sensitive=str_to_bool(config["Mastodon"]["SensitiveMedia"]),
            post_visibility=config["Mastodon"].get("PostVisibility", "public"),
            throttling_enabled=str_to_bool(config["Mastodon"]["ThrottlingEnabled"]),
            throttling_max_delay=int(config["Mastodon"]["ThrottlingMaxDelay"]),
            number_of_errors=0,
            use_caption=config["Mastodon"].getboolean("UseCaption", fallback=True),
            use_tags=config["Mastodon"].getboolean("UseTags", fallback=True),
            use_backlink=config["Mastodon"].getboolean("UseBacklink", fallback=True),
            link_to_media=config["Mastodon"].getboolean("MediaLink", fallback=False),
            use_redditor_tag=config["Mastodon"].getboolean(
                "UseRedditorTag", fallback=False
            ),
        )
        subreddits = await Configuration._load_subreddits_settings(config)

        ignore_users_list = Configuration._load_ignore_users_list(config)

        configuration = cls(
            bot=bot,
            subreddits=subreddits,
            promo=promo,
            health=health,
            media=media,
            mastodon_config=mastodon_config,
            reddit=reddit,
            ignore_users_list=ignore_users_list,
        )
        logger.debug("After loading of config: %s", configuration)
        return configuration

    @staticmethod
    async def _load_subreddits_settings(
        config: configparser.ConfigParser,
    ) -> List[SubredditConfig]:
        """Load Subreddit configuration options."""
        subreddits = []
        for subreddit, hashtags in config.items("Subreddits"):
            subreddits.append(SubredditConfig(subreddit, hashtags.strip()))
        return subreddits

    @staticmethod
    def _load_ignore_users_list(
        config: configparser.ConfigParser,
    ) -> List[str]:
        """Load ignore_users_list."""
        ignore_users: List[str] = []

        if config.has_section("IgnoreUsersList"):
            for ignore_user, _ in config.items("IgnoreUsersList"):
                ignore_users.append(str(ignore_user))

        return ignore_users

    @staticmethod
    async def _load_healthchecks_settings(
        config: configparser.ConfigParser,
    ) -> HealthCheckConfig:
        """Load HealthChecks configuration options."""
        health_enabled = False
        if len(config["HealthChecks"]["BaseUrl"]) > 0:
            health_enabled = True
        health = HealthCheckConfig(
            enabled=health_enabled,
            base_url=config["HealthChecks"]["BaseUrl"],
            uuid=config["HealthChecks"]["UUID"],
        )
        return health

    @staticmethod
    async def _load_bot_settings(
        config: configparser.ConfigParser,
        config_dir: str,
    ) -> BotConfig:
        """Load BotSettings configuration options."""
        hash_tags = []
        if config["BotSettings"]["Hashtags"]:
            # Parse list of hashtags
            hash_tags_string = config["BotSettings"]["Hashtags"]
            hash_tags = [x.strip() for x in hash_tags_string.split(",")]
        bot = BotConfig(
            post_recorder=PostRecorder(history_db_dir=config_dir),
            delay_between_posts=int(config["BotSettings"]["DelayBetweenPosts"]),
            run_once_only=str_to_bool(config["BotSettings"]["RunOnceOnly"]),
            hash_tags=hash_tags,
            log_level=config["BotSettings"]["LogLevel"],
        )
        await bot.post_recorder.db_init()
        return bot

    @staticmethod
    async def _set_up_logging(config: configparser.ConfigParser) -> None:
        """Configure logging."""
        log_level = "INFO"
        if config["BotSettings"]["LogLevel"]:
            log_level = config["BotSettings"]["LogLevel"]

        std_out_formatter = Formatter(
            "%(name)s[%(process)d] %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
        )
        std_out_handler = StreamHandler(sys.stdout)
        std_out_handler.setFormatter(std_out_formatter)
        std_out_handler.setLevel(log_level)
        logger.addHandler(std_out_handler)


def str_to_bool(value: Any) -> bool:
    """Convert a string into a boolean value.

    returns: bool
    """
    if not value:
        return False
    return str(value).lower() in ("y", "yes", "t", "true", "on", "1")
