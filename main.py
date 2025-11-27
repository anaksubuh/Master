import streamlit as st

st.set_page_config(
    page_title="Aplikasi Utama",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Halaman Utama")
st.write("Selamat datang di aplikasi multi-halaman!")

st.markdown("""
### Akses halaman melalui URL:
- **Halaman 1**: http://localhost:8501/halaman1
- **Halaman 2**: http://localhost:8501/halaman2

### Atau navigasi dari sidebar 👈
""")

# Informasi tambahan
st.sidebar.success("Pilih halaman di atas ↑")

# Tampilkan data dari session state (jika ada)
if 'shared_data' in st.session_state:
    st.subheader("Data yang dibagikan antar halaman:")
    st.write(st.session_state.shared_data)