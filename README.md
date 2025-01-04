# BTC Price and AVIV Ratio Analysis Script

This script fetches Bitcoin (BTC) price data and the AVIV Ratio, processes the data, merges them into a single dataset, and visualizes the log-transformed AVIV Ratio alongside BTC price over time. The goal of this indicator is to identify potential overbought and oversold zones within the typical 4 year cycle of Bitcoin.

Historical performance:

![image](https://github.com/user-attachments/assets/bb663021-1acc-4450-862c-f0bfd75b73d9)

## Features
- Fetches BTC price and AVIV Ratio data from APIs.
- Merges and processes data into a single dataset.
- Filters data to start from a specified date (`2014-01-01` by default).
- Generates a visualization of the AVIV Ratio and BTC price over time.

---

## Installation

### Prerequisites
- Python 3.7 or later.
- Ensure `pip` is installed on your system.

### Steps

#### MacOS
1. **Install Python**:
   - Use Homebrew:
     ```bash
     brew install python
     ```

2. **Install required libraries**
   ```
   pip install pandas numpy matplotlib requests
   ```

3. **Run the Script**
   ```
   python btc_aviv_analysis.py
   ```


