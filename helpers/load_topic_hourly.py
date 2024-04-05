import os
from datetime import datetime, timedelta
from serpapi import GoogleSearch
import json


# REQUEST
def request_gtrends(folder, filename, alias, pagename, start_time, end_time):
    saving_path = f'../{folder}/{filename}/{filename}_googletrends_{alias}.json'
    start_time = start_time
    end_time = end_time
    params = {
        "engine": "google_trends",
        "q": pagename,
        "data_type": "TIMESERIES",
        "cat": "0",
        "api_key": "b640c5aec03eb8f4a6df2c3d12ffb238b6cbaa645d10a91e00642ddcd2bec9f3",
        "date": f"{start_time.strftime('%Y-%m-%dT%H')} {end_time.strftime('%Y-%m-%dT%H')}",
        "tz": "0"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    json_object = json.dumps(results)

    with open(saving_path, 'w') as f:
        f.write(json_object)
