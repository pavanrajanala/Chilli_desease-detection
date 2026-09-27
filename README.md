# 🌶️ Chilli (Mirchi) Leaf Disease Detection — Step-by-Step Guide

This is your full project: a Colab training notebook, a Flask backend, and a web frontend.
Everything is free (₹0). Follow the steps **in order**. Total time: ~1–2 hours (mostly Colab training time, which runs unattended).

Classes the model will detect (from the chosen dataset, see Phase 1 report):
`Bacterial_Spot, Cercospora_Leaf_Spot, Curl_Virus, Healthy_Leaf, Nutrient_Deficiency, Powdery_Mildew`

---

## STEP 1 — Download the dataset (5 min)

1. Go to: **https://data.mendeley.com/datasets/tm3v4zmh7c/1**
2. Click **"Download all files"** (a `.zip`, ~free, no login needed for most Mendeley sets; if it asks, a free account is fine).
3. You'll get a folder with 6 class subfolders:
   `Bacterial_Spot / Cercospora_Leaf_Spot / Curl_Virus / Healthy_Leaf / Nutrient_Deficiency / Powdery_Mildew`

## STEP 2 — Upload the dataset to Google Drive (5–10 min)

1. Zip the dataset folder if it isn't already a single `.zip`.
2. Upload `chilli_dataset.zip` to your Google Drive, e.g. into `My Drive/chilli_dataset.zip`.
   (Uploading the zip is much faster than uploading thousands of individual images.)

## STEP 3 — Train the model on Google Colab (free GPU, ~30–45 min)

1. Go to **https://colab.research.google.com**
2. Upload the notebook from this project: `train/train_chilli_model.ipynb`
   (File → Upload notebook)
3. Go to **Runtime → Change runtime type → T4 GPU** (free tier).
4. Run the cells **top to bottom** (Runtime → Run all).
   - It will ask you to authorize Google Drive access — accept it.
   - It unzips your dataset, splits it 80/10/10 (train/val/test), trains MobileNetV2 in two stages, evaluates it, and plots a confusion matrix.
5. At the end, it saves and downloads two files to your computer:
   - `chilli_disease_model.keras`
   - `class_names.json`

If you don't have `chilli_dataset.zip` ready yet and just want to see the **whole app working end-to-end right now**, skip to Step 4 — the backend runs in a "demo mode" with random predictions if no model file is present, so you can test the full flow first and plug in the real model later.

## STEP 4 — Set up the backend locally (5 min)

Requirements: Python 3.9+ installed on your computer.

```bash
cd chilli-app/backend
pip install -r requirements.txt
```

Copy the two files you downloaded from Colab into `backend/model/`:
```
backend/model/chilli_disease_model.keras
backend/model/class_names.json
```

## STEP 5 — Run the backend

```bash
cd chilli-app/backend
python app.py
```
You should see: `Running on http://127.0.0.1:5000`

## STEP 6 — Open the frontend

Just double-click `frontend/index.html` to open it in your browser (Chrome/Edge/Firefox).
It talks to `http://127.0.0.1:5000/predict`, so keep the backend running in a terminal.

1. Click **Upload Leaf Image** (or use your phone camera if opening on mobile)
2. Preview appears
3. Click **Analyze**
4. See disease name, confidence %, symptoms, and recommended next step
5. **Reset** to try another photo. Past results are kept in **Prediction History** (stored in your browser only).

## STEP 7 — Test with real photos

Take/find a few chilli leaf photos that were **not** in the training dataset and try them. Note down where it struggles (see "Known Limitations" in the backend `disease_info.py` and the model card in Colab output) — this is expected and part of a proper evaluation, not a bug.

## STEP 8 — (Optional) Deploy for free

- Backend: Render.com free tier or PythonAnywhere free tier (Flask apps supported).
- Frontend: GitHub Pages, or serve it directly from Flask (`static/` folder) so it's one deployment.
- Ask me when you're ready for this and I'll write the exact deployment steps for whichever platform you pick.

---

## What's already built for you in this folder

```
chilli-app/
├── train/
│   └── train_chilli_model.ipynb   ← run this in Colab (Step 3)
├── backend/
│   ├── app.py                     ← Flask API, /predict endpoint
│   ├── disease_info.py            ← symptoms + recommendations per class
│   ├── requirements.txt
│   └── model/                     ← put chilli_disease_model.keras + class_names.json here
└── frontend/
    └── index.html                 ← the whole UI (HTML+CSS+JS in one file)
```

## Notes / honesty about limitations (per project scope)

This is a **preliminary AI screening tool**, not a certified diagnosis. The UI and API responses always say this. Known weak spots to expect and mention if asked: confusing background clutter, poor lighting/blur, multiple leaves in one shot, Bacterial_Spot vs Cercospora_Leaf_Spot look-alikes, and nutrient-deficiency symptoms that can resemble disease. Encourage expert verification for anything beyond casual curiosity.
