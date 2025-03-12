import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bike Rental", layout="wide")

day = pd.read_csv("dashboard/days.csv") 
day.head()
# Data Cleaning & Transformation
day.drop(columns=['windspeed'], inplace=True, errors='ignore')
day.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
             7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weekday_map = {0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'}
weather_map = {1: 'Clear/Partly Cloudy', 2: 'Misty/Cloudy', 3: 'Light Snow/Rain', 4: 'Severe Weather'}

day['month'] = day['month'].map(month_map)
day['season'] = day['season'].map(season_map)
day['weekday'] = day['weekday'].map(weekday_map)
day['weather_cond'] = day['weather_cond'].map(weather_map)

day['dateday'] = pd.to_datetime(day['dateday'])

categorical_cols = ['season', 'year', 'month', 'holiday', 'weekday', 'workingday', 'weather_cond']
day[categorical_cols] = day[categorical_cols].astype('category')

# Streamlit Dashboard
st.title("🚴‍♂️ Bike Rental Analysis Dashboard 🚴‍♂️")
st.markdown("### Analisis Penyewaan Sepeda Berdasarkan Berbagai Faktor")

# Sidebar filters
st.sidebar.header("Filter Tahun🚴‍♂️")
year_filter = st.sidebar.selectbox("Pilih Tahun", options=day['year'].cat.categories, index=0)
filtered_df = day[day['year'] == year_filter]

# Pengaruh Kondisi Cuaca Terhadap Penyewaan
avg_rentals = filtered_df.groupby('weather_cond')['count'].mean().reset_index()
fig = px.bar(avg_rentals, x='weather_cond', y='count', color='weather_cond',
             title='Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca',
             labels={'weather_cond': 'Kondisi Cuaca', 'count': 'Rata-rata Jumlah Penyewaan'})
st.plotly_chart(fig)

#Tren Penyewaan Sepeda Berdasarkan Waktu
fig = px.line(filtered_df, x='dateday', y='count', color='year',
              title='Tren Penyewaan Sepeda Berdasarkan Waktu',
              labels={'dateday': 'Tanggal', 'count': 'Jumlah Penyewaan', 'year': 'Tahun'})
st.plotly_chart(fig)

# Pengaruh Musim Terhadap Penyewaan Sepeda
seasonal_usage = day.groupby('season')[['registered', 'casual']].sum().reset_index()

fig = px.bar(seasonal_usage, x='season', y=['registered', 'casual'],
             title='Jumlah penyewaan sepeda berdasarkan musim',
             labels={'value': 'Jumlah Penyewaan', 'season': 'Musim'},
             barmode='group',
             category_orders={"season": ["Spring", "Summer", "Fall", "Winter"]})
st.plotly_chart(fig)

# Perbandingan hari kerja vs non-hari kerja
workingday_counts = filtered_df.groupby('workingday')['count'].sum().reset_index()
workingday_counts['workingday'] = workingday_counts['workingday'].map({0: 'Non-Working Day', 1: 'Working Day'})
fig = px.bar(workingday_counts, x='workingday', y='count', color='workingday',
             title='Perbandingan Penyewaan Working Day vs Non-Working Day',
             labels={'workingday': 'Kategori Hari', 'count': 'Jumlah Penyewaan'})
st.plotly_chart(fig)

# Hubungan antara suhu dan penyewaan
fig = px.scatter(filtered_df, x='temp', y='count', color='season',
                 title='Hubungan Antara Suhu dan Jumlah Penyewaan',
                 labels={'temp': 'Suhu', 'count': 'Jumlah Penyewaan', 'season': 'Musim'})
st.plotly_chart(fig)

# Penyewaan berdasarkan hari dalam seminggu
weekday_counts = filtered_df.groupby('weekday')['count'].sum().reset_index()
fig = px.bar(weekday_counts, x='weekday', y='count', color='weekday',
             category_orders={"weekday": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]},
             title='Jumlah Penyewaan Sepeda Berdasarkan Hari dalam Minggu',
             labels={'weekday': 'Hari', 'count': 'Jumlah Penyewaan'})
st.plotly_chart(fig)
st.caption('Copyright (c) Sukma Suciyana 2025')

