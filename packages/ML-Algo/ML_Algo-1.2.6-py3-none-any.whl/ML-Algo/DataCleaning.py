import pandas as pd
import numpy as np

def fill_missing_values(df):
    # Iterate over each row
    for row_index, row in df.iterrows():
        # Iterate over each column
        for col_index, value in enumerate(row):
            # Check if the value is empty
            if pd.isnull(value):
                # Find the closest non-empty values
                before = df.loc[row_index, df.columns[:col_index]][::-1].dropna()
                after = df.loc[row_index, df.columns[col_index+1:]].dropna()
                
                # Fill the missing value with the closest non-empty value
                if len(before) > 0 and len(after) > 0:
                    df.loc[row_index, df.columns[col_index]] = np.mean([before.iloc[0], after.iloc[0]])
                elif len(before) > 0:
                    df.loc[row_index, df.columns[col_index]] = before.iloc[0]
                elif len(after) > 0:
                    df.loc[row_index, df.columns[col_index]] = after.iloc[0]

                # If there are no non-empty values, set the missing value to 0
                else:
                    df.loc[row_index, df.columns[col_index]] = 0

    return df

def remove_outliers(df, low_percentile=25, high_percentile=75, outlier_threshold=1.5):
    cleaned_df = df.copy()
    removed_values = []
    for row_idx, row in cleaned_df.iterrows():
        low_threshold = np.percentile(row, low_percentile)
        high_threshold = np.percentile(row, high_percentile)
        iqr = high_threshold - low_threshold
        low_limit = low_threshold - outlier_threshold * iqr
        high_limit = high_threshold + outlier_threshold * iqr
        outliers = row[(row < low_limit) | (row > high_limit)]
        for col_name in outliers.index:
            removed_values.append({'Row': row_idx, 'Column': col_name, 'Value': row[col_name]})
            cleaned_df.loc[row_idx, col_name] = np.nan
    removed_values_df = pd.DataFrame(removed_values)
    return cleaned_df, removed_values_df