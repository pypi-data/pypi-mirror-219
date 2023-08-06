import requests
import json
import pandas as pd
from ML_Algo.Series_Time import *

def getData(date):  
    url =  'http://192.168.0.35:5060/ldat'
    param =  {
        "id": "10751",
        "reqdate": date
         # 04-06-2023
    }   
    try:
        response = requests.post(url,json=param, verify=False, timeout=20)
    
    except:
        print('server busy')
    dat = response.text
    dt = json.loads(dat)
    return dt

def get_live_data(yesterday,today,interval=15,manual_override=0,ct=0):
    if manual_override == 0:
        t = calculate_completed_intervals(interval)
    else:
        t = ct
    if t == 0:
        live_data = pd.concat([yesterday.iloc[:, -2:], today.iloc[:, :1]], axis=1)
        return live_data
    elif t == 1:
        live_data = pd.concat([yesterday.iloc[:, -1:], today.iloc[:, :2]], axis=1)
        return live_data
    elif t == 2:
        live_data = today.iloc[:,0:3]
        return live_data
    elif t >= 3:
        live_data = today.iloc[:,t-2:t+1]
        return live_data
    
def get_pred_data(yesterday,pred_data,interval=15,manual_override=0,ct=0):
    if manual_override == 0:
        t = calculate_completed_intervals(interval)
    else:
        t = ct

    if t == 0:
        pred = pd.concat([yesterday.iloc[:, -2:], pred_data.iloc[:, :1]], axis=1)
        return pred
    elif t == 1:
        pred = pd.concat([yesterday.iloc[:, -1:], pred_data.iloc[:, :2]], axis=1)
        return pred
    elif t == 2:
        pred = pred_data.iloc[:,0:3]
        return pred
    elif t >= 3:
        pred = pred_data.iloc[:,t-2:t+1]
        return pred
    
def get_next_pred(pred,next_pred_intervals=8,interval=15,manual_override=0,ct=0):
    if manual_override == 0:
        t = calculate_completed_intervals(interval)
    else:
        t = ct
    return pred.iloc[:,t:t+next_pred_intervals]    

