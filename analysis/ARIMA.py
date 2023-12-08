import pandas as pd

df = pd.read_csv('/content/data.csv')

df = df.set_index('Date')
df.index = pd.to_datetime(df.index)

# MOVING AVERAGE and AUTOREGRESSION
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
length = 500
pred_length = 4
MA_model = ARIMA(df['Value'][-length:], order=(0, 0, 1))
AR_model = ARIMA(df['Value'][-length:], order=(1, 0, 0))
MA_fit = MA_model.fit()
AR_fit = AR_model.fit()
MA_prediction = MA_fit.predict(0, length+pred_length)
AR_prediction = AR_fit.predict(0, length+pred_length)

# plot
dates = df.index[-length:]
plt.plot(dates, df['Value'][-length:])
dates = df.index[-length:].append(pd.date_range('2023-12-07', '2023-12-13', freq='B'))
plt.plot(dates, AR_prediction)
plt.plot(dates, MA_prediction)
