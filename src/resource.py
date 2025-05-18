from requests import get
from PIL import Image
from io import BytesIO


def get_content_from_url(url: str) -> bytes: return get(url).content


def get_image_from_url(url: str) -> Image: return Image.open(BytesIO(get_content_from_url(url)))


