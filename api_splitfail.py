import pandas as pd
import requests
import json
from datetime import timedelta

def fetch_splitfail_data(signal_ids, start_date, end_date):
    # Fetch the data from the ATSPM API
    # Replace with the actual URL for the split failure API
    url = 'https://report-api-bdppc3riba-wm.a.run.app/v1/SplitFail/GetReportData'

    # If there are any specific headers, like authorization tokens, add them here
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        # Add other headers you might need
        'Origin': 'https://atspm-website-bdppc3riba-wm.a.run.app',
        'Referer': 'https://atspm-website-bdppc3riba-wm.a.run.app/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Ch-Ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"'
    }

    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Location needs to be a string
    signal_ids = [str(signal_id) for signal_id in signal_ids]

    # Create empty list before loops
    dfs = []
    
    for location in signal_ids:
        for date in date_range:
            # construct start and end datetime strings
            start = date.strftime('%Y-%m-%dT00:00:00')
            end = (date + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00')

            # Payload for the request
            payload = {
                "locationIdentifier": location,
                "start": start,
                "end": end,
                "firstSecondsOfRed": "5",
                "showAvgLines": True,
                "showFailLines": True,
                "showPercentFailLines": False
            }

            # Make the API request
            response = requests.post(url, headers=headers, json=payload)

            # Check if the response is successful
            if response.status_code == 200:
                data = response.json()
                # Process each phase in the response
                for phase in data:
                    # Create a base record with phase info
                    base_record = {
                        'locationIdentifier': phase['locationIdentifier'],
                        'locationDescription': phase['locationDescription'],
                        'phaseNumber': phase['phaseNumber'],
                        'phaseType': phase['phaseType'],
                        'approachDescription': phase['approachDescription']
                    }
                    
                    

                    # Process time of day plans
                    for plan in phase['plans']:
                        record_plans = base_record.copy()
                        record_plans.update({
                            'planNumber': plan['planNumber'],
                            'planDescription': plan['planDescription'],
                            'start': plan['start'],
                            'end': plan['end'],
                            'totalCycles': plan['totalCycles'],
                            'failsInPlan': plan['failsInPlan'],
                            'percentFails': plan['percentFails']
                        })
                        dfs.append(pd.DataFrame([record_plans]))

            else:
                print(f"Error fetching data for location {location} on {date}: {response.status_code}")
                continue
    
    # Combine all DataFrames at the end
    df = pd.concat(dfs, ignore_index=True)

    return df



# -------------------------------------------------------------------------------------------------
# Example usage

# df = fetch_splitfail_data(signal_ids=[7115], start_date='2024-11-06', end_date='2024-11-08')
# print(df)
