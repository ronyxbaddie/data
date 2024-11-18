import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title and description
st.title("Traffic Data Analysis")
st.write("Analyze traffic patterns, peak hours, and holiday effects.")

# Upload file
uploaded_file = st.file_uploader("Upload your traffic data CSV file", type=["csv"])
if uploaded_file:
    # Read the uploaded file
    traffic_data = pd.read_csv(uploaded_file)
    
    # Ensure 'DateTime' column is datetime format
    traffic_data['DateTime'] = pd.to_datetime(traffic_data['DateTime'])

    # Sidebar options
    st.sidebar.header("Select Analysis")
    options = st.sidebar.multiselect(
        "Choose analysis to perform:",
        ["Peak Hours", "Holiday Effects", "Traffic by Junction"]
    )
    
    # Peak Hour Analysis
    if "Peak Hours" in options:
        st.subheader("Peak Hour Analysis")
        traffic_data['Hour'] = traffic_data['DateTime'].dt.hour
        hourly_traffic = traffic_data.groupby('Hour')['Vehicles'].mean().reset_index()

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='Hour', y='Vehicles', data=hourly_traffic, ax=ax)
        ax.set_title('Average Traffic Volume by Hour of Day')
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Average Traffic Volume')
        st.pyplot(fig)

    # Holiday Effects Analysis
    if "Holiday Effects" in options:
        st.subheader("Holiday Effects")
        public_holidays = ['2016-01-01', '2016-07-04', '2016-12-25']  # Example
        public_holidays = pd.to_datetime(public_holidays)

        traffic_data['IsHoliday'] = traffic_data['DateTime'].dt.normalize().isin(public_holidays)
        holiday_traffic = traffic_data.groupby('IsHoliday')['Vehicles'].mean().reset_index()

        fig, ax = plt.subplots()
        holiday_traffic.plot(kind='bar', x='IsHoliday', y='Vehicles', ax=ax, legend=False)
        ax.set_title("Average Traffic Volume: Holidays vs. Non-Holidays")
        ax.set_xlabel("Is Holiday")
        ax.set_ylabel("Average Traffic Volume")
        st.pyplot(fig)

    # Traffic by Junction Analysis
    if "Traffic by Junction" in options:
        st.subheader("Traffic Volume by Junction")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(x='Junction', y='Vehicles', data=traffic_data, ax=ax)
        ax.set_title("Traffic Volume by Junction")
        ax.set_xlabel("Junction")
        ax.set_ylabel("Number of Vehicles")
        st.pyplot(fig)
