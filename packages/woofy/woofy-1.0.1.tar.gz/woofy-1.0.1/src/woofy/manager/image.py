import typing

import attrs
import requests
import msgspec

from ..struct.image import Image


@attrs.define
class ImageManager:
    session: requests.Session

    def search(self) -> Image:
        url = "https://api.thedogapi.com/v1/images/search"
        response = self.session.get(url)

        content = response.content
        image = msgspec.json.decode(content, type=typing.Sequence[Image])

        return image
