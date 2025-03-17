
import streamlit as st
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Konfigurasi MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
MONGO_collection = os.getenv("MONGO_collection")
db = client[MONGO_collection]
cv_collection = db["cvs"]
roles_collection = db["roles"]

# Konfigurasi API FastAPI
FASTAPI_URL = os.getenv("DEV_BE_URL")

# Sidebar Navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Pilih Halaman:", ["📂 Upload & Match CV", "📝 Tambah Role"])

# 📂 **Page 1: Upload & Match CV**
if page == "📂 Upload & Match CV":
    st.title("🚀 AI-Powered Applicant Tracking System")
    st.subheader("Powered by Qwen 2.5 | Streamline Your Hiring Process")

    # **Upload CV**
    st.header("📂 Upload CV")
    uploaded_file = st.file_uploader("Pilih file CV (PDF atau DOCX)", type=["pdf", "docx"])

    if uploaded_file:
        with st.spinner("📤 Mengunggah CV..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post(f"{FASTAPI_URL}/upload_cv_file", files=files)

        if response.status_code == 200:
            st.success("✅ CV berhasil diunggah!")
            st.balloons()
        else:
            st.error(f"❌ Gagal mengunggah CV! ({response.status_code})")

    # **Matching CV dengan Role**
    st.header("🎯 Match CV ke Role")

    def get_cv_list():
        """Ambil daftar CV dari database."""
        return list(cv_collection.find({}))

    cvs = get_cv_list()

    if cvs:
        cv_options = {cv["filename"]: str(cv["_id"]) for cv in cvs}
        selected_cv = st.selectbox("Pilih CV:", list(cv_options.keys()))

        if st.button("🔍 Match CV"):
            cv_id = cv_options[selected_cv]
            with st.spinner("⚡ Menganalisis CV..."):
                match_response = requests.post(f"{FASTAPI_URL}/match_cv/{cv_id}")

            if match_response.status_code == 200:
                result = match_response.json()
                st.write("### 🏆 Hasil Matching")

                if result["matched_roles"]:
                    for role in result["matched_roles"]:
                        st.markdown(f"""
                        **🛠 Role:** {role["role"]}  
                        **📊 Score:** {role["score"]}   
                        **📌 Justifikasi:** {role["justification"]}
                        """)
                else:
                    st.info("❌ Tidak ada role yang cocok untuk kandidat ini.")
            else:
                st.error(f"❌ Matching gagal! ({match_response.status_code})")
    else:
        st.warning("⚠️ Tidak ada CV yang tersedia. Silakan unggah CV terlebih dahulu.")

# 📝 **Page 2: Tambah Role**
elif page == "📝 Tambah Role":
    st.title("📝 Tambah Role Baru")

    role_name = st.text_input("🛠 Nama Role")
    role_description = st.text_area("📄 Deskripsi Role")

    if st.button("➕ Tambah Role"):
        if role_name and role_description:
            new_role = {"role": role_name, "description": role_description}
            roles_collection.insert_one(new_role)
            st.success(f"✅ Role **{role_name}** berhasil ditambahkan!")
        else:
            st.error("❌ Harap isi semua field!")
    
    # Tampilkan daftar role yang sudah ada
    st.subheader("📜 Daftar Role yang Tersedia")
    roles = list(roles_collection.find({}, {"_id": 0}))

    if roles:
        for role in roles:
            st.markdown(f"**🛠 {role['role']}** - {role['description']}")
    else:
        st.info("🚀 Belum ada role yang ditambahkan.")
