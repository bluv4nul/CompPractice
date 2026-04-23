import os

from PIL import Image
from huggingface_hub import InferenceClient
from dotenv import load_dotenv


def image_generator(
    prompt: str,
    width: int,
    height: int,
):

    load_dotenv()

    HF_TOKEN = os.environ.get("HF_TOKEN")

    if HF_TOKEN:
        if width % 1 != 0 and height % 1 != 0:
            raise ValueError("Invalid image size")

        if width % 32 != 0 or height % 32 != 0:
            raise ValueError("Width and height must be multiples of 32")

        if width < 32 or height < 32 or width > 1024 or height > 1024:
            raise ValueError("Height and width must be [32;1024]")

        client = InferenceClient(token=HF_TOKEN)

        image = client.text_to_image(
            prompt=prompt,
            width=width,
            height=height,
            model="black-forest-labs/FLUX.1-schnell",
        )

        return image

    else:
        raise PermissionError("Token nod found/Invalid token")
