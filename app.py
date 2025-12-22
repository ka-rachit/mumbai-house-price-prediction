import streamlit as st
import joblib
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Mumbai House Price Predictor", layout="centered")

# --- 2. FINAL CSS FIX (FORCE WHITE THEME EVERYWHERE) ---
st.markdown("""
    <style>
    /* 1. Main Background */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }

    /* 2. Text Colors (Headings, Labels, Paragraphs) */
    h1, h2, h3, h4, h5, h6, p, div, label, span {
        color: #000000 !important;
    }
    
    /* 3. Input Boxes (Dropdowns & Number Inputs) - FORCE WHITE BACKGROUND */
    .stSelectbox div[data-baseweb="select"] > div,
    .stNumberInput div[data-baseweb="input"] > div {
        background-color: #F0F2F6 !important; /* Light Grey for input box */
        color: #000000 !important;
        border-color: #CCCCCC !important;
    }
    
    /* 4. Text INSIDE Input Boxes */
    input[type="text"], input[type="number"] {
        color: #000000 !important;
        background-color: transparent !important; /* Let parent background show */
    }

    /* 5. Dropdown Menu Items (When you click the list) */
    ul[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
    }
    li[data-baseweb="option"] {
        color: #000000 !important; 
    }
    
    /* 6. Fix for Placeholder Text (The "Type to search..." text) */
    div[data-baseweb="select"] span {
        color: #555555 !important; /* Dark Grey for placeholder */
    }

    /* 7. Buttons */
    .stButton>button {
        background-color: #007BFF !important;
        color: white !important;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0056b3 !important;
    }

    /* 8. Slider Color */
    div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"] {
        background-color: #007BFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOAD DATA & MODEL ---
@st.cache_resource
def load_resources():
    model = joblib.load('model_advanced.pkl')
    # Load CSV to get the list of REGIONS
    df = pd.read_csv('cleaned_data_v2.csv')
    df['region'] = df['region'].astype(str)
    df = df[df['region'].str.lower() != 'nan']
    regions = sorted(df['region'].unique().tolist())
    return model, regions

try:
    model, region_options = load_resources()
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
st.write("### AI-Powered Valuation")

st.write("---")
col1, col2 = st.columns(2)

with col1:
    # SEARCHABLE DROPDOWN
    selected_region = st.selectbox(
        "📍 Select Location", 
        region_options, 
        index=None, 
        placeholder="Type to search (e.g. Bandra)..."
    )

with col2:
    bhk = st.number_input("🛏️ Bedrooms (BHK)", min_value=1, max_value=10, value=2)

st.write("**📏 Total Area (Sq Ft)**")
area = st.slider("Adjust Area", min_value=500, max_value=5000, value=1000, step=50, label_visibility="collapsed")
st.caption(f"Selected: {area} Sq Ft")

# --- 6. LOGIC ---
if selected_region is None:
    st.info("👈 Please search for a location to begin.")
    st.stop()

st.markdown("---")

if st.button("Calculate Value", use_container_width=True):
    # Input must use 'region' column name to match training
    input_data = pd.DataFrame([[selected_region, area, bhk]], 
                              columns=['region', 'area', 'bhk'])
    
    prediction = model.predict(input_data)[0]
    formatted_price = format_currency(prediction)
    
    st.markdown(f"""
        <div style="background-color: #F0F8FF; padding: 20px; border-radius: 10px; border-left: 5px solid #007BFF; text-align: center;">
            <h3 style="margin:0; color: #007BFF !important;">Estimated Value</h3>
            <h2 style="margin:10px 0; color: #333333 !important;">{formatted_price}</h2>
            <p style="margin:0; color: #555555 !important;">for a {bhk} BHK in <b>{selected_region}</b></p>
        </div>
    """, unsafe_allow_html=True)