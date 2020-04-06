from datetime import datetime
import pandas as pd
import numpy as np
from selenium import webdriver
import plotly.graph_objects as go
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import win32com.client
import pythoncom
class get_data:
    def hose_stock_list():
        global webdriver
        chrome_driver_path = 'D:\python\selenium\driver\chromedriver.exe'
        chrome_options = Options()
        #chrome_options.page_load_strategy
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--user-data-dir=C:\\Users\\hung-pro7\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Default')
        webdriver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
        url = 'https://trade-hcm.vndirect.com.vn/chung-khoan/hose'
        webdriver.get(url)
        webdriver.find_element_by_xpath('//*[@id="menuWrp"]/div/a[2]').click()
        time.sleep(2)
        webdriver.find_element_by_xpath('//*[@id="login-popup"]/form/div[1]/div/input').send_keys("tuanhungstar")
        webdriver.find_element_by_xpath('//*[@id="login-popup"]/form/div[2]/div/input').send_keys("Khanhha-1")
        webdriver.find_element_by_xpath('//*[@id="login-popup"]/form/button').click()
        time.sleep(2)
        webdriver.find_element_by_xpath('//*[@id="nav"]/ul[1]/li[2]/a/span').click()
        time.sleep(2)
        HOSE_table = webdriver.find_elements_by_class_name('txt-gia-tran')
        HOSE_ticker=[]
        for row in HOSE_table:
            text = row.get_attribute('id').replace('ceil','')
            HOSE_ticker.append(text)
        return HOSE_ticker

#''''''''''''''scan_amibroker''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def scan_amibroker(program_link):
        AB = win32com.client.Dispatch("Broker.Application")
        Analysis_program = AB.AnalysisDocs.Open(program_link)
        Analysis_program.Run (1)
        while Analysis_program.IsBusy != 0:
            time.sleep(1)
        result_ok = Analysis_program.Export("C:/Users/hung-pro7/Amibroker/result.csv")
        df_result = pd.read_csv("C:/Users/hung-pro7/Amibroker/result.csv",index_col='Ticker',parse_dates = ['Date/Time'])
        Analysis_program.Close()
        return df_result

    def Market_status(df):
        top5up = df['Ty le tang trong ngay'].nlargest(5)
        top5down = df['Ty le tang trong ngay'].nsmallest(5)
        up_ceil = df['Ty le tang trong ngay'][df['Ty le tang trong ngay']>=0.068]
        down_floor = df['Ty le tang trong ngay'][df['Ty le tang trong ngay']<=0.068]
        up = df['Ty le tang trong ngay'][df['Ty le tang trong ngay']>0]
        down = df['Ty le tang trong ngay'][df['Ty le tang trong ngay']<0]
        nochange = df['Ty le tang trong ngay'][df['Ty le tang trong ngay']==0.0]
        Vol_up = df['Do bien KL'][df['Do bien KL']>=0.03]
        return top5up,top5down,up_ceil,down_floor,up,down,nochange,Vol_up

    def Top_bottom(df):
        top_month = df['Close P'] > df['chieukhau_1thang']
        Bottom_month = df['Close P'] < df['chieukhau_1thang']
        return top_month,Bottom_month
    def radar_data(df):
        MA_status_5 = int(df['MA_status'][df['MA_status']==5].count()/len(df['MA_status'])*100)
        MA_status_0 = int(df['MA_status'][df['MA_status']==0].count()/len(df['MA_status'])*100)
        Earth3Dailystatus_0 = int(df['Earth3Dailystatus'][df['Earth3Dailystatus']==0].count()/len(df['Earth3Dailystatus'])*100)
        Earth3Dailystatus_2 = int(df['Earth3Dailystatus'][df['Earth3Dailystatus']==2].count()/len(df['Earth3Dailystatus'])*100)
        Earth3Weeklystatus_0 = int(df['Earth3Weeklystatus'][df['Earth3Weeklystatus']==0].count()/len(df['Earth3Weeklystatus'])*100)
        Earth3Weeklystatus_2 = int(df['Earth3Weeklystatus'][df['Earth3Weeklystatus']==2].count()/len(df['Earth3Weeklystatus'])*100)
        Earth3Weeklystatus_0 = int(df['Earth3Weeklystatus'][df['Earth3Weeklystatus']==0].count()/len(df['Earth3Weeklystatus'])*100)
        Pice_MA20_above = int(df['Pice/MA20'][df['Pice/MA20']>=0].count()/len(df['Pice/MA20'])*100)
        Pice_MA20_below = int(df['Pice/MA20'][df['Pice/MA20']<=0].count()/len(df['Pice/MA20'])*100)
        Pice_MA200_above = int(df['Pice/MA200'][df['Pice/MA200']>=0].count()/len(df['Pice/MA200'])*100)
        Pice_MA200_below = int(df['Pice/MA200'][df['Pice/MA200']<=0].count()/len(df['Pice/MA200'])*100)
        return MA_status_5,Earth3Dailystatus_2,Earth3Weeklystatus_2,Pice_MA20_above,Pice_MA200_above,MA_status_0,Earth3Dailystatus_0,Earth3Weeklystatus_0,Pice_MA20_below,Pice_MA200_below
