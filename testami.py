import win32com.client
import time
import pandas as pd
import re
from get_data_Ami import get_data
'''
link_program_scan_update_data ="C:/Users/hung-pro7/Amibroker/Update data cho chart tam ly.apx"
#list_hose = get_data.hose_stock_list()
#print(list_hose)
status_update =get_data.scan_amibroker(link_program_scan_update_data)
top5up,top5down,up_ceil,down_floor,up,down,nochange,Vol_up = get_data.Market_status(status_update)
top_month,Bottom_month = get_data.Top_bottom(status_update)

MA_status_5 = int(status_update['MA_status'][status_update['MA_status']==5].count()/len(status_update['MA_status'])*100)
MA_status_0 = int(status_update['MA_status'][status_update['MA_status']==0].count()/len(status_update['MA_status'])*100)
Earth3Dailystatus_0 = int(status_update['Earth3Dailystatus'][status_update['Earth3Dailystatus']==0].count()/len(status_update['Earth3Dailystatus'])*100)
Earth3Dailystatus_2 = int(status_update['Earth3Dailystatus'][status_update['Earth3Dailystatus']==2].count()/len(status_update['Earth3Dailystatus'])*100)
Earth3Weeklystatus_0 = int(status_update['Earth3Weeklystatus'][status_update['Earth3Weeklystatus']==0].count()/len(status_update['Earth3Weeklystatus'])*100)
Earth3Weeklystatus_2 = int(status_update['Earth3Weeklystatus'][status_update['Earth3Weeklystatus']==2].count()/len(status_update['Earth3Weeklystatus'])*100)
Earth3Weeklystatus_0 = int(status_update['Earth3Weeklystatus'][status_update['Earth3Weeklystatus']==0].count()/len(status_update['Earth3Weeklystatus'])*100)
Pice_MA20_above = int(status_update['Pice/MA20'][status_update['Pice/MA20']>=0].count()/len(status_update['Pice/MA20'])*100)
Pice_MA20_below = int(status_update['Pice/MA20'][status_update['Pice/MA20']<=0].count()/len(status_update['Pice/MA20'])*100)
Pice_MA200_above = int(status_update['Pice/MA200'][status_update['Pice/MA200']>=0].count()/len(status_update['Pice/MA200'])*100)
Pice_MA200_below = int(status_update['Pice/MA200'][status_update['Pice/MA200']<=0].count()/len(status_update['Pice/MA200'])*100)
print(Pice_MA20_above)
print(Pice_MA20_below)
'''
link_program_scan_update_data ="C:/Users/hung-pro7/Amibroker/Update data cho chart tam ly.apx"
status_update =get_data.scan_amibroker(link_program_scan_update_data)
VN_30 = pd.read_csv("C:\\Program Files (x86)\\AmiBroker\\MyNewData\\WatchLists\\VN30.tls",index_col=0,header=None,names=['Ticker'])
VN_30 = VN_30.merge(status_update,left_on=VN_30.index,right_on = status_update.index ).set_index('key_0')
color = []
for p_value in VN_30['Earth3_Position_trend']:
    if p_value==0:
        color.append('Chartreuse')
    else:
        color.append('Crimson')

print(color)
