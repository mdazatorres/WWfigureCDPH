#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 17:37:42 2022

@author: marialuisa
"""

# import pandas as pd
import numpy as np
# import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import trim_mean, pearsonr
from sklearn.linear_model import LinearRegression
import plotly.express as px



# double click on legend to isolete the trace

def trim_fun1(x):
    x1 = x[x != x.max()]  # Remove max values
    x2 = x1[x1 != x1.min()]  # Remove min values
    return x2.mean(skipna=True)


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
    #color = ['royalblue', 'firebrick', 'yellowgreen', 'coral', 'black', 'hotpink', 'plum','gray', 'turquosi','chocolate']
    color=px.colors.qualitative.Plotly
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

    fig.update_layout(font=dict(family="sans-serif", size=fontsize, color="black"), template="plotly_white",
                      legend_font_size=14, legend_title_font_size=fontsize)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.6, xanchor="right", x=0.9))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})

    fig.update_layout(autosize=False, width=450, height=250, margin=dict(l=0, r=0, b=10, t=10, pad=4),
                      yaxis=dict(title='N gene / PMMoV'))  # ,xaxis=dict(title="Date"))
    fig.update_layout(font_family="Arial", title_font_family="Arial")
    return fig


