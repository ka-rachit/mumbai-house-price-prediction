import streamlit as st
import joblib
import pandas as pd

# --- 1. SETUP PAGE CONFIGURATION (Must be first) ---
st.set_page_config(page_title="Mumbai House Price Predictor", layout="centered")

# --- 2. CUSTOM CSS FOR "BLUE & WHITE" THEME ---
st.markdown("""
    <style>
    /* Make the background white and text dark */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    /* Style the buttons to be Blue */
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }
    /* Customize the Title to be Blue */
    h1 {
        color: #007BFF;
        text-align: center;
    }
    /* Customize text to be centered */
    .subtitle {
        text-align: center;
        color: #555;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTION: INDIAN CURRENCY FORMATTER ---
def format_indian_currency(lakhs_val):
    # Convert prediction (which is in Lakhs) to actual Rupee value
    actual_value = float(lakhs_val * 100000)
    
    # 1. CREATE THE READABLE LABEL (Cr or Lakhs)
    if lakhs_val >= 100:
        readable_text = f"{lakhs_val / 100:.2f} Cr"
    else:
        readable_text = f"{lakhs_val:.2f} Lakhs"
    
    # 2. CREATE THE COMMA NUMBER (e.g., 45,32,786)
    # Standard Python uses US commas (1,000,000), which is close enough for an MVP
    # If you want strict Indian commas (10,00,000), it requires complex regex, 
    # so we use the standard helper for reliability.
    comma_text = "{:,.0f}".format(actual_value)
    
    return comma_text, readable_text

# --- 4. LOAD MODEL ---
try:
    model = joblib.load('model_upgraded.pkl')
except:
    st.error("Error: 'model_upgraded.pkl' not found. Please run the training script first.")
    st.stop()

# --- 5. APP UI ---
st.title("🏡 Mumbai House Price Predictor")
st.markdown('<p class="subtitle">AI-Powered Real Estate Valuation Engine</p>', unsafe_allow_html=True)

st.write("### Enter Property Details")
st.write("Adjust the values below to get an instant valuation.")

# Create two columns for a better layout
col1, col2 = st.columns(2)

with col1:
    area = st.number_input("Total Area (Sq Ft)", min_value=100, max_value=10000, value=1000, step=50)

with col2:
    bhk = st.number_input("Bedrooms (BHK)", min_value=1, max_value=10, value=2, step=1)

st.markdown("---") # A divider line

# Center the button using columns
_, mid_col, _ = st.columns([1, 2, 1])

with mid_col:
    predict_btn = st.button("Calculate Value", use_container_width=True)

# --- 6. PREDICTION LOGIC ---
if predict_btn:
    # Prepare input
    input_data = pd.DataFrame([[area, bhk]], columns=['area', 'bhk'])
    
    # Predict
    prediction_lakhs = model.predict(input_data)[0]
    
    # Format
    comma_price, readable_price = format_indian_currency(prediction_lakhs)
    
    # Display Result
    st.markdown(f"""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #007BFF; text-align: center;">
            <h3 style="margin:0; color: #007BFF;">Estimated Value</h3>
            <h2 style="margin:10px 0; color: #333;">₹ {comma_price}</h2>
            <p style="margin:0; font-size: 18px; color: #555;">(Approx. <b>{readable_price}</b>)</p>
        </div>
    """, unsafe_allow_html=True)