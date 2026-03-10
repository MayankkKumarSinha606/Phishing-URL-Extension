from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib # or 'import pickle' if you are still using .pkl
import warnings

# Import your custom feature extractor
from core.feature import FeatureExtraction

warnings.filterwarnings('ignore')

# 1. Initialize the FastAPI app
app = FastAPI(
    title="Phishing Detection API",
    description="API for the Phishing URL Browser Extension",
    version="1.0.0"
)

# 2. Load the Machine Learning Model exactly ONCE at startup
# (Make sure the path matches where you placed your model file)
try:
    model = joblib.load("pickle/model.pkl") 
    # If using pickle: 
    # with open("models/model.pkl", "rb") as file:
    #     model = pickle.load(file)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

# 3. Define the Input Data Schema using Pydantic
# This ensures the API only accepts requests that contain a "url" string.
class URLRequest(BaseModel):
    url: str

# 4. Create the API Endpoint
@app.post("/predict")
def predict_phishing(request: URLRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Check File path.")
    try:
        # Sanitize the URL: add a scheme if the user just typed "google.com"
        clean_url = request.url.strip()
        if not clean_url.startswith("http://") and not clean_url.startswith("https://"):
            clean_url = "https://" + clean_url

        # Extract features just like the old Flask app
        obj = FeatureExtraction(clean_url)
        features_list = obj.getFeaturesList()
        
        # --- DIAGNOSTIC PRINT ---
        print(f"\n--- DIAGNOSTICS FOR {clean_url} ---")
        print("Extracted Features Array:")
        print(features_list)
        print("-----------------------------------\n")
        # -------------------------
        
        # Reshape for the model (1 sample, 30 features)
        x = np.array(features_list).reshape(1, 29)
        
        # Get Predictions
        y_pred = model.predict(x)[0]
        probabilities = model.predict_proba(x)[0]
        
        # Map probabilities based on your model's classes
        # Index 0 is usually Phishing (-1 or 0), Index 1 is Safe (1)
        prob_phishing = float(probabilities[0])
        prob_safe = float(probabilities[1])
        
        # Determine human-readable status
        # Update the condition if you changed your labels to 0 and 1 in Colab
        is_safe = True if y_pred == 1 else False 

        # Return a clean JSON response for the browser extension
        return {
            "url": request.url,
            "is_safe": is_safe,
            "confidence_safe_percentage": round(prob_safe * 100, 2),
            "confidence_phishing_percentage": round(prob_phishing * 100, 2),
            "raw_prediction_class": int(y_pred)
        }

    except Exception as e:
        # If something goes wrong (e.g., bad URL format), return a 500 Error
        raise HTTPException(status_code=500, detail=str(e))