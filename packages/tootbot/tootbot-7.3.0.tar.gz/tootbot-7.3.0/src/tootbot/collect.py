"""Helper classes and methods to assist with the collection of content to be posted to Mastodon."""
import asyncio
import configparser
import hashlib
import logging
import os
import re
import tempfile
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar
from urllib.parse import urlsplit

import aiofiles
import aiohttp
import arrow
import asyncpraw.exceptions
import asyncprawcore
import magic
import yt_dlp.utils
from asyncpraw.models import Redditor
from asyncpraw.models import Submission
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from imgurpython.helpers.error import ImgurClientRateLimitError
from tqdm import tqdm
from tqdm.asyncio import tqdm as aiotqdm

from . import PROGRESS_BAR_FORMAT
from . import USER_AGENT
from . import __display_name__
from .control import Configuration
from .control import Secret
from .control import SubredditConfig

logger = logging.getLogger(__display_name__)

RH = TypeVar("RH", bound="RedditHelper")
LMH = TypeVar("LMH", bound="LinkedMediaHelper")


@dataclass()
class Attachment:
    """Represents a media attachment. temp_file is a temporary file object containing media attachment content."""

    temp_file: Any
    mime_type: Optional[str]
    checksum: Optional[str]

    def __init__(self) -> None:
        """Create temporary file object to store the content of the media attachment."""
        self.temp_file = tempfile.TemporaryFile()
        self.checksum = None
        self.mime_type = None

    def __del__(self) -> None:
        """Close temporary file object when deleting attachment instance. This will also clean up the temporary file."""
        self.temp_file.close()


async def get_secrets(config_dir: str) -> Dict[str, Secret]:
    """Collect all api secrets either from already store secrets files or from user input.

    :param config_dir: directory to check read config.ini file from
    """
    secrets = {}
    secrets["reddit"] = await _get_reddit_secret(config_dir=config_dir)
    secrets["imgur"] = _get_imgur_secret(config_dir=config_dir)

    return secrets


async def _get_reddit_secret(config_dir: str) -> Secret:
    """Collect reddit secret from stored secrets file or from user input.

    :param config_dir: directory to check read config.ini file from
    """
    reddit_secrets_file = f"{config_dir}/reddit.secret"  # pragma: allowlist secret
    reddit_config = configparser.ConfigParser()
    if not os.path.exists(reddit_secrets_file):
        print("Reddit API keys not found. Please provide Reddit API values.")
        print("(See wiki if you need help).")
        # Whitespaces are stripped from input: https://stackoverflow.com/a/3739939
        reddit_agent = "".join(input("[ .. ] Enter Reddit agent: ").split())
        reddit_client_secret = "".join(
            input("[ .. ] Enter Reddit client secret: ").split()
        )
        # Make sure authentication is working
        # create Reddit api connection and load posts from announcements subreddit
        # to confirm reddit connection works
        reddit_client = asyncpraw.Reddit(
            user_agent="Tootbot",
            client_id=reddit_agent,
            client_secret=reddit_client_secret,
        )
        subreddit = await reddit_client.subreddit("announcements")
        async for _post in subreddit.hot():
            continue

        # It worked, so save the keys to a file
        reddit_config["Reddit"] = {
            "Agent": reddit_agent,
            "ClientSecret": reddit_client_secret,
        }
        with open(reddit_secrets_file, "w", encoding="utf8") as new_reddit_secrets:
            reddit_config.write(new_reddit_secrets)
    else:
        # Read API keys from secret file
        reddit_config.read(reddit_secrets_file)

    return Secret(
        client_id=reddit_config["Reddit"]["Agent"],
        client_secret=reddit_config["Reddit"]["ClientSecret"],
    )


