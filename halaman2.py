import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Halaman 2", 
    page_icon="📊",
    layout="wide"
)

st.title("📊 Halaman 2 - Analisis Data")
st.write("Ini adalah halaman 2 yang dapat diakses via URL: `/halaman2`")

# Tab untuk berbagai fungsi
tab1, tab2, tab3 = st.tabs(["📁 Upload Data", "📈 Visualisasi", "⚙️ Pengaturan"])

with tab1:
    st.header("Upload File CSV")
    uploaded_file = st.file_uploader("Pilih file CSV", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ File berhasil diupload! Shape: {df.shape}")
        
        st.subheader("Preview Data:")
        st.dataframe(df.head(), use_container_width=True)
        
        st.subheader("Informasi Data:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Jumlah Baris", df.shape[0])
        with col2:
            st.metric("Jumlah Kolom", df.shape[1])
        with col3:
            st.metric("Total Data Points", df.size)

with tab2:
    st.header("Visualisasi Data")
    
    # Generate sample data jika tidak ada file yang diupload
    if 'uploaded_file' not in locals() or uploaded_file is None:
        st.info("📝 Upload file di tab pertama atau gunakan data sample")
        
        if st.button("Generate Sample Data"):
            # Buat sample data
            np.random.seed(42)
            sample_data = pd.DataFrame({
                'Kategori': ['A', 'B', 'C', 'D', 'E'] * 20,
                'Nilai_X': np.random.randn(100),
                'Nilai_Y': np.random.randn(100) * 2 + 1,
                'Tanggal': pd.date_range('2023-01-01', periods=100, freq='D')
            })
            
            st.session_state.sample_data = sample_data
            st.dataframe(sample_data.head())
    
    if 'sample_data' in st.session_state:
        st.line_chart(st.session_state.sample_data[['Nilai_X', 'Nilai_Y']].head(20))

with tab3:
    st.header("Pengaturan Aplikasi")
    
    # Theme settings
    st.subheader("Tema")
    theme = st.selectbox("Pilih tema:", ["Light", "Dark"])
    
    # Data management
    st.subheader("Manajemen Data")
    if st.button("Hapus Semua Data"):
        if 'shared_data' in st.session_state:
            del st.session_state.shared_data
        if 'sample_data' in st.session_state:
            del st.session_state.sample_data
        st.success("🧹 Semua data berhasil dihapus!")

# Tampilkan shared data jika ada
if 'shared_data' in st.session_state:
    st.sidebar.subheader("Data dari Halaman 1:")
    st.sidebar.write(st.session_state.shared_data)

# Navigasi cepat
st.markdown("---")
st.page_link("Main_App.py", label="🏠 Kembali ke Halaman Utama", icon="🏠")
st.page_link("pages/1_📝_Halaman_1.py", label="📝 Pergi ke Halaman 1", icon="📝")