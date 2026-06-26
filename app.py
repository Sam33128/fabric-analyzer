from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from convex_service import save_analysis
import os
import shutil

from fabric_service import analyze_image
from analytics import track

app = FastAPI()

# ---------------------------------
# Static Files
# ---------------------------------
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.mount(
    "/images",
    StaticFiles(directory="images"),
    name="images"
)

# ---------------------------------
# Templates
# ---------------------------------
templates = Jinja2Templates(
    directory="templates"
)


# ---------------------------------
# Home Page
# ---------------------------------
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):

    try:
        track(
            "fabric_homepage_viewed"
        )
    except Exception:
        pass

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

    # -----------------------------
    # Track Upload
    # -----------------------------
    try:
        track(
            "fabric_image_uploaded",
            {
                "filename": file.filename,
                "extension": os.path.splitext(file.filename)[1]
            }
        )
    except Exception:
        pass

    # -----------------------------
    # Run Analysis
    # -----------------------------

    result = analyze_image(
        image_path
    )
    try:
        save_analysis(
            file.filename,
            result
        )
    except Exception as e:
        print(
            "convex error:",
            e
        )


    # -----------------------------
    # Track Result
    # -----------------------------
    try:

        success = (
            "message" not in result
            or result.get("success", True)
        )

        track(
            "fabric_analysis_completed",
            {
                "filename": file.filename,
                "success": success,
                "total_garments": result.get(
                    "total_garments",
                    0
                )
            }
        )

        if "items" in result:

            for item in result["items"]:

                track(
                    "fabric_garment_detected",
                    {
                        "type": item.get("type"),
                        "fabric": item.get("fabric"),
                        "color": item.get("color"),
                        "confidence": item.get(
                            "confidence",
                            0
                        )
                    }
                )

    except Exception:
        pass

    # -----------------------------
    # Return Result Page
    # -----------------------------
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "result": result,
            "image_name": file.filename,
            "image_path": "/" + image_path.replace("\\", "/")
        }
    ) 