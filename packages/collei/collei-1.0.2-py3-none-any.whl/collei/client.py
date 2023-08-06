import attrs
import requests

from .manager.nsfw import NsfwManager
from .manager.sfw import SfwManager


@attrs.define
class Client:
    _session = requests.Session()

    _nsfw_manager = NsfwManager(_session)
    _sfw_manager = SfwManager(_session)

    @property
    def nsfw(self) -> NsfwManager:
        return self._nsfw_manager

    @property
    def sfw(self) -> SfwManager:
        return self._sfw_manager
