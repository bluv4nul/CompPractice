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
