#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:51:08 2022

@author: marialuisa
"""
import pandas as pd
import numpy as np
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
#from plot_conc import  plotN_C
from datetime import  timedelta


st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title=None, page_icon=None)
cities_solids = ['Davis (sludge)', 'Merced', 'Modesto', 'Woodland (solids)', 'Winters (solids)', 'Turlock (solids)', 'Los Banos (solids)',
                 'Esparto (solids)']
cts_label = {'Davis (sludge)':'Davis', 'Merced':'Merced', 'Modesto':'Modesto', 'Woodland (solids)':'Woodland',
                'Winters (solids)':'Winters', 'Turlock (solids)':'Turlock', 'Los Banos (solids)':'Los Banos',
                 'Esparto (solids)':'Esparto'}


def read_data():
    city_data=pd.read_csv('data_ww_cases_full.csv')
    data = city_data[city_data['SampleDate'] > '2021-09-30']
    return data

def trim_fun(x):
    x = x.dropna()
    x1 = x.sort_values().ravel()
    return np.mean(x1[1:-1]) # Remove max values and min values


def plotN_CV(data_ww, start_date, end_date, log, opt, size_window, center, cts, cts_label):
    fontsize = 14
    min_period = 3
    start_date=pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    n = len(cts) # number of cities
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    color = px.colors.qualitative.Plotly
    sw = size_window-1
    swc = size_window//2

    for i in range(n):
        city_data_new = data_ww[data_ww['City'] == cts[i]]
        city_data = city_data_new[(city_data_new['SampleDate'] >= start_date) & (city_data_new['SampleDate'] <= end_date)]
        if log:
            city_data['NormalizedConc_wo'] = city_data['NormalizedConc_wo'] + 1e-6

        if opt == 'Moving average':
            X = city_data.SampleDate
            Y = city_data['NormalizedConc_wo'].rolling(window=size_window, center=center, min_periods=min_period).mean()
            if center:
                fig.add_trace(go.Scatter(name=cts_label[cts[i]], mode='lines', x=X[swc:-swc], y=Y[swc:-swc], line=dict(color=color[i], width=3)), secondary_y=False, )
            else:
                fig.add_trace(go.Scatter(name=cts_label[cts[i]], mode='lines', x=X[sw-1:], y=Y[sw-1:], line=dict(color=color[i], width=3)), secondary_y=False, )
        elif opt == 'Trimmed average':  # .apply(lambda x: trim_mean(x, 0.2))
            Y = city_data['NormalizedConc_wo'].rolling(window=size_window, center=center, min_periods=min_period).apply(lambda x: trim_fun(x))
            X = city_data.SampleDate
            if center:
                fig.add_trace(go.Scatter(name=cts_label[cts[i]], mode='lines', x=X[swc:-swc], y=Y[swc:-swc], line=dict(color=color[i], width=3)), secondary_y=False,)
            else:
                fig.add_trace(go.Scatter(name=cts_label[cts[i]], mode='lines', x=X[sw-1:], y=Y[swc:-swc], line=dict(color=color[i], width=3)), secondary_y=False, )
        else:
            fig.add_trace(go.Scatter(name=cts_label[cts[i]], mode='lines', x=city_data.SampleDate, y=city_data['NormalizedConc_wo'],
                                     line=dict(color=color[i], width=3)), secondary_y=False, )
    if log:
        fig.update_yaxes(type="log")
        fig.update_layout(yaxis=dict(title="Log-Scale"))

    fig.update_layout(font=dict(family="sans-serif", size=fontsize, color="black"), template="plotly_white", legend_font_size=14, legend_title_font_size=fontsize)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.6, xanchor="right", x=0.9))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(autosize=False, width=450, height=250, margin=dict(l=0, r=0, b=10, t=10, pad=4),yaxis=dict(title='N gene / PMMoV'))  # ,xaxis=dict(title="Date"))
    fig.update_layout(font_family="Arial", title_font_family="Arial")
    return fig




with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

city_data = read_data()

st.header('Healthy Central Valley Together: Wastewater SARS-CoV-2 data for Central Valley')

city_data['SampleDate'] = pd.to_datetime(city_data['SampleDate'])
start_date = city_data['SampleDate'].min().to_pydatetime()
end_date = city_data['SampleDate'].max().to_pydatetime()

st.sidebar.header('PLOT DETAILS')
col1, col2 = st.sidebar.columns([1, 0.51])
smooth = col1.selectbox('Smoothing function', ['Trimmed average', 'Moving average', 'None'], index=1)

if smooth != 'None':
    size_window = col2.selectbox('Size window', [5,7,10,14], index=1)
    center = col1.checkbox('Center')
else:
    size_window = 0
    center = False

log = st.sidebar.checkbox('Log transformation')
col1, col2, col3 = st.columns([4, 0.2, 1])

sl_init, sl_end = col1.slider('', min_value=start_date, max_value=end_date+timedelta(days = 0), value=(start_date, end_date+timedelta(days =0)),format='MMM DD, YYYY')


figCV = plotN_CV(city_data, sl_init, sl_end, log, smooth, size_window, center, cities_solids, cts_label)
col1.plotly_chart(figCV, use_container_width=True)

st.markdown(""" <style>[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {width: 280px;}
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {width: 280px;margin-left: -300px;}
    </style>""", unsafe_allow_html=True, )






# con respecto a la semana anterior. Para la concentracion el cambio se da en porcentajes

