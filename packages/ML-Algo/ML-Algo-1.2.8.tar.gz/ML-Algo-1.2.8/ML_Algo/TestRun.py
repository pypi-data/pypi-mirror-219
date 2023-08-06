from ML_Algo.FetchData import *
from ML_Algo.Series_Data import *
import numpy as np

def get_test_live_data(yesterday,today,t=0):
    if t == 0:
        live_data = pd.concat([yesterday.iloc[:, -2:], today.iloc[:, :1]], axis=1)
        # live_data = pd.concat([yesterday.iloc[:, :2], today.iloc[:, :1]], axis=1)
        return live_data.stack().dropna().tolist()
    elif t == 1:
        live_data = pd.concat([yesterday.iloc[:, -1:], today.iloc[:, :2]], axis=1)
        # live_data = pd.concat([yesterday.iloc[:, :1], today.iloc[:, :2]], axis=1)
        return live_data.stack().dropna().tolist()
    elif t == 2:
        live_data = today.iloc[:,0:3]
        return live_data.stack().dropna().tolist()
    elif t >= 3:
        live_data = today.iloc[:,t-2:t+1]
        return live_data.stack().dropna().tolist()
    
def get_test_pred_data(yesterday,pred_data,t=0):
    if t == 0:
        # pred = pd.concat([yesterday.iloc[:, :2], pred_data.iloc[:, :1]], axis=1)
        pred = pd.concat([yesterday.iloc[:, -2:], pred_data.iloc[:, :1]], axis=1)
        return pred.stack().dropna().tolist()
    elif t == 1:
        # pred = pd.concat([yesterday.iloc[:, :1], pred_data.iloc[:, :2]], axis=1)
        pred = pd.concat([yesterday.iloc[:, -1:], pred_data.iloc[:, :2]], axis=1)
        return pred.stack().dropna().tolist()
    elif t == 2:
        pred = pred_data.iloc[:,0:3]
        return pred.stack().dropna().tolist()
    elif t >= 3:
        pred = pred_data.iloc[:,t-2:t+1]
        return pred.stack().dropna().tolist()
    
def get_test_next_pred(pred,next_pred_intervals=8,t=0):
    return pred.iloc[:,t:t+next_pred_intervals].stack().dropna().tolist()    

def Test_Predict(combine_df,jump=8,next_pred_intervals=8):
    yesterday = combine_df.iloc[2:,:]
    today = combine_df.iloc[1:2,:]
    pred_data = combine_df.iloc[:1,:]
    Complete_Day = []
    for i in range (0,97,jump):
        l = get_test_live_data(yesterday,today,t=i)
        p = get_test_pred_data(yesterday,pred_data,t=i)
        n = get_test_next_pred(pred_data,next_pred_intervals=next_pred_intervals,t=i)
        # print(i)
        prev_day_err = (np.array(l)-np.array(p))/np.array(l)
        prev_day_err = prev_day_err.mean()
        # print(prev_day_err)
        # print(n)
        output_values= []
        for i in n:
            corr = (i+(i*prev_day_err))
            output_values.append(corr)
        Complete_Day.append(output_values[:jump])
    return Complete_Day