def _get_imgur_secret(config_dir: str) -> Secret:
    """Check if the Imgur api secrets file exists.

    - If the file exists, this method reads the imgur secrets file and returns the
      secrets a Secret dataclass.
    - If the file doesn't exist it asks the user over stdin to supply these values
      and then saves them into the imgur_secrets file

    :param config_dir: directory to check read config.ini file from

    :returns:
        api_secrets (Secret): instance of Secret class containing the api secrets
        to work with imgur
    """
    secrets_file = f"{config_dir}/imgur.secret"  # pragma: allowlist secret
    if not os.path.exists(secrets_file):
        print("Imgur API keys not found. (See wiki if you need help).")

        # Whitespaces are stripped from input: https://stackoverflow.com/a/3739939
        imgur_client_id = "".join(input("[ .. ] Enter Imgur client ID: ").split())
        imgur_client_secret = "".join(
            input("[ .. ] Enter Imgur client secret: ").split()
        )
        # Make sure authentication is working
        imgur_client = ImgurClient(imgur_client_id, imgur_client_secret)

        # If this call doesn't work, it'll throw an ImgurClientError
        imgur_client.get_album("dqOyj")
        # It worked, so save the keys to a file
        imgur_config = configparser.ConfigParser()
        imgur_config["Imgur"] = {
            "ClientID": imgur_client_id,
            "ClientSecret": imgur_client_secret,
        }
        with open(secrets_file, "w", encoding="UTF-8") as file:
            imgur_config.write(file)
    else:
        # Read API keys from secret file
        imgur_config = configparser.ConfigParser()
        imgur_config.read(secrets_file)

    return Secret(
        client_id=imgur_config["Imgur"]["ClientID"],
        client_secret=imgur_config["Imgur"]["ClientSecret"],
    )


