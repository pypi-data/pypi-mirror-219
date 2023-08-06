import attrs
import requests

from ..model.image import Image
from ..model.enums.categories.sfw import SfwCategory


@attrs.define
class SfwManager:
    session: requests.Session

    def get(self, sfw_category: SfwCategory) -> Image:
        url = f"https://api.waifu.pics/sfw/{sfw_category.value}"
        response = self.session.get(url)

        image = Image(**response.json())

        return image
