Here is the updated, professional `README.md` file. I have integrated the **Browser Extension** details, the **FastAPI Batch Testing** features, and the credits for your friends so it's ready for your LinkedIn launch.

---

# 🛡️ Phishing URL Detection 2.0: Browser Extension & API

## Table of Content

* [Introduction](https://www.google.com/search?q=%23introduction)
* [New Features](https://www.google.com/search?q=%23new-features)
* [Installation](https://www.google.com/search?q=%23installation)
* [Running the API](https://www.google.com/search?q=%23running-the-api)
* [Browser Extension Setup](https://www.google.com/search?q=%23browser-extension-setup)
* [Directory Tree](https://www.google.com/search?q=%23directory-tree)
* [Contributors](https://www.google.com/search?q=%23contributors)
* [Results & Model Performance](https://www.google.com/search?q=%23result)

---

## Introduction

Internet security is more critical than ever. Phishers use sophisticated social engineering and mockup websites to steal credentials. This project leverages **Machine Learning** to identify the technical "DNA" of a phishing attack.

Moving beyond a simple notebook, this version provides an **active defense system** via a browser extension and a high-performance **FastAPI** backend that analyzes URLs across 29 technical features in real-time.

---

## New Features

🚀 **Real-Time Extension**: Protects users as they browse by analyzing active tabs.
✅ **29-Feature Optimization**: Retrained to eliminate "HTTPS Bias," ensuring legitimate sites are not falsely flagged.
📊 **Batch Analysis**: Upload Excel files via the `/predict-batch` endpoint for bulk URL verification.
🛡️ **Hybrid Intelligence**: Integrated **Whitelisting** for trusted global domains (LinkedIn, Google, GitHub) to ensure zero false positives on critical platforms.

---

## Installation

This project requires **Python 3.12+**. It is optimized for [uv](https://docs.astral.sh/uv/) for dependency management but supports standard `pip`.

### 1. Clone the repository

```bash
git clone https://github.com/MayankkKumarSinha606/Phishing-URL-Extension.git
cd Phishing-URL-Extension

```

### 2. Install dependencies

```bash
# Using uv (Recommended)
uv sync

# Using pip
pip install -r requirements.txt

```

---

## Running the API

### Start the Server

```bash
# Using uv
uv run fastapi dev api/main.py

# Using standard python
python -m uvicorn api.main:app --reload

```

Once running, access the interactive docs at: `http://127.0.0.1:8000/docs`

### Batch Testing via Excel

You can now upload an `.xlsx` file with a `url` column to the `/predict-batch` endpoint.
*Note: Requires `openpyxl` (included in requirements).*

---

## Browser Extension Setup

1. Open **Brave** or **Chrome** and navigate to `chrome://extensions/`.
2. Enable **Developer Mode** (top right toggle).
3. Click **Load Unpacked**.
4. Select the `extension` folder from this repository.
5. Ensure the FastAPI server is running locally to handle the analysis.

---

## Contributors

This project reached its production state through collaboration:

* **Mayank Sinha** - Lead ML Engineer & Backend Developer.
* **[Friend 1 Name]** - Technical Research: Optimized Extension architecture and V3 Manifest implementation.
* **[Friend 2 Name]** - Testing & QA Lead: Developed the batch-testing pipeline and validated 60+ edge cases using PhishTank data.

---

## Directory Tree

```text
├── api/
│   └── main.py              # FastAPI app with Whitelist & Batch logic
├── core/
│   └── feature.py           # 29-Feature extraction engine
├── extension/
│   ├── manifest.json        # Extension config
│   ├── popup.html           # Extension UI
│   └── popup.js             # API communication logic
├── pickle/
│   └── model.pkl            # Trained Gradient Boosting Model
├── requirements.txt         # Project dependencies
└── README.md

```

---

## Result

Our model was validated against 10,000+ URLs. The **Gradient Boosting Classifier** emerged as the top performer:

| ML Model | Accuracy | F1 Score | Recall | Precision |
| --- | --- | --- | --- | --- |
| **Gradient Boosting Classifier** | **0.974** | **0.977** | **0.994** | **0.986** |
| CatBoost Classifier | 0.972 | 0.975 | 0.994 | 0.989 |
| XGBoost Classifier | 0.969 | 0.973 | 0.993 | 0.984 |

---

## Conclusion

1. **Real-World Validation**: The system successfully flags verified threats from **PhishTank** (e.g., Exodus wallet clones) while maintaining 100% confidence for whitelisted sites like **LinkedIn, Google, Microsoft etc**.
2. **Feature Importance**: Features like "AnchorURL", "WebsiteTraffic", and "URL Length" remain the most critical indicators of malicious intent.
