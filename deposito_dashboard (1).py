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
        df.columns = df.columns.str.strip()  # normalisasi nama kolom
        return df
    except Exception as e:
        st.error(f"Gagal memuat data dari Google Sheets: {e}")
        return pd.DataFrame()

# Load data dari Google Sheets
df = load_data(CSV_URL)

if df.empty:
    st.warning("Data kosong atau tidak berhasil dimuat.")
    st.stop()

# Tampilkan struktur data mentah untuk debug awal
st.sidebar.markdown("### Debugging Info")
st.sidebar.write("Kolom ditemukan:", df.columns.tolist())

# Identifikasi kolom dinamis
month_keywords = ["jan", "feb", "mar", "apr", "mei", "jun", "jul", "agu", "aug", "sep", "okt", "oct", "nov", "des", "dec"]
month_columns = [col for col in df.columns if any(k in col.lower() for k in month_keywords)]
base_candidates = ["bank", "jatuh tempo", "bilyet", "amount", "rate", "interest"]
base_columns = [col for col in df.columns if any(k in col.lower() for k in base_candidates)]

# Deteksi nama kolom Bank secara fleksibel
bank_column = next((col for col in df.columns if 'bank' in col.lower()), None)

# Sidebar Filter
st.sidebar.header("Filter Data")
selected_bank = "Semua"
if bank_column:
    bank_options = ["Semua"] + sorted(df[bank_column].dropna().unique().tolist())
    selected_bank = st.sidebar.selectbox("Pilih Bank", bank_options)

selected_month = st.sidebar.selectbox("Pilih Bulan", ["Semua"] + month_columns)

# Terapkan filter
if selected_bank != "Semua" and bank_column:
    df = df[df[bank_column] == selected_bank]

# Tentukan kolom yang akan ditampilkan
if selected_month != "Semua" and selected_month in df.columns:
    display_columns = base_columns + [selected_month]
else:
    display_columns = base_columns + month_columns

# Tampilkan data
st.subheader("Tabel Deposito")
if not df.empty and display_columns:
    st.dataframe(df[display_columns].reset_index(drop=True))
else:
    st.info("Tidak ada data yang sesuai dengan filter.")

st.caption("*Data ditampilkan berdasarkan filter bank dan bulan, menyesuaikan struktur Google Sheets terbaru.*")
