import attrs
import requests

from .manager.image import ImageManager


@attrs.define
class Client:
    _session = requests.Session()

    _image_manager = ImageManager(_session)

    @property
    def images(self) -> ImageManager:
        return self._image_manager
