import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_user_device_tab(df):
    """
    Display user and device analysis in the second tab
    """
    st.header("User & Device Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Device comparison
        st.subheader("Device Comparison")
        device_data = df.groupby('is_mobile').agg(
            searches=('is_booking', 'count'),
            bookings=('is_booking', 'sum')
        ).reset_index()
        
        device_data['conversion_rate'] = (device_data['bookings'] / device_data['searches']) * 100
        device_data['is_mobile'] = device_data['is_mobile'].map({0: 'Desktop', 1: 'Mobile'})
        device_data = device_data.rename(columns={'is_mobile': 'device'})
        
        fig = px.bar(
            device_data, 
            x='device', 
            y='conversion_rate',
            color='device',
            text=device_data['conversion_rate'].round(2).astype(str) + '%',
            title='Conversion Rate by Device Type',
            height=400
        )
        
        fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        - Desktop conversion rate: **{device_data[device_data['device'] == 'Desktop']['conversion_rate'].values[0]:.2f}%**
        - Mobile conversion rate: **{device_data[device_data['device'] == 'Mobile']['conversion_rate'].values[0]:.2f}%**
        - Gap: **{(device_data[device_data['device'] == 'Desktop']['conversion_rate'].values[0] - device_data[device_data['device'] == 'Mobile']['conversion_rate'].values[0]):.2f}%**
        """)
    
    with col2:
        # Mobile usage trend
        st.subheader("Mobile Usage Trend")
        
        # Group by year and month for mobile trend
        monthly_data = df.groupby('year_month').agg(
            searches=('is_booking', 'count'),
            mobile_searches=('is_mobile', 'sum')
        ).reset_index()
        
        monthly_data['mobile_percentage'] = (monthly_data['mobile_searches'] / monthly_data['searches']) * 100
        
        fig = px.line(
            monthly_data, 
            x='year_month', 
            y='mobile_percentage',
            labels={'year_month': 'Month', 'mobile_percentage': 'Mobile Usage (%)'},
            title='Mobile Usage Percentage Over Time',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate growth in mobile usage
        first_month = monthly_data.iloc[0]['mobile_percentage']
        last_month = monthly_data.iloc[-1]['mobile_percentage']
        growth = ((last_month - first_month) / first_month) * 100
        
        st.markdown(f"""
        - Mobile usage increased from **{first_month:.2f}%** to **{last_month:.2f}%** over the period
        - Overall growth: **{growth:.1f}%**
        - Peak mobile usage in December 2014: **{monthly_data['mobile_percentage'].max():.2f}%**
        """)
    
    # Package vs Non-package
    st.subheader("Package vs. Non-Package Performance")
    package_data = df.groupby('is_package').agg(
        searches=('is_booking', 'count'),
        bookings=('is_booking', 'sum')
    ).reset_index()
    
    package_data['conversion_rate'] = (package_data['bookings'] / package_data['searches']) * 100
    package_data['is_package'] = package_data['is_package'].map({0: 'Non-package', 1: 'Package'})
    package_data = package_data.rename(columns={'is_package': 'package_type'})
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Volume comparison
        fig = px.pie(
            package_data, 
            values='searches', 
            names='package_type',
            title='Search Volume Distribution',
            hole=0.4,
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Conversion rate comparison
        fig = px.bar(
            package_data, 
            x='package_type', 
            y='conversion_rate',
            color='package_type',
            text=package_data['conversion_rate'].round(2).astype(str) + '%',
            title='Conversion Rate by Package Type',
            height=350
        )
        fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='')
        st.plotly_chart(fig, use_container_width=True)
    
    # Combined device and package analysis
    st.subheader("Combined Device and Package Analysis")
    
    # First create the combination column (already done in data loading)
    combined_data = df.groupby('device_package').agg(
        searches=('is_booking', 'count'),
        bookings=('is_booking', 'sum')
    ).reset_index()
    
    combined_data['conversion_rate'] = (combined_data['bookings'] / combined_data['searches']) * 100
    
    fig = px.bar(
        combined_data,
        x='device_package',
        y='conversion_rate',
        color='device_package',
        text=combined_data['conversion_rate'].round(2).astype(str) + '%',
        title='Conversion Rate by Device and Package Combination',
        height=400
    )
    
    fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='')
    st.plotly_chart(fig, use_container_width=True)
    
    best_combo = combined_data.loc[combined_data['conversion_rate'].idxmax()]
    worst_combo = combined_data.loc[combined_data['conversion_rate'].idxmin()]
    
    st.markdown(f"""
    - Best combination: **{best_combo['device_package']}** with **{best_combo['conversion_rate']:.2f}%** conversion
    - Worst combination: **{worst_combo['device_package']}** with **{worst_combo['conversion_rate']:.2f}%** conversion
    - This analysis shows how device type and package offering interact, revealing that packages perform poorly across both devices.
    """)
    
    # Travel group analysis
    st.subheader("Travel Group Analysis")
    
    group_data = df.groupby('travel_group').agg(
        searches=('is_booking', 'count'),
        bookings=('is_booking', 'sum')
    ).reset_index()
    
    group_data['conversion_rate'] = (group_data['bookings'] / group_data['searches']) * 100
    group_data['percentage_of_searches'] = (group_data['searches'] / group_data['searches'].sum()) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Volume by travel group
        fig = px.pie(
            group_data, 
            values='searches', 
            names='travel_group',
            title='Search Volume by Travel Group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Conversion by travel group
        fig = px.bar(
            group_data.sort_values('conversion_rate', ascending=False), 
            x='travel_group', 
            y='conversion_rate',
            color='travel_group',
            text=group_data['conversion_rate'].round(2).astype(str) + '%',
            title='Conversion Rate by Travel Group',
            height=400
        )
        fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='')
        st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("Analysis of User Segments"):
        st.markdown("""
        - **Solo Travelers and Single Parents**: These segments have significantly higher conversion rates (12.23% and 13.66% respectively).
        - **Couples**: Despite being the largest segment (50.74% of searches), they convert at only 6.98%.
        - **Opportunity**: There's a clear opportunity to develop specialized offerings for solo travelers and single parents.
        - **Targeting Strategy**: While couples represent volume, focusing on high-converting segments can drive efficiency.
        """)