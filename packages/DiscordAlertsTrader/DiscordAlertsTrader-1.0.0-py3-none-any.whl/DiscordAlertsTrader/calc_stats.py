import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime
import numpy as np

def parse_option_info(symbol):
    option_inf = {
    "symbol": symbol.split('_')[0],
    "date": symbol.split('_')[1][:6],
    "otype": symbol.split('_')[1][6],
    "strike": symbol.split('_')[1][7:],
    }
    return option_inf

def calculate_days_to_expiration(row):
    option_date_str = parse_option_info(row['Symbol'])['date']
    option_date = datetime.strptime(option_date_str, '%m%d%y').date()
    expiration_date = pd.to_datetime(row['Date']).date()
    days_to_expiration = (option_date - expiration_date).days
    return days_to_expiration

port = pd.read_csv('data/analysts_portfolio.csv')
port = port[(port['isOpen']==0) & (port['Asset']=='option')]
port['days_to_expiration'] = port.apply(calculate_days_to_expiration, axis=1)
print("Keeping only trades with 0 dtoe, removing: ", (port['days_to_expiration']!=0).sum())
port = port[port['days_to_expiration']==0]

stats = port['TrailStats']
stats = stats[~stats.isna()]


percentage_values = []
time_values = []

stats_parsed = pd.DataFrame(columns="min min_time max max_time TS2 TS2_time TS3 TS3_time TS4 TS4_time TS5 TS5_time".split(' '))
for string in stats:
    # Extract the percentage using regular expression
    stat = []
    min_match = re.search(r"min,(-?\d+\.\d+)%.*?in ((\d+ days )?(\d{2}:\d{2}:\d{2}))", string)
    if min_match:
        min_percentage = float(min_match.group(1))
        min_time = min_match.group(2)
    else:
        min_percentage = None
        min_time = None

    # Extract max percentage and time
    max_match = re.search(r"max,(-?\d+\.\d+)%.*?in ((\d+ days )?(\d{2}:\d{2}:\d{2}))", string)
    if max_match:
        max_percentage = float(max_match.group(1))
        max_time = max_match.group(2)
    else:
        max_percentage = None
        max_time = None

    stat = [min_percentage, min_time, max_percentage, max_time]

    # Extract TS values and their respective percentages and times
    ts_matches = re.findall(r"TS:(\d+\.\d+),(-?\d+\.\d+)%.*?in ((\d+ days )?(\d{2}:\d{2}:\d{2}))", string)
    ts_data = {}
    for ts_match in ts_matches:
        ts_value = ts_match[0]
        ts_percentage = float(ts_match[1])
        ts_time = ts_match[2]
        ts_data[ts_value] = {'percentage': ts_percentage, 'time': ts_time}
        stat.extend([ts_percentage, ts_time])
    
    stat += [None] * (len(stats_parsed.columns) - len(stat))
    stats_parsed.loc[len(stats_parsed)] = stat

count = (stats_parsed['min_time'] < stats_parsed['max_time']).sum()


stats_parsed['min'].hist(bins=100, alpha=.5, color='b', label='min')
stats_parsed['max'].hist(bins=100, alpha=.5, color='r', label='max')
stats_parsed['TS5'].hist(bins=100, alpha=.5, color='g', label='TS5')
stats_parsed['TS4'].hist(bins=100, alpha=.5, color='k', label='TS4')
stats_parsed['TS3'].hist(bins=100, alpha=.5, color='m', label='TS3')
stats_parsed['TS2'].hist(bins=100, alpha=.5, color='y', label='TS2')
plt.legend()
plt.show(block=False)


# Calculate the largest TS value for each row
stats_parsed['largest_TS'] = stats_parsed.apply(
    lambda row: row['TS5'] if not np.isnan(row['TS5'])
    else row['TS4'] if not np.isnan(row['TS4'])
    else row['TS3'] if not np.isnan(row['TS3'])
    else row['TS2'], axis=1
)

pd.to_timedelta(stats_parsed['TS2_time']).mean()
# Calculate the mean of the largest TS values
mean_largest_TS = stats_parsed['largest_TS'].mean()

ts = ['TS2', 'TS3', 'TS4', 'TS5']
print('total trades:', len(stats_parsed))
for t in ts:
    print(f"Count for {t}: larger than 0: { (stats_parsed[t] > 0).sum()}/{len(stats_parsed.loc[~stats_parsed[t].isna(),t])}, mean: {round(stats_parsed[t].mean(),2)}")
    
