from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import shutil
import os

from fabric_service import analyze_image

app = FastAPI()

templates = Jinja2Templates(
    directory="templates"
)


# ---------------------------------
# Home Page
# ---------------------------------
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# ---------------------------------
# Analyze Image
# ---------------------------------
@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    file: UploadFile = File(...)
):

    os.makedirs(
        "images",
        exist_ok=True
    )

    image_path = os.path.join(
        "images",
        file.filename
    )

    with open(
        image_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = analyze_image(
        image_path
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "result": result,
            "image_name": file.filename
        }
    ) 