class get_chart:

    def chart_top5_up_down(app,status_update):

        top5up,top5down,up_ceil,down_floor,up,down,nochange,Vol_up = get_data.Market_status(status_update)
        x_value_up = top5up.index
        y_value_up = top5up.values

        fig = go.Figure(
                data=[
                        go.Bar(name='top5up',x=top5up.index,y=top5up.values),
                        go.Bar(name='top5down',x=top5down.index,y=top5down.values),
                                ],
                layout  = go.Layout(margin = dict(l=10,r=10,t=30,b=10),
                                    height = 180,
                                    autosize=True,
                                    xaxis = dict(title=dict(font=dict(size=12))))

        )
        #fig.update_layout(style{'height':'200px'})
        fig.update_layout(title_text='Top 5 up and down')
        fig.update_layout(showlegend=False)

        return fig

    def chart_Volume_break(app,status_update):

        top5up,top5down,up_ceil,down_floor,up,down,nochange,Vol_up = get_data.Market_status(status_update)

        fig = go.Figure(
                data=[
                        go.Bar(name='top5up',x=Vol_up.index,y=Vol_up.values),
                                ],
                layout  = go.Layout(margin = dict(l=10,r=10,t=30,b=10),
                                    height = 180,
                                    autosize=True)

        )
        #fig.update_layout(style{'height':'200px'})
        fig.update_layout(title_text='Top Volume Break')
        fig.update_layout(showlegend=False)

        return fig

    def chart_radar(app,status_update):
        MA_status_5,Earth3Dailystatus_2,Earth3Weeklystatus_2,Pice_MA20_above,Pice_MA200_above,MA_status_0,Earth3Dailystatus_0,Earth3Weeklystatus_0,Pice_MA20_below,Pice_MA200_below = get_data.radar_data(status_update)
        categories = ['MA Status','Earth 3 daily','Earth3 Weekly',
              'MA 20', 'MA 200']

        fig = go.Figure(
                data=[
                        go.Scatterpolar(
                        r=[MA_status_5,Earth3Dailystatus_2,Earth3Weeklystatus_2,Pice_MA20_above,Pice_MA200_above],
                        theta=categories,
                        fill='toself',
                        name='Strong stock'
                                ),
                        go.Scatterpolar(
                        r=[MA_status_0,Earth3Dailystatus_0,Earth3Weeklystatus_0,Pice_MA20_below,Pice_MA200_below],
                        theta=categories,
                        fill='toself',
                        name='Weak stock'
                                )

                                ],
                layout  = go.Layout(margin = dict(l=10,r=10,t=30,b=20),
                                    height = 180,
                                    autosize=True)

        )
        #fig.update_layout(style{'height':'200px'})
        fig.update_layout(title_text='Radar overview')
        fig.update_layout(showlegend=False)

        return fig

    def chart_earth_vn_30(app,status_update):
        VN_30 = pd.read_csv("C:\\Program Files (x86)\\AmiBroker\\MyNewData\\WatchLists\\VN30.tls",index_col=0,header=None,names=['Ticker'])
        VN_30 = VN_30.merge(status_update,left_on=VN_30.index,right_on = status_update.index ).set_index('key_0')
        color_daily = []
        for p_value in VN_30['Earth3_Position_trend']:
            if p_value==1:
                color_daily.append('Chartreuse')
            else:
                color_daily.append('Crimson')
        color_weekly = []
        for p_value in VN_30['Earth3_Position_Weekly_trend']:
            if p_value==1:
                color_weekly.append('Chartreuse')
            else:
                color_weekly.append('Crimson')
        fig = go.Figure(
                data=[
                        go.Bar(x=VN_30.index,
                                   y=VN_30['Earth3_Position'],
                                   name='Earth Position Daily',
                                   marker_color=color_daily
                                        ),
                        go.Bar(x=VN_30.index,
                                   y=VN_30['Earth3_Position_weekly'],
                                   name='Earth Position Weekly',
                                   marker_color=color_weekly
                                        )

                                ],
                layout  = go.Layout(margin = dict(l=10,r=10,t=30,b=20),
                                    height = 180,
                                    autosize=True,
                                    showlegend=False))
        fig.update_layout(title_text='Earth VN30')
        return fig
    def chart_price_vn30(app,status_update):
        VN_30 = pd.read_csv("C:\\Program Files (x86)\\AmiBroker\\MyNewData\\WatchLists\\VN30.tls",index_col=0,header=None,names=['Ticker'])
        VN_30 = VN_30.merge(status_update,left_on=VN_30.index,right_on = status_update.index ).set_index('key_0')
        color_daily=[]
        for p_value in VN_30['Ty le tang trong ngay']:
            if p_value>0:
                color_daily.append('Chartreuse')
            elif p_value==0:
                color_daily.append('gold')
            else:
                color_daily.append('Crimson')

        fig = go.Figure(
                data=[
                        go.Bar(name='VN 30 Stock',x=VN_30.index,y=VN_30['Ty le tang trong ngay'],marker_color=color_daily),
                        #go.Bar(name='top5down',x=top5down.index,y=top5down.values),
                                ],
                layout  = go.Layout(margin = dict(l=10,r=10,t=30,b=10),
                                    height = 180,
                                    autosize=True,
                                    xaxis = dict(title=dict(font=dict(size=12))))

        )
        #fig.update_layout(style{'height':'200px'})
        fig.update_layout(title_text='VN30 Price chart')
        fig.update_layout(showlegend=False)

        return fig
