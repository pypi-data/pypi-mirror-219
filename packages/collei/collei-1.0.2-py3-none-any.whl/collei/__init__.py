"""🍂 An unofficial Waifu.pics API wrapper for Python"""

# ruff: noqa: F401

from .client import Client
from .manager.nsfw import NsfwManager
from .manager.sfw import SfwManager
from .model.enums.categories.nsfw import NsfwCategory
from .model.enums.categories.sfw import SfwCategory
from .model.image import Image
