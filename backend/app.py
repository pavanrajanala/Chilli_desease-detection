"""
Chilli Leaf Disease Detection - Flask backend.

Endpoints:
  GET  /health   -> simple status check, tells you if the real model is loaded
  POST /  -> accepts an image file (field name "image"), returns prediction JSON

Run:
  python app.py
"""

import io
import json
import os
import random

import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError

from disease_info import GENERAL_DISCLAIMER, get_info

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "chilli_disease_model.keras")
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, "class_names.json")
IMG_SIZE = (224, 224)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB

app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# ---------------------------------------------------------------------------
# Model loading (lazy + graceful demo-mode fallback so the app still runs
# and can be tested end-to-end before a trained model is available)
# ---------------------------------------------------------------------------
_model = None
_class_names = None
_demo_mode = False

DEFAULT_CLASS_NAMES = [
    "Bacterial_Spot",
    "Cercospora_Leaf_Spot",
    "Curl_Virus",
    "Healthy_Leaf",
    "Nutrition_Deficiency",
    "Powdery_Mildew",
]


def load_model_and_classes():
    global _model, _class_names, _demo_mode

    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, "r") as f:
            _class_names = json.load(f)
    else:
        _class_names = DEFAULT_CLASS_NAMES

    if os.path.exists(MODEL_PATH):
        import tensorflow as tf  # imported here so the server still starts even if TF is slow to import
        _model = tf.keras.models.load_model(MODEL_PATH)
        _demo_mode = False
        print(f"[app] Loaded trained model from {MODEL_PATH}")
    else:
        _model = None
        _demo_mode = True
        print(
            "[app] WARNING: no trained model found at "
            f"{MODEL_PATH}. Running in DEMO MODE with randomized predictions. "
            "Train the model (see train/train_chilli_model.ipynb) and place the "
            "two output files into backend/model/ to get real predictions."
        )


load_model_and_classes()


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(file_bytes: bytes) -> np.ndarray:
    """Load bytes -> PIL Image -> RGB -> resize -> MobileNetV2 preprocessing -> batch of 1."""
    img = Image.open(io.BytesIO(file_bytes))
    img = img.convert("RGB")
    img = img.resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32)

    if _demo_mode:
        return np.expand_dims(arr, axis=0)

    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    arr = preprocess_input(arr)
    return np.expand_dims(arr, axis=0)


def run_prediction(batch: np.ndarray):
    """Returns (predicted_class_name, confidence_percent, all_probs_dict)."""
    if _demo_mode:
        # Randomized but stable-looking demo output so the UI can be tested end-to-end.
        probs = np.random.dirichlet(np.ones(len(_class_names)) * 2)
    else:
        preds = _model.predict(batch, verbose=0)
        probs = preds[0]

    top_idx = int(np.argmax(probs))
    predicted_class = _class_names[top_idx]
    confidence = float(probs[top_idx]) * 100
    all_probs = {
        _class_names[i]: round(float(probs[i]) * 100, 2) for i in range(len(_class_names))
    }
    return predicted_class, round(confidence, 2), all_probs


@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "model_loaded": not _demo_mode,
            "demo_mode": _demo_mode,
            "classes": _class_names,
        }
    )


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded. Use form field name 'image'."}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Empty filename."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type. Use JPG, JPEG, PNG, or WEBP."}), 400

    file_bytes = file.read()
    if len(file_bytes) == 0:
        return jsonify({"error": "Uploaded file is empty."}), 400

    try:
        batch = preprocess_image(file_bytes)
    except UnidentifiedImageError:
        return jsonify({"error": "Could not read this file as an image. Please upload a valid leaf photo."}), 400
    except Exception as e:  # noqa: BLE001
        return jsonify({"error": f"Image processing failed: {str(e)}"}), 400

    try:
        predicted_class, confidence, all_probs = run_prediction(batch)
    except Exception as e:  # noqa: BLE001
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    info = get_info(predicted_class)

    response = {
        "disease": info["display_name"],
        "raw_class": predicted_class,
        "confidence": confidence,
        "symptoms": info["symptoms"],
        "recommendation": info["recommendation"],
        "is_healthy": predicted_class == "Healthy_Leaf",
        "all_class_probabilities": all_probs,
        "disclaimer": GENERAL_DISCLAIMER,
        "demo_mode": _demo_mode,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
