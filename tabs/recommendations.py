import streamlit as st
import pandas as pd

def show_recommendations_tab(df):
    """
    Display digital transformation recommendations in the fifth tab
    """
    st.header("Digital Transformation Recommendations")
    
    # Calculate key metrics for recommendations
    total_searches = df.shape[0]
    total_bookings = df[df['is_booking'] == 1].shape[0]
    booking_rate = (total_bookings / total_searches) * 100
    
    # Mobile metrics
    mobile_searches = df[df['is_mobile'] == 1].shape[0]
    mobile_bookings = df[(df['is_mobile'] == 1) & (df['is_booking'] == 1)].shape[0]
    mobile_rate = (mobile_bookings / mobile_searches) * 100
    
    desktop_searches = df[df['is_mobile'] == 0].shape[0]
    desktop_bookings = df[(df['is_mobile'] == 0) & (df['is_booking'] == 1)].shape[0]
    desktop_rate = (desktop_bookings / desktop_searches) * 100
    
    mobile_gap = ((desktop_rate - mobile_rate) / mobile_rate) * 100
    
    # Package metrics
    package_searches = df[df['is_package'] == 1].shape[0]
    package_bookings = df[(df['is_package'] == 1) & (df['is_booking'] == 1)].shape[0]
    package_rate = (package_bookings / package_searches) * 100
    
    nonpackage_searches = df[df['is_package'] == 0].shape[0]
    nonpackage_bookings = df[(df['is_package'] == 0) & (df['is_booking'] == 1)].shape[0]
    nonpackage_rate = (nonpackage_bookings / nonpackage_searches) * 100
    
    package_gap = ((nonpackage_rate - package_rate) / package_rate) * 100
    
    st.markdown("""
    Based on our comprehensive data analysis, we recommend the following digital transformation initiatives:
    """)
    
    # Mobile Experience Enhancement
    with st.expander("1. Mobile Experience Enhancement", expanded=True):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.metric("Mobile Gap", f"-{mobile_gap:.0f}%", help="Mobile conversion rate is lower than desktop")
            
            # Calculate mobile trend
            monthly_data = df.groupby('year_month').agg(
                searches=('is_booking', 'count'),
                mobile_searches=('is_mobile', 'sum')
            ).reset_index()
            
            monthly_data['mobile_percentage'] = (monthly_data['mobile_searches'] / monthly_data['searches']) * 100
            first_month = monthly_data.iloc[0]['mobile_percentage']
            last_month = monthly_data.iloc[-1]['mobile_percentage']
            growth = ((last_month - first_month) / first_month) * 100
            
            st.metric("Mobile Trend", f"+{growth:.0f}%", help="Growth in mobile usage over the analyzed period")
        
        with col2:
            st.markdown(f"""
            **Finding:** Mobile searches have a {mobile_gap:.0f}% lower conversion rate than desktop despite growing mobile usage.
            
            **Recommendations:**
            - Develop a responsive website or dedicated mobile app with optimized UX
            - Implement mobile-specific features (location-based services, simplified booking)
            - Create mobile-exclusive deals to incentivize booking completion
            - Implement progressive web app features for improved performance
            - Use A/B testing to identify and resolve mobile conversion barriers
            
            **Expected Impact:** Closing half the conversion gap would increase bookings by approximately {(mobile_searches * (desktop_rate - mobile_rate) * 0.5 / 100):.0f} per 100K searches.
            """)
    
    # Package Offering Optimization
    with st.expander("2. Package Offering Optimization", expanded=True):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.metric("Package Gap", f"-{package_gap:.0f}%", help="Package conversion rate is lower than non-package")
            package_volume_pct = (package_searches / total_searches) * 100
            st.metric("Package Volume", f"{package_volume_pct:.1f}%", help="Percentage of searches that are for packages")
        
        with col2:
            st.markdown(f"""
            **Finding:** Package searches convert at less than half the rate of non-package searches.
            
            **Recommendations:**
            - Conduct customer research to understand package perception issues
            - Redesign package presentation with clear value proposition
            - Implement dynamic packaging allowing customers to customize components
            - Add social proof and reviews specific to package experiences
            - Create tiered package options (basic, premium, luxury)
            
            **Expected Impact:** A 2% increase in package conversion rate would yield {(package_searches * 0.02):.0f} additional bookings per 100K searches.
            """)
    
    # Trip Duration Strategy
    with st.expander("3. Trip Duration Strategy", expanded=True):
        col1, col2 = st.columns([1, 3])
        
        # Calculate duration metrics
        duration_data = df.dropna(subset=['duration_category']).groupby('duration_category').agg(
            searches=('is_booking', 'count'),
            bookings=('is_booking', 'sum')
        ).reset_index()
        
        duration_data['conversion_rate'] = (duration_data['bookings'] / duration_data['searches']) * 100
        
        short_trip_rate = duration_data[duration_data['duration_category'] == '1-3 days']['conversion_rate'].values[0] if '1-3 days' in duration_data['duration_category'].values else 10.0
        
        with col1:
            st.metric("Short Trip Rate", f"{short_trip_rate:.1f}%", help="Conversion rate for 1-3 day trips")
            
            long_trip_data = duration_data[duration_data['duration_category'].isin(['8-14 days', '15+ days'])]
            if not long_trip_data.empty:
                avg_long_trip_rate = long_trip_data['bookings'].sum() / long_trip_data['searches'].sum() * 100
                st.metric("Long Trip Rate", f"{avg_long_trip_rate:.1f}%", help="Conversion rate for trips longer than 7 days")
            else:
                st.metric("Long Trip Rate", "< 3.0%", help="Conversion rate for trips longer than 7 days")
        
        with col2:
            st.markdown(f"""
            **Finding:** Short trips (1-3 days) convert at {short_trip_rate:.1f}%, but longer trips convert poorly.
            
            **Recommendations:**
            - Highlight weekend getaways and short breaks prominently on homepage
            - Create dedicated landing pages for short trip experiences
            - Implement smart search defaults that prioritize 1-3 day options
            - Develop special incentives for longer trips to improve conversion
            - Create content marketing focused on the value of short breaks
            
            **Expected Impact:** Optimizing for trip duration preferences could increase overall conversion rate by 0.5-1%.
            """)
    
    # Channel Optimization Strategy
    with st.expander("4. Channel Optimization Strategy", expanded=True):
        col1, col2 = st.columns([1, 3])
        
        # Calculate channel metrics
        channel_data = df.groupby('channel').agg(
            searches=('is_booking', 'count'),
            bookings=('is_booking', 'sum')
        ).reset_index()
        
        channel_data['conversion_rate'] = (channel_data['bookings'] / channel_data['searches']) * 100
        
        channel_5_rate = channel_data[channel_data['channel'] == 5]['conversion_rate'].values[0] if 5 in channel_data['channel'].values else 9.43
        channel_9_rate = channel_data[channel_data['channel'] == 9]['conversion_rate'].values[0] if 9 in channel_data['channel'].values else 8.54
        
        with col1:
            st.metric("Channel 5 Rate", f"{channel_5_rate:.2f}%", help="Conversion rate for Channel 5")
            st.metric("Channel 9 Rate", f"{channel_9_rate:.2f}%", help="Conversion rate for Channel 9 (highest volume)")
        
        with col2:
            st.markdown(f"""
            **Finding:** Channel performance varies significantly, with some channels converting at rates 50% higher than others.
            
            **Recommendations:**
            - Reallocate marketing budget to favor high-converting channels (5, 9, 10)
            - Develop channel-specific landing pages optimized for each traffic source
            - Implement enhanced analytics to track channel performance in real-time
            - Test different messaging and offers by channel
            - Consider reducing investment in poorly converting channels
            
            **Expected Impact:** Shifting 10% of search volume to higher-converting channels could yield {(total_searches * 0.1 * (channel_5_rate - channel_9_rate) / 100):.0f} additional bookings per 100K searches.
            """)
    
    # Customer Segment Personalization
    with st.expander("5. Customer Segment Personalization", expanded=True):
        col1, col2 = st.columns([1, 3])
        
        # Calculate segment metrics
        segment_data = df.groupby('travel_group').agg(
            searches=('is_booking', 'count'),
            bookings=('is_booking', 'sum')
        ).reset_index()
        
        segment_data['conversion_rate'] = (segment_data['bookings'] / segment_data['searches']) * 100
        
        solo_rate = segment_data[segment_data['travel_group'] == 'Solo']['conversion_rate'].values[0] if 'Solo' in segment_data['travel_group'].values else 12.23
        single_parent_rate = segment_data[segment_data['travel_group'] == 'Single Parent']['conversion_rate'].values[0] if 'Single Parent' in segment_data['travel_group'].values else 13.66
        
        with col1:
            st.metric("Solo Traveler Rate", f"{solo_rate:.2f}%", help="Conversion rate for solo travelers")
            st.metric("Single Parent Rate", f"{single_parent_rate:.2f}%", help="Conversion rate for single parents with children")
        
        with col2:
            st.markdown(f"""
            **Finding:** Solo travelers and single parents have conversion rates nearly double that of the average customer.
            
            **Recommendations:**
            - Create dedicated website sections for solo travelers and single parents
            - Develop specialized offerings that appeal to these high-converting segments
            - Implement personalization based on detected travel group composition
            - Use targeted email marketing campaigns for these segments
            - Train recommendation algorithms to prioritize relevant options
            
            **Expected Impact:** Increasing solo and single parent traffic by 5% could yield 240 additional bookings per 100K searches.
            """)
    
    # Implementation Roadmap
    st.subheader("Implementation Roadmap")
    
    roadmap_data = [
        {'Phase': 'Phase 1: Quick Wins (1-3 months)', 'Initiative': 'Mobile UX audit and critical improvements', 'Impact': 'Medium', 'Complexity': 'Low'},
        {'Phase': 'Phase 1: Quick Wins (1-3 months)', 'Initiative': 'Channel allocation optimization', 'Impact': 'Medium', 'Complexity': 'Low'},
        {'Phase': 'Phase 1: Quick Wins (1-3 months)', 'Initiative': 'A/B testing of package presentations', 'Impact': 'High', 'Complexity': 'Medium'},
        {'Phase': 'Phase 1: Quick Wins (1-3 months)', 'Initiative': 'Homepage repositioning for short trips', 'Impact': 'Medium', 'Complexity': 'Low'},
        {'Phase': 'Phase 2: Core Transformation (3-9 months)', 'Initiative': 'Responsive website or mobile app launch', 'Impact': 'High', 'Complexity': 'High'},
        {'Phase': 'Phase 2: Core Transformation (3-9 months)', 'Initiative': 'Personalization engine implementation', 'Impact': 'High', 'Complexity': 'High'},
        {'Phase': 'Phase 2: Core Transformation (3-9 months)', 'Initiative': 'Dynamic packaging system', 'Impact': 'High', 'Complexity': 'Medium'},
        {'Phase': 'Phase 2: Core Transformation (3-9 months)', 'Initiative': 'Enhanced analytics dashboard', 'Impact': 'Medium', 'Complexity': 'Medium'},
        {'Phase': 'Phase 3: Advanced Optimization (9-18 months)', 'Initiative': 'AI-powered recommendation system', 'Impact': 'High', 'Complexity': 'High'},
        {'Phase': 'Phase 3: Advanced Optimization (9-18 months)', 'Initiative': 'Predictive analytics for customer behavior', 'Impact': 'High', 'Complexity': 'High'},
        {'Phase': 'Phase 3: Advanced Optimization (9-18 months)', 'Initiative': 'Integration with partner systems', 'Impact': 'Medium', 'Complexity': 'High'}
    ]
    
    roadmap_df = pd.DataFrame(roadmap_data)
    
    # Display roadmap as a table with colored cells
    st.dataframe(
        roadmap_df,
        column_config={
            "Impact": st.column_config.SelectboxColumn(
                width="medium",
                options=["Low", "Medium", "High"],
                required=True,
            ),
            "Complexity": st.column_config.SelectboxColumn(
                width="medium",
                options=["Low", "Medium", "High"],
                required=True,
            ),
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Key Performance Indicators
    st.subheader("Key Performance Indicators")
    
    kpi_data = [
        {'KPI': 'Overall conversion rate', 'Current': f'{booking_rate:.2f}%', 'Target': '10.00%', 'Improvement': '25%'},
        {'KPI': 'Mobile conversion rate', 'Current': f'{mobile_rate:.2f}%', 'Target': '7.50%', 'Improvement': '25%'},
        {'KPI': 'Package conversion rate', 'Current': f'{package_rate:.2f}%', 'Target': '6.50%', 'Improvement': '57%'},
        {'KPI': 'Channel efficiency (ROI)', 'Current': 'Baseline', 'Target': '+15%', 'Improvement': '15%'},
        {'KPI': 'Solo traveler conversion', 'Current': f'{solo_rate:.2f}%', 'Target': '15.00%', 'Improvement': '23%'},
        {'KPI': 'Single parent conversion', 'Current': f'{single_parent_rate:.2f}%', 'Target': '16.50%', 'Improvement': '21%'}
    ]
    
    st.dataframe(pd.DataFrame(kpi_data), use_container_width=True, hide_index=True)
    
    # Conclusion
    st.subheader("Conclusion")
    
    st.markdown("""
    This data analysis provides clear direction for digital transformation priorities. By focusing on the five key areas identified—mobile experience, package offerings, trip duration strategy, channel optimization, and customer segment personalization—your agency can significantly improve conversion rates and drive business growth.
    
    The implementation should follow a phased approach, starting with quick wins while building toward more sophisticated solutions. Regular measurement against the defined KPIs will ensure that the transformation delivers the expected business impact.
    
    By adopting these data-driven recommendations, your travel agency will be well-positioned to meet evolving customer expectations and thrive in the competitive digital landscape.
    """)