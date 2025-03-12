import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk memuat data
def load_data(filename):
    base_dir = os.path.abspath(os.path.join(__file__, ".."))
    file_path = os.path.join(base_dir, filename)
    return pd.read_csv(file_path)

# Fungsi untuk mengkategorikan tipe hari
def categorize_day(day):
    return 'Weekend' if day in ['Saturday', 'Sunday'] else 'Weekday'

# Memuat dan membersihkan data
@st.cache_data
def prepare_data():
    # Memuat dataset
    hour_df = load_data('../data/hour.csv')
    day_df = load_data('../data/day.csv')

    # Mengubah tipe data
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])

    # Mengubah kolom kategori
    category_columns = ['season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit']
    for col in category_columns:
        if col in hour_df.columns:
            hour_df[col] = hour_df[col].astype('category')
        if col in day_df.columns:
            day_df[col] = day_df[col].astype('category')

    # Mapping nilai musim
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    hour_df['season'] = hour_df['season'].map(season_mapping)
    day_df['season'] = day_df['season'].map(season_mapping)

    # Mapping hari dalam seminggu
    day_mapping = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 
                   4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
    hour_df['weekday'] = hour_df['weekday'].map(day_mapping)
    day_df['weekday'] = day_df['weekday'].map(day_mapping)

    # Mapping cuaca
    weather_mapping = {1: 'Clear', 2: 'Mist', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
    hour_df['weathersit'] = hour_df['weathersit'].map(weather_mapping)
    day_df['weathersit'] = day_df['weathersit'].map(weather_mapping)

    # Menambahkan kolom tipe hari
    hour_df['day_type'] = hour_df['weekday'].apply(categorize_day)
    day_df['day_type'] = day_df['weekday'].apply(categorize_day)

    return hour_df, day_df

# Main app
def main():
    st.title("Dashboard Analisis Penyewaan Sepeda")
    st.write("Dashboard ini menganalisis data penyewaan sepeda di Washington, D.C. 2011-2012")

    # Memuat data
    hour_df, day_df = prepare_data()

    # Sidebar untuk filter
    st.sidebar.header("Filter Data")
    selected_season = st.sidebar.multiselect("Pilih Musim", options=day_df['season'].unique(), default=day_df['season'].unique())
    selected_weather = st.sidebar.multiselect("Pilih Cuaca", options=day_df['weathersit'].unique(), default=day_df['weathersit'].unique())
    selected_day_type = st.sidebar.multiselect("Pilih Tipe Hari", options=day_df['day_type'].unique(), default=day_df['day_type'].unique())

    # Filter data berdasarkan pilihan pengguna
    filtered_hour_df = hour_df[
        (hour_df['season'].isin(selected_season)) &
        (hour_df['weathersit'].isin(selected_weather)) &
        (hour_df['day_type'].isin(selected_day_type))
    ]
    filtered_day_df = day_df[
        (day_df['season'].isin(selected_season)) &
        (day_df['weathersit'].isin(selected_weather)) &
        (day_df['day_type'].isin(selected_day_type))
    ]

    # Analisis 1: Penyewaan per jam
    st.header("Penyewaan Sepeda per Jam")
    if not filtered_hour_df.empty:
        hourly_rentals = filtered_hour_df.groupby('hr', observed=True)['cnt'].sum()
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        hourly_rentals.plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_title("Total Penyewaan Sepeda per Jam")
        ax1.set_xlabel("Jam")
        ax1.set_ylabel("Total Penyewaan")
        st.pyplot(fig1)
        st.write("**Insight**: Penyewaan puncak terjadi pada jam 17:00 (5 PM), terendah pada jam 04:00 (4 AM), mencerminkan pola komuter.")
    else:
        st.write("Tidak ada data yang tersedia untuk filter yang dipilih pada Penyewaan Sepeda per Jam.")

    # Analisis 2: Penyewaan per musim
    st.header("Penyewaan Sepeda per Musim")
    if not filtered_day_df.empty:
        seasonal_rentals = filtered_day_df.groupby('season', observed=True)['cnt'].sum()
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        seasonal_rentals.plot(kind='bar', ax=ax2, color='salmon')
        ax2.set_title("Total Penyewaan Sepeda per Musim")
        ax2.set_xlabel("Musim")
        ax2.set_ylabel("Total Penyewaan")
        st.pyplot(fig2)
        st.write("**Insight**: Musim gugur (Fall) memiliki total penyewaan tertinggi, kemungkinan karena cuaca nyaman di Washington, D.C.")
    else:
        st.write("Tidak ada data yang tersedia untuk filter yang dipilih pada Penyewaan Sepeda per Musim.")

    # Analisis Tambahan: Pengaruh cuaca dan tipe hari
    st.header("Pengaruh Cuaca dan Tipe Hari")
    if not filtered_day_df.empty:
        weather_day_rentals = filtered_day_df.groupby(['weathersit', 'day_type'], observed=True)['cnt'].mean().unstack()
        if not weather_day_rentals.empty:
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            sns.heatmap(weather_day_rentals, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax3)
            ax3.set_title("Rata-rata Penyewaan Berdasarkan Cuaca dan Tipe Hari")
            ax3.set_xlabel("Tipe Hari")
            ax3.set_ylabel("Kondisi Cuaca")
            st.pyplot(fig3)
            st.write("**Insight**: Cuaca cerah pada hari kerja meningkatkan penyewaan secara signifikan.")
        else:
            st.write("Tidak ada data untuk heatmap setelah pengelompokan.")
    else:
        st.write("Tidak ada data yang tersedia untuk filter yang dipilih pada Pengaruh Cuaca dan Tipe Hari.")

    # Rekomendasi
    st.header("Rekomendasi Bisnis")
    st.markdown("""
    - **Tambah stok sepeda** pada jam 17:00 untuk mengakomodasi puncak penyewaan.
    - **Kurangi stok** pada jam 04:00 saat permintaan rendah.
    - **Promosi di musim gugur**, terutama pada hari kerja dengan cuaca cerah, untuk memaksimalkan penyewaan.
    """)

if __name__ == "__main__":
    main()
