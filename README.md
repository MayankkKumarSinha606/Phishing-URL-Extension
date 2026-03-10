# Phishing URL Detection

## Table of Content
  * [Introduction](#introduction)
  * [Installation](#installation)
  * [Running the API](#running-the-api)
  * [API Usage](#api-usage)
  * [Directory Tree](#directory-tree)
  * [Result](#result)
  * [Conclusion](#conclusion)


## Introduction

The Internet has become an indispensable part of our life, However, It also has provided opportunities to anonymously perform malicious activities like Phishing. Phishers try to deceive their victims by social engineering or creating mockup websites to steal information such as account ID, username, password from individuals and organizations. Although many methods have been proposed to detect phishing websites, Phishers have evolved their methods to escape from these detection methods. One of the most successful methods for detecting these malicious activities is Machine Learning. This is because most Phishing attacks have some common characteristics which can be identified by machine learning methods. To see project click [here]("/").


## Installation

This project requires **Python 3.12+** and uses [uv](https://docs.astral.sh/uv/) for fast, reliable dependency management.

### 1. Install uv

If you don't have `uv` installed, you can install it with:

```bash
# On macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone the repository

```bash
git clone https://github.com/your-username/Phishing-URL-Detection.git
cd Phishing-URL-Detection
```

### 3. Install dependencies

```bash
uv sync
```

This reads `pyproject.toml`, creates a virtual environment automatically, and installs all dependencies — no manual `venv` activation needed.

> **Note:** A `requirements.txt` is still provided for compatibility, but `uv sync` with `pyproject.toml` is the recommended approach.


## Running the API

The API is built with **FastAPI** and served via **Uvicorn**.

### Development server

```bash
uv run fastapi dev api/main.py
```

This starts the server at `http://127.0.0.1:8000` with hot-reload enabled.

### Production server

```bash
uv run fastapi run api/main.py
```

### Interactive API docs

Once the server is running, visit:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)


## API Usage

### `POST /predict`

Send a JSON body with the URL to check:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**Response:**

```json
{
  "url": "https://example.com",
  "is_safe": true,
  "confidence_safe_percentage": 97.42,
  "confidence_phishing_percentage": 2.58,
  "raw_prediction_class": 1
}
```


## Directory Tree
```
├── api/
│   ├── __init__.py
│   └── main.py                # FastAPI application
├── core/
│   ├── __init__.py
│   └── feature.py             # Feature extraction logic
├── models/
│   └── phishing_model.joblib  # Trained ML model
├── Phishing-URL-Api-Testing/
│   ├── opencollection.yml
│   └── Predict.yml            # API test collections
├── Phishing URL Detection.ipynb
├── Procfile
├── pyproject.toml             # Project config & dependencies (uv)
├── README.md
├── phishing.csv
└── requirements.txt           # Legacy pip requirements
```

## Technologies Used

- [Python 3.12+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [scikit-learn](https://scikit-learn.org/stable/)
- [NumPy](https://numpy.org/doc/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [uv](https://docs.astral.sh/uv/)

## Result

Accuracy of various model used for URL detection
<br>

<br>

||ML Model|Accuracy|  f1_score|Recall|Precision|
|---|---|---|---|---|---|
0|Gradient Boosting Classifier|0.974|0.977|0.994|0.986|
1|CatBoost Classifier|        0.972|0.975|0.994|0.989|
2|XGBoost Classifier|         0.969|0.973|0.993|0.984|
3|Multi-layer Perceptron|        0.969|0.973|0.995|0.981|
4|Random Forest|                0.967|0.971|0.993|0.990|
5|Support Vector Machine|        0.964|0.968|0.980|0.965|
6|Decision Tree|              0.960|0.964|0.991|0.993|
7|K-Nearest Neighbors|        0.956|0.961|0.991|0.989|
8|Logistic Regression|        0.934|0.941|0.943|0.927|
9|Naive Bayes Classifier|     0.605|0.454|0.292|0.997|



## Conclusion
1. The final take away form this project is to explore various machine learning models, perform Exploratory Data Analysis on phishing dataset and understanding their features. 
2. Creating this notebook helped me to learn a lot about the features affecting the models to detect whether URL is safe or not, also I came to know how to tuned model and how they affect the model performance.
3. The final conclusion on the Phishing dataset is that the some feature like "HTTTPS", "AnchorURL", "WebsiteTraffic" have more importance to classify URL is phishing URL or not. 
4. Gradient Boosting Classifier currectly classify URL upto 97.4% respective classes and hence reduces the chance of malicious attachments.
