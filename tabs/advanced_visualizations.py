import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import calculate_conversion_rate, create_conversion_heatmap

def show_advanced_visualizations_tab(df):
    """
    Display advanced visualizations (optional additional tab)
    """
    st.header("Advanced Visualizations")
    
    st.write("""
    This tab contains additional, more complex visualizations that provide deeper insights
    into the travel agency data. These visualizations can help identify more nuanced patterns
    and opportunities for digital transformation.
    """)
    
    # Create sections for different visualization types
    viz_type = st.selectbox(
        "Select Visualization Type",
        ["Conversion Heatmaps", "Geospatial Analysis", "Temporal Patterns", "Customer Segmentation"]
    )
    
    if viz_type == "Conversion Heatmaps":
        show_conversion_heatmaps(df)
    elif viz_type == "Geospatial Analysis":
        show_geospatial_analysis(df)
    elif viz_type == "Temporal Patterns":
        show_temporal_patterns(df)
    elif viz_type == "Customer Segmentation":
        show_customer_segmentation(df)

def show_conversion_heatmaps(df):
    """
    Display conversion rate heatmaps
    """
    st.subheader("Conversion Rate Heatmaps")
    
    st.write("""
    These heatmaps show how conversion rates vary across different combinations of factors.
    Darker colors indicate higher conversion rates.
    """)
    
    # Select dimensions for the heatmap
    heatmap_option = st.radio(
        "Select dimensions for heatmap:",
        ["Device × Package Type", "Trip Duration × Booking Window", "Adults × Children"]
    )
    
    if heatmap_option == "Device × Package Type":
        # Create a pivot table for device x package
        device_package_data = df.copy()
        device_package_data['device'] = df['is_mobile'].map({0: 'Desktop', 1: 'Mobile'})
        device_package_data['package'] = df['is_package'].map({0: 'Non-package', 1: 'Package'})
        
        # Create a pivot table
        pivot_data = device_package_data.pivot_table(
            index='device',
            columns='package',
            values='is_booking',
            aggfunc=lambda x: 100 * x.mean()  # Convert to percentage
        ).round(2)
        
        # Plot heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Blues',
            text=pivot_data.values,
            texttemplate='%{text}%',
            textfont={"size":14},
        ))
        
        fig.update_layout(
            title="Conversion Rate by Device and Package Type",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("""
        **Insights:**
        - Desktop non-package searches have the highest conversion rate
        - Mobile package searches have the lowest conversion rate
        - Both device types show significantly lower conversion for packages
        """)
        
    elif heatmap_option == "Trip Duration × Booking Window":
        # Ensure we have valid data for both dimensions
        filtered_df = df.dropna(subset=['duration_category', 'window_category'])
        
        # Create heatmap using utility function
        fig = create_conversion_heatmap(
            filtered_df, 
            'duration_category', 
            'window_category', 
            'is_booking'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("""
        **Insights:**
        - Short trips booked 30-59 days in advance have the highest conversion rates
        - Last-minute bookings (0-6 days) for short trips also convert well
        - Long trips (8+ days) generally have poor conversion rates regardless of booking window
        """)
        
    elif heatmap_option == "Adults × Children":
        # Limit to common combinations to avoid sparse data
        filtered_df = df[
            (df['srch_adults_cnt'] <= 4) & 
            (df['srch_children_cnt'] <= 3)
        ]
        
        # Create pivot table
        pivot_data = filtered_df.pivot_table(
            index='srch_adults_cnt',
            columns='srch_children_cnt',
            values='is_booking',
            aggfunc=lambda x: 100 * x.mean()
        ).round(2)
        
        # Plot heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Blues',
            text=pivot_data.values,
            texttemplate='%{text}%',
            textfont={"size":14},
        ))
        
        fig.update_layout(
            title="Conversion Rate by Number of Adults and Children",
            xaxis_title="Number of Children",
            yaxis_title="Number of Adults",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("""
        **Insights:**
        - Single adults (with or without children) have higher conversion rates
        - Couples with no children have average conversion rates
        - Larger family groups tend to have lower conversion rates
        """)

def show_geospatial_analysis(df):
    """
    Display geospatial analysis visualizations
    """
    st.subheader("Geospatial Analysis")
    
    st.write("""
    This section analyzes how geographical factors affect conversion rates.
    Note: Since the dataset uses numeric codes for locations, we're analyzing patterns 
    rather than showing actual maps.
    """)
    
    # User location analysis
    st.subheader("User Location Analysis")
    
    # Top user countries by conversion rate
    user_country_data = calculate_conversion_rate(df, 'user_location_country')
    top_countries = user_country_data[user_country_data['searches'] >= 100].sort_values('conversion_rate', ascending=False).head(10)
    
    fig = px.bar(
        top_countries,
        x='user_location_country',
        y='conversion_rate',
        title="Top 10 User Countries by Conversion Rate",
        color='conversion_rate',
        text=top_countries['conversion_rate'].round(2).astype(str) + '%',
        height=400
    )
    
    fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='User Country Code')
    st.plotly_chart(fig, use_container_width=True)
    
    # Distance analysis
    st.subheader("Distance Impact Analysis")
    
    # Create distance buckets to analyze impact on conversion
    distance_data = df.dropna(subset=['orig_destination_distance'])
    distance_data['distance_bucket'] = pd.cut(
        distance_data['orig_destination_distance'],
        bins=[0, 100, 500, 1000, 2000, np.inf],
        labels=['0-100', '100-500', '500-1000', '1000-2000', '2000+']
    )
    
    distance_conv = calculate_conversion_rate(distance_data, 'distance_bucket')
    
    fig = px.line(
        distance_conv,
        x='distance_bucket',
        y='conversion_rate',
        title="Conversion Rate by Origin-Destination Distance",
        markers=True,
        height=400
    )
    
    fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='Distance (km)')
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("""
    **Insights:**
    - Certain user countries have significantly higher conversion rates
    - Conversion rates typically decrease as origin-destination distance increases
    - Targeting marketing efforts to high-converting countries could improve overall performance
    """)

