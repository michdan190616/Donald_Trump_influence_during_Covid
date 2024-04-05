import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt

def load_gtrend_df(pagename, filename):
    trend_data = []
    month_mapping = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    with open('{filename}/{filename}_googletrends.json'.format(filename=filename), 'r') as file:
        gtrends_dict = json.load(file)

        dates = []
        views = [int(data['values'][0]['value']) for data in gtrends_dict['interest_over_time']['timeline_data']]

        for data in gtrends_dict['interest_over_time']['timeline_data']:
            parts = data['date'].replace('–', ' '). replace(',', ' ').split()    
            dates.append(datetime(year=int(parts[2 if len(parts) == 6 else -1]), 
                                    month=month_mapping[parts[0]], 
                                    day=int(parts[1])))
        
        gtrends_df = pd.DataFrame({'Date': dates, 'Views': views})
        gtrends_df.set_index('Date', inplace=True)

    return gtrends_df

def load_wikipedia_df(folder, filename):
    with open(f'{folder}/{filename}/{filename}_wikipedia.json', 'r') as file:
        wikipedia_dict = json.load(file)

        dates = [item['timestamp'] for item in wikipedia_dict['items']]
        views = [item['views'] for item in wikipedia_dict['items']]

        wikipedia_df = pd.DataFrame({'Date': dates, 'Views': views})
        wikipedia_df['Date'] = pd.to_datetime(wikipedia_df['Date'], format='%Y%m%d00')
        wikipedia_df['Week'] = wikipedia_df['Date'] - pd.to_timedelta((wikipedia_df['Date'].dt.dayofweek+1) % 7, unit='D')
        weekly_wikipedia_df = wikipedia_df.groupby('Week').apply(lambda x: x.Views.sum()).reset_index(name='Views').set_index('Week')

        wikipedia_df.set_index('Date', inplace=True)

    return weekly_wikipedia_df, wikipedia_df