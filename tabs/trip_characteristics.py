import streamlit as st
import pandas as pd
import plotly.express as px

def show_trip_characteristics_tab(df):
    """
    Display trip characteristics analysis in the third tab
    """
    st.header("Trip Characteristics Analysis")
    
    # Trip duration analysis
    st.subheader("Trip Duration Analysis")
    
    # Use the duration categories created during data loading
    duration_data = df.dropna(subset=['duration_category']).groupby('duration_category').agg(
        searches=('is_booking', 'count'),
        bookings=('is_booking', 'sum')
    ).reset_index()
    
    duration_data['conversion_rate'] = (duration_data['bookings'] / duration_data['searches']) * 100
    
    fig = px.bar(
        duration_data,
        x='duration_category',
        y=['searches', 'bookings'], 
        barmode='group',
        title='Search Volume and Bookings by Trip Duration',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    fig = px.bar(
        duration_data,
        x='duration_category',
        y='conversion_rate',
        color='duration_category',
        text=duration_data['conversion_rate'].round(2).astype(str) + '%',
        title='Conversion Rate by Trip Duration',
        height=400
    )
    
    fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='Trip Duration')
    st.plotly_chart(fig, use_container_width=True)
    
    # Booking window analysis
    st.subheader("Booking Window Analysis")
    
    # Use window categories created during data loading
    window_data = df.dropna(subset=['window_category']).groupby('window_category').agg(
        searches=('is_booking', 'count'),
        bookings=('is_booking', 'sum')
    ).reset_index()
    
    window_data['conversion_rate'] = (window_data['bookings'] / window_data['searches']) * 100
    
    fig = px.bar(
        window_data,
        x='window_category',
        y='conversion_rate',
        color='window_category',
        text=window_data['conversion_rate'].round(2).astype(str) + '%',
        title='Conversion Rate by Booking Window',
        height=400
    )
    
    fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='Days Between Search and Check-in')
    st.plotly_chart(fig, use_container_width=True)
    
    # Distance analysis
    st.subheader("Travel Distance Analysis")
    
    # Use distance categories created during data loading
    distance_data = df.dropna(subset=['distance_category']).groupby('distance_category').agg(
        searches=('is_booking', 'count'),
        bookings=('is_booking', 'sum')
    ).reset_index()
    
    distance_data['conversion_rate'] = (distance_data['bookings'] / distance_data['searches']) * 100
    
    fig = px.bar(
        distance_data,
        x='distance_category',
        y='conversion_rate',
        color='distance_category',
        text=distance_data['conversion_rate'].round(2).astype(str) + '%',
        title='Conversion Rate by Origin-Destination Distance',
        height=400
    )
    
    fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='Distance (km)')
    st.plotly_chart(fig, use_container_width=True)
    
    # Top hotel markets
    st.subheader("Top Hotel Markets Analysis")
    
    market_data = df.groupby('hotel_market').agg(
        searches=('is_booking', 'count'),
        bookings=('is_booking', 'sum')
    ).reset_index()
    
    market_data['conversion_rate'] = (market_data['bookings'] / market_data['searches']) * 100
    top_markets = market_data[market_data['searches'] >= 100].sort_values('conversion_rate', ascending=False).head(10)
    
    fig = px.bar(
        top_markets,
        x='hotel_market',
        y='conversion_rate',
        color='conversion_rate',
        text=top_markets['conversion_rate'].round(2).astype(str) + '%',
        title='Top 10 Hotel Markets by Conversion Rate',
        height=400
    )
    
    fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='Hotel Market ID', coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("Analysis of Trip Characteristics"):
        st.markdown("""
        - **Short Trip Preference**: Trips of 1-3 days have the highest conversion rate (10%), significantly higher than longer trips.
        - **Booking Window**: Last-minute bookings (0-6 days before check-in) and advance bookings (30-59 days) show higher conversion rates.
        - **Distance Impact**: Shorter distances generally convert better, with trips under 100km having the highest conversion rate.
        - **Market Opportunity**: There are specific hotel markets with conversion rates 2-3x higher than average, suggesting targeting opportunities.
        - **Recommendation**: Focus digital marketing on short trips, implement dynamic pricing for last-minute bookings, and develop targeted campaigns for high-converting markets.
        """)