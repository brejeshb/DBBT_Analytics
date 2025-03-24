import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def calculate_conversion_rate(df, group_by_col):
    """
    Calculate conversion rates for a given grouping column
    
    Parameters:
    df (pandas.DataFrame): The dataframe containing the data
    group_by_col (str): The column to group by
    
    Returns:
    pandas.DataFrame: A dataframe with searches, bookings, and conversion rates
    """
    grouped_data = df.groupby(group_by_col).agg(
        searches=('is_booking', 'count'),
        bookings=('is_booking', 'sum')
    ).reset_index()
    
    grouped_data['conversion_rate'] = (grouped_data['bookings'] / grouped_data['searches']) * 100
    
    return grouped_data

def plot_conversion_rates(data, x_col, title, color_col=None):
    """
    Create a bar chart of conversion rates
    
    Parameters:
    data (pandas.DataFrame): The dataframe containing the data
    x_col (str): The column to use for x-axis
    title (str): The chart title
    color_col (str, optional): The column to use for color
    
    Returns:
    plotly.graph_objects.Figure: A plotly figure
    """
    if color_col is None:
        color_col = x_col
        
    fig = px.bar(
        data,
        x=x_col,
        y='conversion_rate',
        color=color_col,
        text=data['conversion_rate'].round(2).astype(str) + '%',
        title=title,
        height=400
    )
    
    fig.update_layout(yaxis_title='Conversion Rate (%)', xaxis_title='')
    
    return fig

def format_percentage(value):
    """
    Format a number as a percentage string
    
    Parameters:
    value (float): The value to format
    
    Returns:
    str: The formatted percentage
    """
    return f"{value:.2f}%"

def get_monthly_data(df):
    """
    Prepare monthly trend data
    
    Parameters:
    df (pandas.DataFrame): The dataframe containing the data
    
    Returns:
    pandas.DataFrame: A dataframe with monthly aggregated data
    """
    monthly_data = df.groupby('year_month').agg(
        searches=('is_booking', 'count'),
        bookings=('is_booking', 'sum'),
        mobile_searches=('is_mobile', 'sum')
    ).reset_index()
    
    monthly_data['conversion_rate'] = (monthly_data['bookings'] / monthly_data['searches']) * 100
    monthly_data['mobile_percentage'] = (monthly_data['mobile_searches'] / monthly_data['searches']) * 100
    
    # Add year and month columns for easier filtering
    monthly_data['year'] = monthly_data['year_month'].str.split('-').str[0]
    monthly_data['month'] = monthly_data['year_month'].str.split('-').str[1]
    
    return monthly_data

def create_conversion_heatmap(df, rows, columns, values):
    """
    Create a heatmap of conversion rates
    
    Parameters:
    df (pandas.DataFrame): The dataframe containing the data
    rows (str): The column to use for rows
    columns (str): The column to use for columns
    values (str): The column to use for cell values
    
    Returns:
    plotly.graph_objects.Figure: A plotly figure
    """
    pivot_table = df.pivot_table(
        index=rows,
        columns=columns,
        values=values,
        aggfunc='mean'
    ).round(2)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale='Blues',
        text=pivot_table.values,
        texttemplate='%{text}%',
        textfont={"size":10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title=f'Conversion Rate (%) by {rows} and {columns}',
        height=500
    )
    
    return fig