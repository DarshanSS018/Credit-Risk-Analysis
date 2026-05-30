# 🏦 Credit Risk Analysis & Loan Default Prediction
### AI-Powered Streamlit Web Application

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?style=flat-square&logo=streamlit)](https://streamlit.io)
[![XGBoost](https://img.shields.io/badge/XGBoost-1.7+-orange?style=flat-square)](https://xgboost.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

A professional, interactive web application built with Streamlit that leverages Machine Learning to predict loan default risk. Trained on **32,581 real loan records**, the XGBoost model achieves **92.18% accuracy** on the held-out test set.

---

## 📸 Features

| Page | Description |
|------|-------------|
| 🏠 **Home** | Project overview, problem statement, business objective, and ML pipeline |
| 🔮 **Prediction** | Real-time loan default risk assessment with professional result cards |
| 📊 **Dashboard** | 8+ interactive Plotly visualisations of the dataset |
| ℹ️ **About** | Model details, preprocessing steps, risk categories, and limitations |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip package manager

### 1. Clone or navigate to the project
```bash
cd "Credit-Risk-Analysis-Default-Prediction-main"
```

### 2. Install dependencies
```bash
cd CreditRiskApp
pip install -r requirements.txt
```

### 3. Train and save the model
```bash
python train_model.py
```
This script:
- Loads the original dataset (`Original Data/credit_risk.csv`)
- Reproduces the full preprocessing pipeline from the notebook
- Trains the best XGBoost model (`lr=0.2, depth=5, n_estimators=200`)
- Saves the model bundle to `model.pkl`

### 4. Launch the application
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## 📁 Project Structure

```
CreditRiskApp/
│
├── app.py                  # Main entry point with sidebar navigation
├── train_model.py          # Model training & pkl export script
├── model.pkl               # Trained XGBoost model bundle (generated)
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── pages/
│   ├── __init__.py
│   ├── home.py             # Home / overview page
│   ├── prediction.py       # Loan risk prediction page
│   ├── dashboard.py        # Interactive analytics dashboard
│   └── about.py            # About & methodology page
│
└── assets/                 # Static assets (images, etc.)
```

---

## 🤖 Model Details

### Final Model: XGBoost
| Hyperparameter | Value |
|----------------|-------|
| Learning Rate  | 0.2   |
| Max Depth      | 5     |
| N Estimators   | 200   |
| Eval Metric    | Log Loss |

### Test Set Performance
| Metric     | Score  |
|------------|--------|
| Accuracy   | 92.18% |
| Precision  | 94.91% |
| Recall     | 69.69% |
| F1 Score   | 80.37% |
| AUC-ROC    | 0.8429 |

---

## 🔧 Preprocessing Pipeline

1. **One-Hot Encoding** — `Home` (4 categories) and `Intent` (6 categories)
2. **Binary Encoding** — `Default` column (Y/N → 1/0)
3. **Rate Imputation** — Missing `Rate` filled with mean per loan Intent group
4. **Emp_length Cleaning** — Outliers (123 years) replaced; NaN filled by age-group mean
5. **Log Transformation** — Applied to `Age`, `Income`, `Amount`, `Emp_length+1`
6. **Train/Val/Test Split** — 80% / 10% / 10% stratified split

---

## 🚦 Risk Categories

| Probability Range | Risk Level | Recommendation |
|-------------------|-----------|----------------|
| 0% – 30% | 🟢 Low Risk | Loan Recommended |
| 31% – 70% | 🟡 Medium Risk | Further Review Required |
| 71% – 100% | 🔴 High Risk | Loan Not Recommended |

---

## 📊 Dataset

- **Source**: `credit_risk.csv` (32,581 loan records)
- **Features**: Age, Income, Home Ownership, Employment Length, Loan Intent, Amount, Interest Rate, Past Default, Credit History Length
- **Target**: Loan Status (0 = No Default, 1 = Default)

---

## ⚠️ Disclaimer

This application is for **educational and portfolio demonstration purposes only**. Predictions should not be used as the sole basis for real lending decisions. Real credit decisions require compliance with fair lending laws (ECOA, FCRA, etc.).

---

## 🛠️ Built With

- [Python](https://python.org) — Core language
- [Streamlit](https://streamlit.io) — Web application framework
- [XGBoost](https://xgboost.readthedocs.io) — Gradient boosting library
- [Scikit-Learn](https://scikit-learn.org) — ML utilities & preprocessing
- [Plotly](https://plotly.com/python/) — Interactive visualisations
- [Pandas](https://pandas.pydata.org) & [NumPy](https://numpy.org) — Data manipulation
