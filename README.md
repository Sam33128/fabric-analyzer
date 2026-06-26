# 🧵 FabricVision AI

An AI-powered web application that analyzes clothing images to identify **garment type, fabric material, and color** using **YOLO 11** and **Google Gemini 2.5 Flash**. The application provides an intuitive web interface built with **FastAPI**, tracks application analytics using **PostHog**, stores analysis history in **Convex**, and is designed for containerized deployment with Docker.

---

# Features

* Upload garment or clothing images
* AI-based clothing image validation
* Person detection using YOLO 11
* Automatic person cropping for improved analysis
* Garment type detection
* Fabric prediction
* Color prediction
* Confidence score estimation
* Modern responsive UI
* Analysis history stored in Convex
* User analytics using PostHog
* JSON export of predictions

---

# Tech Stack

| Category               | Technology                       |
| ---------------------- | -------------------------------- |
| Backend                | FastAPI                          |
| AI Object Detection    | YOLO 11 (Ultralytics)            |
| Vision LLM             | Google Gemini 2.5 Flash          |
| Frontend               | HTML, CSS, Bootstrap, JavaScript |
| Image Processing       | Pillow                           |
| Database               | Convex                           |
| Analytics              | PostHog                          |
| Environment Management | Python Dotenv                    |
| Deployment             | Docker (Work in Progress)        |

---

# Project Architecture

```text
                 User
                   │
                   ▼
          FastAPI Web Application
                   │
                   ▼
         Clothing Image Validation
             (Gemini Vision)
                   │
                   ▼
          YOLO 11 Person Detection
                   │
          ┌────────┴────────┐
          │                 │
      Person Found      No Person
          │                 │
          ▼                 ▼
     Crop Person      Analyze Full Image
             \         /
              ▼       ▼
         Gemini 2.5 Flash
     (Garment + Fabric + Color)
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   Result UI   PostHog   Convex Database
                   │
                   ▼
          outputs/result.json
```

---

# Workflow

1. User uploads an image through the web interface.
2. Gemini validates whether the uploaded image contains clothing.
3. If validation fails, the user is prompted to upload a valid garment image.
4. YOLO 11 detects a person in the image.
5. If a person is detected, the image is cropped to focus on the clothing.
6. If no person is detected, the full garment image is analyzed.
7. Gemini analyzes the image and predicts:

   * Garment Type
   * Fabric
   * Color
   * Confidence Score
8. Results are displayed on the web page.
9. The analysis is:

   * Saved as JSON
   * Logged to PostHog
   * Stored in Convex

---

# Why YOLO + Gemini?

### YOLO 11

YOLO specializes in object detection. It identifies the location of the person or garment, allowing irrelevant background information to be removed before analysis.

### Gemini 2.5 Flash

Gemini excels at understanding visual content and reasoning about clothing characteristics. It predicts:

* Garment type
* Fabric
* Color
* Confidence

Using both models creates a more reliable pipeline than relying on a single vision model for the entire task.

---

# PostHog Integration

PostHog is used to monitor application usage and user interactions.

Tracked events include:

* Homepage visited
* Image uploaded
* Clothing validation passed
* Clothing validation failed
* YOLO detection started
* Person detected
* Full image analysis
* Gemini analysis started
* Gemini analysis completed
* Analysis completed
* Garment detected

This helps understand application usage and identify areas for improvement.

---

# Convex Integration

Convex serves as the application's persistent database.

Each successful analysis stores:

* Image name
* Total garments detected
* Garment type
* Fabric
* Color
* Confidence score
* Timestamp

This enables future features such as:

* Analysis history
* Search
* Dashboard
* Usage statistics
* User-specific records

---

# Project Structure

```text
FabricVision-AI
│
├── app.py
├── fabric_service.py
├── analytics.py
├── convex_service.py
├── requirements.txt
├── Dockerfile
├── .env
│
├── convex/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── outputs/
├── images/
└── crops/
```

---

# Docker Status

A Dockerfile has been created for the project.

The application runs successfully in the local Python environment.

Docker image creation is currently incomplete due to repeated installation failures of large machine learning dependencies (primarily PyTorch and Ultralytics) caused by network timeouts and interrupted downloads during the build process.

The application code itself is compatible with Docker. Completing containerization will require improving dependency installation reliability, such as using pinned versions, cached layers, or a stable network during image creation.

---

# Environment Variables

Create a `.env` file containing:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

POSTHOG_API_KEY=YOUR_POSTHOG_API_KEY
POSTHOG_HOST=https://us.posthog.com

CONVEX_URL=YOUR_CONVEX_DEPLOYMENT_URL
```

---

# Installation

```bash
git clone https://github.com/your-username/fabric-analyzer.git

cd fabric-analyzer

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app:app --reload
```

---

# Future Improvements

* Docker build optimization
* User authentication
* Analysis history page
* PDF report generation
* AI garment care recommendations
* Batch image processing
* REST API documentation
* Cloud deployment
* Mobile responsive enhancements

---

# Contributors

**Samyam Prakash**

B.Tech CSE (AI & ML)

---

# License

This project is intended for educational and research purposes.
