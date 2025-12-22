import streamlit as st
import joblib
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Mumbai House Price Predictor", layout="centered")

# --- 2. LOAD RESOURCES ---
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

# --- 3. HELPER: CURRENCY FORMATTER ---
def format_currency(value):
    val_lakhs = value
    if val_lakhs >= 100:
        return f"₹ {val_lakhs/100:.2f} Cr"
    else:
        return f"₹ {val_lakhs:.2f} Lakhs"

# --- 4. APP UI ---
st.title("🏡 Mumbai House Price Predictor")
st.caption("AI-Powered Real Estate Valuation Engine")

st.markdown("---")

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
        st.metric(label="Config", value=f"{bhk} BHK, {area} Sq Ft")