import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA_URL=(
    "~/Desktop/Webapp/covid_19_clean_complete.csv"
)

st.title("Cases in World")
st.markdown("This application is a Streamlit dashboard that "
"can be used to analyze covid-19 cases in World.")

@st.cache(allow_output_mutation=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data.dropna(subset=['Latitude','Longitude'], inplace = True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    
    
    return data

data = load_data()
original_data = data
original_data['date'] = pd.to_datetime(original_data.date)
original_data['date'] = pd.to_datetime(original_data["date"].dt.strftime('%Y/%m/%d'))
st.header("Where are the most cases in World?")
cases = st.slider("Number of ",100,10000)

st.map(data.query("confirmed >= @cases")[["latitude","longitude"]].dropna(how = "any"))

st.header("Top 5 Country of Recovered/Deaths in the world")
select = st.selectbox('Recovered/Deaths',['Recovered','Deaths'])

if select == 'Recovered':
    data1 = original_data.query("recovered >=1")[["country/region","recovered"]].sort_values(by=['recovered'],ascending = False).dropna(how ="any")[:]
    data1 = data1["country/region"].unique()
    st.write(data1[:5])
else:
    data1 =original_data.query("deaths >=1")[["country/region","deaths"]].sort_values(by=['deaths'],ascending = False).dropna(how ="any")[:]
    data1 = data1["country/region"].unique()
    st.write(data1[:5])

st.header("How many cases confirmed on a particular date?")
date = st.date_input('Date')
data1 = original_data[original_data['date'] == date]
st.write(original_data.query("date== @date")[["date", "country/region",'confirmed']].sort_values(by=['confirmed'],ascending = False).dropna(how = 'any'))
#st.markdown("Vehicle collision between %i:00 and %i:00" %(hour, (hour+1)%24))
list1 = list(original_data["date"])
list2 = list(original_data["country/region"])
list3 = list(original_data["confirmed"])
list4 = list(original_data["recovered"])
list5 = list(original_data["deaths"])
idx = pd.MultiIndex.from_arrays([
    list1,
    list2],
    names=['date', 'country/region']
)
s = pd.Series(list3, name='confirmed', index=idx)
data_date_confirmed =list(s.sum(level="date"))
data_country_confirmed = list(s.sum(level="country/region"))
l= pd.Series(list4, name='deaths', index=idx)
data_date_deaths =list(l.sum(level="date"))
data_country_deaths = list(l.sum(level="country/region"))
k= pd.Series(list5, name='recovered', index=idx)
data_date_recovered =list( k.sum(level="date"))
data_country_recovered = list(k.sum(level="country/region"))
data_date = pd.DataFrame(list(zip(data_date_confirmed[25:],data_date_deaths[25:],data_date_recovered[25:])),columns=["confirmed","recovered","deaths"])
st.header("How many cases  of Confirmed, Deaths and Recovered in world?")
st.area_chart(data_date)