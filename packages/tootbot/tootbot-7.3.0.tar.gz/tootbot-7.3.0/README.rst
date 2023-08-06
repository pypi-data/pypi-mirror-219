Tootbot
=======

|Repo| |CI - Woodpecker| |Downloads|

|Checked against| |Checked with| |Interrogate|

|Code style| |PyPI - Python Version| |PyPI - Wheel|

|GPL|


This is a Python bot that looks up posts from specified subreddits and automatically posts them on `Mastodon`_.
It is based on `reddit-twitter-bot`_.

Features:
---------

* Tootbot posts to `Mastodon`_
* Media from direct links, Gfycat, Imgur, Reddit, and Giphy is automatically attached in the social media post.
  Tootbot attaches up to the first 4 pictures for imgur albums and reddit gallery posts.
* Links that do not contain media can be skipped, ideal for meme accounts like `@babyelephantgifs`_
* NSFW content, spoilers, and self-posts can be filtered
* Tootbot can monitor multiple subreddits at once
* Tootbot is fully open-source, so you don't have to give an external service full access to your social media accounts
* Tootbot also checks the sha256 checksum of media files to stop posting of the same media file from different subreddits.
* Tootbot can ping a `Healthchecks`_ instance for monitoring continuous operation of Tootbot
* Optionally throttle down frequency of tooting when mastodon errors are detected.

**!!! Tootbot no longer supports posting to Twitter. !!!**

If you need twitter functionality look into `reddit-twitter-bot`_ as a possible alternative.

**!!! Tootbot no longer supports deleting old toots. !!!**

If you'd like to delete older toots from your Mastodon account look into `MastodonAmnesia`_ as a tool that might
work for you.

Disclaimer
----------

The developers of Tootbot hold no liability for what you do with this script or what happens to you by using this
script. Abusing this script *can* get you banned from Mastodon, so make sure to read up on proper usage of the API
for each site.

Setup and usage
---------------

For instructions on setting up and using Tootbot, please visit `the wiki`_

Supporting Tootbot
------------------

There are a number of ways you can support Tootbot:

- Create an issue with problems or ideas you have with/for Tootboot
- You can `buy me a coffee`_.
- You can send me small change in Monero to the address below:

Monero donation address:
`87C65WhSDMhg4GfCBoiy861XTB6DL2MwHT3SWudhjR3LMeGEJG8zeZZ9y4Exrtx5ihavXyfSEschtH4JqHFQS2k1Hmn2Lkt`

Changelog
---------

See the `Changelog`_ for any changes introduced with each version.

License
-------

Tootbot is licences under the `GNU General Public License v3.0`_



.. _Mastodon: https://joinmastodon.org/
.. _reddit-twitter-bot: https://github.com/rhiever/reddit-twitter-bot
.. _MastodonAmnesia: https://pypi.org/project/mastodonamnesia/
.. _@babyelephantgifs: https://botsin.space/@babyelephantgifs
.. _Healthchecks: https://healthchecks.io/
.. _the wiki: https://codeberg.org/MarvinsMastodonTools/tootbot/wiki
.. _buy me a coffee: https://www.buymeacoffee.com/marvin8
.. _GNU General Public License v3.0: http://www.gnu.org/licenses/agpl-3.0.html
.. _Changelog: https://codeberg.org/MarvinsMastodonTools/tootbot/src/branch/main/CHANGELOG.rst

.. |GPL| image:: https://www.gnu.org/graphics/gplv3-with-text-136x68.png
    :alt: GPL3
    :target: https://codeberg.org/MarvinsMastodonTools/tootbot/src/branch/main/license.txt

.. |Repo| image:: https://img.shields.io/badge/repo-Codeberg.org-blue
    :alt: Repo at Codeberg
    :target: https://codeberg.org/MarvinsMastodonTools/tootbot

.. |Downloads| image:: https://pepy.tech/badge/tootbot
    :target: https://pepy.tech/project/tootbot

.. |Code style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code Style: Black
    :target: https://github.com/psf/black

.. |Checked against| image:: https://img.shields.io/badge/Safety--DB-Checked-green
    :alt: Checked against Safety DB
    :target: https://pyup.io/safety/

.. |Checked with| image:: https://img.shields.io/badge/pip--audit-Checked-green
    :alt: Checked with pip-audit
    :target: https://pypi.org/project/pip-audit/

.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/tootbot

.. |PyPI - Wheel| image:: https://img.shields.io/pypi/wheel/tootbot

.. |CI - Woodpecker| image:: https://ci.codeberg.org/api/badges/MarvinsMastodonTools/tootbot/status.svg
    :target: https://ci.codeberg.org/MarvinsMastodonTools/tootbot

.. |Interrogate| image:: https://codeberg.org/MarvinsMastodonTools/tootbot/raw/branch/main/interrogate_badge.svg
    :alt: Doc-string coverage
    :target: https://interrogate.readthedocs.io/en/latest/
