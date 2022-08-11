#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:51:08 2022

@author: marialuisa
"""
import pandas as pd
import numpy as np
import streamlit as st
from plot_conc import  plotN_CV
from aux_function import is_authenticated, generate_login_block, clean_blocks, login
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

col1, col2, col3 = st.columns([4, 0.2, 1])
figCV = plotN_CV(city_data, sl_init, sl_end, log, smooth, size_window, center, cities_solids, cts_label)
col1.plotly_chart(figCV, use_container_width=True)

st.markdown(""" <style>[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {width: 280px;}
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {width: 280px;margin-left: -300px;}
    </style>""", unsafe_allow_html=True, )






# con respecto a la semana anterior. Para la concentracion el cambio se da en porcentajes

