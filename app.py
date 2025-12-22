import streamlit as st
import joblib
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Mumbai House Price Predictor", layout="centered")

# --- 2. CUSTOM STYLING (Blue & White) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    h1 { color: #007BFF; text-align: center; }
    .stButton>button { background-color: #007BFF; color: white; border-radius: 5px; }
    .stButton>button:hover { background-color: #0056b3; color: white; }
    /* Style the slider to be blue */
    div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
        background-color: #007BFF;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOAD DATA & MODEL ---
@st.cache_resource
def load_resources():
    # Load the model
    model = joblib.load('model_advanced.pkl')
    # Load the column names (we need the CSV to get the list of locations)
    df = pd.read_csv('cleaned_data_v2.csv')
    locations = sorted(df['locality'].unique().tolist())
    return model, locations

try:
    model, location_options = load_resources()
except Exception as e:
    st.error(f"Error loading files: {e}")
    st.stop()

# --- 4. HELPER: CURRENCY FORMATTER ---
def format_currency(value):
    val_lakhs = value
    val_actual = val_lakhs * 100000
    
    if val_lakhs >= 100:
        return f"₹ {val_lakhs/100:.2f} Cr"
    else:
        return f"₹ {val_lakhs:.2f} Lakhs"

# --- 5. APP UI ---
st.title("🏡 Mumbai House Price Predictor")
st.write("### AI-Powered Valuation (Accuracy: 84%)")
st.write("Now using **Ridge Regression** & **One-Hot Encoding** for location-aware pricing.")

# INPUTS
st.write("---")
col1, col2 = st.columns(2)

with col1:
    # LOCATION DROPDOWN
    selected_location = st.selectbox("📍 Select Location", location_options)

with col2:
    # BHK INPUT
    bhk = st.number_input("🛏️ Bedrooms (BHK)", min_value=1, max_value=10, value=2)

# AREA SLIDER
st.write("**📏 Total Area (Sq Ft)**")
area = st.slider("Adjust Area", min_value=500, max_value=5000, value=1000, step=50, label_visibility="collapsed")
st.caption(f"Selected: {area} Sq Ft")

st.markdown("---")

# PREDICT BUTTON
if st.button("Calculate Value", use_container_width=True):
    # Prepare input for the pipeline (must match training columns exactly)
    input_data = pd.DataFrame([[selected_location, area, bhk]], 
                              columns=['locality', 'area', 'bhk'])
    
    # Predict
    prediction = model.predict(input_data)[0]
    
    # Display
    formatted_price = format_currency(prediction)
    
    st.markdown(f"""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #007BFF; text-align: center;">
            <h3 style="margin:0; color: #007BFF;">Estimated Value</h3>
            <h2 style="margin:10px 0; color: #333;">{formatted_price}</h2>
            <p style="margin:0; color: #555;">for a {bhk} BHK in <b>{selected_location}</b></p>
        </div>
    """, unsafe_allow_html=True)