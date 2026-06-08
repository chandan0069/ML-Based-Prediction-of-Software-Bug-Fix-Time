# Bug Fix Time Predictor

A machine learning system that predicts whether a software bug will be resolved in a **short time (< 8 days)** or **long time (≥ 8 days)**, trained on real Apache Jira issue data from projects including Hadoop, Spark, Kafka, Cassandra, Hive, Flink, and HBase.

---

## Project Structure

```
BUG/
├── main.py                        # FastAPI backend — prediction API
├── schema.py                      # Pydantic input/output models
├── app.py                         # Flask frontend server
├── requirements.txt
├── model/
│   └── best_rf_pipeline.joblib    # Trained Random Forest pipeline
├── templates/
│   └── index.html                 # Bootstrap UI
└── notebook/
    └── MAIN.ipynb                 # Training notebook
```

---

## How It Works

### Data
- Source: Apache Jira issues from 7 open-source projects (HADOOP, SPARK, KAFKA, CASSANDRA, HIVE, FLINK, HBASE)
- Target: Binary classification — Short (< 8 days) vs Long (≥ 8 days) resolution time

## Setup

### Prerequisites
- Python 3.12
- pip

### Installation

```bash
git clone <your-repo-url>
cd BUG

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Run

Open two terminals:

```bash
# Terminal 1 — FastAPI prediction API (port 8000)
uvicorn main:app --reload --port 8000

# Terminal 2 — Flask frontend (port 5000)
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

---


## Tech Stack

| Layer | Technology |
|---|---|
| ML | scikit-learn, XGBoost, imbalanced-learn |
| API | FastAPI, Pydantic, Uvicorn |
| Frontend | Flask, Bootstrap 5 |
| Serialization | joblib |
| Data | Apache Jira REST API |

---

## Author

Chandan 
