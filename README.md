

# 🏡 Mumbai Real Estate Price Prediction Engine

A Machine Learning powered web application that estimates residential property prices in Mumbai. It uses **Ridge Regression** with a sophisticated data pipeline to analyze location, area, and bedroom count, providing users with instant, data-driven valuations.

### 🚀 [Click Here to Try the Live App](https://www.google.com/search?q=https://%5B[YOUR-STREAMLIT-LINK-HERE](https://mumbai-house-price-prediction-yogin.streamlit.app/)%5D)

---

## 📸 Screenshots

*(Add a screenshot of your app here)*

---

## 🧠 The Intelligence (How it Works)

Unlike basic calculators that use simple averages, this project implements a full **Supervised Learning Pipeline**:

1. **Data Processing:** * Cleaned a dataset of 5,000+ real Mumbai listings.
* Handled high-cardinality location data (300+ unique regions) using **One-Hot Encoding**.
* Scaled numerical features (Area, BHK) using `StandardScaler` to normalize distributions.


2. **The Model:**
* **Algorithm:** Ridge Regression (Linear Least Squares with L2 Regularization).
* **Why Ridge?** Chosen over standard Linear Regression to handle multicollinearity between location features and prevent overfitting.
* **Performance:** Achieved an **R² Score of 0.84**, significantly outperforming the baseline.


3. **Deployment:**
* Wrapped the model in a **Streamlit** web interface.
* Deployed via CI/CD pipeline on Streamlit Community Cloud.



---

## 🛠️ Tech Stack

* **Language:** Python
* **Machine Learning:** Scikit-Learn (Ridge, Pipeline, ColumnTransformer)
* **Data Manipulation:** Pandas, NumPy
* **Web Framework:** Streamlit
* **Model Persistence:** Joblib

---

## 📂 Project Structure

```bash
├── app.py                 # The main Streamlit web application
├── train_advanced.py      # The training script (Data cleaning -> Pipeline -> Model Save)
├── model_advanced.pkl     # The trained serialized model file
├── cleaned_data_v2.csv    # Processed dataset used for the Location Dropdown
├── requirements.txt       # Dependencies for deployment
└── README.md              # Documentation

```

---

## ⚡ How to Run Locally

If you want to run this project on your own machine:

1. **Clone the repository**
```bash
git clone https://github.com/[YOUR-USERNAME]/mumbai-house-prices.git
cd mumbai-house-prices

```


2. **Install dependencies**
```bash
pip install -r requirements.txt

```


3. **Run the app**
```bash
streamlit run app.py

```



---

## 🔮 Future Roadmap (PropShare)

This tool is the MVP for a larger vision: **PropShare**, a fractional real estate investment platform.

* **Phase 1 (Done):** Price Discovery Engine.
* **Phase 2 (In Progress):** "Undervalued Deal" Alert System using Anomaly Detection.
* **Phase 3:** Fractional Investment Marketplace.

---

## 👨‍💻 Author

**Yogin**

* **LinkedIn:** www.linkedin.com/in/yogin-langalia


---
