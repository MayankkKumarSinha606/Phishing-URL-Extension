from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import joblib 
import warnings
import pandas as pd
import io

# Import your custom feature extractor
from core.feature import FeatureExtraction

warnings.filterwarnings('ignore')

# 1. Initialize the FastAPI app
app = FastAPI(
    title="Phishing Detection API",
    description="API for the Phishing URL Browser Extension",
    version="1.0.0"
)

# --- ADDED CORS MIDDLEWARE ---
# This is required so your Chrome Extension can talk to localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Load the Machine Learning Model exactly ONCE at startup
try:
    model = joblib.load("pickle/model.pkl") 
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

# 3. Define the Input Data Schema using Pydantic
class URLRequest(BaseModel):
    url: str


# ==========================================
# SINGLE URL PREDICTION ENDPOINT (Original)
# ==========================================
@app.post("/predict")
def predict_phishing(request: URLRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Check File path.")
    try:
        clean_url = request.url.strip()
        if not clean_url.startswith("http://") and not clean_url.startswith("https://"):
            clean_url = "https://" + clean_url

        obj = FeatureExtraction(clean_url)
        features_list = obj.getFeaturesList()
        
        x = np.array(features_list).reshape(1, 29)
        
        y_pred = model.predict(x)[0]
        probabilities = model.predict_proba(x)[0]
        
        prob_phishing = float(probabilities[0])
        prob_safe = float(probabilities[1])
        
        is_safe = True if y_pred == 1 else False 

        return {
            "url": request.url,
            "is_safe": is_safe,
            "confidence_safe_percentage": round(prob_safe * 100, 2),
            "confidence_phishing_percentage": round(prob_phishing * 100, 2),
            "raw_prediction_class": int(y_pred)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# NEW BATCH EXCEL UPLOAD ENDPOINT
# ==========================================
@app.post("/predict-batch")
async def predict_batch(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Check File path.")

    try:
        # 1. Read the uploaded Excel file into a Pandas DataFrame
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading Excel file: {e}")
    
    # 2. Check if 'url' column exists
    if 'url' not in df.columns:
        raise HTTPException(status_code=400, detail="Excel file must contain a column named 'url'")

    results = []

    # 3. Loop through the URLs and run the exact same logic
    for raw_url in df["url"]:
        # Skip empty cells
        if pd.isna(raw_url):
            continue
            
        try:
            clean_url = str(raw_url).strip()
            if not clean_url.startswith("http://") and not clean_url.startswith("https://"):
                clean_url = "https://" + clean_url

            obj = FeatureExtraction(clean_url)
            features_list = obj.getFeaturesList()
            
            x = np.array(features_list).reshape(1, 29)
            
            y_pred = model.predict(x)[0]
            probabilities = model.predict_proba(x)[0]
            
            prob_phishing = float(probabilities[0])
            prob_safe = float(probabilities[1])
            
            is_safe = True if y_pred == 1 else False 

            results.append({
                "url": str(raw_url),
                "is_safe": is_safe,
                "confidence_safe_percentage": round(prob_safe * 100, 2),
                "confidence_phishing_percentage": round(prob_phishing * 100, 2),
                "raw_prediction_class": int(y_pred)
            })
        except Exception as e:
            # If one URL fails, catch the error but keep processing the rest
            results.append({
                "url": str(raw_url),
                "error": str(e)
            })

    # 4. Return the list of results
    return {"results": results}