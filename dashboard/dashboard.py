import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style='dark')

data = pd.read_csv('dashboard/main_data.csv')
data['dteday'] = pd.to_datetime(data['dteday'])

# Judul aplikasi
st.title("Dashboard Analisis Data")

# Menampilkan data
st.subheader("Dataset")
st.write(data.head())

# Pilih kolom untuk visualisasi
st.subheader("Visualisasi Data")
selected_column = st.selectbox("Pilih kolom untuk visualisasi:", data.columns)

# Plot histogram
fig, ax = plt.subplots()
sns.histplot(data[selected_column], kde=True, ax=ax)
st.pyplot(fig)

# Ringkasan statistik
st.subheader("Ringkasan Statistik")
st.write(data.describe())

# Pertanyaan 1: Tren Penyewaan Sepeda Berdasarkan Musim
st.subheader("Tren Penyewaan Sepeda Berdasarkan Musim (Jan 2012 - Jan 2013)")

# Filter data untuk periode 2012-01 hingga 2013-01
data_filtered = data[(data["dteday"] >= "2012-01-01") & (data["dteday"] < "2013-02-01")]

# Mengelompokkan data berdasarkan waktu dan musim
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
data_filtered["season_label"] = data_filtered["season"].map(season_mapping)
data_season_trend = data_filtered.groupby(["dteday", "season_label"])["cnt"].mean().reset_index()

# Membuat line plot tren penyewaan sepeda berdasarkan musim
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x="dteday", y="cnt", hue="season_label", data=data_season_trend, palette="coolwarm", marker="o", ax=ax)

ax.set_xlabel(None)
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Tren Penyewaan Sepeda Berdasarkan Musim (Jan 2012 - Jan 2013)")
ax.legend(title="Musim")
ax.grid(axis="y", linestyle="--", alpha=0.5)
st.pyplot(fig)

# Pertanyaan 2: Jam dengan Penyewaan Tertinggi dan Terendah
st.subheader("Jam dengan Rata-Rata Penyewaan Sepeda Tertinggi dan Terendah")

# Mengelompokkan data berdasarkan jam
data_hour = data.groupby("hr")["cnt"].mean().reset_index().rename(columns={"cnt": "mean"})

# Menentukan jam dengan penyewaan tertinggi dan terendah
top_5_hours = data_hour.sort_values(by="mean", ascending=False).head(5)
bottom_5_hours = data_hour.sort_values(by="mean", ascending=True).head(5)

# Urutan jam untuk top 5 dan bottom 5
top_5_order = top_5_hours["hr"].tolist()
bottom_5_order = bottom_5_hours["hr"].tolist()

# Membuat plot berdampingan
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

# Warna khusus untuk bar terbesar/kecil
colors = ["#3200FF"] + ["#D3D3D3"] * 4

# Bar plot jam dengan penyewaan tertinggi
sns.barplot(x="mean", y="hr", data=top_5_hours, palette=colors, orient='h', order=top_5_order, ax=ax[0])
ax[0].set_xlabel("Rata-rata Penyewaan Sepeda")
ax[0].set_ylabel("Jam")
ax[0].set_title("Jam dengan Penyewaan Tertinggi", loc="center", fontsize=15, y=1.03)
ax[0].tick_params(axis='x', labelsize=12)

# Bar plot jam dengan penyewaan terendah
sns.barplot(x="mean", y="hr", data=bottom_5_hours, palette=colors, orient='h', order=bottom_5_order, ax=ax[1])
ax[1].set_xlabel("Rata-rata Penyewaan Sepeda")
ax[1].set_ylabel("Jam")
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Jam dengan Penyewaan Terendah", loc="center", fontsize=15, y=1.03)
ax[1].tick_params(axis='x', labelsize=12)

plt.suptitle("Jam dengan Rata-Rata Penyewaan Sepeda Tertinggi dan Terendah", fontsize=20, y=1.05)
st.pyplot(fig)