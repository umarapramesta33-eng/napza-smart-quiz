import streamlit as st
import random
import time

# =========================
# KONFIGURASI HALAMAN
# =========================

st.set_page_config(
    page_title="NAPZA BATTLE",
    page_icon="⚔️",
    layout="wide"
)

# =========================
# BANK SOAL
# =========================

QUESTIONS = [
    {
        "q": "Apa kepanjangan dari NAPZA?",
        "a": "Narkotika, Psikotropika, dan Zat Adiktif",
        "options": [
            "Narkotika, Psikotropika, dan Zat Adiktif",
            "Nasional, Psikologi, dan Zat Aktif",
            "Narkoba, Psikologi, dan Zat Alami",
            "Narkotika, Penyakit, dan Zat Asing"
        ]
    },
    {
        "q": "Apa yang dimaksud dengan ketergantungan?",
        "a": "Kondisi sulit berhenti menggunakan suatu zat",
        "options": [
            "Kondisi tubuh selalu sehat",
            "Kondisi sulit berhenti menggunakan suatu zat",
            "Kemampuan menghindari penyakit",
            "Kebiasaan berolahraga"
        ]
    },
    {
        "q": "Apa tindakan yang tepat ketika diajak mencoba NAPZA?",
        "a": "Menolak dengan tegas",
        "options": [
            "Mencoba sekali saja",
            "Mengikuti ajakan teman",
            "Menolak dengan tegas",
            "Menyimpannya"
        ]
    },
    {
        "q": "Siapa yang dapat dimintai bantuan ketika menghadapi masalah?",
        "a": "Orang dewasa yang terpercaya",
        "options": [
            "Orang dewasa yang terpercaya",
            "Orang yang tidak dikenal",
            "Teman yang mengajak melakukan hal berbahaya",
            "Tidak perlu meminta bantuan"
        ]
    },
    {
        "q": "Apa contoh kegiatan positif untuk menghindari penyalahgunaan NAPZA?",
        "a": "Mengikuti kegiatan olahraga",
        "options": [
            "Mencoba zat berbahaya",
            "Mengikuti kegiatan olahraga",
            "Mengikuti pergaulan negatif",
            "Menghindari keluarga"
        ]
    },
    {
        "q": "Apa peran keluarga dalam pencegahan NAPZA?",
        "a": "Memberikan dukungan dan pengawasan",
        "options": [
            "Membiarkan semua perilaku",
            "Memberikan dukungan dan pengawasan",
            "Mengajak mencoba NAPZA",
            "Mengabaikan masalah"
        ]
    },
    {
        "q": "Apa arti dari berani menolak?",
        "a": "Tidak mengikuti ajakan yang merugikan",
        "options": [
            "Selalu mengikuti teman",
            "Tidak mengikuti ajakan yang merugikan",
            "Menghindari semua orang",
            "Menyembunyikan masalah"
        ]
    },
    {
        "q": "Apa dampak penyalahgunaan NAPZA bagi kesehatan?",
        "a": "Dapat mengganggu kesehatan fisik dan mental",
        "options": [
            "Meningkatkan kesehatan",
            "Membuat tubuh selalu bugar",
            "Dapat mengganggu kesehatan fisik dan mental",
            "Meningkatkan daya tahan tubuh"
        ]
    },
    {
        "q": "Apa yang dimaksud dengan pergaulan positif?",
        "a": "Pertemanan yang memberikan pengaruh baik",
        "options": [
            "Pertemanan yang memberikan pengaruh baik",
            "Pertemanan yang mengajak melanggar aturan",
            "Pertemanan yang memaksa orang lain",
            "Pertemanan tanpa saling menghargai"
        ]
    },
    {
        "q": "Apa yang harus dilakukan jika teman mengalami masalah penyalahgunaan NAPZA?",
        "a": "Membantu mencari pertolongan",
        "options": [
            "Mengejeknya",
            "Membiarkannya",
            "Membantu mencari pertolongan",
            "Mengajaknya mencoba lagi"
        ]
    },
    {
        "q": "Apa tujuan edukasi tentang NAPZA?",
        "a": "Meningkatkan pengetahuan dan kesadaran",
        "options": [
            "Meningkatkan pengetahuan dan kesadaran",
            "Mengajak menggunakan NAPZA",
            "Menyebarkan informasi palsu",
            "Mengabaikan kesehatan"
        ]
    },
    {
        "q": "Apa yang dimaksud dengan literasi informasi?",
        "a": "Kemampuan memahami dan menilai informasi",
        "options": [
            "Kemampuan menyebarkan rumor",
            "Kemampuan memahami dan menilai informasi",
            "Kemampuan mengabaikan fakta",
            "Kemampuan meniru orang lain"
        ]
    },
    {
        "q": "Apa yang sebaiknya dilakukan ketika menerima informasi NAPZA yang belum jelas?",
        "a": "Memeriksa kebenarannya dari sumber tepercaya",
        "options": [
            "Langsung menyebarkannya",
            "Memeriksa kebenarannya dari sumber tepercaya",
            "Mengubah isi informasinya",
            "Mengabaikan semua informasi"
        ]
    },
    {
        "q": "Apa arti perlindungan diri?",
        "a": "Usaha menjaga diri dari pengaruh buruk",
        "options": [
            "Mengikuti semua ajakan",
            "Usaha menjaga diri dari pengaruh buruk",
            "Menghindari kegiatan positif",
            "Menyembunyikan kesalahan"
        ]
    },
    {
        "q": "Apa pilihan yang tepat untuk menjaga masa depan?",
        "a": "Menjalani hidup sehat dan menjauhi NAPZA",
        "options": [
            "Mencoba zat berbahaya",
            "Mengikuti tekanan teman",
            "Menjalani hidup sehat dan menjauhi NAPZA",
            "Mengabaikan pendidikan"
        ]
    }
]

