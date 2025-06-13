import streamlit as st
import pandas as pd

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Deposito Bulanan", layout="wide")

st.title("Dashboard Monitoring Deposito Bulanan")

# URL CSV Google Sheets publik
CSV_URL = "https://docs.google.com/spreadsheets/d/1eoIkgdM2IH513xAx9A_IcumdH23Tw29fvc-KzSrkuGk/export?format=csv"

@st.cache_data(show_spinner=False)
def load_data(url: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Gagal memuat data dari Google Sheets: {e}")
        return pd.DataFrame()

# Load data dari Google Sheets
df = load_data(CSV_URL)

if df.empty:
    st.stop()

# Identifikasi kolom utama dan bulan
known_base = ["Bank", "Jatuh Tempo", "Bilyet", "Amount", "Rate", "Interest"]
base_columns = [col for col in known_base if col in df.columns]
month_keywords = ["jan", "feb", "mar", "apr", "mei", "jun", "jul", "agu", "aug", "sep", "okt", "oct", "nov", "des", "dec"]
month_columns = [col for col in df.columns if any(k in col.lower() for k in month_keywords)]

# Sidebar filter kombinasi
st.sidebar.header("Filter Data")

# Filter bank
if "Bank" in df.columns:
    bank_options = ["Semua"] + sorted(df['Bank'].dropna().unique().tolist())
    selected_bank = st.sidebar.selectbox("Pilih Bank", bank_options)
else:
    selected_bank = "Semua"

# Filter bulan
selected_month = st.sidebar.selectbox("Pilih Bulan", ["Semua"] + month_columns)

# Filter data
if selected_bank != "Semua":
    df = df[df['Bank'] == selected_bank]

# Tentukan kolom yang ditampilkan
if selected_month != "Semua" and selected_month in month_columns:
    display_columns = base_columns + [selected_month]
else:
    display_columns = base_columns + month_columns

# Tampilkan data
st.subheader("Tabel Deposito")
st.dataframe(df[display_columns].reset_index(drop=True))

st.caption("*Data ditampilkan dengan filter kombinasi Bank dan Bulan, dalam format horizontal.*")
