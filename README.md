# 🍕 Food Delivery Time Prediction

> Predicting food delivery times using Machine Learning — Linear Regression, Logistic Regression, and Random Forest — with a live Streamlit web app.

📌 Problem Statement

Food delivery platforms lose customer trust when delivery times are inaccurate. This project builds a predictive system that estimates delivery time (in minutes) and classifies deliveries as **Fast** or **Delayed** based on real-world factors like distance, traffic, and weather.

 📂 Dataset

| Feature | Description |
|---|---|
| Distance | Distance between restaurant and customer (km) |
| Weather_Conditions | Clear, Fog, Stormy, etc. |
| Traffic_Conditions | Low, Medium, High, Jam |
| Vehicle_Type | Scooter, Motorcycle, Bicycle, etc. |
| Delivery_Person_Experience | Years of experience |
| Order_Priority | Low / Medium / High |
| Delivery_Time | Target variable (minutes) |

-----------------------------------------------------------------

 🔧 Tech Stack

- **Python** — pandas, numpy, scikit-learn, matplotlib, seaborn
- **Models** — Linear Regression, Logistic Regression, Random Forest
- **Deployment** — Streamlit
- **Environment** — Google Colab / Jupyter Notebook

----------------------------------------------------------------

 🚀 Project Pipeline

```
Data Loading → Preprocessing → EDA → Feature Engineering → Modeling → Evaluation → Deployment
```

StepS

1. **Data Preprocessing**
   - Handled missing values via median imputation
   - Label encoded categorical features (Weather, Traffic, Vehicle Type)
   - StandardScaler applied to numeric features

2. **Feature Engineering**
   - Haversine formula for accurate distance calculation
   - Rush Hour flag (8–10 AM, 6–9 PM)

3. **EDA**
   - Correlation heatmap, boxplots for outlier detection
   - Distribution analysis of delivery times

4. **Models Trained**
   - Linear Regression → predicts exact delivery time
   - Logistic Regression → classifies Fast vs Delayed
   - Random Forest → best overall performance

---

## 📊 Model Comparison

| Model | R² / Accuracy | MAE / F1-Score |
|---|---|---|
| Linear Regression | ~0.82 R² | ~4.2 min MAE |
| Logistic Regression | ~84% Accuracy | ~0.83 F1 |
| Random Forest | ~0.91 R² | ~2.8 min MAE |

> Random Forest outperforms both baseline models significantly.

---

## 📈 Visualizations

- Correlation heatmap
- Outlier detection boxplots
- Confusion matrix (Logistic Regression)
- ROC Curve with AUC score
- Feature importance plot (Random Forest)
- Actual vs Predicted scatter plot

---

## 🌐 Streamlit App

🌐 Live Demo: https://fooddeliverypredictionnp.streamlit.app

**App Features:**
- Input distance, weather, traffic, vehicle type, experience
- Outputs predicted delivery time in minutes
- Shows Fast ✅ or Delayed 🔴 classification
- Bar chart showing impact of each feature

---

## 💡 Key Insights & Recommendations

1. **Traffic is the #1 delay factor** — High/Jam conditions add 9–16 mins
2. **Rush hours (8–10 AM, 6–9 PM)** cause consistent delays → staff up proactively
3. **Experienced delivery agents** reduce time by ~1 min/year of experience
4. **Stormy weather** adds ~12 mins — suggest dynamic ETAs during bad weather
5. **Motorcycle > Scooter > Bicycle** for speed — optimize vehicle assignment

---

## 📁 Repository Structure

```
food-delivery-prediction/
├── Food_Delivery_Predictionpr.ipynb
├── app.py
├── model_comparison.png
├── feature_importance.png
├── actual_vs_predicted_rf.png
├── confusion_roc.png
└── README.md
```

---

## 👤 AYUSHMAN MISHRA

B.E. Computer Science | NMIT Bengaluru
[LinkedIn](www.linkedin.com/in/ayushman-mishra01) 
| [GitHub](https://github.com/ayushmanmishra2027)
