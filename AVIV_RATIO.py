#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime

# Function to fetch the list of BTC prices from the API
def fetch_btc_price_list():
    url = 'https://bitcoin-data.com/api/v1/btc-price'  # Replace with the actual API endpoint
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            return data
        else:
            print("Unexpected data format or empty list.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to fetch the MVRV Ratio from the API
def fetch_aviv_ratio_list():
    url = 'https://bitcoin-data.com/api/v1/aviv'  # Updated endpoint for MVRV Ratio
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            return data
        else:
            print("Unexpected data format or empty list.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def merge_btc_and_aviv(btc_price_data, aviv_ratio_data):
    """
    Merges BTC Price data and AVIV Ratio data into a pandas DataFrame, 
    truncating the time to start at the beginning of 2012.

    Parameters:
        btc_price_data (list of dict): List of BTC price data with keys 'd', 'unixTs', and 'btcPrice'.
        aviv_ratio_data (list of dict): List of AVIV ratio data with keys 'd', 'unixTs', and 'avivRatio'.

    Returns:
        pd.DataFrame: Merged DataFrame with columns 'DateTime', 'BTC price', and 'AVIV Ratio'.
    """
    # Convert to pandas DataFrames
    btc_df = pd.DataFrame(btc_price_data).rename(columns={'d': 'DateTime', 'btcPrice': 'BTC price'})
    aviv_df = pd.DataFrame(aviv_ratio_data).rename(columns={'d': 'DateTime', 'aviv': 'AVIV Ratio'})

    # Merge dataframes on 'DateTime'
    merged_df = pd.merge(btc_df[['DateTime', 'BTC price']], aviv_df[['DateTime', 'AVIV Ratio']], on='DateTime')

    # Convert 'DateTime' to datetime format and ensure numeric data
    merged_df['DateTime'] = pd.to_datetime(merged_df['DateTime'])
    merged_df['BTC price'] = pd.to_numeric(merged_df['BTC price'])
    merged_df['AVIV Ratio'] = pd.to_numeric(merged_df['AVIV Ratio'])

    # Filter to include only dates from the beginning of 2012 onward
    start_date = pd.Timestamp('2014-01-01')
    merged_df = merged_df[merged_df['DateTime'] >= start_date]

    return merged_df
        
def plot_aviv_ratio_and_btc_price(data):
    """
    Function to plot the log-transformed AVIV Ratio and BTC price.
    """
    # Perform the log transformation on the AVIV Ratio
    log_aviv_ratio = np.log(data['AVIV Ratio'])
    data['Log AVIV Ratio'] = log_aviv_ratio

    # Calculate thresholds for the top 2.5% and bottom 2.5%
    upper_threshold = np.percentile(log_aviv_ratio, 97.5)
    lower_threshold = np.percentile(log_aviv_ratio, 2.5)

    # Create the plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot Log-Transformed AVIV Ratio
    ax1.plot(data['DateTime'], log_aviv_ratio, label='Log Transformed AVIV Ratio', color='blue', alpha=0.7)
    ax1.fill_between(data['DateTime'], log_aviv_ratio, where=(log_aviv_ratio >= upper_threshold), color='red', alpha=0.3, label='AVIV Ratio Z-Score > 1.96')
    ax1.fill_between(data['DateTime'], log_aviv_ratio, where=(log_aviv_ratio <= lower_threshold), color='green', alpha=0.3, label='AVIV Ratio Z-Score < -1.96')
    ax1.set_ylim(3, None)  # Start AVIV Ratio at 3
    ax1.set_ylabel("Log AVIV Ratio")

    # Add a second y-axis for BTC price
    ax2 = ax1.twinx()
    ax2.plot(data['DateTime'], data['BTC price'], label='BTC Price', color='orange', alpha=0.7)
    ax2.set_yscale('log')
    ax2.set_ylabel("BTC Price (Log Scale)", color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')
    ax2.set_yticks([100, 1000, 10000, 100000])  # Set specific tick values
    ax2.get_yaxis().set_major_formatter(plt.ScalarFormatter())  # Use actual values, not power notation

    # Combine legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')

    # Title and grid
    plt.title("Log-Transformed AVIV Ratio and BTC Price Over Time")
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # Show the plot
    plt.show()

btc_price = fetch_btc_price_list()
aviv_ratio = fetch_aviv_ratio_list()
mod_data = merge_btc_and_aviv(btc_price, aviv_ratio)

# Call the plot function
plot_aviv_ratio_and_btc_price(mod_data)


# In[ ]:




