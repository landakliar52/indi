import streamlit as st
import json
import os

# Nama file untuk menyimpan data pengguna
USER_DATA_FILE = 'users.json'

# Fungsi untuk memuat data pengguna dari file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

# Fungsi untuk menyimpan data pengguna ke file
def save_user_data(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file)

# Memuat data pengguna saat aplikasi dimulai
users = load_user_data()

# Fungsi untuk menampilkan halaman login
def login_page():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login", key="login_button"):
        if username in users and users[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"Welcome {username}!")
        else:
            st.error("Username atau password salah!")

# Fungsi untuk menampilkan halaman sign-up
def signup_page():
    st.subheader("Sign Up")
    new_username = st.text_input("Username Baru")
    new_password = st.text_input("Password Baru", type="password")
    confirm_password = st.text_input("Konfirmasi Password", type="password")
    if st.button("Sign Up", key="signup_button"):
        if new_username in users:
            st.error("Username sudah terdaftar, gunakan username lain.")
        elif new_password != confirm_password:
            st.error("Password dan konfirmasi password tidak cocok.")
        else:
            # Menambahkan pengguna baru ke data users
            users[new_username] = new_password
            save_user_data(users)  # Menyimpan data pengguna yang diperbarui ke file
            st.success("Pendaftaran berhasil! Silakan login.")
            st.session_state["signup"] = False

# Pengelolaan sesi login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "signup" not in st.session_state:
    st.session_state["signup"] = False

# Menampilkan pilihan Login atau Sign Up
if st.session_state["logged_in"]:
    st.sidebar.write(f"Logged in as: {st.session_state['username']}")
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state["logged_in"] = False
        st.sidebar.write("You have been logged out.")
else:
    if st.sidebar.button("Login", key="show_login"):
        st.session_state["signup"] = False
    if st.sidebar.button("Sign Up", key="show_signup"):
        st.session_state["signup"] = True

    if st.session_state["signup"]:
        signup_page()
    else:
        login_page()

# Menampilkan aplikasi utama hanya jika pengguna sudah login
if st.session_state["logged_in"]:
    # Formulir Deteksi Kesehatan Mental
    st.title("Formulir Deteksi Kesehatan Mental")
    st.write("Isilah formulir berikut untuk menilai kesehatan mental Anda.")
    
    # Informasi pribadi
    st.header("Informasi Pribadi")
    name = st.text_input("Nama")
    age = st.number_input("Usia", min_value=0)
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan", "Lainnya"])
    
    # Gejala dan Faktor Risiko
    st.header("Gejala dan Faktor Risiko")
    anxiety = st.checkbox("Kecemasan yang berlebihan")
    depression = st.checkbox("Perasaan sedih atau tidak tertarik pada aktivitas")
    stress = st.checkbox("Stres berlebihan")
    insomnia = st.checkbox("Masalah tidur atau gangguan tidur lainnya")
    fatigue = st.checkbox("Kelelahan yang berlebihan")
    mood_swings = st.checkbox("Perubahan suasana hati yang signifikan")
    social_withdrawal = st.checkbox("Menarik diri dari aktivitas sosial")
    
    # Kondisi Kesehatan yang Ada
    st.header("Kondisi Kesehatan yang Ada")
    chronic_conditions = st.multiselect(
        "Apakah Anda memiliki kondisi kesehatan kronis?",
        ["Hipertensi", "Diabetes", "Penyakit Jantung", "Penyakit Autoimun", "Lainnya"]
    )
    
    # Tombol Submit
    if st.button("Submit", key="submit_button"):
        # Logika deteksi sederhana
        risk_score = 0
        
        # Penilaian berdasarkan gejala dan faktor risiko
        if anxiety:
            risk_score += 1
        if depression:
            risk_score += 1
        if stress:
            risk_score += 1
        if insomnia:
            risk_score += 1
        if fatigue:
            risk_score += 1
        if mood_swings:
            risk_score += 1
        if social_withdrawal:
            risk_score += 1
        
        # Penilaian berdasarkan kondisi kesehatan yang ada
        if "Hipertensi" in chronic_conditions:
            risk_score += 1
        if "Diabetes" in chronic_conditions:
            risk_score += 1
        if "Penyakit Jantung" in chronic_conditions:
            risk_score += 1
        if "Penyakit Autoimun" in chronic_conditions:
            risk_score += 1
    
        # Menentukan hasil
        if risk_score >= 4:
            st.error("Hasil: Perlu Konsultasi - Terdapat tanda-tanda yang perlu diperiksa lebih lanjut oleh profesional kesehatan mental.")
        else:
            st.success("Hasil: Normal - Tidak ada tanda-tanda yang mencurigakan secara klinis. Tetap jaga kesehatan mental Anda.")
else:
    st.info("Silakan login atau sign up untuk melanjutkan.")
