import streamlit as st

# =====================================
#       NAPZA SMART QUIZ
# =====================================

st.set_page_config(
    page_title="NAPZA SMART QUIZ",
    page_icon="🌿",
    layout="centered"
)

# Tampilan website
st.markdown("""
<style>
.stApp {
    background-color: #F5F0E6;
}
h1, h2, h3 {
    color: #42543B;
}
.stButton button {
    background-color: #657653;
    color: white;
    border-radius: 10px;
    border: none;
}
.stForm {
    background-color: #EAE3D3;
    padding: 20px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# Judul
st.markdown(
    "<h1 style='text-align:center;'>NAPZA SMART QUIZ</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center;color:#8A7655;'>"
    "Kenali, Pahami, Lindungi Diri</h4>",
    unsafe_allow_html=True
)

st.divider()

st.write(
    "Selamat datang! Uji pengetahuanmu tentang NAPZA "
    "melalui lima pertanyaan berikut."
)

st.info(
    "Setiap jawaban benar mendapatkan 1 poin. "
    "Kerjakan dengan teliti, ya!"
)

# =====================================
#           DATA PERTANYAAN
# =====================================

pertanyaan = [
    {
        "soal": "1. Apa kepanjangan dari NAPZA?",
        "pilihan": [
            "A. Narkotika, Psikotropika, dan Zat Adiktif",
            "B. Narkoba dan Zat Alami",
            "C. Narkotika dan Zat Aman"
        ],
        "benar": "A. Narkotika, Psikotropika, dan Zat Adiktif"
    },
    {
        "soal": "2. Apa yang harus dilakukan jika diajak mencoba zat berbahaya?",
        "pilihan": [
            "A. Mengikuti ajakan",
            "B. Menolak dan menjauh",
            "C. Mencoba sekali saja"
        ],
        "benar": "B. Menolak dan menjauh"
    },
    {
        "soal": "3. Mengapa remaja perlu mengetahui informasi NAPZA?",
        "pilihan": [
            "A. Agar terlihat keren",
            "B. Agar mengenali risiko dan melindungi diri",
            "C. Agar bisa mencobanya"
        ],
        "benar": "B. Agar mengenali risiko dan melindungi diri"
    },
    {
        "soal": "4. Apa yang dilakukan jika teman mengajak melakukan hal berisiko?",
        "pilihan": [
            "A. Mengikuti teman",
            "B. Membiarkannya",
            "C. Mencari bantuan orang terpercaya"
        ],
        "benar": "C. Mencari bantuan orang terpercaya"
    },
    {
        "soal": "5. Bagaimana cara melindungi diri dari penyalahgunaan NAPZA?",
        "pilihan": [
            "A. Memilih lingkungan pertemanan positif",
            "B. Mengikuti semua ajakan teman",
            "C. Mengabaikan informasi"
        ],
        "benar": "A. Memilih lingkungan pertemanan positif"
    }
]

# =====================================
#            FORM KUIS
# =====================================

with st.form("napza_quiz"):

    nama = st.text_input("Masukkan nama peserta:")

    jawaban_peserta = []

    for i, item in enumerate(pertanyaan):
        st.markdown("---")
        st.subheader(item["soal"])

        jawaban = st.radio(
            "Pilih jawaban:",
            item["pilihan"],
            key=f"jawaban_{i}"
        )

        jawaban_peserta.append(jawaban)

    kirim = st.form_submit_button("LIHAT HASIL KUIS")

# =====================================
#           PROSES NILAI
# =====================================

if kirim:

    if not nama.strip():
        st.warning("Silakan masukkan nama terlebih dahulu.")

    else:
        skor = 0

        for i in range(5):
            if jawaban_peserta[i] == pertanyaan[i]["benar"]:
                skor += 1

        st.divider()

        st.header("HASIL KUIS")
        st.write(f"Nama peserta: **{nama}**")

        st.metric("SKOR AKHIR", f"{skor}/5")

        st.progress(skor / 5)

        st.subheader("Pembahasan Jawaban")

        for i in range(5):
            if jawaban_peserta[i] == pertanyaan[i]["benar"]:
                st.success(f"Soal {i+1}: Jawaban benar!")
            else:
                st.error(
                    f"Soal {i+1}: Jawaban benar adalah "
                    f"{pertanyaan[i]['benar']}"
                )

        # KATEGORI HASIL
        st.divider()

        if skor >= 4:
            st.success("⭐ REMAJA CERDAS!")
            st.write(
                "Pengetahuanmu tentang NAPZA sudah baik. "
                "Pertahankan sikap positif dan lindungi dirimu!"
            )

            st.code("""
             *
            ***
           *****
          *******
         *********
          *******
           *****
            ***
             *
            """)

            st.balloons()

        elif skor >= 2:
            st.warning("💡 TERUS BELAJAR!")
            st.write(
                "Pengetahuanmu sudah cukup. "
                "Ayo tingkatkan lagi pemahamanmu!"
            )

            st.code("""
           *********
         **         **
        **           **
        **           **
         **         **
           *********
              ***
           *********
            """)

        else:
            st.info("📖 YUK BELAJAR LAGI!")
            st.write(
                "Jangan menyerah! Pelajari kembali informasi "
                "NAPZA dari sumber terpercaya."
            )

            st.code("""
        *****************
        *               *
        *   NAPZA       *
        *   SMART QUIZ  *
        *               *
        *****************
            """)

        # PENUTUP
        st.divider()

        st.markdown(
            "<h3 style='text-align:center;'>"
            "KENALI, PAHAMI, LINDUNGI DIRI!</h3>",
            unsafe_allow_html=True
        )

        st.caption(
            "NAPZA SMART QUIZ | Edukasi Remaja"
        )
