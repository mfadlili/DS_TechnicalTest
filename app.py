import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Franchise Sales Review 2021",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/mfadlili',
        'Report a bug': "https://github.com/mfadlili",
        'About': "#TechnicalTest."
    }
)

@st.cache_data
def load_data1():
    data = pd.read_csv('https://raw.githubusercontent.com/mfadlili/upload_csv/master/data_franchise_clean.csv')
    return data

@st.cache_data
def load_data2():
    data = pd.read_csv('https://raw.githubusercontent.com/mfadlili/upload_csv/master/franchise_total_revenue_per_month_province.csv')
    return data


df1 = load_data1()
df2 = load_data2()

st.title('Franchise Sales Review 2021')
st.title('')
col1, col2, col3 = st.columns(3)

def total_sales():
    total_revenue = "Rp " +str(round(df1['revenue'].sum()))
    st.metric(label="Total Revenue", value=total_revenue)

def total_franchise():
    franchise = df1.groupby('Province').id.nunique().reset_index().id.sum()
    st.metric(label="Total Franchise", value=franchise)

def average_revenue():
    revenue_avg = "Rp " + str(round(df1.revenue.mean()))
    st.metric(label="Monthly Average Revenue per Franchise", value=revenue_avg)

with col1:
    total_sales()

with col2:
    total_franchise()

with col3:
    average_revenue()

st.title('')

col1,col2 = st.columns([1,1])

col3,col4 = st.columns([1,1])

with col1:
    st.markdown("<h2 style='text-align: center; color: black;'>Franchise Distribution</h2>", unsafe_allow_html=True)
    list_options = ["Province", "Regional", "Class"]
    dict_options = {'Province':'Province', 'Regional':'regional', "Class":'class'}
    option = st.selectbox("By:", list_options)
    st.title("")
    st.title("")
    st.title(" ")
    result = df1.groupby(dict_options[option]).id.nunique().reset_index().rename(columns={"id":"num_of_franchise"})
    fig1 = px.bar(result,y=dict_options[option],x='num_of_franchise',color=dict_options[option],color_discrete_sequence=px.colors.sequential.Darkmint,height=700,width=750, text_auto='.2s')
    fig1.update_layout(xaxis_title='Number of Franchise',yaxis_title=' ', showlegend = False)
    st.plotly_chart(fig1) 

with col2:
    st.markdown("<h2 style='text-align: center; color: black;'>Revenue Distribution</h2>", unsafe_allow_html=True)
    list_options1 = ["Province", "Regional", "Class"]
    dict_options1 = {'Province':'Province', 'Regional':'regional', "Class":'class'}
    list_month = ['All Months', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'Desember']
    month_num = [i for i in range(0,13)]
    dict_month = dict(zip(list_month, month_num))

    option1 = st.selectbox("By: ", list_options1)
    option2 = st.selectbox("Month", list_month)

    if option2=="All Months":
        result2 = df1.groupby(dict_options1[option1]).revenue.sum().reset_index().rename(columns={"revenue":"total_revenue"})
        fig15 = px.treemap(result2, path=[dict_options1[option1]], values='total_revenue',height=780,width=800, color_discrete_sequence=px.colors.sequential.Darkmint)
        fig15.update_traces(textinfo='label+value+percent root')
        st.plotly_chart(fig15)
    
    else:
        result2 = df1[df1.month==dict_month[option2]].groupby(dict_options1[option1]).revenue.sum().reset_index().rename(columns={"revenue":"total_revenue"})
        fig15 = px.treemap(result2, path=[dict_options1[option1]], values='total_revenue',height=780,width=800, color_discrete_sequence=px.colors.sequential.Darkmint)
        fig15.update_traces(textinfo='label+value+percent root')
        st.plotly_chart(fig15)        

with col3:
    st.markdown("<h2 style='text-align: center; color: black;'>Revenue per Month</h2>", unsafe_allow_html=True)
    list_province = [i for i in df1.Province.unique()]
    list_province.insert(0, "All Provinces")
    option_province = st.selectbox("Province:", list_province)

    if option_province=="All Provinces":
        result3 = df1.groupby('month').revenue.sum().reset_index()
        fig3 = px.bar(result3,y='revenue',x='month',color='revenue',color_discrete_sequence=px.colors.sequential.Darkmint,height=600,width=800, text_auto='.2s')
        fig3.update_layout(xaxis_title='Month',yaxis_title='Total Revenue', showlegend = False)
        st.plotly_chart(fig3)
    else:
        result3 = df1[df1.Province==option_province].groupby('month').revenue.sum().reset_index()
        fig3 = px.bar(result3,y='revenue',x='month',color='revenue',color_discrete_sequence=px.colors.sequential.Darkmint,height=600,width=800, text_auto='.2s')
        fig3.update_layout(xaxis_title='Month',yaxis_title='Total Revenue', showlegend = False)
        st.plotly_chart(fig3)

with col4:
    st.markdown("<h2 style='text-align: center; color: black;'>Revenue Growth per Month</h2>", unsafe_allow_html=True)
    list_province = [i for i in df1.Province.unique()]
    list_province.insert(0, "All Provinces")
    option_province = st.selectbox("Province: ", list_province)

    if option_province=="All Provinces":
        a = df2.groupby('month').revenue.sum().reset_index()
        res = [0]
        for i in range(1, len(a)):
            res.append((a.revenue[i]-a.revenue[i-1])*100/a.revenue[i-1])
        a['growth'] = res

        fig1= px.line(data_frame=a,x='month',y='growth',markers=True,height=600,width=800)
        fig1.add_bar(x=a['month'].tolist(),y=a['growth'].tolist())
        fig1.update_layout(xaxis_title='Month',yaxis_title='Growth (%)', showlegend = False)
        fig1.update_traces(marker_color='#5aa17f')
        st.plotly_chart(fig1)
    
    else:
        a = df2[df2.Province == option_province].groupby('month').revenue.sum().reset_index()
        res = [0]
        for i in range(1, len(a)):
            res.append((a.revenue[i]-a.revenue[i-1])*100/a.revenue[i-1])
        a['growth'] = res

        fig1= px.line(data_frame=a,x='month',y='growth',markers=True,height=600,width=800)
        fig1.add_bar(x=a['month'].tolist(),y=a['growth'].tolist())
        fig1.update_layout(xaxis_title='Month',yaxis_title='Growth (%)', showlegend = False)
        fig1.update_traces(marker_color='#5aa17f')
        st.plotly_chart(fig1)   



