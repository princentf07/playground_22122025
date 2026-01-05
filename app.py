# app.py
# Web App Streamlit: IC50, LC50, EC50 & TPC (Input Manual)

import streamlit as st
import numpy as np
from scipy.stats import linregress

st.set_page_config(page_title="Pengolah Data Bioaktivitas", layout="wide")
st.title("🧪 Sistem Pengolah Data IC₅₀, LC₅₀, EC₅₀ & Total Phenolic Content")

menu = st.sidebar.selectbox(
    "Pilih Jenis Analisis",
    ["IC50 / LC50 / EC50", "Total Phenolic Content (TPC)"]
)

# ==========================
# FUNGSI IC50
# ==========================
def hitung_x50(x, y):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x ** 2)

    a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    b = (sum_y - a * sum_x) / n

    x50 = (50 - b) / a
    return x50, a, b

# ==========================
# IC50 / LC50 / EC50
# ==========================
if menu == "IC50 / LC50 / EC50":
    st.header("📊 Perhitungan IC₅₀ / LC₅₀ / EC₅₀")

    n = st.number_input("Jumlah titik data", min_value=3, value=5)

    x, y = [], []
    for i in range(int(n)):
        col1, col2 = st.columns(2)
        with col1:
            x.append(st.number_input(f"Konsentrasi ke-{i+1}", key=f"x{i}"))
        with col2:
            y.append(st.number_input(f"% Efek ke-{i+1}", key=f"y{i}"))

    if st.button("Hitung X50"):
        x50, a, b = hitung_x50(x, y)
        st.success(f"Persamaan regresi: y = {a:.4f}x + {b:.4f}")
        st.success(f"Nilai X₅₀ = {x50:.4f}")

# ==========================
# TPC
# ==========================
if menu == "Total Phenolic Content (TPC)":
    st.header("🧫 Perhitungan Total Phenolic Content")

    n = st.number_input("Jumlah titik standar", min_value=3, value=5)

    x_std, y_std = [], []
    for i in range(int(n)):
        col1, col2 = st.columns(2)
        with col1:
            x_std.append(st.number_input(f"Konsentrasi standar {i+1}", key=f"xs{i}"))
        with col2:
            y_std.append(st.number_input(f"Absorbansi {i+1}", key=f"ys{i}"))

    slope, intercept, r, p, se = linregress(x_std, y_std)

    st.write(f"Persamaan: y = {slope:.4f}x + {intercept:.4f}")
    st.write(f"R² = {r**2:.4f}")

    abs_sample = st.number_input("Absorbansi sampel")
    dilution = st.number_input("Faktor pengenceran", value=1.0)

    if st.button("Hitung TPC"):
        konsen = (abs_sample - intercept) / slope
        tpc = konsen * dilution
        st.success(f"Total Phenolic Content = {tpc:.4f} mg GAE/g")
