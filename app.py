import streamlit as st
import joblib
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Mumbai House Price Predictor", layout="centered")

# --- 2. THE FIX: NUCLEAR CSS FOR COLORS ---
st.markdown("""
    <style>
    /* 1. Main Page Background */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }

    /* 2. FORCE ALL TEXT TO BLACK */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #000000 !important;
    }

    /* 3. INPUT BOXES (The box you type in) */
    .stSelectbox div[data-baseweb="select"] > div,
    .stNumberInput div[data-baseweb="input"] > div {
        background-color: #F0F2F6 !important; /* Light Grey Background */
        color: #000000 !important;             /* Black Text */
        border-color: #CCCCCC !important;
    }
    
    /* 4. THE DROPDOWN MENU LIST (The part that was black-on-black) */
    /* Target the container of the list */
    div[data-baseweb="popover"] > div {
        background-color: #FFFFFF !important;
    }
    /* Target the items inside the list */
    ul[data-baseweb="menu"] li {
        background-color: #FFFFFF !important; /* White Background */
        color: #000000 !important;            /* Black Text */
    }
    /* Target the highlighted item (when you hover) */
    ul[data-baseweb="menu"] li[aria-selected="true"], 
    ul[data-baseweb="menu"] li:hover {
        background-color: #007BFF !important; /* Blue Background */
        color: #FFFFFF !important;            /* White Text */
    }

    /* 5. Placeholder Text ("Type to search...") */
    div[data-baseweb="select"] span {
        color: #555555 !important;
    }

    /* 6. Buttons */
    .stButton>button {
        background-color: #007BFF !important;
        color: white !important;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOAD RESOURCES ---
@st.cache_resource
def load_resources():
    try:
        model = joblib.load('model_advanced.pkl')
        df = pd.read_csv('cleaned_data_v2.csv')
        df['region'] = df['region'].astype(str)
        df = df[df['region'].str.lower() != 'nan']
        regions = sorted(df['region'].unique().tolist())
        return model, regions
    except Exception as e:
        return None, []

model, region_options = load_resources()

if model is None:
    st.error("Error loading files. Please ensure 'model_advanced.pkl' and 'cleaned_data_v2.csv' are in the GitHub folder.")
    st.stop()

# --- 4. HELPER FUNCTION ---
def format_currency(value):
    val_lakhs = value
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
    selected_region = st.selectbox(
        "📍 Select Location", 
        region_options, 
        index=None, 
        placeholder="Type to search..."
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