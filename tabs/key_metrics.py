import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_key_metrics_tab(df):
    """
    Display key metrics and trend analysis in the first tab
    """
    st.header("Key Metrics & Trends")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    total_searches = df.shape[0]
    total_bookings = df[df['is_booking'] == 1].shape[0]
    booking_rate = (total_bookings / total_searches) * 100
    
    col1.metric("Total Searches", f"{total_searches:,}")
    col2.metric("Total Bookings", f"{total_bookings:,}")
    col3.metric("Conversion Rate", f"{booking_rate:.2f}%")
    col4.metric("Mobile Searches", f"{df[df['is_mobile'] == 1].shape[0] / total_searches:.2f}%")
    
    # Monthly trend analysis
    st.subheader("Monthly Trends (2013-2014)")
    
    # Group by year and month
    monthly_data = df.groupby('year_month').agg(
        searches=('is_booking', 'count'),
        bookings=('is_booking', 'sum'),
        mobile_searches=('is_mobile', 'sum')
    ).reset_index()
    
    monthly_data['conversion_rate'] = (monthly_data['bookings'] / monthly_data['searches']) * 100
    monthly_data['mobile_percentage'] = (monthly_data['mobile_searches'] / monthly_data['searches']) * 100
    
    # Plot conversion rate and search volume
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_data['year_month'], 
        y=monthly_data['searches'], 
        name='Searches',
        mode='lines',
        line=dict(color='royalblue')
    ))
    fig.add_trace(go.Scatter(
        x=monthly_data['year_month'], 
        y=monthly_data['conversion_rate'], 
        name='Conversion Rate (%)',
        mode='lines',
        line=dict(color='green'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='Monthly Search Volume and Conversion Rate',
        xaxis_title='Month',
        yaxis=dict(title='Number of Searches'),
        yaxis2=dict(
            title='Conversion Rate (%)',
            overlaying='y',
            side='right',
            range=[0, 12]  # Set range for conversion rate
        ),
        hovermode='x unified',
        legend=dict(x=0.01, y=0.99),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Seasonal pattern comparison (2013 vs 2014)
    monthly_data['year'] = monthly_data['year_month'].str.split('-').str[0]
    monthly_data['month'] = monthly_data['year_month'].str.split('-').str[1]
    
    st.subheader("Seasonal Patterns Comparison (2013 vs 2014)")
    fig = px.line(
        monthly_data, 
        x='month', 
        y='conversion_rate', 
        color='year',
        labels={'month': 'Month', 'conversion_rate': 'Conversion Rate (%)', 'year': 'Year'},
        title='Conversion Rate by Month - Year over Year Comparison',
        markers=True,
        height=400
    )
    
    fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray':['01','02','03','04','05','06','07','08','09','10','11','12']})
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("Analysis of Monthly Trends"):
        st.markdown("""
        - **Search Volume Growth**: There was a significant increase in search volume from 2013 to 2014, indicating growing market interest.
        - **Conversion Rate Decline**: Despite increased search volume, conversion rates showed a declining trend in 2014 compared to 2013.
        - **Seasonality**: August-September showed the highest conversion rates in 2013 (10%+), while 2014 had more consistent but lower rates.
        - **Mobile Growth**: Mobile usage showed a steady increase over the two-year period, reaching 16.21% by December 2014.
        """)
        
    return monthly_data  # Return for potential use in other tabs