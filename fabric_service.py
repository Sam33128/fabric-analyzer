import os
import json

from ultralytics import YOLO
from PIL import Image
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# -----------------------------
# Gemini Client
# -----------------------------
client = genai.Client(api_key=api_key)

# -----------------------------
# YOLO Model
# -----------------------------
model = YOLO("yolo11n.pt")


# -----------------------------
# Image Validation
# -----------------------------
def validate_clothing_image(image_path):

    img = Image.open(image_path)

    prompt = """
    Determine whether this image contains clothing garments.

    Return ONLY valid JSON.

    Format:

    {
      "contains_clothing": true,
      "reason": ""
    }

    Return true if the image contains:
    - clothing
    - garments
    - apparel
    - fashion products
    - people wearing clothes

    Return false for:
    - vehicles
    - animals
    - landscapes
    - food
    - documents
    - random household objects
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[img, prompt]
    )

    clean_json = (
        response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(clean_json)


# -----------------------------
# Main Analysis Function
# -----------------------------
def analyze_image(image_path):

    os.makedirs("crops", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # -----------------------------
    # Validate Input
    # -----------------------------
    validation = validate_clothing_image(image_path)

    if not validation.get("contains_clothing", False):

        return {
            "success": False,
            "message": "Please upload an image containing clothing garments.",
            "reason": validation.get("reason", "No clothing detected")
        }

    print("Validation Passed")

    # -----------------------------
    # YOLO Detection
    # -----------------------------
    print("Running YOLO...")

    results = model(image_path)

    img = Image.open(image_path)

    crop_path = None

    # -----------------------------
    # Find Person
    # -----------------------------
    for result in results:

        boxes = result.boxes

        for box in boxes:

            cls = int(box.cls[0])

            # COCO Class 0 = Person
            if cls == 0:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                crop = img.crop((x1, y1, x2, y2))

                crop_path = "crops/person_crop.jpg"

                crop.save(crop_path)

                print("Person cropped")

                break

    # -----------------------------
    # If no person found,
    # analyze entire image
    # -----------------------------
    if crop_path is None:

        crop_path = image_path

        print("No person detected. Using full image.")

    # -----------------------------
    # Gemini Analysis
    # -----------------------------
    crop_img = Image.open(crop_path)

    prompt = """
    Analyze all visible garments.

    Return ONLY valid JSON.

    Format:

    {
      "total_garments": 0,
      "items": [
        {
          "type": "",
          "fabric": "",
          "color": "",
          "confidence": 0.0
        }
      ]
    }

    Allowed garment types:
    shirt, t-shirt, pants, shorts,
    jacket, hoodie, dress, skirt,
    sweater, belt

    Allowed fabrics:
    cotton, denim, linen, wool,
    polyester, leather, silk, fleece

    Confidence must be between 0 and 1.

    No explanation.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[crop_img, prompt]
    )

    clean_json = (
        response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    parsed = json.loads(clean_json)

    with open(
        "outputs/result.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            parsed,
            f,
            indent=4
        )

    return parsed 