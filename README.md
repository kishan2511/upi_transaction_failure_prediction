# 💳 UPI Transaction Failure Root-Cause Intelligence System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange)
![License](https://img.shields.io/badge/License-MIT-green)

> **GTU Post Graduate Diploma in Data Science — Mini Project**
> **Student:** Kishan Patel | **Enrollment:** 251370680017 | **Guide:** Komal Prajapati

---

## 🚀 Live Demo

🔗 **[Open Streamlit App](https://your-app-link.streamlit.app/)**

---

## 📌 Problem Statement

UPI (Unified Payments Interface) processes billions of transactions daily. Transaction failures cause user frustration and financial loss. Identifying the **root cause** of each failure automatically helps banks, NPCI, and payment apps resolve issues faster.

**Goal:** Classify the root cause of failed UPI transactions into one of 8 categories using supervised machine learning.

---

## 🔍 Root-Cause Classes (8)

| # | Root Cause | Key Signal |
|---|-----------|------------|
| 1 | Bank_Server_Down | server_status=down, high response_time |
| 2 | Insufficient_Funds | high amount relative to limit |
| 3 | Wrong_Credentials | high retry_count |
| 4 | Network_Timeout | very high response_time, poor network |
| 5 | VPA_Not_Found | invalid payee VPA |
| 6 | Fraud_Flag | unusually high amount |
| 7 | NPCI_Gateway_Error | high NPCI latency |
| 8 | User_Declined | user-initiated decline |

---

## 📊 Dataset

| Property | Value |
|----------|-------|
| Total Records | 100,000 transactions |
| Failure Rate | ~28% (28,000 failed transactions) |
| Features | 12 input features |
| Target | root_cause (8 classes) |
| Source | Synthetically generated (realistic UPI log simulation) |

---

## ⚙️ Methodology

```
Data Generation → EDA → Preprocessing → SMOTE → Model Training → Evaluation → Deployment
```

1. **Dataset Generation** — Synthetic UPI logs with realistic failure class distributions
2. **EDA** — Failure rate analysis, class distribution, feature correlation
3. **Preprocessing** — OneHotEncoding for categoricals, StandardScaler for numerics
4. **SMOTE** — Synthetic Minority Oversampling for imbalanced classes (Fraud_Flag, VPA_Not_Found)
5. **Model** — Random Forest Classifier (150 estimators)
6. **Deployment** — Streamlit web app for live root-cause prediction

---

## 📈 Model Results

| Metric | Value |
|--------|-------|
| **Accuracy** | ~88–92% |
| **Model** | Random Forest (150 estimators) |
| **Classes** | 8 failure root-cause categories |

---

## 🗂️ Project Structure

```
upi_transaction_failure_prediction/
├── app.py                                      # Streamlit web application
├── upi_transaction_failure_prediction.ipynb    # Full analysis notebook
├── requirements.txt                            # Dependencies
├── runtime.txt                                 # Python version
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| pandas & NumPy | Data handling |
| scikit-learn | ML pipeline, Random Forest |
| imbalanced-learn | SMOTE oversampling |
| matplotlib & seaborn | Visualizations |
| Streamlit | Web application |
| Jupyter Notebook | Analysis & report |

---

## 💻 Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/upi_transaction_failure_prediction.git
cd upi_transaction_failure_prediction
pip install -r requirements.txt
streamlit run app.py
```

---

## 📚 References

1. NPCI — UPI Transaction Statistics (2024)
2. scikit-learn — Random Forest Classifier
3. Chawla, N.V. et al. (2002). SMOTE: Synthetic Minority Over-sampling Technique
4. Breiman, L. (2001). Random Forests. Machine Learning, 45(1)
5. Streamlit Documentation

---

## 👤 Author

**Kishan Patel**
Enrollment: 251370680017
Gujarat Technological University (GTU) — PGDDS Mini Project
Academic Year 2025-26, Semester-2
Internal Guide: Komal Prajapati
