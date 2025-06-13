import streamlit as st
import pandas as pd

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Deposito Bulanan", layout="wide")

st.title("Dashboard Monitoring Deposito Bulanan")

# URL CSV Google Sheets publik
CSV_URL = "https://docs.google.com/spreadsheets/d/1eoIkgdM2IH513xAx9A_IcumdH23Tw29fvc-KzSrkuGk/export?format=csv"

@st.cache_data(show_spinner=False)
def load_data(url: str) -> pd.DataFrame:
    return pd.read_csv(url)

# Load data terbaru dari Google Sheets
df = load_data(CSV_URL)

# Tampilkan preview seluruh isi data tanpa filter
st.subheader("Tabel Lengkap Deposito (Google Sheets Terbaru)")
st.dataframe(df)

# Catatan untuk pengguna
st.caption("*Data ditarik langsung dari Google Sheets terbaru. Jika struktur berubah (nama kolom baru, baris header berbeda, dsb), silakan pastikan kesesuaian manual atau informasikan perubahan tersebut agar kode disesuaikan kembali.*")
