"""Collection of classes and methods to perform the actual posting of content to Mastodon."""
import asyncio
import logging
import os
from dataclasses import dataclass
from typing import Any
from typing import AsyncIterator
from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar

import aiofiles
import aiohttp
from minimal_activitypub.client_2_server import ActivityPub
from minimal_activitypub.client_2_server import ActivityPubError
from tqdm.asyncio import tqdm

from . import CLIENT_WEBSITE
from . import USER_AGENT
from . import __display_name__
from .collect import Attachment
from .collect import LinkedMediaHelper
from .collect import RedditHelper
from .control import BotConfig
from .control import Configuration
from .control import MastodonConfig
from .control import PromoConfig
from .control import Secret

# pylint: disable=too-few-public-methods
# With two private methods it is still nice to have these in their own module


logger = logging.getLogger(__display_name__)

MP = TypeVar("MP", bound="MastodonPublisher")
FileManagerClass = TypeVar("FileManagerClass", bound="FileManager")

SECRETS_FILE = "mastodon.secret"


@dataclass
class MastodonPublisher:
    """Ease the publishing of content to Mastodon."""

    bot: BotConfig
    media_only: bool
    nsfw_marked: bool
    mastodon_config: MastodonConfig
    promo: PromoConfig
    instance: ActivityPub

    num_non_promo_posts: int = 0

    MAX_LEN_TOOT = 500

    @classmethod
    async def initialise(
        cls: Type[MP],
        config: Configuration,
        session: aiohttp.ClientSession,
        secrets: Secret,
    ) -> MP:
        """Initialise and returns a new MastodonPublisher class."""
        instance = ActivityPub(
            instance=config.mastodon_config.domain,
            access_token=secrets.client_secret.strip(),
            session=session,
        )
        await instance.determine_instance_type()

        user_info = await instance.verify_credentials()

        print(
            f"Successfully authenticated as "
            f"@{user_info['username']} on {config.mastodon_config.domain}"
        )
        logger.debug(
            "Successfully authenticated on %s as @%s",
            config.mastodon_config.domain,
            user_info["username"],
        )

        return cls(
            instance=instance,
            mastodon_config=config.mastodon_config,
            bot=config.bot,
            media_only=config.media.media_only,
            nsfw_marked=config.reddit.nsfw_marked,
            promo=config.promo,
        )

    @staticmethod
    async def get_secrets(mastodon_domain: str, config_dir: str) -> Secret:
        """Check that Mastodon API secrets are available. If not collects
        necessary info from user input the create and store APi secrets for
        Mastodon API secrets.

        :param mastodon_domain: domain name for Mastodon instance used for tooting. This
            is read from config.ini file, where it must be configured
        :type mastodon_domain: str
        :param config_dir: directory containing all the configuration files
        :type config_dir: str
        """
        mastodon_secrets = Secret(  # nosec B106
            client_id=None,
            client_secret="undefined",  # noqa: S106 - placeholder, not actually a 'password' or secret
        )

        secrets_file = f"{config_dir}/{SECRETS_FILE}"
        # Log into Mastodon if enabled in settings
        if not os.path.exists(secrets_file):
            # If the secret file doesn't exist,
            # it means the setup process hasn't happened yet
            print("Mastodon API keys not found. (See wiki for help).")

            async with aiohttp.ClientSession() as session:
                # Create app
                client_id, client_secret = await ActivityPub.create_app(
                    instance_url=mastodon_domain,
                    session=session,
                    client_website=CLIENT_WEBSITE,
                )

                # Get Authorization Code / URL
                authorization_request_url = (
                    await ActivityPub.generate_authorization_url(
                        instance_url=mastodon_domain,
                        client_id=client_id,
                        user_agent=USER_AGENT,
                    )
                )
                print(
                    f"Please go to the following URL and follow the instructions:\n"
                    f"{authorization_request_url}"
                )
                authorization_code = input("[...] Please enter the authorization code:")

                # Validate authorization code and get access token
                access_token = await ActivityPub.validate_authorization_code(
                    session=session,
                    instance_url=mastodon_domain,
                    authorization_code=authorization_code,
                    client_id=client_id,
                    client_secret=client_secret,
                )

                # Verify access token works
                mastodon = ActivityPub(
                    instance=mastodon_domain,
                    access_token=access_token,
                    session=session,
                )
                await mastodon.determine_instance_type()
                user_info = await mastodon.verify_credentials()
            mastodon_username = user_info["username"]
            print(
                f"Successfully authenticated on "
                f"{mastodon_domain} as @{mastodon_username}"
            )
            async with aiofiles.open(file=secrets_file, mode="w") as file:
                await file.write(access_token)
                await file.write("\n")
                await file.write(mastodon_domain)
                mastodon_secrets.client_secret = access_token
            print(f"Mastodon login information now stored in " f"{secrets_file} file")

        else:
            async with aiofiles.open(
                file=secrets_file,
                mode="r",
            ) as file:
                mastodon_secrets.client_secret = await file.readline()

        return mastodon_secrets

    async def make_post(  # noqa: C901 PLR0912
        self: MP,
        posts: Dict[Any, Any],
        reddit_helper: RedditHelper,
        media_helper: LinkedMediaHelper,
        duplicate_checks: bool = True,
    ) -> None:
        """Post status on mastodon from a selection of reddit submissions.

        :param posts: A dictionary of subreddit specific hashtags and PRAW Submission objects
        :type posts: Dict[Any, Any}
        :param reddit_helper: Helper class to work with Reddit
        :type reddit_helper: RedditHelper
        :param media_helper: Helper class to retrieve media linked to from a reddit Submission.
        :type media_helper: LinkedMediaHelper
        :param duplicate_checks: flag to determine if duplicate checks should be performed.
        :type duplicate_checks: bool
        """
        # pylint: disable=too-many-locals
        logger.debug(
            "MastodonPublisher.make_post(posts=%s, "
            "reddit_helper, "
            "media_helper, "
            "duplicate_checks=%s)",
            posts,
            duplicate_checks,
        )
        break_to_mainloop = False
        for additional_hashtags, source_posts in posts.items():
            if break_to_mainloop:
                break

            for post in source_posts:
                # Find out if we have any attachments to include with toot.
                logger.debug(
                    "MastodonPublisher.make_post - Getting attachments for post %s",
                    source_posts[post].id,
                )
                attachments = await media_helper.get_attachments(
                    reddit_post=source_posts[post]
                )
                if duplicate_checks:
                    attachments = await self._remove_posted_earlier(attachments)

                # Make sure the post contains media,
                # if MEDIA_POSTS_ONLY in config is set to True
                if self.media_only and len(attachments) == 0:
                    logger.warning(
                        "MastodonPublisher.make_post - "
                        "Skipping %s, non-media posts disabled or media file not found",
                        source_posts[post].id,
                    )
                    # Log the post anyway
                    if duplicate_checks:
                        await self.bot.post_recorder.log_post(
                            reddit_id=source_posts[post].id,
                        )
                        continue

                # Generate promo message if needed
                promo_message = None
                if self.num_non_promo_posts >= self.promo.every > 0:
                    promo_message = self.promo.message
                    self.num_non_promo_posts = -1

                # Generate post caption
                caption = reddit_helper.get_caption(
                    source_posts[post],
                    MastodonPublisher.MAX_LEN_TOOT,
                    add_hash_tags=additional_hashtags,
                    promo_message=promo_message,
                )

                try:
                    # Upload media files if available
                    media_ids = await self._post_attachments(
                        attachments=attachments,
                        duplicate_checks=duplicate_checks,
                    )
                    if self.media_only and len(media_ids) == 0:
                        # Skip posts where no media has been able to be uploaded
                        # and we've set media_only posts to True
                        continue

                    # Determine if spoiler is necessary
                    spoiler = None
                    if source_posts[post].over_18 and self.nsfw_marked:
                        spoiler = "NSFW"

                    logger.debug(
                        "MastodonPublisher.make_post"
                        " - self.mastodon_config.media_always_sensitive=%s",
                        self.mastodon_config.media_always_sensitive,
                    )
                    # Post to Mastodon
                    toot = await self.instance.post_status(
                        status=caption,
                        media_ids=media_ids,
                        visibility=self.mastodon_config.post_visibility,
                        sensitive=self.mastodon_config.media_always_sensitive,
                        spoiler_text=spoiler,
                    )
                    print(f'Posted to Mastodon: "{caption}" (at {toot["url"]})')
                    logger.debug("Posted to Mastodon: %s (at %s)", caption, toot["url"])

                    # Log the toot
                    if duplicate_checks:
                        await self.bot.post_recorder.log_post(
                            reddit_id=source_posts[post].id,
                            shared_url=source_posts[post].url,
                        )

                    self.num_non_promo_posts += 1
                    self.mastodon_config.number_of_errors = 0

                except ActivityPubError as error:
                    logger.error("Error while posting toot: %s", error)
                    # Log the post anyway, so we don't get into a loop of the
                    # same error
                    await self.bot.post_recorder.log_post(
                        reddit_id=source_posts[post].id
                    )
                    self.mastodon_config.number_of_errors += 1

                # Clean up media file
                for attachment in attachments:
                    del attachment
                del attachments

                # Return control to main loop
                break_to_mainloop = True
                break

    async def _post_attachments(
        self: MP,
        attachments: List[Attachment],
        duplicate_checks: bool,
    ) -> List[str]:
        """_post_attachments post any media in attachments.media_paths list.

        :param attachments: List of Attachment objects to be posted on Mastodon
        :param duplicate_checks: specifying if duplicate checks should be performed (True) or not (False)

        Returns
        -------
            media_ids: List of dicts returned by mastodon.media_post
        """
        media_ids: List[str] = []
        if len(attachments) == 0:
            return media_ids

        print("Uploading attachments")
        tasks: List[Any] = []

        for single_att in attachments:
            attachment = FileManager(temp_file=single_att.temp_file)
            tasks.append(
                self.instance.post_media(
                    file=attachment.file_reader(),
                    mime_type=single_att.mime_type,
                )
            )

            # Log the media upload
            if duplicate_checks:
                await self.bot.post_recorder.log_post(check_sum=single_att.checksum)
        try:
            medias = await asyncio.gather(*tasks)
            for media in medias:
                logger.debug("MastodonPublisher._post_attachments - result: %s", media)
                media_ids.append(media.get("id"))
        except (ActivityPubError, TypeError) as error:
            logger.debug(
                "MastodonPublisher._post_attachements - Error when uploading media: %s",
                error,
            )

        logger.debug("MastodonPublisher._post_attachments - media_ids: %s", media_ids)
        return media_ids

    async def _remove_posted_earlier(
        self: MP, attachments: List[Attachment]
    ) -> List[Attachment]:
        """_remove_posted_earlier checks che checksum of all proposed
        attachments and removes any from the list that have already been posted
        earlier.

        :param attachments: object with list of paths to media files proposed to be
            posted on Mastodon
        :type attachments: MediaAttachment
        """
        # Build a list of checksums for files that have already been posted earlier
        logger.debug(
            "MastodonPublisher._remove_posted_earlier(attachments=%s)", attachments
        )
        logger.debug(
            "MastodonPublisher._remove_posted_earlier(...) - number of attachements %s",
            len(attachments),
        )
        non_duplicates = []
        for attachment in attachments:
            if attachment.checksum and await self.bot.post_recorder.duplicate_check(
                attachment.checksum
            ):
                logger.debug(
                    "MastodonPublisher._remove_posted_earlier(...) - "
                    "Media with checksum %s has already been posted",
                    attachment.checksum,
                )
                del attachment
            else:
                non_duplicates.append(attachment)

        logger.debug(
            "MastodonPublisher._remove_posted_earlier(...) - number of attachements after check %s",
            len(non_duplicates),
        )

        return non_duplicates


class FileManager:
    """Class to wrap around file reads with a tqdm progress bar."""

    def __init__(
        self: FileManagerClass,
        temp_file: Any,
        chunk_size: int = 64 * 1024,
    ) -> None:
        """Initialise new FileManager instance.

        :param temp_file: file handle of TemporaryFile
        :param chunk_size: Size of chunks of data. Defaults to 64kb
        """
        self.temp_file = temp_file
        self.chunk_size = chunk_size
        self.size = os.path.getsize(temp_file.name)
        description = f"Attachment id {temp_file.name}"
        self.pbar = tqdm(
            total=os.path.getsize(filename=temp_file.name),
            desc=f"{description:.<60}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            ncols=120,
            leave=True,
        )

    async def file_reader(self: FileManagerClass) -> AsyncIterator[bytes]:
        """file_reader returns file contents in chunks of bytes and updates an
        associated progress bar.
        """
        # async with aiofiles.open(self.name, "rb") as file:
        self.temp_file.seek(0)
        chunk = self.temp_file.read(self.chunk_size)
        while chunk:
            self.pbar.update(len(chunk))
            yield chunk
            chunk = self.temp_file.read(self.chunk_size)
        self.pbar.close()