class RedditHelper:
    """RedditHelper provides methods to collect data / content from reddit to
    then post on Mastodon.
    """

    # Check if reddit access details in 'reddit.secret' file has already been set up
    # and load it, otherwise guide user through setting it up.
    def __init__(self: RH, config: Configuration, api_secret: Secret) -> None:
        """Initialise RedditHelper instance.

        :param config: Configuration settings
        :param api_secret: Secrets to use with reddit api
        """
        self.config = config
        self.posts: Dict[str, asyncpraw.models.Submission] = {}
        self.api_secret = api_secret

    async def get_all_reddit_posts(self: RH) -> None:
        """Collect posts from all configured subreddits."""
        tasks = []

        reddit_con = asyncpraw.Reddit(
            user_agent=USER_AGENT,
            client_id=self.api_secret.client_id,
            client_secret=self.api_secret.client_secret,
        )

        for subreddit in self.config.subreddits:
            tasks.append(self.get_reddit_posts(subreddit, reddit_con))
        progress_title = "Processing Subreddits"
        task_results = await aiotqdm.gather(
            *tasks,
            desc=f"{progress_title:.<60}",
            ncols=120,
            bar_format=PROGRESS_BAR_FORMAT,
            total=len(tasks),
        )

        for result in task_results:
            self.posts.update(result)

        await reddit_con.close()

    async def get_reddit_posts(
        self: RH,
        subreddit: SubredditConfig,
        reddit_con: asyncpraw.Reddit,
    ) -> Dict[str, Dict[str, asyncpraw.models.Submission]]:
        """Collect posts considered hot from configured sub/multi-reddits.

        :param subreddit: subreddits to check for posts to x-post
        :param reddit_con: API reference

        :returns:
        Dictionary with str of tags to use and subreddit posts
        """
        posts = {}
        logger.debug("Retrieving posts from %s", subreddit.name)
        try:
            subreddit_info = await reddit_con.subreddit(subreddit.name)
            subreddit_posts: Dict[str, asyncpraw.models.Submission] = {}
            async for submission in subreddit_info.hot(
                limit=self.config.reddit.post_limit
            ):
                subreddit_posts[submission.id] = submission
            posts[subreddit.tags] = subreddit_posts
        except asyncprawcore.AsyncPrawcoreException as reddit_error:
            logger.warning(
                "Error when getting reddit posts from r/%s: %s",
                subreddit.name,
                reddit_error,
            )
        return posts

    def remove_posts_by_ignored_users(self: RH) -> None:
        """Remove posts by users on the ignore list."""
        logger.debug("RedditHelper.remove_posts_by_ignored_users() started")
        logger.debug(
            "RedditHelper.remove_posts_by_ignored_users() - Ingore list is: %s",
            self.config.ignore_users_list,
        )
        # Guard against empty or undefined ignore users list
        if (
            self.config.ignore_users_list is None
            or len(self.config.ignore_users_list) == 0
        ):
            logger.debug(
                "RedditHelper.remove_posts_by_ignored_users() ignore list empty"
            )
            return

        title = "Remove posts by 'ingored users'"
        for posts in tqdm(
            self.posts.values(),
            desc=f"{title:.<60}",
            total=len(self.posts),
            ncols=120,
            bar_format=PROGRESS_BAR_FORMAT,
        ):
            post_ids = list(posts.keys())
            for id in post_ids:
                logger.debug(
                    "RedditHelper.remove_posts_by_ignored_users() - Checking post: %s from user: %s",
                    id,
                    posts[id].author.name,
                )
                if str(posts[id].author.name) in self.config.ignore_users_list:
                    del posts[id]
                    logger.debug("Removed post %s; post made by ignored user.", id)

    async def winnow_reddit_posts(self: RH) -> None:
        """Filter out reddit posts according to configuration and whether it has already been posted."""
        recorder = self.config.bot.post_recorder
        nsfw_allowed = self.config.reddit.nsfw_allowed
        self_posts_allowed = self.config.reddit.self_posts
        spoilers_allowed = self.config.reddit.spoilers
        stickied_allowed = self.config.reddit.stickied_allowed

        title = "Winnowing chaff "
        for posts in tqdm(
            self.posts.values(),
            desc=f"{title:.<60}",
            total=len(self.posts),
            ncols=120,
            bar_format=PROGRESS_BAR_FORMAT,
        ):
            post_ids = list(posts.keys())
            for post_id in post_ids:
                if posts[post_id].over_18 and not nsfw_allowed:
                    # Skip over NSFW posts if they are disabled in the config file
                    logger.debug("Skipping %s, it is marked as NSFW", post_id)
                    del posts[post_id]
                    continue

                if posts[post_id].is_self and not self_posts_allowed:
                    # Skip over NSFW posts if they are disabled in the config file
                    logger.debug("Skipping %s, it is a self post", post_id)
                    del posts[post_id]
                    continue

                if posts[post_id].spoiler and not spoilers_allowed:
                    # Skip over posts marked as spoilers if they are disabled in
                    # the config file
                    logger.debug("Skipping %s, it is marked as a spoiler", post_id)
                    del posts[post_id]
                    continue

                if posts[post_id].stickied and not stickied_allowed:
                    logger.debug("Skipping %s, it is stickied", post_id)
                    del posts[post_id]
                    continue

                if await recorder.duplicate_check(post_id):
                    logger.debug("Skipping %s, it has already been tooted", post_id)
                    del posts[post_id]
                    continue

                if await recorder.duplicate_check(posts[post_id].url):
                    logger.debug("Skipping %s, it has already been tooted", post_id)
                    del posts[post_id]
                    continue

    def get_caption(  # noqa C901
        self: RH,
        submission: Submission,
        max_len: int,
        add_hash_tags: Optional[str] = None,
        promo_message: Optional[str] = None,
    ) -> str:
        """get_caption returns the text to be posted to mastodon. This is
        determined from the text of the reddit submission, if a promo message
        should be included, and any hashtags.

        :param submission: PRAW Submission object for the reddit post we are
            determining the mastodon toot text for.
        :param max_len: The maximum length the text for the mastodon toot can be.
        :param add_hash_tags: additional hashtags to be added to global hashtags
            defined in config file. The hashtags must be comma delimited
        :param promo_message: Any promo message that must be added to end of caption.
            Set to None if no promo message to be added

        :returns:
        Caption to use in fediverse post
        """
        logger.debug(
            "RedditHelper.get_caption("
            "submission='%s', max_len=%s, add_hash_tags='%s', promo_message='%s')",
            submission.id,
            max_len,
            add_hash_tags,
            promo_message,
        )

        author_tag = ""
        if self.config.mastodon_config.use_redditor_tag:
            redditor: Redditor = submission.author
            # "-" breaks hashtags on Mastodon, so replace any "-" with "_"
            reddit_user = redditor.name.replace("-", "_")
            author_tag = f"posted by #u{reddit_user} "

        hashtags_for_post = self.config.bot.hash_tags

        # Workout hashtags for post
        hashtag_string = ""
        if add_hash_tags:
            hashtags_for_subreddit = [x.strip() for x in add_hash_tags.split(",")]
            hashtags_for_post = hashtags_for_subreddit + self.config.bot.hash_tags
        if hashtags_for_post:
            for tag in hashtags_for_post:
                # Add hashtag to string, followed by a space for the next one
                hashtag_string += f"#{tag} "

        promo_string = ""
        if promo_message:
            promo_string = f" \n \n{self.config.promo.message}"

        caption_max_length = max_len
        caption_max_length -= (
            len(submission.shortlink)
            + len(author_tag)
            + len(hashtag_string)
            + len(promo_string)
        )

        caption: str = ""
        # Create contents of the Mastodon post
        if len(submission.title) < caption_max_length:
            temp_caption = submission.title + " "
        else:
            temp_caption = submission.title[caption_max_length - 2] + "... "
        if self.config.mastodon_config.use_caption:
            caption += temp_caption
        caption += author_tag

        if self.config.mastodon_config.use_tags:
            caption += hashtag_string

        if self.config.mastodon_config.use_backlink:
            if self.config.mastodon_config.link_to_media:
                caption += submission.url
            else:
                caption += submission.shortlink
        caption += promo_string

        return caption


