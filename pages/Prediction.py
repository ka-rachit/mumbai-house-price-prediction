import streamlit as st
import joblib
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Mumbai House Price Predictor", layout="wide", initial_sidebar_state="collapsed")

# Hide sidebar
st.markdown("""
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
""", unsafe_allow_html=True)

if "theme" not in st.session_state:
    st.session_state.theme = "light"

def apply_theme():
    if st.session_state.theme == "dark":
        st.markdown("""
            <style>
                :root {
                    --primary-color: #ffffff;
                    --background-color: #0e1117;
                    --secondary-background-color: #161b22;
                    --text-color: #c9d1d9;
                }
                body {
                    background-color: #0e1117;
                    color: #c9d1d9;
                }
            </style>
        """, unsafe_allow_html=True)

# --- 2. NAVBAR ---
def navbar():
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown("### 🏡 Mumbai House Price Predictor")

    with col2:
        if st.button("Home", use_container_width=True, key="home_btn"):
            st.switch_page("app.py")

    with col3:
        if st.button("Prediction", use_container_width=True, key="pred_btn"):
            st.rerun()

    st.markdown("---")

apply_theme()

navbar()

# --- 3. LOAD RESOURCES ---
@st.cache_resource
def load_resources():
    try:
        # Load Model
        model = joblib.load('model_advanced.pkl')

        # Load Data for Region List
        df = pd.read_csv('cleaned_data_v2.csv')
        df['region'] = df['region'].astype(str)
        # remove 'nan' and sort
        df = df[df['region'].str.lower() != 'nan']
        regions = sorted(df['region'].unique().tolist())

        return model, regions
    except Exception as e:
        return None, []

model, region_options = load_resources()

# Error handling if files are missing
if model is None:
    st.error("Error loading files. Please check GitHub for 'model_advanced.pkl' and 'cleaned_data_v2.csv'.")
    st.stop()

# --- 4. HELPER: CURRENCY FORMATTER ---
def format_currency(value):
    val_lakhs = value
    if val_lakhs >= 100:
        return f"₹ {val_lakhs/100:.2f} Cr"
    else:
        return f"₹ {val_lakhs:.2f} Lakhs"

# --- 5. APP UI ---
st.title("Price Prediction")

col1, col2 = st.columns(2)

with col1:
    # SEARCHABLE DROPDOWN
    # Streamlit handles the text color automatically
    selected_region = st.selectbox(
        "📍 Select Location",
        region_options,
        index=None,
        placeholder="Type to search..."
    )

with col2:
    bhk = st.number_input("🛏️ Bedrooms (BHK)", min_value=1, max_value=10, value=2)

st.write("") # Spacer
st.write("**📏 Total Area (Sq Ft)**")
area = st.slider("Area", min_value=500, max_value=5000, value=1000, step=50, label_visibility="collapsed")
st.caption(f"Selected: {area} Sq Ft")

# --- 5. LOGIC ---
if selected_region is None:
    st.info("👈 Please select a location to estimate price.")
    st.stop()

st.markdown("---")

# Use a primary button (automatically highlighted theme color)
if st.button("Calculate Value", type="primary", use_container_width=True):

    # Prepare Input
    input_data = pd.DataFrame([[selected_region, area, bhk]],
                              columns=['region', 'area', 'bhk'])

    # Predict
    prediction = model.predict(input_data)[0]
    formatted_price = format_currency(prediction)

    # Display Result using Native Streamlit Metrics (Looks good in both modes)
    st.success("Valuation Complete!")

    col_res1, col_res2 = st.columns([2, 1])

    with col_res1:
        st.metric(label="Estimated Price", value=formatted_price)

    with col_res2:
        st.metric(label="Location", value=selected_region)