# =========================
# CSS DAN TEMA
# =========================

THEMES = {
    "🌌 Galaxy": ["#17002e", "#32105c"],
    "🌊 Ocean": ["#001f3f", "#005f73"],
    "🌅 Sunset": ["#511845", "#900c3f"],
    "🌲 Forest": ["#052e16", "#14532d"],
    "🍬 Candy": ["#4a1942", "#9d4edd"],
    "🌑 Dark Arena": ["#111111", "#292929"]
}

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #17002e, #32105c);
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    color: #f5d0fe;
    text-shadow: 0 0 15px #d946ef;
}

.subtitle {
    text-align: center;
    color: #e9d5ff;
    font-size: 17px;
}

.player-card {
    background: rgba(255,255,255,0.10);
    padding: 20px;
    border-radius: 18px;
    border: 2px solid #d946ef;
    text-align: center;
    margin-bottom: 15px;
}

.question-card {
    background: rgba(255,255,255,0.12);
    padding: 25px;
    border-radius: 20px;
    border: 2px solid #a855f7;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    min-height: 48px;
    font-weight: bold;
    border: 1px solid #c084fc;
    background: #6b21a8;
    color: white;
}

div.stButton > button:hover {
    background: #a855f7;
    border: 1px solid white;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================

defaults = {
    "started": False,
    "round": 0,
    "scores": [0, 0],
    "answers": [None, None],
    "answer_times": [None, None],
    "bombs": [True, True],
    "question_order": [],
    "round_start": None,
    "finished": False,
    "revealed": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================
# JUDUL
# =========================

st.markdown(
    '<div class="main-title">⚔️ NAPZA BATTLE ⚔️</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">DUEL PENGETAHUAN • 2 PLAYERS • 1 ARENA</div>',
    unsafe_allow_html=True
)

st.write("")

# =========================
# HALAMAN PERSIAPAN
# =========================

if not st.session_state.started:

    st.subheader("🎮 PERSIAPAN PERMAINAN")

    col1, col2 = st.columns(2)

    with col1:
        name1 = st.text_input("Nama Player 1", value="PLAYER 1")
        avatar1 = st.selectbox(
            "Pilih Avatar Player 1",
            ["🦊", "🐼", "🐯", "🐸", "🐱", "🐲", "🦁", "🐰"]
        )

    with col2:
        name2 = st.text_input("Nama Player 2", value="PLAYER 2")
        avatar2 = st.selectbox(
            "Pilih Avatar Player 2",
            ["🐼", "🦊", "🐯", "🐸", "🐱", "🐲", "🦁", "🐰"]
        )

    theme = st.selectbox(
        "Pilih Arena",
        list(THEMES.keys())
    )

    st.info(
        "Kedua pemain menjawab pertanyaan yang sama. "
        "Masing-masing punya area tombol jawaban sendiri."
    )

    if st.button("🚀 MULAI BATTLE", use_container_width=True):

        st.session_state.name1 = name1.strip() or "PLAYER 1"
        st.session_state.name2 = name2.strip() or "PLAYER 2"

        st.session_state.avatar1 = avatar1
        st.session_state.avatar2 = avatar2
        st.session_state.theme = theme

        st.session_state.question_order = list(range(len(QUESTIONS)))
        random.shuffle(st.session_state.question_order)

        st.session_state.started = True
        st.session_state.round = 0
        st.session_state.scores = [0, 0]
        st.session_state.answers = [None, None]
        st.session_state.answer_times = [None, None]
        st.session_state.bombs = [True, True]
        st.session_state.finished = False
        st.session_state.revealed = False
        st.session_state.round_start = time.time()

        st.rerun()

# =========================
# PERMAINAN
# =========================

else:

    name1 = st.session_state.name1
    name2 = st.session_state.name2

    avatar1 = st.session_state.avatar1
    avatar2 = st.session_state.avatar2

    if st.session_state.finished:

        st.balloons()

        st.markdown(
            "<h1 style='text-align:center;'>🏆 BATTLE SELESAI!</h1>",
            unsafe_allow_html=True
        )

        st.subheader("🏅 HASIL AKHIR")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                f"{avatar1} {name1}",
                st.session_state.scores[0]
            )

        with c2:
            st.metric(
                f"{avatar2} {name2}",
                st.session_state.scores[1]
            )

        if st.session_state.scores[0] > st.session_state.scores[1]:
            winner = name1
            winner_avatar = avatar1
        elif st.session_state.scores[1] > st.session_state.scores[0]:
            winner = name2
            winner_avatar = avatar2
        else:
            winner = "SERI!"
            winner_avatar = "🤝"

        st.markdown(
            f"<h2 style='text-align:center;'>"
            f"{winner_avatar} PEMENANG: {winner} 🎉</h2>",
            unsafe_allow_html=True
        )

        if st.button("🔄 MAIN LAGI"):
            for key in defaults:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    else:

        current_round = st.session_state.round
        question_index = st.session_state.question_order[current_round]
        question = QUESTIONS[question_index]

        # Skor
        c1, c2 = st.columns(2)

        with c1:
            st.markdown(
                f"<div class='player-card'>"
                f"<h2>{avatar1} {name1}</h2>"
                f"<h1>{st.session_state.scores[0]} PTS</h1>"
                f"</div>",
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"<div class='player-card'>"
                f"<h2>{avatar2} {name2}</h2>"
                f"<h1>{st.session_state.scores[1]} PTS</h1>"
                f"</div>",
                unsafe_allow_html=True
            )

        st.progress(
            (current_round + 1) / len(QUESTIONS)
        )

        st.markdown(
            f"<div class='question-card'>"
            f"ROUND {current_round + 1} / 15<br><br>"
            f"{question['q']}"
            f"</div>",
            unsafe_allow_html=True
        )

        st.write("")

        # TIMER
        elapsed = time.time() - st.session_state.round_start
        remaining = max(0, 15 - int(elapsed))

        st.markdown(
            f"<h2 style='text-align:center;'>⏱️ {remaining} DETIK</h2>",
            unsafe_allow_html=True
        )

        # Pilihan jawaban
        if not st.session_state.revealed:

            option_list = question["options"].copy()
            random.shuffle(option_list)

            # Simpan pilihan agar tidak berubah saat aplikasi rerun
            if "current_options" not in st.session_state:
                st.session_state.current_options = option_list

            option_list = st.session_state.current_options

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    f"<div class='player-card'>"
                    f"<h3>{avatar1} {name1}</h3>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                if st.session_state.answers[0] is None:

                    for i, option in enumerate(option_list):
                        if st.button(
                            f"{chr(65+i)}. {option}",
                            key=f"p1_{current_round}_{i}"
                        ):
                            st.session_state.answers[0] = option
                            st.session_state.answer_times[0] = time.time()
                            st.rerun()

                else:
                    st.success("Jawaban sudah dikunci!")

            with col2:
                st.markdown(
                    f"<div class='player-card'>"
                    f"<h3>{avatar2} {name2}</h3>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                if st.session_state.answers[1] is None:

                    for i, option in enumerate(option_list):
                        if st.button(
                            f"{chr(65+i)}. {option}",
                            key=f"p2_{current_round}_{i}"
                        ):
                            st.session_state.answers[1] = option
                            st.session_state.answer_times[1] = time.time()
                            st.rerun()

                else:
                    st.success("Jawaban sudah dikunci!")

            # BOM
            st.divider()
            st.subheader("💣 BOMB ATTACK")

            b1, b2 = st.columns(2)

            with b1:
                if st.session_state.bombs[0]:
                    if st.button("💣 BOM PLAYER 1"):
                        if st.session_state.scores[0] >= 20:
                            st.session_state.scores[0] -= 20
                            st.session_state.scores[1] = max(
                                0, st.session_state.scores[1] - 10
                            )
                            st.session_state.bombs[0] = False
                            st.warning("Player 1 menggunakan bom!")
                            st.rerun()
                        else:
                            st.warning("Poin belum cukup! Butuh 20 poin.")

            with b2:
                if st.session_state.bombs[1]:
                    if st.button("💣 BOM PLAYER 2"):
                        if st.session_state.scores[1] >= 20:
                            st.session_state.scores[1] -= 20
                            st.session_state.scores[0] = max(
                                0, st.session_state.scores[0] - 10
                            )
                            st.session_state.bombs[1] = False
                            st.warning("Player 2 menggunakan bom!")
                            st.rerun()
                        else:
                            st.warning("Poin belum cukup! Butuh 20 poin.")

            # CEK WAKTU
            if remaining <= 0:
                st.session_state.revealed = True
                st.rerun()

            # KEDUA PEMAIN SUDAH MENJAWAB
            if (
                st.session_state.answers[0] is not None
                and st.session_state.answers[1] is not None
            ):
                st.session_state.revealed = True
                st.rerun()

        # =========================
        # HASIL JAWABAN
        # =========================

        else:

            correct_answer = question["a"]

            st.subheader("📢 HASIL JAWABAN")

            result1, result2 = st.columns(2)

            for player in range(2):

                answer = st.session_state.answers[player]

                if answer == correct_answer:

                    st.session_state.scores[player] += 10

                    answer_time = st.session_state.answer_times[player]

                    if answer_time is not None:
                        response_time = (
                            answer_time - st.session_state.round_start
                        )

                        if response_time <= 7:
                            st.session_state.scores[player] += 5

            with result1:
                if st.session_state.answers[0] == correct_answer:
                    st.success("PLAYER 1 BENAR! +10 POIN")
                else:
                    st.error("PLAYER 1 SALAH / WAKTU HABIS")

            with result2:
                if st.session_state.answers[1] == correct_answer:
                    st.success("PLAYER 2 BENAR! +10 POIN")
                else:
                    st.error("PLAYER 2 SALAH / WAKTU HABIS")

            st.info(f"Jawaban yang benar: **{correct_answer}**")

            # Penanda agar poin tidak ditambahkan berkali-kali
            if "scored_round" not in st.session_state:
                st.session_state.scored_round = -1

            if st.session_state.scored_round != current_round:

                for player in range(2):

                    answer = st.session_state.answers[player]

                    if answer == correct_answer:
                        st.session_state.scores[player] += 10

                        answer_time = st.session_state.answer_times[player]

                        if answer_time is not None:
                            if (
                                answer_time - st.session_state.round_start
                                <= 7
                            ):
                                st.session_state.scores[player] += 5

                st.session_state.scored_round = current_round

            if st.button("➡️ PERTANYAAN BERIKUTNYA"):

                st.session_state.round += 1
                st.session_state.answers = [None, None]
                st.session_state.answer_times = [None, None]
                st.session_state.revealed = False
                st.session_state.round_start = time.time()
                st.session_state.current_options = None
                del st.session_state.current_options

                if st.session_state.round >= len(QUESTIONS):
                    st.session_state.finished = True

                st.rerun()
