# This file will fetch the Turning movement count data from the ATSPM API and organize into a pandas dataframe.
# These functions will be used in the streamlit app.

import pandas as pd
import requests
import json
from datetime import timedelta

def fetch_tmc_data(signal_ids, start_date, end_date):
    # Fetch the data from the ATSPM API
    # Replace with the actual URL for the split failure API
    url = 'https://report-api-bdppc3riba-wm.a.run.app/v1/TurningMovementCounts/GetReportData'

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
    plans_dfs = []
    
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
                "binSize": "5"
            }

            # Make the API request
            response = requests.post(url, headers=headers, json=payload)

            # Check if the response is successful
            if response.status_code == 200:
                data = response.json()
                # Process each movement in the table
                for movement in data['table']:
                    # Create a base record with movement info
                    base_record = {
                        'locationIdentifier': location,
                        'direction': movement['direction'],
                        'movementType': movement['movementType']
                    }
                    
                    # Create records for each volume entry
                    for volume in movement['volumes']:
                        record = base_record.copy()
                        record['timestamp'] = volume['timestamp']
                        record['count'] = volume['value']
                        dfs.append(pd.DataFrame([record]))

                # get the time of day plans
                for chart in data['charts']:
                    # create base record
                    base_record_plans = {
                        'locationIdentifier': chart['locationIdentifier'],
                        'locationDescription': chart['locationDescription'],
                        'direction': chart['direction'],
                        'movementType': chart['movementType']
                    }

                    # create records for each time of day plan
                    for plan in chart['plans']:
                        record_plans = base_record_plans.copy()
                        record_plans['planNumber'] = plan['planNumber']
                        record_plans['planDescription'] = plan['planDescription']
                        record_plans['start'] = plan['start']
                        record_plans['end'] = plan['end']
                        plans_dfs.append(pd.DataFrame([record_plans]))

            else:
                print(f"Error fetching data for location {location} on {date}: {response.status_code}")
                continue
    
    # Combine all DataFrames at the end
    df = pd.concat(dfs, ignore_index=True)
    plans_df = pd.concat(plans_dfs, ignore_index=True)

    # Convert timestamp columns to datetime and remove milliseconds
    df['timestamp'] = pd.to_datetime(df['timestamp'].str.split('.').str[0])
    plans_df['start'] = pd.to_datetime(plans_df['start'].str.split('.').str[0])
    plans_df['end'] = pd.to_datetime(plans_df['end'].str.split('.').str[0])

    # Merge the dataframes using pandas merge_asof
    df = pd.merge_asof(
        df.sort_values('timestamp'),
        plans_df.sort_values('start'),
        by=['locationIdentifier', 'direction', 'movementType'],
        left_on='timestamp',
        right_on='start',
        direction='backward'
    )

    # Filter out rows where timestamp is outside the plan end time
    df = df[df['timestamp'] < df['end']]

    # Drop the start and end columns if you don't need them
    df = df.drop(['start', 'end'], axis=1)

    return df





# -------------------------------------------------------------------------------------------------
# Example usage

df = fetch_tmc_data(signal_ids=[7115, 7116], start_date='2024-11-06', end_date='2024-11-08')
print(df)
