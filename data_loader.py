import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data():
    """
    Load and preprocess the travel.csv data
    """
    # Read the CSV file
    df = pd.read_csv('travel.csv')
    
    # Convert date columns to datetime
    df['date_time'] = pd.to_datetime(df['date_time'])
    df['srch_ci'] = pd.to_datetime(df['srch_ci'], errors='coerce')
    df['srch_co'] = pd.to_datetime(df['srch_co'], errors='coerce')
    
    # Add derived columns
    df['year_month'] = df['date_time'].dt.strftime('%Y-%m')
    
    # Calculate trip duration
    df['trip_duration'] = (df['srch_co'] - df['srch_ci']).dt.days
    
    # Calculate booking window (days between search and check-in)
    df['booking_window'] = (df['srch_ci'] - df['date_time']).dt.days
    
    # Create travel group types
    conditions = [
        (df['srch_adults_cnt'] == 1) & (df['srch_children_cnt'] == 0),
        (df['srch_adults_cnt'] == 2) & (df['srch_children_cnt'] == 0),
        (df['srch_adults_cnt'] == 1) & (df['srch_children_cnt'] > 0),
        (df['srch_adults_cnt'] == 2) & (df['srch_children_cnt'] > 0),
        (df['srch_adults_cnt'] > 2)
    ]
    
    choices = ['Solo', 'Couple', 'Single Parent', 'Family', 'Group']
    df['travel_group'] = np.select(conditions, choices, default='Other')
    
    # Map duration to categories
    duration_conditions = [
        (df['trip_duration'] <= 3),
        (df['trip_duration'] <= 7),
        (df['trip_duration'] <= 14),
        (df['trip_duration'] > 14)
    ]
    duration_choices = ['1-3 days', '4-7 days', '8-14 days', '15+ days']
    df['duration_category'] = np.select(duration_conditions, duration_choices, default=np.nan)
    
    # Map booking window to categories
    window_conditions = [
        (df['booking_window'] < 7),
        (df['booking_window'] < 14),
        (df['booking_window'] < 30),
        (df['booking_window'] < 60),
        (df['booking_window'] < 90),
        (df['booking_window'] >= 90)
    ]
    window_choices = ['0-6 days', '7-13 days', '14-29 days', '30-59 days', '60-89 days', '90+ days']
    df['window_category'] = np.select(window_conditions, window_choices, default=np.nan)
    
    # Device and package combination
    df['device_package'] = df['is_mobile'].map({1: 'Mobile', 0: 'Desktop'}) + ', ' + df['is_package'].map({1: 'Package', 0: 'Non-Package'})
    
    # Distance buckets
    distance_conditions = [
        (df['orig_destination_distance'] < 100),
        (df['orig_destination_distance'] < 500),
        (df['orig_destination_distance'] < 1000),
        (df['orig_destination_distance'] < 2000),
        (df['orig_destination_distance'] >= 2000)
    ]
    distance_choices = ['< 100', '100-500', '500-1000', '1000-2000', '> 2000']
    df['distance_category'] = np.select(distance_conditions, distance_choices, default=np.nan)
    
    return df