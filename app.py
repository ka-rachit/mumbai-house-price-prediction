import streamlit as st
import joblib
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Mumbai House Price Predictor", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    h1 { color: #007BFF; text-align: center; }
    .stButton>button { background-color: #007BFF; color: white; border-radius: 5px; }
    .stButton>button:hover { background-color: #0056b3; color: white; }
    div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
        background-color: #007BFF;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOAD RESOURCES ---
@st.cache_resource
def load_resources():
    model = joblib.load('model_advanced.pkl')
    # Load CSV to get the list of REGIONS now
    df = pd.read_csv('cleaned_data_v2.csv')
    df['region'] = df['region'].astype(str)
    df = df[df['region'].str.lower() != 'nan']
    # Get sorted unique regions
    regions = sorted(df['region'].unique().tolist())
    return model, regions

try:
    model, region_options = load_resources()
except Exception as e:
    st.error(f"Error loading files: {e}")
    st.stop()

# --- HELPER ---
def format_currency(value):
    val_lakhs = value
    val_actual = val_lakhs * 100000
    if val_lakhs >= 100:
        return f"₹ {val_lakhs/100:.2f} Cr"
    else:
        return f"₹ {val_lakhs:.2f} Lakhs"

# --- UI ---
st.title("🏡 Mumbai House Price Predictor")
st.write("### AI-Powered Valuation")

st.write("---")
col1, col2 = st.columns(2)

with col1:
    # REGION DROPDOWN (Now much cleaner!)
    selected_region = st.selectbox("📍 Select Region", region_options)

with col2:
    bhk = st.number_input("🛏️ Bedrooms (BHK)", min_value=1, max_value=10, value=2)

st.write("**📏 Total Area (Sq Ft)**")
area = st.slider("Adjust Area", min_value=500, max_value=5000, value=1000, step=50, label_visibility="collapsed")
st.caption(f"Selected: {area} Sq Ft")

st.markdown("---")

if st.button("Calculate Value", use_container_width=True):
    # Input must use 'region' column name to match training
    input_data = pd.DataFrame([[selected_region, area, bhk]], 
                              columns=['region', 'area', 'bhk'])
    
    prediction = model.predict(input_data)[0]
    formatted_price = format_currency(prediction)
    
    st.markdown(f"""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #007BFF; text-align: center;">
            <h3 style="margin:0; color: #007BFF;">Estimated Value</h3>
            <h2 style="margin:10px 0; color: #333;">{formatted_price}</h2>
            <p style="margin:0; color: #555;">for a {bhk} BHK in <b>{selected_region}</b></p>
        </div>
    """, unsafe_allow_html=True)