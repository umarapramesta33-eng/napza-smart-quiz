import streamlit as st
import io
import math
import struct
import wave

# ==========================================
#             KONFIGURASI
# ==========================================

st.set_page_config(
    page_title="NAPZA SMART QUIZ",
    page_icon="🌿",
    layout="centered"
)

# ==========================================
#             SOUND EFFECT
# ==========================================

def buat_suara(frekuensi, durasi=0.25):
    sample_rate = 44100
    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(sample_rate)

        frames = []

        for i in range(int(sample_rate * durasi)):
            waktu = i / sample_rate
            volume = 0.35 * (1 - i / (sample_rate * durasi))

            nilai = int(
                32767 * volume *
                math.sin(2 * math.pi * frekuensi * waktu)
            )

            frames.append(struct.pack("<h", nilai))

        audio.writeframes(b"".join(frames))

    return buffer.getvalue()


def suara_kemenangan():
    sample_rate = 44100
    buffer = io.BytesIO()

    nada = [
        (523, 0.18),
        (659, 0.18),
        (784, 0.18),
        (1047, 0.35)
    ]

    with wave.open(buffer, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(sample_rate)

        frames = []

        for frekuensi, durasi in nada:
            jumlah = int(sample_rate * durasi)

            for i in range(jumlah):
                waktu = i / sample_rate
                volume = 0.30 * (1 - i / jumlah)

                nilai = int(
                    32767 * volume *
                    math.sin(2 * math.pi * frekuensi * waktu)
                )

                frames.append(struct.pack("<h", nilai))

        audio.writeframes(b"".join(frames))

    return buffer.getvalue()


# ==========================================
#             DESAIN WEBSITE
#          FOREST GREEN EDITION
# ==========================================

st.markdown("""
<style>

/* Background utama */
.stApp {
    background-color: #F7F8F2;
    color: #26352B;
}

/* Lebar halaman */
.block-container {
    max-width: 750px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Judul */
h1, h2, h3 {
    color: #17452E !important;
    font-weight: 800;
}

/* Tulisan */
p, label, .stMarkdown {
    color: #26352B;
}

/* Kartu pilihan jawaban */
div[data-testid="stRadio"] {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #D5E2D0;
}

/* Tombol */
.stButton button {
    background-color: #286344;
    color: #FFFFFF;
    border-radius: 12px;
    border: none;
    padding: 13px;
    font-weight: bold;
    width: 100%;
}

/* Efek tombol */
.stButton button:hover {
    background-color: #17452E;
    color: #FFFFFF;
    border: 1px solid #D6A84F;
}

/* Progress bar */
.stProgress > div > div {
    background-color: #286344;
}

/* Kotak informasi */
div[data-testid="stAlert"] {
    border-radius: 14px;
}

/* Garis pembatas */
hr {
    border-color: #D5E2D0;
}

/* Input nama */
.stTextInput input {
    background-color: #FFFFFF;
    color: #26352B;
    border: 1px solid #A8BDA5;
    border-radius: 10px;
}

/* Kartu pertanyaan */
.kartu-soal {
    background-color: #E5EEDC;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #C9D9C1;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
#             DATA PERTANYAAN
# ==========================================

pertanyaan = [

    {
        "emoji": "🌿",
        "soal": "Apa kepanjangan dari NAPZA?",
        "pilihan": [
            "A. Narkotika, Psikotropika, dan Zat Adiktif",
            "B. Narkoba dan Zat Alami",
            "C. Narkotika dan Zat Aman"
        ],
        "benar": "A. Narkotika, Psikotropika, dan Zat Adiktif",
        "penjelasan": "NAPZA merupakan singkatan dari Narkotika, Psikotropika, dan Zat Adiktif."
    },

    {
        "emoji": "🚫",
        "soal": "Apa yang harus dilakukan jika diajak mencoba zat berbahaya?",
        "pilihan": [
            "A. Mengikuti ajakan",
            "B. Menolak dan menjauh",
            "C. Mencoba sekali saja"
        ],
        "benar": "B. Menolak dan menjauh",
        "penjelasan": "Menolak ajakan dan menjauh merupakan langkah untuk melindungi diri."
    },

    {
        "emoji": "🧠",
        "soal": "Mengapa remaja perlu mengetahui informasi NAPZA?",
        "pilihan": [
            "A. Agar terlihat keren",
            "B. Agar mengenali risiko dan melindungi diri",
            "C. Agar bisa mencobanya"
        ],
        "benar": "B. Agar mengenali risiko dan melindungi diri",
        "penjelasan": "Pengetahuan membantu remaja mengenali bahaya dan mengambil keputusan yang tepat."
    },

    {
        "emoji": "🤝",
        "soal": "Apa yang dilakukan jika teman mengajak melakukan hal berisiko?",
        "pilihan": [
            "A. Mengikuti teman",
            "B. Membiarkannya",
            "C. Mencari bantuan orang terpercaya"
        ],
        "benar": "C. Mencari bantuan orang terpercaya",
        "penjelasan": "Orang tua, guru, atau orang dewasa terpercaya dapat membantu menghadapi situasi berisiko."
    },

    {
        "emoji": "🛡️",
        "soal": "Bagaimana cara melindungi diri dari penyalahgunaan NAPZA?",
        "pilihan": [
            "A. Memilih lingkungan pertemanan positif",
            "B. Mengikuti semua ajakan teman",
            "C. Mengabaikan informasi"
        ],
        "benar": "A. Memilih lingkungan pertemanan positif",
        "penjelasan": "Lingkungan positif membantu kita membangun kebiasaan dan keputusan yang sehat."
    }

]


# ==========================================
#             SESSION STATE
# ==========================================

if "nama" not in st.session_state:
    st.session_state.nama = ""

if "mulai" not in st.session_state:
    st.session_state.mulai = False

if "skor" not in st.session_state:
    st.session_state.skor = 0

if "no_soal" not in st.session_state:
    st.session_state.no_soal = 0

if "sudah_jawab" not in st.session_state:
    st.session_state.sudah_jawab = False

if "hasil_jawaban" not in st.session_state:
    st.session_state.hasil_jawaban = False


# ==========================================
#             HEADER WEBSITE
# ==========================================

st.markdown(
    """
    <h1 style='text-align:center;'>
    🌿 NAPZA SMART QUIZ
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h4 style='text-align:center; color:#A17B35;'>
    Kenali, Pahami, Lindungi Diri
    </h4>
    """,
    unsafe_allow_html=True
)

st.divider()


# ==========================================
#             HALAMAN PEMBUKA
# ==========================================

if not st.session_state.mulai:

    st.markdown(
        """
        <h2 style='text-align:center;'>
        👋 HALO, REMAJA CERDAS!
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="kartu-soal">
            <h3>🎮 SIAP MENGUJI PENGETAHUANMU?</h3>
            <p>
            Jawab 5 pertanyaan menarik seputar NAPZA.
            Kumpulkan poin dan buktikan pengetahuanmu!
            </p>
            <h2>⭐ 5 SOAL | 5 POIN</h2>
            <p>🔊 Aktifkan suara perangkatmu untuk pengalaman kuis!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    nama = st.text_input(
        "👤 Masukkan nama peserta:",
        placeholder="Tulis namamu di sini..."
    )

    if st.button("🚀 MULAI KUIS SEKARANG"):

        if nama.strip():
            st.session_state.nama = nama.strip()
            st.session_state.mulai = True
            st.rerun()

        else:
            st.warning("Ups! Masukkan namamu terlebih dahulu 😊")


# ==========================================
#             HALAMAN KUIS
# ==========================================

elif st.session_state.no_soal < len(pertanyaan):

    nomor = st.session_state.no_soal
    soal = pertanyaan[nomor]

    st.markdown(
        f"### 👤 Peserta: {st.session_state.nama}"
    )

    st.progress(
        (nomor + 1) / len(pertanyaan)
    )

    st.caption(
        f"PERTANYAAN {nomor + 1} DARI {len(pertanyaan)}"
    )

    st.markdown("---")

    st.markdown(
        f"""
        <div class="kartu-soal">
            <h1>{soal['emoji']}</h1>
            <h3>SOAL {nomor + 1}</h3>
            <p style="font-size:18px;">
            {soal['soal']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if not st.session_state.sudah_jawab:

        jawaban = st.radio(
            "💭 Pilih jawaban yang menurutmu benar:",
            soal["pilihan"],
            key=f"pilihan_{nomor}"
        )

        if st.button("KIRIM JAWABAN ➜"):

            if jawaban == soal["benar"]:
                st.session_state.skor += 1
                st.session_state.hasil_jawaban = True

            else:
                st.session_state.hasil_jawaban = False

            st.session_state.sudah_jawab = True

            st.rerun()

    else:

        if st.session_state.hasil_jawaban:

            st.success("🎉 BENAR! KERJA BAGUS!")

            st.audio(
                buat_suara(880),
                format="audio/wav",
                autoplay=True
            )

        else:

            st.error("💡 BELUM TEPAT! TETAP SEMANGAT!")

            st.audio(
                buat_suara(260),
                format="audio/wav",
                autoplay=True
            )

            st.write(
                f"Jawaban yang benar: **{soal['benar']}**"
            )

        st.info(
            f"📚 Pembahasan: {soal['penjelasan']}"
        )

        if st.button("LANJUT KE SOAL BERIKUTNYA ➜"):

            st.session_state.no_soal += 1
            st.session_state.sudah_jawab = False

            st.rerun()


# ==========================================
#             HALAMAN HASIL
# ==========================================

else:

    st.balloons()

    st.audio(
        suara_kemenangan(),
        format="audio/wav",
        autoplay=True
    )

    st.markdown(
        """
        <h1 style='text-align:center;'>
        🏆 KUIS SELESAI!
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <h3 style='text-align:center;'>
        Hebat, {st.session_state.nama}!
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    skor = st.session_state.skor

    st.metric(
        "⭐ SKOR AKHIR",
        f"{skor}/5"
    )

    st.progress(skor / 5)

    if skor >= 4:

        st.success("🌟 REMAJA CERDAS!")

        st.write(
            "Wah, pengetahuanmu tentang NAPZA sudah baik! "
            "Pertahankan sikap positif dan terus lindungi dirimu."
        )

    elif skor >= 2:

        st.warning("💡 TERUS BELAJAR!")

        st.write(
            "Pengetahuanmu sudah cukup. "
            "Yuk, tingkatkan lagi pemahamanmu tentang NAPZA!"
        )

    else:

        st.info("📖 YUK BELAJAR LAGI!")

        st.write(
            "Jangan menyerah! Terus belajar dan kenali "
            "informasi NAPZA dari sumber terpercaya."
        )

    st.divider()

    st.markdown(
        """
        <div class="kartu-soal">
            <h3>🌿 PESAN UNTUK KITA SEMUA</h3>
            <h2>KENALI, PAHAMI, LINDUNGI DIRI!</h2>
            <p>Jadilah remaja cerdas, sehat, dan berprestasi.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("🔄 MAIN LAGI"):

        st.session_state.nama = ""
        st.session_state.mulai = False
        st.session_state.skor = 0
        st.session_state.no_soal = 0
        st.session_state.sudah_jawab = False
        st.session_state.hasil_jawaban = False

        st.rerun()

    st.caption(
        "NAPZA SMART QUIZ | Media Edukasi Remaja"
    )