def show_temporal_patterns(df):
    """
    Display temporal patterns visualizations
    """
    st.subheader("Temporal Patterns")
    
    st.write("""
    This section analyzes how time-related factors affect conversion rates.
    """)
    
    # Extract time components
    df['search_hour'] = pd.to_datetime(df['date_time']).dt.hour
    df['search_day'] = pd.to_datetime(df['date_time']).dt.day_name()
    df['search_month'] = pd.to_datetime(df['date_time']).dt.month_name()
    
    # Create tabs for different temporal analyses
    time_tab1, time_tab2, time_tab3 = st.tabs(["Time of Day", "Day of Week", "Seasonality"])
    
    with time_tab1:
        # Time of day analysis
        hour_data = calculate_conversion_rate(df, 'search_hour')
        
        fig = px.line(
            hour_data,
            x='search_hour',
            y='conversion_rate',
            title="Conversion Rate by Hour of Day",
            markers=True,
            height=400
        )
        
        fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='Hour of Day')
        st.plotly_chart(fig, use_container_width=True)
        
        # Also show search volume by hour
        fig = px.bar(
            hour_data,
            x='search_hour',
            y='searches',
            title="Search Volume by Hour of Day",
            height=400
        )
        
        fig.update_layout(yaxis_title='Number of Searches', xaxis_title='Hour of Day')
        st.plotly_chart(fig, use_container_width=True)
    
    with time_tab2:
        # Day of week analysis
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_data = calculate_conversion_rate(df, 'search_day')
        
        # Ensure correct order of days
        day_data['day_order'] = day_data['search_day'].map({day: i for i, day in enumerate(day_order)})
        day_data = day_data.sort_values('day_order')
        
        fig = px.bar(
            day_data,
            x='search_day',
            y='conversion_rate',
            title="Conversion Rate by Day of Week",
            color='conversion_rate',
            text=day_data['conversion_rate'].round(2).astype(str) + '%',
            height=400
        )
        
        fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='Day of Week')
        st.plotly_chart(fig, use_container_width=True)
    
    with time_tab3:
        # Month analysis
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        month_data = calculate_conversion_rate(df, 'search_month')
        
        # Ensure correct order of months
        month_data['month_order'] = month_data['search_month'].map({month: i for i, month in enumerate(month_order)})
        month_data = month_data.sort_values('month_order')
        
        fig = px.line(
            month_data,
            x='search_month',
            y='conversion_rate',
            title="Conversion Rate by Month",
            markers=True,
            height=400
        )
        
        fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='Month')
        st.plotly_chart(fig, use_container_width=True)
        
        # Show search volume by month
        fig = px.bar(
            month_data,
            x='search_month',
            y='searches',
            title="Search Volume by Month",
            height=400
        )
        
        fig.update_layout(yaxis_title='Number of Searches', xaxis_title='Month')
        st.plotly_chart(fig, use_container_width=True)
    
    st.write("""
    **Insights:**
    - Conversion rates vary significantly by time of day
    - Certain days of the week show higher conversion rates
    - There are clear seasonal patterns in both search volume and conversion rates
    - Time-based personalization and marketing can be optimized based on these patterns
    """)

