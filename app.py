
import streamlit as st
import time
import io
import wave
import math
import struct
import random
import re

# =====================================
# NAPZA BATTLE
# =====================================

st.set_page_config(
    page_title="NAPZA BATTLE",
    page_icon="⚔️",
    layout="centered"
)

# =====================================
# PILIHAN AVATAR
# =====================================

AVATAR = ["🦊", "🐼", "🐯", "🐸",
          "🐱", "🐲", "🦁", "🐰"]

# =====================================
# PILIHAN BACKGROUND
# =====================================

TEMA = {
    "🌌 Galaxy": """
        radial-gradient(circle at 15% 15%, #5526a8, transparent 40%),
        radial-gradient(circle at 85% 85%, #063b83, transparent 45%),
        linear-gradient(135deg, #100b2e, #101b43, #170d35)
    """,

    "🌊 Ocean": """
        radial-gradient(circle at 15% 15%, #00bcd4, transparent 40%),
        radial-gradient(circle at 85% 85%, #005bea, transparent 45%),
        linear-gradient(135deg, #001f3f, #003b70, #001529)
    """,

    "🌅 Sunset": """
        radial-gradient(circle at 15% 15%, #ff8c42, transparent 40%),
        radial-gradient(circle at 85% 85%, #ff2d75, transparent 45%),
        linear-gradient(135deg, #351044, #8f2457, #29113d)
    """,

    "🌿 Forest": """
        radial-gradient(circle at 15% 15%, #2ecc71, transparent 40%),
        radial-gradient(circle at 85% 85%, #007f5f, transparent 45%),
        linear-gradient(135deg, #092b22, #164b35, #061c19)
    """,

    "🍬 Candy": """
        radial-gradient(circle at 15% 15%, #ff69b4, transparent 40%),
        radial-gradient(circle at 85% 85%, #9b5de5, transparent 45%),
        linear-gradient(135deg, #39104f, #8e44ad, #30104b)
    """,

    "🌑 Dark Arena": """
        radial-gradient(circle at 15% 15%, #a00000, transparent 40%),
        radial-gradient(circle at 85% 85%, #5a0000, transparent 45%),
        linear-gradient(135deg, #090909, #241010, #100000)
    """
}

# =====================================
# 15 TEBAK-TEBAKAN NAPZA
# =====================================

SOAL = [
    ("🧠 + 🛡️", ["melindungi diri"]),
    ("🚫 + 💊", ["menolak penyalahgunaan napza", "menolak napza"]),
    ("👨‍👩‍👧 + ❤️", ["dukungan keluarga"]),
    ("🏫 + 📚", ["edukasi"]),
    ("🤝 + 🚫", ["berani menolak"]),
    ("Singkatan Narkotika, Psikotropika, dan Zat Adiktif?", ["napza"]),
    ("Sulit berhenti menggunakan suatu zat disebut?", ["ketergantungan"]),
    ("Pergaulan dengan pengaruh baik disebut?", ["pertemanan positif"]),
    ("Orang yang bisa dimintai bantuan disebut?", ["orang terpercaya"]),
    ("Kemampuan membedakan fakta dan hoaks disebut?", ["literasi informasi"]),
    ("Jika diajak mencoba zat berbahaya, kita harus?", ["menolak"]),
    ("Jika teman membutuhkan bantuan, kita harus?", ["mencari pertolongan"]),
    ("Olahraga dan berkarya termasuk kegiatan?", ["aktivitas positif"]),
    ("Menjaga diri dari pengaruh buruk disebut?", ["perlindungan diri"]),
    ("Pilihan untuk menjaga kesehatan disebut?", ["hidup sehat"])
]

# =====================================
# SESSION STATE
# =====================================

