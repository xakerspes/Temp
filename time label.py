import numpy as np
import matplotlib.pyplot as plt
#  Подключаем модуль управления тиками:
import matplotlib.ticker as ticker

from matplotlib import dates

df2["Time"]=pd.to_datetime(df2["Time"])
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
%matplotlib inline
df2.set_index('Time',inplace=True)
fig, ax = plt.subplots(figsize=(15,7))
df2.plot(ax=ax)
ax.xaxis.set_major_locator(mdates.WeekdayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
