#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:51:08 2022

@author: marialuisa
"""
import pandas as pd
import numpy as np
import streamlit as st
from plot_conc import plotN1N2, plotPMMoV, plotN, plot_Rsquared, plotN_CV, plotNgen, plot_Ro, plot_Infl_Slud
from aux_function import is_authenticated, generate_login_block, clean_blocks, login
from datetime import datetime, timedelta
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import trim_mean, pearsonr





def data_city(city, data_ww):
    city_data = data_ww[data_ww['City'] == city]
    city_data = city_data.reset_index()
    return city_data


def read_data():
    return pd.read_csv('data_ww_cases_full.csv')
#return pd.read_csv('data_ww_cases_full.csv')


data_ww = read_data()
county_data = pd.read_csv('data_cases_county.csv')
county_data_all = pd.read_csv('data_cases_county.csv')


city='Davis'
city_data = data_city(city, data_ww)
city_data['SampleDate'] = pd.to_datetime(city_data['SampleDate'])
county_data['date'] = pd.to_datetime(county_data['date'])
date_county_cases = county_data['date'].max().strftime('%B-%d, %Y')
city_data[['positives', 'Testing']].plot()


fig = make_subplots(specs=[[{"secondary_y": True}]])

size_window=7
center=True
lag=0
fig.add_trace(go.Scatter(name='cases', mode='lines', x=x, y=city_data['positives'].rolling(window=size_window, center=center).mean()[lag:],
                                 line=dict(color='gray', width=3)), secondary_y=True, )
