import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt

def load_gtrend_df(folder, filename):
    month_mapping = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    with open(f'{folder}/{filename}/{filename}_googletrends.json', 'r') as file:
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

import json
import pandas as pd
from datetime import datetime

def load_gtrend_hourly_df(folder, filename, alias):
    month_mapping = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    with open(f'{folder}/{filename}/{filename}_googletrends_{alias}.json', 'r') as file:
        gtrends_dict = json.load(file)

        dates = []
        views = [int(data['values'][0]['value']) for data in gtrends_dict['interest_over_time']['timeline_data']]

        for data in gtrends_dict['interest_over_time']['timeline_data']:
            parts = data['date'].replace(' at ', ' ').replace(',', '').split()

            month = month_mapping[parts[0]]
            day = int(parts[1])
            year = int(parts[2])
            
            time_parts = parts[3].split(':')
            hour = int(time_parts[0])

            if parts[4].upper() == 'PM':
                if hour != 12:
                    hour += 12
            else:
                if hour == 12:
                    hour -= 12

            dates.append(datetime(year=year, month=month, day=day, hour=hour))
        
        gtrends_df = pd.DataFrame({'Date': dates, 'Views': views})
        gtrends_df.set_index('Date', inplace=True)

    return gtrends_df