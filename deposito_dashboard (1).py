import streamlit as st
import pandas as pd
import altair as alt
import re

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Deposito Bulanan", layout="wide")

st.title("Dashboard Monitoring Deposito Bulanan")

# URL CSV Google Sheets publik
CSV_URL = "https://docs.google.com/spreadsheets/d/1Ouct7adiZK51oI2DVtU56kMDqE-exQ3ljFtaWnGuXkc/export?format=csv"

@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    return pd.read_csv(url)

df = load_data(CSV_URL)

# Validasi kolom
expected_cols = {"Bulan", "Bank"}
if not expected_cols.issubset(df.columns):
    st.error("Kolom data tidak sesuai. Pastikan terdapat kolom 'Bulan' dan 'Bank'.")
    st.stop()

ALL = "Semua"

def parse_month(month_str: str):
    try:
        return pd.to_datetime(month_str, dayfirst=False)
    except Exception:
        mapping = {
            "Januari": 1, "Februari": 2, "Maret": 3, "April": 4, "Mei": 5, "Juni": 6,
            "Juli": 7, "Agustus": 8, "September": 9, "Oktober": 10, "November": 11, "Desember": 12,
            "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Mei": 5, "Jun": 6,
            "Jul": 7, "Aug": 8, "Agu": 8, "Sep": 9, "Oct": 10, "Okt": 10, "Nov": 11, "Dec": 12
        }
        match = re.search(r"(\d{4})", month_str)
        year = int(match.group(1)) if match else None
        month_num = None
        for name, num in mapping.items():
            if name in month_str:
                month_num = num
                break
        if year and month_num:
            return pd.Timestamp(year, month_num, 1)
        else:
            return None

unique_months = df["Bulan"].unique()
unique_banks = df["Bank"].unique()
months_sorted = sorted(unique_months, key=lambda x: parse_month(x) or x)
month_options = [ALL] + months_sorted
bank_options = [ALL] + sorted(unique_banks)

# Sidebar filter
st.sidebar.header("Filter")
selected_month = st.sidebar.selectbox("Filter Bulan", month_options)
selected_bank = st.sidebar.selectbox("Filter Bank", bank_options)

# Terapkan filter
df_filtered = df.copy()
if selected_month != ALL:
    df_filtered = df_filtered[df_filtered["Bulan"] == selected_month]
if selected_bank != ALL:
    df_filtered = df_filtered[df_filtered["Bank"] == selected_bank]

# Tampilkan data yang difilter
st.subheader("Data Deposito yang Difilter")
st.dataframe(df_filtered)

st.caption("*Menampilkan data dari Google Sheets berdasarkan filter bulan dan bank.*")
