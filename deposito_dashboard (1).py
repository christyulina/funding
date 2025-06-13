import streamlit as st
import pandas as pd

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Deposito Bulanan", layout="wide")

st.title("Dashboard Monitoring Deposito Bulanan")

# URL CSV Google Sheets publik
CSV_URL = "https://docs.google.com/spreadsheets/d/1Ouct7adiZK51oI2DVtU56kMDqE-exQ3ljFtaWnGuXkc/export?format=csv"

@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    return pd.read_csv(url)

# Load data dari Google Sheets
df = load_data(CSV_URL)

# Cek kolom penting
required_cols = ['Bank', 'Jatuh Tempo', 'Bilyet']
if not set(required_cols).issubset(df.columns):
    st.error("Kolom 'Bank', 'Jatuh Tempo', dan 'Bilyet' wajib tersedia di data.")
    st.stop()

# Tampilkan data asli dalam bentuk pivot (lebar)
st.subheader("Tabel Deposito per Bulan")
st.dataframe(df)

# Filter opsional
st.sidebar.header("Filter Data")
bank_list = ["Semua"] + sorted(df['Bank'].dropna().unique().tolist())
selected_bank = st.sidebar.selectbox("Pilih Bank", bank_list)

if selected_bank != "Semua":
    df = df[df['Bank'] == selected_bank]

st.subheader(f"Data Deposito {'- ' + selected_bank if selected_bank != 'Semua' else ''}")
st.dataframe(df.reset_index(drop=True))

st.caption("*Tampilan menunjukkan data dalam format per bulan secara horizontal sesuai struktur Google Sheets.*")
