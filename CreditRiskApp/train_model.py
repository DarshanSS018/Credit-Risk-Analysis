"""
train_model.py
Reproduces the full preprocessing pipeline from credit_risk_analysis_Scikit.ipynb
and trains the best XGBoost model, then saves it as model.pkl
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '..', 'Original Data', 'credit_risk.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')

print("Loading data...")
df = pd.read_csv(DATA_PATH)

# ─── Step 1: One-hot encode Home and Intent ───────────────────────────────────
df = pd.get_dummies(df, columns=['Home', 'Intent'])

# ─── Step 2: Binary-encode Default ───────────────────────────────────────────
df['Default'] = df['Default'].map({'Y': 1, 'N': 0})

# ─── Step 3: Impute Rate by mean per Intent group ────────────────────────────
intent_columns = [col for col in df.columns if 'Intent_' in col]
df['Original_Intent'] = df[intent_columns].idxmax(axis=1).str.replace('Intent_', '')
mean_rate_by_intent = df.groupby('Original_Intent')['Rate'].mean()
for intent in mean_rate_by_intent.index:
    mask = (df['Original_Intent'] == intent) & (df['Rate'].isnull())
    df.loc[mask, 'Rate'] = mean_rate_by_intent[intent]
df.drop('Original_Intent', axis=1, inplace=True)

# ─── Step 4: Fix Emp_length outliers (123 → age-group mean) ──────────────────
mean_emp_length_age_22 = df[(df['Age'] == 22) & (df['Emp_length'] != 123)]['Emp_length'].mean()
mean_emp_length_age_21 = df[(df['Age'] == 21) & (df['Emp_length'] != 123)]['Emp_length'].mean()
df.loc[(df['Age'] == 22) & (df['Emp_length'] == 123), 'Emp_length'] = round(mean_emp_length_age_22, 1)
df.loc[(df['Age'] == 21) & (df['Emp_length'] == 123), 'Emp_length'] = round(mean_emp_length_age_21, 1)

# ─── Step 5: Impute remaining Emp_length NaN by age-group mean ───────────────
mean_emp_length_by_age = df[df['Emp_length'] < 100].groupby('Age')['Emp_length'].mean().round(1)
for age in mean_emp_length_by_age.index:
    mask = (df['Age'] == age) & (df['Emp_length'].isnull())
    df.loc[mask, 'Emp_length'] = mean_emp_length_by_age[age]

# ─── Step 6: Log-transform skewed numeric features ───────────────────────────
df['Age']        = np.log(df['Age'])
df['Income']     = np.log(df['Income'])
df['Emp_length'] = np.log(df['Emp_length'] + 1)   # +1 avoids log(0)
df['Amount']     = np.log(df['Amount'])

# ─── Step 7: Prepare features & target ───────────────────────────────────────
X = df.drop(['Status', 'Id'], axis=1)
y = df['Status']

# Store the feature column order for inference
feature_columns = list(X.columns)

# ─── Step 8: Train / test split ──────────────────────────────────────────────
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
X_val, X_test, y_val, y_test     = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# ─── Step 9: Train best XGBoost model (tuned hyper-params from notebook) ─────
print("Training XGBoost model...")
best_xgb = XGBClassifier(
    learning_rate=0.2,
    max_depth=5,
    n_estimators=200,
    eval_metric='logloss',
    random_state=42,
    use_label_encoder=False
)
best_xgb.fit(X_train, y_train)

# ─── Step 10: Quick evaluation ───────────────────────────────────────────────
from sklearn.metrics import accuracy_score, classification_report
y_pred = best_xgb.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nTest Accuracy: {acc:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ─── Step 11: Bundle model + metadata and save ───────────────────────────────
model_bundle = {
    'model': best_xgb,
    'feature_columns': feature_columns,
    'mean_rate_by_intent': mean_rate_by_intent.to_dict(),
    'mean_emp_length_by_age': mean_emp_length_by_age.to_dict(),
}

with open(MODEL_PATH, 'wb') as f:
    pickle.dump(model_bundle, f)

print(f"\nModel saved to: {MODEL_PATH}")
print(f"Feature columns ({len(feature_columns)}): {feature_columns}")
