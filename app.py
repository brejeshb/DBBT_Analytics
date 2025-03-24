import streamlit as st
from data_loader import load_data
from tabs.key_metrics import show_key_metrics_tab
from tabs.user_device import show_user_device_tab
from tabs.trip_characteristics import show_trip_characteristics_tab
from tabs.predictive_model import show_predictive_model_tab
from tabs.recommendations import show_recommendations_tab
from tabs.advanced_visualizations import show_advanced_visualizations_tab  # Import the advanced tab

# Set page configuration
st.set_page_config(
    page_title="Travel Agency Digital Transformation Dashboard",
    page_icon="✈️",
    layout="wide"
)

# Page title
st.title("Travel Agency Digital Transformation Dashboard")
st.markdown("### Data-Driven Analysis and Recommendations")

# Load data
with st.spinner('Loading and processing data...'):
    try:
        df = load_data()
        st.success('Data loaded successfully!')
    except Exception as e:
        st.error(f'Error loading data: {e}')
        st.stop()

# Show raw data sample if requested
with st.expander("View Raw Data Sample"):
    st.dataframe(df.sample(5))
    st.text(f"Total rows: {df.shape[0]}, Total columns: {df.shape[1]}")

# Create tabs for different analyses including the advanced visualizations tab
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Key Metrics & Trends", 
    "User & Device Analysis", 
    "Trip Characteristics",
    "Predictive Model",
    "Recommendations",
    "Advanced Visualizations"  # Add the new tab
])

# Display content in each tab
with tab1:
    show_key_metrics_tab(df)

with tab2:
    show_user_device_tab(df)

with tab3:
    show_trip_characteristics_tab(df)

with tab4:
    show_predictive_model_tab(df)

with tab5:
    show_recommendations_tab(df)

with tab6:
    # Show the advanced visualizations tab
    show_advanced_visualizations_tab(df)

if __name__ == "__main__":
    # This allows the app to be run standalone
    pass