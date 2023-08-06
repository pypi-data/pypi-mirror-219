import pandas as pd
import numpy as np

def MasterPredict(input_df,live_data,sample_data):
    output_values = []
    prev_day = input_df
    sample_data_columns = sample_data.columns 
    prev_day_values = prev_day.values
    live_data_values = live_data.values
    sample_data_values = sample_data.values.flatten()
    prev_day_err=(np.array(live_data)-prev_day_values)/prev_day_values
    prev_day_err = prev_day_err.mean()
    for i in list(sample_data_values):
        corr = (i+(i*prev_day_err))
        output_values.append(corr)
    
    output_df = pd.DataFrame([output_values],columns=sample_data_columns)
    return output_df