import streamlit as st
import pandas as pd
import altair as alt

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Deposito Bulanan", layout="wide")

st.title("Dashboard Monitoring Deposito Bulanan")

# URL CSV Google Sheets publik
CSV_URL = "https://docs.google.com/spreadsheets/d/1Ouct7adiZK51oI2DVtU56kMDqE-exQ3ljFtaWnGuXkc/export?format=csv"

@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    return pd.read_csv(url)

# Load and transform data
raw_df = load_data(CSV_URL)

# Cek kolom wajib awal
required_prefix = ['Bank', 'Jatuh Tempo', 'Bilyet']
if not set(required_prefix).issubset(raw_df.columns):
    st.error("Kolom wajib 'Bank', 'Jatuh Tempo', dan 'Bilyet' tidak ditemukan di spreadsheet.")
    st.stop()

# Transformasi dari wide ke long
value_vars = [col for col in raw_df.columns if col not in required_prefix]
df = raw_df.melt(id_vars=required_prefix, var_name='Bulan', value_name='Nilai')

# Drop data kosong dan pastikan kolom Nilai numerik
df.dropna(subset=['Nilai'], inplace=True)
df = df[df['Nilai'] != 0]
df['Nilai'] = pd.to_numeric(df['Nilai'], errors='coerce')
df.dropna(subset=['Nilai'], inplace=True)

# Filter unik
bulan_options = ["Semua"] + sorted(df['Bulan'].unique().tolist())
bank_options = ["Semua"] + sorted(df['Bank'].unique().tolist())

# Sidebar Filter
st.sidebar.header("Filter")
selected_bulan = st.sidebar.selectbox("Pilih Bulan", bulan_options)
selected_bank = st.sidebar.selectbox("Pilih Bank", bank_options)

# Filter data sesuai pilihan
filtered_df = df.copy()
if selected_bulan != "Semua":
    filtered_df = filtered_df[filtered_df['Bulan'] == selected_bulan]
if selected_bank != "Semua":
    filtered_df = filtered_df[filtered_df['Bank'] == selected_bank]

# Tampilkan data
st.subheader("Data Deposito")
st.dataframe(filtered_df)

# Grafik Total per Bank
st.subheader("Total per Bank")
total_bank = filtered_df.groupby('Bank')['Nilai'].sum().reset_index()
bar_chart = alt.Chart(total_bank).mark_bar().encode(
    x=alt.X('Bank:N', sort='-y'),
    y=alt.Y('Nilai:Q', title='Total Nilai'),
    tooltip=['Bank', 'Nilai']
)
st.altair_chart(bar_chart, use_container_width=True)

# Grafik Tren per Bulan
st.subheader("Tren per Bulan")
total_bulan = filtered_df.groupby('Bulan')['Nilai'].sum().reset_index()
line_chart = alt.Chart(total_bulan).mark_line(point=True).encode(
    x=alt.X('Bulan:N', sort=None),
    y=alt.Y('Nilai:Q', title='Total Nilai'),
    tooltip=['Bulan', 'Nilai']
)
st.altair_chart(line_chart, use_container_width=True)

st.caption("*Data diambil dari Google Sheets format pivot dan ditransformasi otomatis.")
