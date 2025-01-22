import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import time

# Membaca data
day_df = pd.read_csv('/day.csv')
hour_df = pd.read_csv('/hour.csv')

# Mengubah kolom tanggal menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Menggabungkan dataset
all_df = pd.concat([day_df, hour_df], ignore_index=True)

# Tema Streamlit (Gunakan tema bawaan dengan pengaturan "Dark Theme" di Streamlit settings)
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

# Progress bar simulasi loading
with st.spinner("Memuat data..."):
    time.sleep(1)

if menu == "Rata-rata Penyewaan Bulanan":
    st.header("📊 Rata-rata Penyewaan Sepeda per Bulan")

    # Filter data untuk 2011 dan 2012
    data_2011 = day_df[day_df['yr'] == 0]
    data_2012 = day_df[day_df['yr'] == 1]

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

    avg_rentals_holiday = day_df[day_df['holiday'] == 1]['cnt'].mean()
    avg_rentals_non_holiday = day_df[day_df['holiday'] == 0]['cnt'].mean()
    avg_rentals_weekday = day_df.groupby('weekday')['cnt'].mean()

    st.write(f"**Rata-rata Penyewaan Hari Libur:** {avg_rentals_holiday:.2f}")
    st.write(f"**Rata-rata Penyewaan Hari Biasa:** {avg_rentals_non_holiday:.2f}")

    st.subheader("Penyewaan Berdasarkan Hari dalam Seminggu")
    st.line_chart(avg_rentals_weekday)

    st.subheader("Distribusi Penyewaan pada Hari Libur vs Hari Kerja")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(
        x='holiday', 
        y='cnt', 
        data=day_df, 
        palette="Blues",  # Menggunakan palet warna bawaan seaborn
        ax=ax
    )
    ax.set_title("Distribusi Penyewaan Berdasarkan Status Hari Libur")
    st.pyplot(fig)

elif menu == "Rata-rata Penyewaan Registered vs Casual":
    st.header("👥 Rata-rata Penyewaan Registered vs Casual")

    avg_registered_day = day_df['registered'].mean()
    avg_casual_day = day_df['casual'].mean()
    avg_registered_hour = hour_df['registered'].mean()
    avg_casual_hour = hour_df['casual'].mean()

    data = pd.DataFrame({
        'Kategori': ['Registered (Day)', 'Casual (Day)', 'Registered (Hour)', 'Casual (Hour)'],
        'Rata-rata': [avg_registered_day, avg_casual_day, avg_registered_hour, avg_casual_hour]
    }).set_index('Kategori')

    st.bar_chart(data)

# Footer sederhana
st.sidebar.markdown("---")
st.sidebar.caption("💡 Created by Agung Nugraha")
