import streamlit as st

st.set_page_config(
    page_title="Halaman 1",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Halaman 1 - Input Data")
st.write("Ini adalah halaman 1 yang dapat diakses via URL: `/halaman1`")

# Form input data
with st.form("input_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        nama = st.text_input("Nama Lengkap:")
        email = st.text_input("Email:")
    
    with col2:
        umur = st.number_input("Umur:", min_value=0, max_value=100)
        kota = st.selectbox("Kota:", ["Jakarta", "Bandung", "Surabaya", "Medan", "Makassar"])
    
    submitted = st.form_submit_button("Simpan Data")
    
    if submitted:
        # Simpan ke session state untuk berbagi data antar halaman
        st.session_state.shared_data = {
            'nama': nama,
            'email': email,
            'umur': umur,
            'kota': kota,
            'dari_halaman': 'Halaman 1'
        }
        st.success("✅ Data berhasil disimpan!")
        st.balloons()

# Tampilkan data yang disimpan
if 'shared_data' in st.session_state:
    st.subheader("Data Tersimpan:")
    st.json(st.session_state.shared_data)

# Navigasi cepat
st.markdown("---")
st.page_link("Main_App.py", label="🏠 Kembali ke Halaman Utama", icon="🏠")
st.page_link("pages/2_📊_Halaman_2.py", label="📊 Pergi ke Halaman 2", icon="📊")