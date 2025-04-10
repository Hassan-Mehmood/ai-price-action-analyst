import streamlit as st
import requests

# Configure the page
st.set_page_config(page_title="Price Action Analyst", page_icon="📈", layout="wide")

# Title and description
st.title("Price Action Analyst")
st.markdown("Upload your price charts for analysis across different timeframes")

# API endpoint
API_URL = "http://localhost:7999/analysis"

# Create three columns for the uploaders
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Daily Analysis")
    daily_image = st.file_uploader(
        "Upload Daily Chart", type=["png", "jpg", "jpeg"], key="daily"
    )

    if daily_image is not None:
        st.image(daily_image, caption="Daily Chart", use_container_width=True)
        if st.button("Analyze Daily", key="daily_btn"):
            with st.spinner("Analyzing daily chart..."):
                files = {"image": daily_image.getvalue()}
                response = requests.post(f"{API_URL}/daily", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success("Analysis Complete!")
                    st.json(result)
                else:
                    st.error("Error in analysis")

with col2:
    st.subheader("Hourly Analysis")
    hourly_image = st.file_uploader(
        "Upload Hourly Chart", type=["png", "jpg", "jpeg"], key="hourly"
    )

    if hourly_image is not None:
        st.image(hourly_image, caption="Hourly Chart", use_container_width=True)
        if st.button("Analyze Hourly", key="hourly_btn"):
            with st.spinner("Analyzing hourly chart..."):
                files = {"image": hourly_image.getvalue()}
                response = requests.post(f"{API_URL}/hourly", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success("Analysis Complete!")
                    st.json(result)
                else:
                    st.error("Error in analysis")

with col3:
    st.subheader("Weekly Analysis")
    weekly_image = st.file_uploader(
        "Upload Weekly Chart", type=["png", "jpg", "jpeg"], key="weekly"
    )

    if weekly_image is not None:
        st.image(weekly_image, caption="Weekly Chart", use_container_width=True)
        if st.button("Analyze Weekly", key="weekly_btn"):
            with st.spinner("Analyzing weekly chart..."):
                files = {"image": weekly_image.getvalue()}
                response = requests.post(f"{API_URL}/weekly", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success("Analysis Complete!")
                    st.json(result)
                else:
                    st.error("Error in analysis")
