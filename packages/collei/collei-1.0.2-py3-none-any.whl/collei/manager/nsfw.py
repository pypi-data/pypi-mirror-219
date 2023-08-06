import attrs
import requests

from ..model.image import Image
from ..model.enums.categories.nsfw import NsfwCategory


@attrs.define
class NsfwManager:
    session: requests.Session

    def get(self, nsfw_category: NsfwCategory) -> Image:
        url = f"https://api.waifu.pics/nsfw/{nsfw_category.value}"
        response = self.session.get(url)

        image = Image(**response.json())

        return image