def show_customer_segmentation(df):
    """
    Display customer segmentation visualizations
    """
    st.subheader("Customer Segmentation")
    
    st.write("""
    This section uses advanced segmentation to identify high-value customer groups.
    """)
    
    # Create a combined segmentation based on multiple factors
    segment_df = df.copy()
    
    # Create segment categories
    conditions = [
        (segment_df['is_mobile'] == 1) & (segment_df['is_package'] == 1),
        (segment_df['is_mobile'] == 1) & (segment_df['is_package'] == 0),
        (segment_df['is_mobile'] == 0) & (segment_df['is_package'] == 1),
        (segment_df['is_mobile'] == 0) & (segment_df['is_package'] == 0)
    ]
    
    choices = [
        'Mobile Package',
        'Mobile Non-Package',
        'Desktop Package',
        'Desktop Non-Package'
    ]
    
    segment_df['device_package'] = np.select(conditions, choices, default='Other')
    
    # Add travel party segmentation
    conditions = [
        (segment_df['srch_adults_cnt'] == 1) & (segment_df['srch_children_cnt'] == 0),
        (segment_df['srch_adults_cnt'] == 2) & (segment_df['srch_children_cnt'] == 0),
        (segment_df['srch_adults_cnt'] == 1) & (segment_df['srch_children_cnt'] > 0),
        (segment_df['srch_adults_cnt'] == 2) & (segment_df['srch_children_cnt'] > 0),
        (segment_df['srch_adults_cnt'] > 2)
    ]
    
    choices = [
        'Solo Traveler',
        'Couple',
        'Single Parent',
        'Family',
        'Group'
    ]
    
    segment_df['travel_party'] = np.select(conditions, choices, default='Other')
    
    # Add trip type based on duration
    conditions = [
        (segment_df['trip_duration'] <= 3),
        (segment_df['trip_duration'] <= 7),
        (segment_df['trip_duration'] > 7)
    ]
    
    choices = [
        'Short Break',
        'Standard Vacation',
        'Extended Trip'
    ]
    
    segment_df['trip_type'] = np.select(conditions, choices, default=np.nan)
    
    # Create multi-level segmentation
    segment_df['full_segment'] = segment_df['device_package'] + ' - ' + segment_df['travel_party'] + ' - ' + segment_df['trip_type']
    
    # Calculate conversion rates for the full segmentation
    # But only include segments with sufficient data
    segment_data = calculate_conversion_rate(segment_df.dropna(subset=['full_segment']), 'full_segment')
    top_segments = segment_data[segment_data['searches'] >= 100].sort_values('conversion_rate', ascending=False).head(15)
    
    fig = px.bar(
        top_segments,
        x='conversion_rate',
        y='full_segment',
        orientation='h',
        title="Top 15 Customer Segments by Conversion Rate",
        color='conversion_rate',
        text=top_segments['conversion_rate'].round(2).astype(str) + '%',
        height=600
    )
    
    fig.update_layout(xaxis_title='Conversion Rate (%)', yaxis_title='')
    st.plotly_chart(fig, use_container_width=True)
    
    # Create a bubble chart showing volume vs conversion
    fig = px.scatter(
        segment_data[segment_data['searches'] >= 50],
        x='searches',
        y='conversion_rate',
        size='bookings',
        hover_name='full_segment',
        title="Segment Volume vs. Conversion Rate",
        height=500,
        color='conversion_rate',
        log_x=True
    )
    
    fig.update_layout(xaxis_title='Search Volume (log scale)', yaxis_title='Conversion Rate (%)')
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("""
    **Insights:**
    - Desktop Non-Package searches for Solo Travelers and Short Breaks have the highest conversion rates
    - Mobile Package searches consistently show the lowest conversion rates across segments
    - Some high-converting segments have low search volume but represent growth opportunities
    - The bubble chart helps identify segments with the best balance of volume and conversion rate
    """)