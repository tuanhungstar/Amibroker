import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pythoncom
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from get_data_Ami import get_data,get_chart
app = dash.Dash()

link_program_scan_update_data ="C:/Users/hung-pro7/Amibroker/Update data cho chart tam ly.apx"
status_update =get_data.scan_amibroker(link_program_scan_update_data)
#print(status_update)
#app.layout = html.Div(html.H6("Phung Tuan Hung"),className ='page main-title')
##css3###
main_item = {'margin':'20px','color':'#0803f8'}
server = app.server
app.layout = html.Div([
                        html.Div([
                            html.Div([
                                dcc.Graph(
                                id='top5upanddown',
                                    figure = get_chart.chart_top5_up_down(app,status_update),
                                    #style={"height" : "100px", "width" : "100%"}
                                    )
                                    ],className="pretty_container_inside four columns chart"),
                            html.Div([
                                dcc.Graph(
                                id='break_vol',
                                    figure = get_chart.chart_Volume_break(app,status_update),
                                    #style={"height" : "100px", "width" : "100%"}
                                    )
                                    ],className="pretty_container_inside four columns"),
                            html.Div([],className="pretty_container_inside four columns"),
                                    ],className="pretty_container display_in_line"),   #line 1
                        html.Div([
                            html.Div([
                                dcc.Graph(
                                id='Radar_overview',
                                    figure = get_chart.chart_radar(app,status_update),
                                    #style={"height" : "100px", "width" : "100%"}
                                    )
                                    ],className="pretty_container_inside four columns chart"),
                            html.Div([
                                dcc.Graph(
                                id='Earth3_Position',
                                    figure = get_chart.chart_earth_vn_30(app,status_update),
                                    #style={"height" : "100px", "width" : "100%"}
                                    )
                                    ],className="pretty_container_inside eight columns chart"),
                            ],className="pretty_container twelve columns display_in_line"),   #line 2
                        html.Div([
                            html.Div([
                                dcc.Graph(
                                id='VN30_price_chart',
                                    figure = get_chart.chart_price_vn30(app,status_update),
                                    #style={"height" : "100px", "width" : "100%"}
                                    )
                                    ],className="pretty_container_inside eight columns chart"),

                        ],className="pretty_container twelve columns"),   #line 3
                        html.Button(
                            id='refresh_data',
                            n_clicks=0,
                            children='Refesh Data',
                            style={'fontSize':18}
                        )
                        ],className ='page') #

@app.callback(
    [Output('top5upanddown', 'figure'),
     Output('break_vol', 'figure'),
     Output('Radar_overview', 'figure'),
     Output('Earth3_Position', 'figure'),
     Output('VN30_price_chart', 'figure')],
    [Input('refresh_data', 'n_clicks')])
def update_graph_1(n_clicks):
    pythoncom.CoInitialize()
    status_update =get_data.scan_amibroker(link_program_scan_update_data)
    #status_update = pd.read_csv("C:/Users/hung-pro7/Amibroker/result.csv",index_col='Ticker',parse_dates = ['Date/Time'])
    figure1 = get_chart.chart_top5_up_down(app,status_update)
    figure2 = get_chart.chart_Volume_break(app,status_update)
    figure3 = get_chart.chart_radar(app,status_update)
    figure4 = get_chart.chart_earth_vn_30(app,status_update)
    figure5 = get_chart.chart_price_vn30(app,status_update)
    return figure1,figure2,figure3,figure4,figure5


if __name__ == '__main__':
    app.run_server()
