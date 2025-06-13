import streamlit as st
import pandas as pd

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Deposito Bulanan", layout="wide")

st.title("Dashboard Monitoring Deposito Bulanan")

# URL CSV Google Sheets publik (pastikan sudah diatur publik)
CSV_URL = "https://docs.google.com/spreadsheets/d/1eoIkgdM2IH513xAx9A_IcumdH23Tw29fvc-KzSrkuGk/export?format=csv"

@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    return pd.read_csv(url)

# Load data terbaru dari Google Sheets
df = load_data(CSV_URL)

# Tampilkan preview data
st.subheader("Tabel Deposito per Bulan")
st.dataframe(df)

# Filter berdasarkan kolom bulan jika tersedia
st.sidebar.header("Filter Data")
month_cols = [col for col in df.columns if any(bulan in col.lower() for bulan in ["jan", "feb", "mar", "apr", "mei", "jun", "jul", "agu", "sep", "okt", "nov", "des"])]

if month_cols:
    selected_month = st.sidebar.selectbox("Pilih Bulan", ["Semua"] + month_cols)
    if selected_month != "Semua":
        df = df[[col for col in df.columns if col not in month_cols or col == selected_month]]

st.subheader("Data Setelah Filter")
st.dataframe(df.reset_index(drop=True))

st.caption("*Data ditarik langsung dari Google Sheets dan difilter berdasarkan kolom bulan.*")
