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

# Filter berdasarkan kolom jika tersedia
st.sidebar.header("Filter Data")
if 'Bank' in df.columns:
    bank_list = ["Semua"] + sorted(df['Bank'].dropna().unique().tolist())
    selected_bank = st.sidebar.selectbox("Pilih Bank", bank_list)
    if selected_bank != "Semua":
        df = df[df['Bank'] == selected_bank]

st.subheader("Data Setelah Filter")
st.dataframe(df.reset_index(drop=True))

st.caption("*Data ditarik langsung dari Google Sheets yang telah diperbarui.*")
