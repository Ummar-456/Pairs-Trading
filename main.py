

import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import quantstats as qs

# Import necessary libraries
from datetime import datetime

# Download price data for MSFT and AAPL for the last 10 years
end_date = '2025-04-24'
start_date = (datetime.strptime(end_date, '%Y-%m-%d') - pd.DateOffset(years=10)).strftime('%Y-%m-%d')

# Download price data and ensure they are Series
msft = yf.download('MSFT', start=start_date, end=end_date)['Close'].squeeze()
aapl = yf.download('AAPL', start=start_date, end=end_date)['Close'].squeeze()

# Verify they are now Series (optional check)
print("Type of msft after squeeze:", type(msft))
print("Type of aapl after squeeze:", type(aapl))

# Combine into a single DataFrame - this should now work correctly
data = pd.DataFrame({'MSFT': msft, 'AAPL': aapl})

# Step 3: Spread calculation using linear regression
X = sm.add_constant(data['AAPL'].astype(float))
y = data['MSFT'].astype(float)
model = sm.OLS(y, X).fit()
hedge_ratio = model.params['AAPL']

# Calculate the spread
data['Spread'] = data['MSFT'] - hedge_ratio * data['AAPL']


# Mean reversion strategy
# Compute the mean, standard deviation, and trading bands for the spread
spread_mean = data['Spread'].mean()
spread_std = data['Spread'].std()
upper_band = spread_mean + spread_std
lower_band = spread_mean - spread_std

# Entry and Exit Conditions
data['Position_MSFT'] = 0
data['Position_AAPL'] = 0

# Long Entry: Buy MSFT, Sell AAPL
data.loc[data['Spread'] < lower_band, 'Position_MSFT'] = 1
data.loc[data['Spread'] < lower_band, 'Position_AAPL'] = -hedge_ratio

# Short Entry: Sell MSFT, Buy AAPL
data.loc[data['Spread'] > upper_band, 'Position_MSFT'] = -1
data.loc[data['Spread'] > upper_band, 'Position_AAPL'] = hedge_ratio

# Carry forward positions (no exit signal, we hold the position)
data['Position_MSFT'] = data['Position_MSFT'].replace(0, np.nan).ffill()
data['Position_AAPL'] = data['Position_AAPL'].replace(0, np.nan).ffill()

# Calculate daily returns
data['Returns_MSFT'] = data['MSFT'].pct_change()
data['Returns_AAPL'] = data['AAPL'].pct_change()

# Total returns based on position
data['Strategy_Returns'] = (data['Position_MSFT'] * data['Returns_MSFT']) + (data['Position_AAPL'] * data['Returns_AAPL'])

# Total strategy returns on $20,000 investment
initial_investment = 20000
data['Cumulative_Strategy_Returns'] = initial_investment * (1 + data['Strategy_Returns']).cumprod()

# Plot cumulative strategy returns
plt.figure(figsize=(10, 6))
plt.plot(data['Cumulative_Strategy_Returns'], label='Strategy Returns')
plt.title('Pairs Trading Strategy Cumulative Returns')
plt.xlabel('Date')
plt.ylabel('Portfolio Value (USD)')
plt.legend()
plt.show()

# Strategy performance metrics using quantstats
qs.reports.metrics(data['Strategy_Returns'], mode='full')


