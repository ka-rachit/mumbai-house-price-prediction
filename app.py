import streamlit as st

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

def navbar():
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown("### 🏡 Mumbai House Price Predictor")

    with col2:
        if st.button("Home", use_container_width=True, key="home_btn"):
            st.rerun()

    with col3:
        if st.button("Prediction", use_container_width=True, key="pred_btn"):
            st.switch_page("pages/Prediction.py")

    st.markdown("---")

apply_theme()

navbar()

st.title("Welcome to Mumbai House Price Predictor")
st.write("Get AI-powered estimates for property values in Mumbai using advanced machine learning models.")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.info("📊 Advanced ML Model\nPrecision pricing based on location, size, and amenities")
with col2:
    st.info("⚡ Real-time Predictions\nInstant valuations for any Mumbai property")
