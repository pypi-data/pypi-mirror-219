import pandas as pd
import pandas as pd
from datetime import datetime, timedelta

def next_series_data(df):
    # Create an empty DataFrame to store the adjusted averages
    adjusted_moving_df = pd.DataFrame()

    # Iterate over every 3 rows in the original DataFrame
    for i in range(0, len(df), 3):
        # Select the current three rows
        rows = df.iloc[i:i+3]

        # Calculate the adjusted averages for the current three rows
        moving_averages = []
        for column in df.columns:
            r1 = rows[column].iloc[0]
            r2 = rows[column].iloc[1]
            r3 = rows[column].iloc[2]

            # Calculate the initial average for the current column
            average = (r1 + r2 + r3) / 3

            # Adjust the average until the absolute difference is less than 5
            while abs(average - r3) >= 5:
                if average > r3:
                    average -= 0.01  # Decrease the average by 0.01
                else:
                    average += 0.01  # Increase the average by 0.01

            moving_averages.append(average)

        # Append the adjusted averages to the new DataFrame
        adjusted_moving_df = pd.concat([adjusted_moving_df, pd.DataFrame([moving_averages], columns=df.columns)], ignore_index=True)

    return adjusted_moving_df




def combine_json_data(json_files):
    combined_df = pd.DataFrame()

    for index, json_data in enumerate(json_files):
        data = json_data['data']['10751']
        df = pd.DataFrame(data)
        df['ts'] = pd.to_datetime(df['ts'])
        df['ts'] = df['ts'].dt.strftime('%H:%M')
        df = df.drop('status', axis=1)
        
        cols = df.columns.tolist()
        cols = ['ts'] + [col for col in cols if col != 'ts']
        df = df[cols]
        
        if combined_df.empty:
            combined_df = df[['ts', 'value']].rename(columns={'value': 'n-3'})
        else:
            column_name = 'n-' + str(len(json_files) - index)
            combined_df = pd.merge(combined_df, df[['ts', 'value']].rename(columns={'value': column_name}), on='ts')

    combined_df.set_index('ts', inplace=True)
    combined_df = combined_df.astype(float)
    combined_df = combined_df.T

    return combined_df

def prev_date():
    current_date = datetime.now().date()
    yesterday_date = current_date - timedelta(days=1)
    return yesterday_date.strftime("%d-%m-%Y")