class LinkedMediaHelper:
    """Helper class providing methods to get media attachments."""

    def __init__(
        self: LMH,
        imgur_secrets: Secret,
    ) -> None:
        """Initialise LinkedMediaHelper instance.

        :param imgur_secrets: secrets to use with imgur api

        """
        self.imgur_client = None
        try:
            self.imgur_client = ImgurClient(
                client_id=imgur_secrets.client_id,
                client_secret=imgur_secrets.client_secret,
            )

            logger.debug(
                "Imgur rate limiting information: %s", self.imgur_client.credits
            )
            try:
                reset_epoch = int(self.imgur_client.credits.get("UserReset"))
            except (ValueError, TypeError):
                reset_epoch = None
            if reset_epoch:
                reset_at = arrow.get(reset_epoch).format("YYYY-MM-DD HH:mm:ss")
                reset_in = arrow.get(reset_epoch).humanize()
                logger.debug("Imgur rate limit resetting %s at %s", reset_in, reset_at)
        except ImgurClientRateLimitError as rate_limited:
            logger.error("Hit ratelimit at imgur: %s", rate_limited)

    async def get_attachments(
        self: LMH,
        reddit_post: Submission,
    ) -> List[Attachment]:
        """Determine which method to call depending on which site the media_url is pointing to.

        :returns:
        list of Attachment objects
        """
        attachments: List[Attachment] = []
        single_attachment = None
        multiple_attachments = None

        # Download and save the linked media
        if any(s in reddit_post.url for s in ("i.redd.it", "i.reddituploads.com")):
            single_attachment = await LinkedMediaHelper.get_reddit_image(
                reddit_post.url
            )

        elif "v.redd.it" in reddit_post.url and not reddit_post.media:
            logger.error(
                "Reddit API returned no media for this URL: %s",
                reddit_post.url,
            )
        elif "v.redd.it" in reddit_post.url:
            single_attachment = await self.get_reddit_video(reddit_post)

        elif "imgur.com" in reddit_post.url:
            multiple_attachments = await self.get_imgur_image(reddit_post.url)

        elif "giphy.com" in reddit_post.url:
            single_attachment = await LinkedMediaHelper.get_giphy_image(reddit_post.url)

        elif "reddit.com/gallery/" in reddit_post.url:  # Need to check for gallery post
            if hasattr(reddit_post, "is_gallery"):
                logger.debug("%s is a gallery post", reddit_post.id)
                multiple_attachments = await LinkedMediaHelper.get_reddit_gallery(
                    reddit_post
                )

        else:
            single_attachment = await LinkedMediaHelper.get_generic_image(
                reddit_post.url
            )

        if single_attachment:
            attachments.append(single_attachment)
        if multiple_attachments:
            attachments.extend(multiple_attachments)

        return attachments

    @staticmethod
    async def get_single_attachment(
        att_url: str,
        progress_label: str,
    ) -> Optional[Attachment]:
        """Download single attachment and store in an Attachment instance.
        Calculates a checksum for the content of this media.
        Determine mime/type.

        :param att_url: URL from which the media attachment should be collected
        :param progress_label: Label to use for progress bar

        :returns:
        Attachment instance or None
        """
        chunk_size = 64 * 1024

        attachment = Attachment()
        try:
            client = aiohttp.ClientSession(raise_for_status=True)
            meta = await client.head(url=att_url)
            download_size = int(meta.headers["content-length"])
            attachment.mime_type = str(meta.headers.get("content-type", None))
            sha256 = hashlib.sha256()

            progress_bar = tqdm(
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=f"{progress_label:.<60}",
                ncols=120,
                total=download_size,
                leave=True,
            )
            response = await client.get(url=att_url)
            async for data_chunk in response.content.iter_chunked(chunk_size):
                attachment.temp_file.write(data_chunk)
                sha256.update(data_chunk)
                progress_bar.update(len(data_chunk))

            await client.close()
            attachment.checksum = sha256.hexdigest()
            logger.debug(
                "collect.py - get_attachment(...) -> Attachment=%s", attachment
            )
            return attachment

        except aiohttp.ClientError as save_image_error:
            logger.error(
                "collect.py - get_attachment(...) -> None - download failed with: %s",
                save_image_error,
            )
            return None

    async def get_imgur_image(
        self: LMH,
        img_url: str,
        max_images: int = 4,
    ) -> List[Attachment]:
        """Download images from imgur.

        :param img_url: url of imgur image to download
        :param max_images: maximum number of images to download and process, Defaults to 4

        :returns:
        list of attachments, will be empty list if no attachments
        """
        attachments: List[Attachment] = []
        if not self.imgur_client:
            return attachments

        # Working demo of regex: https://regex101.com/r/G29uGl/2
        regex = r"(?:.*)imgur\.com(?:\/gallery\/|\/a\/|\/)(.*?)(?:\/.*|\.|$)"
        regex_match = re.search(regex, img_url, flags=0)

        if not regex_match:
            logger.error("Could not identify Imgur image/gallery ID at: %s", img_url)
            return []

        # Get the Imgur image/gallery ID
        imgur_id = regex_match.group(1)

        image_urls = self._get_image_urls(img_url, imgur_id)

        # Download and process individual images (up to max_images)
        for url in image_urls:
            image_url = url
            logger.debug("Downloading Imgur image at URL %s", image_url)

            attachment = await LinkedMediaHelper.get_single_attachment(
                att_url=image_url,
                progress_label="Downloading Imgur image",
            )

            if attachment:
                attachments.append(attachment)

            if len(attachments) == max_images:
                break

        return attachments

    def _get_image_urls(self: LMH, img_url: str, imgur_id: str) -> List[str]:
        """Build a list of urls of all Imgur images identified by imgur_id.

        :param img_url: URL to IMGUR post
        :param imgur_id: ID for IMGUR post

        :returns:
        imgur_urls: List of urls to images of Imgur post identified byr imgur_id
        """
        image_urls: List[str] = []
        if self.imgur_client is None:
            return image_urls

        try:
            if any(s in img_url for s in ("/a/", "/gallery/")):  # Gallery links
                logger.debug("Imgur link points to gallery: %s", img_url)
                images = self.imgur_client.get_album_images(imgur_id)
                for image in images:
                    image_urls.append(image.link)
            else:  # Single image
                imgur_img = self.imgur_client.get_image(imgur_id)
                image_urls = [imgur_img.link]  # pylint: disable=no-member

            logger.debug(
                "Imgur rate limiting information: %s", self.imgur_client.credits
            )
            try:
                reset_epoch = int(self.imgur_client.credits.get("UserReset"))
            except (ValueError, TypeError):
                reset_epoch = None
            if reset_epoch:
                reset_at = arrow.get(reset_epoch).format("YYYY-MM-DD HH:mm:ss")
                reset_in = arrow.get(reset_epoch).humanize()
                logger.debug("Imgur rate limit resetting %s at %s", reset_in, reset_at)

        except ImgurClientError as imgur_error:
            logger.error("Could not get information from imgur: %s", imgur_error)
        except ImgurClientRateLimitError as rate_limited:
            logger.error("Hit ratelimit at imgur: %s", rate_limited)
            logger.debug("Imgur Rate Limits: %s", self.imgur_client.credits)
        return image_urls

    @staticmethod
    async def get_reddit_image(img_url: str) -> Optional[Attachment]:
        """Download full resolution images from i.reddit or reddituploads.com.

        :param img_url: url of imgur image to download

        :returns:
        Attachment or None
        """
        os.path.basename(urlsplit(img_url).path)
        file_extension = os.path.splitext(img_url)[1].lower()
        # Fix for issue with i.reddituploads.com links not having a
        # file extension in the URL
        if not file_extension:
            img_url += ".jpg"

        logger.debug(
            "LinkedMediaHelper.get_reddit_image(img_url=%s)",
            img_url,
        )

        attachment = await LinkedMediaHelper.get_single_attachment(
            att_url=img_url, progress_label="Downloading reddit image"
        )

        return attachment

    @staticmethod
    async def get_reddit_gallery(
        reddit_post: Submission,
        max_images: int = 4,
    ) -> List[Attachment]:
        """Download up to max_images images from a reddit gallery post and returns a List of file_paths
        downloaded images.

        :param reddit_post:  reddit post / submission object
        :param max_images: [optional] maximum number of images to download. Default is 4

        :returns:
        attachments (List[Attachment]) a list of media attachments to be posted. Empty list if no attachments.
        """
        attachments: List[Attachment] = []
        if gallery_items := reddit_post.gallery_data.get("items"):
            tasks: List[Any] = []
            for item in gallery_items:
                media_id = item["media_id"]
                meta = reddit_post.media_metadata[media_id]
                logger.debug("Media Metadata: %s", meta)
                if "e" in meta and meta["e"] == "Image":
                    source = meta["s"]
                    tasks.append(
                        LinkedMediaHelper.get_single_attachment(
                            att_url=source["u"],
                            progress_label=f"image {len(tasks) + 1}",
                        ),
                    )

                    if len(tasks) == max_images:
                        break

            print("Downloading images from reddit gallery")
            attachments = await asyncio.gather(*tasks)

        return attachments

    @staticmethod
    async def get_reddit_video(reddit_post: Submission) -> Optional[Attachment]:
        """Download full resolution video from i.reddit or reddituploads.

        :param reddit_post: reddit post / submission object

        :returns:
        attachment or None
        """
        logger.debug(
            "LinkedMediaHelper.get_reddit_video(reddit_post = %s)",
            reddit_post.id,
        )
        logger.debug(
            "LinkedMediaHelper.get_reddit_video - reddit_post.media: \n%s)",
            reddit_post.media,
        )

        # Download video with yt-dlp
        yt_dlp_url = reddit_post.media["reddit_video"]["hls_url"]
        print(f"Downloading Reddit video from {yt_dlp_url}")

        attachment = await LinkedMediaHelper._get_video_with_yt_dlp(
            video_url=yt_dlp_url
        )
        return attachment

    @staticmethod
    async def _get_video_with_yt_dlp(video_url: str) -> Optional[Attachment]:
        """Download video files with embedded yt-dlp.

        :param video_url: URL for video to download

        :returns:
            (string) containing file name inclusive file extension and path where yt-dlp
                has saved the downloaded video.
                This can be None if yt-dlp has been unsuccessful.
        """
        logger.debug(
            "LinkedMediaHelper._get_video_with_yt_dlp(video_url=%s)",
            video_url,
        )
        yt_dlp_options = {
            "quiet": "true",
            "ignoreerrors": "true",
            "progress": "true",
            "format": "bestvideo+bestaudio",
        }

        with yt_dlp.YoutubeDL(yt_dlp_options) as ytdl:
            meta = ytdl.extract_info(video_url, download=True)
            meta_san = ytdl.sanitize_info(meta)

        # If there was an error with yt-dlp download meta will be None
        if not meta:
            logger.debug(
                "LinkedMediaHelper._get_video_with_yt_dlp - yt-dlp unsuccessful -> None"
            )
            return None

        yt_dlp_filepath: str = meta.get("filepath")
        if yt_dlp_filepath:
            logger.debug(
                "LinkedMediaHelper.get_reddit_video - yt-dlp DIRECT filepath: '%s'",
                yt_dlp_filepath,
            )
        else:
            yt_dlp_filepath = meta_san.get("requested_downloads")[0].get("filepath")
            logger.debug(
                "LinkedMediaHelper.get_reddit_video - yt-dlp 3 DEEP filepath: '%s'",
                yt_dlp_filepath,
            )
        logger.debug(
            "LinkedMediaHelper.get_reddit_video (...) -> '%s'", yt_dlp_filepath
        )

        # Spool downloaded file into a temporary file in an Attachment class instance
        attachment = await LinkedMediaHelper._attachment_from_file(
            filepath=yt_dlp_filepath
        )

        return attachment

    @staticmethod
    async def _attachment_from_file(filepath: str) -> Attachment:
        """Convert standard file to an Attachment instance.

        :param filepath: path to file to convert

        :returns:
        instance of Attachment
        """
        chunk_size = 64 * 1024

        attachment = Attachment()
        sha256 = hashlib.sha256()
        async with aiofiles.open(file=filepath, mode="rb") as input_file:
            while True:
                data_chunk = await input_file.read(chunk_size)
                if not data_chunk:
                    break
                attachment.temp_file.write(data_chunk)
                sha256.update(data_chunk)
        attachment.checksum = sha256.hexdigest()
        attachment.mime_type = magic.from_file(filename=filepath, mime=True)
        os.remove(filepath)

        return attachment

    @staticmethod
    async def get_giphy_image(img_url: str) -> Optional[Attachment]:
        """Download full or low resolution image from giphy.

        :param img_url: url of giphy image to download

        :returns:
        Attachment or None
        """
        # Working demo of regex: https://regex101.com/r/Cw6YJc/1
        regex = r"https?://((?:.*)giphy\.com/media/|giphy.com/gifs/|i.giphy.com/)(.*-)?(\w+)"
        match = re.match(pattern=regex, string=img_url, flags=0)
        if not match:
            logger.error("Could not identify Giphy ID in this URL: %s", img_url)
            return None

        # Get the Giphy ID
        giphy_id = match.group(3)
        # Download the MP4 version of the GIF
        giphy_url = "https://media.giphy.com/media/" + giphy_id + "/giphy.mp4"

        attachment = await LinkedMediaHelper.get_single_attachment(
            att_url=giphy_url,
            progress_label="Downloading Giphy image/video",
        )

        logger.debug("Downloaded Giphy from URL %s", giphy_url)

        return attachment

    @staticmethod
    async def get_generic_image(img_url: str) -> Optional[Attachment]:
        """Download image or video from a generic url to a media file.

        :param img_url: url to image or video file

        :returns:
        attachment: media attachment
        """
        logger.debug("LinkedMediaHelper.get_generic_image(img_url=%s)", img_url)

        # First check if URL starts with http:// or https://
        regex = r"^https?://"
        match = re.search(regex, img_url, flags=0)
        if not match:
            logger.debug("Post link is not a full link: %s", img_url)
            return None

        # Check if URL is an image or MP4 file, based on the MIME type
        image_formats = (
            "image/png",
            "image/jpeg",
            "image/gif",
            "image/webp",
            "video/mp4",
        )

        try:
            async with aiohttp.ClientSession(
                raise_for_status=True,
                read_timeout=30,
            ) as client:
                response = await client.head(url=img_url)
                headers = response.headers
                content_type = headers.get("content-type", None)

        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError) as error:
            logger.error("Error while opening URL: %s ", error)
            return None

        if content_type not in image_formats:
            logger.debug("URL does not point to a valid image file: %s", img_url)
            return None

        # URL appears to be an image, so download it
        logger.debug("Downloading file at URL %s", img_url)

        attachment = await LinkedMediaHelper.get_single_attachment(
            att_url=img_url,
            progress_label="Downloading generic image",
        )

        return attachment
