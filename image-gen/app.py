from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, StreamingResponse
from typing import Annotated, Optional
import io

from generator import image_generator

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/login")
async def login():
    return {"author": "1155288"}


@app.get("/makeimage")
async def makeimage_html():
    return FileResponse("makeimage.html")


@app.post("/makeimage")
async def makeimage_post(
    prompt: Annotated[str, Form()],
    image_width: Annotated[Optional[str], Form()] = None,
    image_height: Annotated[Optional[str], Form()] = None,
):
    try:
        if not image_width or not image_height:
            width_int = 1024
            height_int = 1024
        else:
            width_int = int(image_width)
            height_int = int(image_height)

        image = image_generator(prompt, width_int, height_int)

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        return StreamingResponse(img_byte_arr, media_type="image/png", status_code=202)

    except ValueError as e:
        return {"error": str(e)}
    except PermissionError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