defaults = {
    "halaman": "awal",
    "nama1": "PLAYER 1",
    "nama2": "PLAYER 2",
    "avatar1": "🦊",
    "avatar2": "🐼",
    "tema": "🌌 Galaxy",
    "skor1": 0,
    "skor2": 0,
    "giliran": 0,
    "urutan": list(range(15)),
    "waktu_mulai": None,
    "jawaban_diperiksa": False,
    "hasil_benar": False,
    "poin_didapat": 0,
    "sound": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =====================================
# SOUND EFFECT
# =====================================

def buat_suara(jenis):
    sample_rate = 44100
    buffer = io.BytesIO()

    nada = {
        "benar": [(660, 0.12), (880, 0.15), (1100, 0.20)],
        "salah": [(220, 0.20), (160, 0.30)],
        "menang": [
            (523, 0.15), (659, 0.15),
            (784, 0.15), (1046, 0.35)
        ]
    }

    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        frames = []

        for frekuensi, durasi in nada[jenis]:
            jumlah = int(sample_rate * durasi)

            for i in range(jumlah):
                fade = min(1, i / 500, (jumlah - i) / 500)

                nilai = int(
                    14000 * fade *
                    math.sin(
                        2 * math.pi * frekuensi * i / sample_rate
                    )
                )

                frames.append(struct.pack("<h", nilai))

        wav.writeframes(b"".join(frames))

    buffer.seek(0)
    return buffer.getvalue()

# =====================================
# CSS ANIMATION
# =====================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Poppins:wght@400;600;700;800&display=swap');

.stApp {
    background: var(--arena-background);
    background-attachment: fixed;
    color: white;
    font-family: 'Poppins', sans-serif;
}

h1, h2, h3 {
    color: white !important;
    font-family: 'Orbitron', sans-serif !important;
}

p, label, span {
    color: white;
}

.main-title {
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 38px;
    font-weight: 900;
    color: #ffe66d;
    text-shadow: 0 0 10px #ff2bd6, 0 0 25px #00d9ff;
    animation: glow 2s infinite alternate;
}

.subtitle {
    text-align: center;
    color: #a9eaff;
    font-size: 13px;
    margin-bottom: 25px;
}

@keyframes glow {
    from {
        text-shadow: 0 0 8px #ff2bd6;
    }
    to {
        text-shadow: 0 0 20px #00d9ff, 0 0 35px #ff2bd6;
    }
}

.card {
    background: rgba(255,255,255,0.10);
    border: 2px solid #8c65ff;
    border-radius: 20px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 0 18px rgba(125,75,255,0.45);
    margin-bottom: 18px;
    animation: cardEnter 0.8s ease-out;
}

@keyframes cardEnter {
    from {
        opacity: 0;
        transform: translateY(25px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.clue {
    background: linear-gradient(135deg, #44217e, #173f78);
    border: 2px solid #00e5ff;
    border-radius: 22px;
    padding: 30px 15px;
    text-align: center;
    font-size: 23px;
    font-weight: 800;
    box-shadow: 0 0 18px #00d9ff;
    margin: 15px 0;
    animation: pulseCard 2s infinite;
}

@keyframes pulseCard {
    0%, 100% {
        box-shadow: 0 0 12px #00d9ff;
    }
    50% {
        box-shadow: 0 0 30px #ff2bd6;
    }
}

.avatar {
    font-size: 65px;
    text-align: center;
    animation: avatarFloat 2s ease-in-out infinite;
    filter: drop-shadow(0 0 12px #00e5ff);
}

@keyframes avatarFloat {
    0%, 100% {
        transform: translateY(0) rotate(-5deg) scale(1);
    }
    50% {
        transform: translateY(-12px) rotate(5deg) scale(1.12);
    }
}

.score {
    background: linear-gradient(135deg, #ff2bd6, #743cff);
    padding: 14px 7px;
    border-radius: 15px;
    text-align: center;
    font-size: 15px;
    font-weight: bold;
    box-shadow: 0 0 15px #ff2bd6;
    margin-bottom: 10px;
}

.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: 2px solid #00e5ff;
    background: linear-gradient(90deg, #743cff, #e52bce);
    color: white !important;
    font-weight: 800;
    font-size: 15px;
    padding: 12px;
    transition: 0.3s;
    animation: buttonGlow 2s infinite alternate;
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 20px #00e5ff;
    border-color: #ffe66d;
}

@keyframes buttonGlow {
    from {
        box-shadow: 0 0 5px #743cff;
    }
    to {
        box-shadow: 0 0 16px #00e5ff;
    }
}

.winner-animation {
    animation: winnerZoom 1.2s infinite alternate;
    font-size: 28px;
    font-weight: bold;
}

@keyframes winnerZoom {
    from {
        transform: scale(1);
        text-shadow: 0 0 10px #ff2bd6;
    }
    to {
        transform: scale(1.08);
        text-shadow: 0 0 30px #ffe66d;
    }
}

.star {
    position: fixed;
    color: #ffe66d;
    font-size: 18px;
    pointer-events: none;
    animation: starMove 7s linear infinite;
    z-index: 0;
}

@keyframes starMove {
    0% {
        transform: translateY(100vh) rotate(0deg);
        opacity: 0;
    }
    20% {
        opacity: 1;
    }
    100% {
        transform: translateY(-100vh) rotate(360deg);
        opacity: 0;
    }
}
</style>
""", unsafe_allow_html=True)

# =====================================
# BACKGROUND AKTIF
# =====================================

tema_aktif = st.session_state.tema

st.markdown(
    f"""
    <style>
    :root {{
        --arena-background: {TEMA[tema_aktif]};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Bintang bergerak
st.markdown("""
<div class="star" style="left:10%; animation-delay:0s;">✦</div>
<div class="star" style="left:25%; animation-delay:2s;">✧</div>
<div class="star" style="left:45%; animation-delay:1s;">✦</div>
<div class="star" style="left:65%; animation-delay:3s;">✧</div>
<div class="star" style="left:85%; animation-delay:1.5s;">✦</div>
<div class="star" style="left:95%; animation-delay:2.5s;">✧</div>
""", unsafe_allow_html=True)

# =====================================
# HEADER
# =====================================

st.markdown(
    '<div class="main-title">⚔️ NAPZA BATTLE ⚔️</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">🔥 DUEL OTAK • 1 VS 1 • BE THE CHAMPION 🔥</div>',
    unsafe_allow_html=True
)

# =====================================
# HALAMAN AWAL
# =====================================

if st.session_state.halaman == "awal":

    st.markdown("""
    <div class="card">
        <h2>🎮 WELCOME TO THE ARENA!</h2>
        <p>Siapkan strategi dan pengetahuanmu!</p>
        <h3>⚡ 1 VS 1 BATTLE ⚡</h3>
        <p>15 tantangan untuk setiap pemain</p>
        <p>Jawaban benar = 10 poin</p>
        <p>Bonus cepat = 5 poin</p>
        <p>⏱️ 15 detik setiap giliran</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🎨 PILIH BACKGROUND ARENA")

    tema_pilihan = st.selectbox(
        "Pilih suasana permainan:",
        list(TEMA.keys()),
        index=list(TEMA.keys()).index(st.session_state.tema),
        key="pilihan_tema"
    )

    st.session_state.tema = tema_pilihan

    # Terapkan tema yang baru dipilih
    st.markdown(
        f"""
        <style>
        :root {{
            --arena-background: {TEMA[tema_pilihan]};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="card">
        <h3>✨ PILIHAN TEMA ✨</h3>
        <p>🌌 Galaxy | 🌊 Ocean | 🌅 Sunset</p>
        <p>🌿 Forest | 🍬 Candy | 🌑 Dark Arena</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("👥 PILIH PEMAIN DAN AVATAR")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🟣 PLAYER 1")

        nama1 = st.text_input(
            "Nama Player 1",
            value="PLAYER 1"
        )

        avatar1 = st.selectbox(
            "Pilih avatar:",
            AVATAR,
            key="pilihan_avatar1"
        )

        st.markdown(
            f'<div class="avatar">{avatar1}</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("### 🔵 PLAYER 2")

        nama2 = st.text_input(
            "Nama Player 2",
            value="PLAYER 2"
        )

        avatar2 = st.selectbox(
            "Pilih avatar:",
            AVATAR,
            index=1,
            key="pilihan_avatar2"
        )

        st.markdown(
            f'<div class="avatar">{avatar2}</div>',
            unsafe_allow_html=True
        )

    if st.button("🚀 MULAI BATTLE!"):

        if not nama1.strip() or not nama2.strip():
            st.warning("Masukkan nama kedua pemain!")

        elif avatar1 == avatar2:
            st.warning("Pilih avatar yang berbeda!")

        else:
            st.session_state.nama1 = nama1.strip()
            st.session_state.nama2 = nama2.strip()

            st.session_state.avatar1 = avatar1
            st.session_state.avatar2 = avatar2
            st.session_state.tema = tema_pilihan

            st.session_state.skor1 = 0
            st.session_state.skor2 = 0
            st.session_state.giliran = 0

            st.session_state.urutan = list(range(15))
            random.shuffle(st.session_state.urutan)

            st.session_state.waktu_mulai = time.time()
            st.session_state.jawaban_diperiksa = False
            st.session_state.sound = None

            st.session_state.halaman = "game"
            st.rerun()

# =====================================
# HALAMAN GAME
# =====================================

elif st.session_state.halaman == "game":

    giliran = st.session_state.giliran

    if giliran >= 30:
        st.session_state.halaman = "hasil"
        st.rerun()

    pemain1 = giliran % 2 == 0

    if pemain1:
        nama = st.session_state.nama1
        avatar = st.session_state.avatar1
    else:
        nama = st.session_state.nama2
        avatar = st.session_state.avatar2

    nomor_soal = giliran // 2
    index_soal = st.session_state.urutan[nomor_soal]

    petunjuk, jawaban_benar = SOAL[index_soal]

    st.markdown(f"""
    <div class="card">
        <h2>⚔️ ARENA BATTLE ⚔️</h2>
        <div class="avatar">{avatar}</div>
        <h3>{nama}</h3>
        <p>RONDE {nomor_soal + 1} / 15</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f'<div class="score">'
            f'{st.session_state.avatar1}<br>'
            f'{st.session_state.nama1}<br>'
            f'{st.session_state.skor1} POIN</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'<div class="score">'
            f'{st.session_state.avatar2}<br>'
            f'{st.session_state.nama2}<br>'
            f'{st.session_state.skor2} POIN</div>',
            unsafe_allow_html=True
        )

    st.progress(giliran / 30)

    st.markdown(
        '<div class="clue">🎯 TEBAK JAWABANNYA!<br><br>'
        + petunjuk +
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state.waktu_mulai is None:
        st.session_state.waktu_mulai = time.time()

    waktu_berjalan = time.time() - st.session_state.waktu_mulai
    waktu_sisa = max(0, 15 - int(waktu_berjalan))

    st.markdown(
        f"<h3 style='text-align:center;color:#ffe66d;'>"
        f"⏱️ WAKTU: {waktu_sisa} DETIK</h3>",
        unsafe_allow_html=True
    )

    if not st.session_state.jawaban_diperiksa:

        with st.form("form_jawaban"):

            jawaban = st.text_input(
                "✍️ Masukkan jawabanmu:"
            )

            submit = st.form_submit_button(
                "⚡ KUNCI JAWABAN!"
            )

        if submit:

            waktu = time.time() - st.session_state.waktu_mulai

            jawaban_user = re.sub(
                r"\s+", " ", jawaban.strip().lower()
            )

            benar = jawaban_user in jawaban_benar

            if waktu > 15:
                benar = False

            st.session_state.hasil_benar = benar

            if benar:

                poin = 10

                if waktu <= 5:
                    poin += 5

                st.session_state.poin_didapat = poin

                if pemain1:
                    st.session_state.skor1 += poin
                else:
                    st.session_state.skor2 += poin

                st.session_state.sound = "benar"

            else:
                st.session_state.poin_didapat = 0
                st.session_state.sound = "salah"

            st.session_state.jawaban_diperiksa = True
            st.rerun()

    else:

        if st.session_state.hasil_benar:

            st.success(
                f"🎉 BENAR! +{st.session_state.poin_didapat} POIN!"
            )

            st.balloons()

        else:
            st.error("❌ JAWABAN BELUM TEPAT!")

        st.info(
            "Jawaban: " + jawaban_benar[0].upper()
        )

        if st.session_state.sound:
            st.audio(
                buat_suara(st.session_state.sound),
                format="audio/wav",
                autoplay=True
            )

        if st.button("➡️ LANJUT KE PEMAIN BERIKUTNYA"):

            st.session_state.giliran += 1
            st.session_state.waktu_mulai = time.time()
            st.session_state.jawaban_diperiksa = False
            st.session_state.sound = None

            st.rerun()

# =====================================
# HALAMAN HASIL
# =====================================

elif st.session_state.halaman == "hasil":

    skor1 = st.session_state.skor1
    skor2 = st.session_state.skor2

    st.balloons()

    st.markdown("""
    <div class="card">
        <h1>🏆 BATTLE COMPLETE! 🏆</h1>
        <h2>THE ARENA HAS A CHAMPION!</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f'<div class="score">'
            f'<div class="avatar">{st.session_state.avatar1}</div>'
            f'{st.session_state.nama1}<br>'
            f'{skor1} POIN</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'<div class="score">'
            f'<div class="avatar">{st.session_state.avatar2}</div>'
            f'{st.session_state.nama2}<br>'
            f'{skor2} POIN</div>',
            unsafe_allow_html=True
        )

    if skor1 > skor2:
        pemenang = st.session_state.nama1
        avatar_pemenang = st.session_state.avatar1

    elif skor2 > skor1:
        pemenang = st.session_state.nama2
        avatar_pemenang = st.session_state.avatar2

    else:
        pemenang = None
        avatar_pemenang = "🤝"

    if pemenang:

        st.markdown(
            f'<div class="clue">'
            f'<div class="avatar">{avatar_pemenang}</div>'
            f'<div class="winner-animation">👑 WINNER 👑</div>'
            f'<br>{pemenang.upper()}<br>🏆 CHAMPION!'
            f'</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="clue">'
            '🤝 DRAW!<br><br>KALIAN SAMA HEBAT!'
            '</div>',
            unsafe_allow_html=True
        )

    st.audio(
        buat_suara("menang"),
        format="audio/wav",
        autoplay=True
    )

    st.markdown("""
    <div class="card">
        <h3>🌿 KENALI, PAHAMI, LINDUNGI DIRI!</h3>
        <p>Jadilah remaja cerdas dan berani menjaga diri.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 MAIN LAGI"):

        for key in defaults:
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()
