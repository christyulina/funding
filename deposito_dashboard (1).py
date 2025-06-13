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

# Deteksi kolom utama
base_columns = [col for col in ["Bank", "Jatuh Tempo", "Bilyet"] if col in df.columns]
month_keywords = ["jan", "feb", "mar", "apr", "mei", "jun", "jul", "agu", "aug", "sep", "okt", "oct", "nov", "des", "dec"]
month_columns = [col for col in df.columns if any(k in col.lower() for k in month_keywords)]

# Sidebar - pilih Bank
st.sidebar.header("Filter Data")
bank_options = ["Semua"] + sorted(df['Bank'].dropna().unique().tolist()) if 'Bank' in df.columns else []
selected_bank = st.sidebar.selectbox("Pilih Bank", bank_options)

# Filter berdasarkan Bank jika dipilih
if selected_bank != "Semua" and 'Bank' in df.columns:
    df = df[df['Bank'] == selected_bank]

# Tentukan kolom yang akan ditampilkan
show_columns = base_columns + month_columns

# Tampilkan data
st.subheader("Tabel Deposito per Bulan")
st.dataframe(df[show_columns].reset_index(drop=True))

st.caption("*Data ditampilkan dalam format horizontal dengan filter berdasarkan Bank.*")
