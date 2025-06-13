import streamlit as st
import pandas as pd

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Deposito Bulanan", layout="wide")

st.title("Dashboard Monitoring Deposito Bulanan")

# URL CSV Google Sheets publik
CSV_URL = "https://docs.google.com/spreadsheets/d/1eoIkgdM2IH513xAx9A_IcumdH23Tw29fvc-KzSrkuGk/export?format=csv"

@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    return pd.read_csv(url)

# Load data dari Google Sheets
df = load_data(CSV_URL)

# Deteksi kolom bulan dari header
month_keywords = ["jan", "feb", "mar", "apr", "mei", "jun", "jul", "agu", "aug", "sep", "okt", "oct", "nov", "des", "dec"]
month_columns = [col for col in df.columns if any(k in col.lower() for k in month_keywords)]

# Sidebar - pilih bulan dari kolom
st.sidebar.header("Filter Data")
selected_month = st.sidebar.selectbox("Pilih Bulan", ["Semua"] + month_columns)

# Kolom dasar
base_columns = [col for col in ["Bank", "Jatuh Tempo", "Bilyet"] if col in df.columns]

# Tentukan kolom yang ditampilkan
if selected_month != "Semua" and selected_month in df.columns:
    show_columns = base_columns + [selected_month]
else:
    show_columns = base_columns + month_columns

# Tampilkan data
st.subheader("Tabel Deposito per Bulan")
st.dataframe(df[show_columns])

st.caption("*Data ditampilkan berdasarkan kolom bulan horizontal yang dipilih.*")
