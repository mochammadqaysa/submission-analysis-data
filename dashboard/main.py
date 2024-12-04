
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

days_df = pd.read_csv("days_dataframe.csv")
days_df["dteday"] = pd.to_datetime(days_df["dteday"])

min_date = days_df["dteday"].min()
max_date = days_df["dteday"].max()

with st.sidebar:
    st.image("https://github.com/mochammadqaysa/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_data = days_df[(days_df["dteday"] >= pd.Timestamp(start_date)) & (days_df["dteday"] <= pd.Timestamp(end_date))]

st.header("Sharing Bike : Dashboard 🚴")

total_bikes = filtered_data["cnt"].sum()
registered_users = filtered_data["registered"].sum()
casual_users = filtered_data["casual"].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sepeda Dipinjam", value=total_bikes)
with col2:
    st.metric("Total Pengguna Terdaftar", value=registered_users)
with col3:
    st.metric("Total Pengguna Kasual", value=casual_users)

st.markdown("---")

st.subheader("Jumlah Total Sepeda Dipinjam dari Waktu ke Waktu")
plt.figure(figsize=(10, 5))
sns.lineplot(data=filtered_data, x="dteday", y="cnt", label="Total Peminjaman")
plt.title("Tren Peminjaman Sepeda Harian")
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Sepeda")
plt.xticks(rotation=45)
st.pyplot(plt.gcf())

st.subheader("Pengguna Terdaftar vs Pengguna Kasual")
user_type_data = filtered_data[["casual", "registered"]].sum().reset_index()
user_type_data.columns = ["Tipe Pengguna", "Jumlah"]
plt.figure(figsize=(6, 4))
sns.barplot(data=user_type_data, x="Tipe Pengguna", y="Jumlah", palette="viridis")
plt.title("Perbandingan Pengguna Kasual dan Terdaftar")
st.pyplot(plt.gcf())

st.subheader("Distribusi Suhu terhadap Total Peminjaman")
plt.figure(figsize=(10, 5))
sns.scatterplot(data=filtered_data, x="temp", y="cnt", hue="weathersit", palette="coolwarm")
plt.title("Suhu vs Total Peminjaman Sepeda")
plt.xlabel("Suhu")
plt.ylabel("Jumlah Sepeda")
st.pyplot(plt.gcf())


st.subheader("Distribusi Jumlah Peminjaman Berdasarkan Musim")
season_data = filtered_data.groupby("season")["cnt"].sum().reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(data=season_data, x="season", y="cnt", palette="pastel")
plt.title("Jumlah Peminjaman Berdasarkan Musim")
plt.xlabel("Musim")
plt.ylabel("Jumlah Sepeda")
st.pyplot(plt.gcf())

st.subheader("Kelembapan vs Peminjaman Berdasarkan Musim")
selected_season = st.selectbox("Pilih Musim", options=filtered_data["season"].unique())
filtered_by_season = filtered_data[filtered_data["season"] == selected_season]
plt.figure(figsize=(10, 5))
sns.scatterplot(data=filtered_by_season, x="hum", y="cnt", hue="weathersit", palette="coolwarm")
plt.title(f"Kelembapan vs Peminjaman Sepeda (Musim: {selected_season})")
plt.xlabel("Kelembapan")
plt.ylabel("Jumlah Sepeda")
st.pyplot(plt.gcf())


st.markdown("---")
st.markdown("Copyright 2024 ©️ Mochammad Qaysa Al-Haq")
