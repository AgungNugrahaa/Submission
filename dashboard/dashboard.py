import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# Membaca data
day_df = pd.read_csv('/dashboard/day.csv')
hour_df = pd.read_csv('/dashboard/hour.csv')

# Mengubah kolom tanggal menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Sidebar untuk filter tanggal
st.sidebar.title("Filter Data Berdasarkan Tanggal")
start_date = st.sidebar.date_input("Pilih Tanggal Mulai", day_df['dteday'].min().date())
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", day_df['dteday'].max().date())

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]

# Sidebar untuk filter season, weathersit
season_filter = st.sidebar.selectbox("Pilih Season:", day_df['season'].unique())
weathersit_filter = st.sidebar.selectbox("Pilih Weathersit:", day_df['weathersit'].unique())

# Filter data berdasarkan pilihan pengguna
filtered_day_df = filtered_day_df[
    (filtered_day_df['season'] == season_filter) &
    (filtered_day_df['weathersit'] == weathersit_filter)
]

filtered_hour_df = filtered_hour_df[
    (filtered_hour_df['season'] == season_filter) &
    (filtered_hour_df['weathersit'] == weathersit_filter)
]

# Judul aplikasi
st.title("🚴‍♂️ Dashboard Analisis Penyewaan Sepeda 🚴‍♀️")

# Sidebar
st.sidebar.title("🚲 Navigasi")
st.sidebar.write("Selamat datang di dashboard penyewaan sepeda!")

menu = st.sidebar.radio(
    "Pilih Analisis:",
    (
        "Rata-rata Penyewaan Bulanan", 
        "Analisis Hari Libur dan Hari Kerja", 
        "Rata-rata Penyewaan Registered vs Casual"
    )
)

if menu == "Rata-rata Penyewaan Bulanan":
    st.header("📊 Rata-rata Penyewaan Sepeda per Bulan")

    # Filter data untuk 2011 dan 2012
    data_2011 = filtered_day_df[filtered_day_df['yr'] == 0]
    data_2012 = filtered_day_df[filtered_day_df['yr'] == 1]

    avg_rentals_2011 = data_2011.groupby('mnth')['cnt'].mean()
    avg_rentals_2012 = data_2012.groupby('mnth')['cnt'].mean()

    # Pemetaan nama bulan
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    avg_rentals_2011.index = avg_rentals_2011.index.map(month_map)
    avg_rentals_2012.index = avg_rentals_2012.index.map(month_map)
    
    st.subheader("Rata-rata Penyewaan Tahun 2011")
    st.line_chart(avg_rentals_2011)

    st.subheader("Rata-rata Penyewaan Tahun 2012")
    st.line_chart(avg_rentals_2012)

elif menu == "Analisis Hari Libur dan Hari Kerja":
    st.header("📅 Analisis Hari Libur dan Hari Kerja")

    avg_rentals_holiday = filtered_day_df[filtered_day_df['holiday'] == 1]['cnt'].mean()
    avg_rentals_non_holiday = filtered_day_df[filtered_day_df['holiday'] == 0]['cnt'].mean()
    avg_rentals_weekday = filtered_day_df.groupby('weekday')['cnt'].mean()

    st.write(f"**Rata-rata Penyewaan Hari Libur:** {avg_rentals_holiday:.2f}")
    st.write(f"**Rata-rata Penyewaan Hari Biasa:** {avg_rentals_non_holiday:.2f}")

    st.subheader("Penyewaan Berdasarkan Hari dalam Seminggu")
    st.line_chart(avg_rentals_weekday)

elif menu == "Rata-rata Penyewaan Registered vs Casual":
    st.header("👥 Rata-rata Penyewaan Registered vs Casual")

    avg_registered_day = filtered_day_df['registered'].mean()
    avg_casual_day = filtered_day_df['casual'].mean()
    avg_registered_hour = filtered_hour_df['registered'].mean()
    avg_casual_hour = filtered_hour_df['casual'].mean()

    data = pd.DataFrame({
        'Kategori': ['Registered (Day)', 'Casual (Day)', 'Registered (Hour)', 'Casual (Hour)'],
        'Rata-rata': [avg_registered_day, avg_casual_day, avg_registered_hour, avg_casual_hour]
    }).set_index('Kategori')

    st.bar_chart(data)
