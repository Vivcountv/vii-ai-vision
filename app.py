import streamlit as st
import requests
from datetime import datetime


# ============================================================
# 1. IDENTITAS UTAMA (VII AI)
# ============================================================

NAMA_AI = "Vii"
MODEL_NAME = "Vision-1"
OLLAMA_URL = "https://paralegal-slather-penny.ngrok-free.dev/"

DESKRIPSI_SISTEM = (
    f"Anda adalah {NAMA_AI}, asisten AI yang sangat cerdas, ramah, "
    "profesional, dan selalu gunakan bahasa Indonesia. "
    "Gunakan format Markdown seperti list atau bold untuk "
    "memperjelas jawaban Anda."
)


# ============================================================
# 2. KONFIGURASI HALAMAN
# ============================================================

st.set_page_config(
    page_title=f"{NAMA_AI} Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 3. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0F111A;
        color: #E2E8F0;
    }

    .block-container {
        max-width: 98% !important;
        padding-top: 0rem !important;
        padding-bottom: 5rem !important;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background-color: #0B0D14 !important;
        border-right: 1px solid #1A1D29 !important;
    }

    .sb-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 30px;
        padding: 0 10px;
    }

    .sb-brand-icon {
        font-size: 28px;
    }

    .sb-brand-text {
        font-weight: 700;
        font-size: 1.2rem;
        color: white;
    }

    .sb-brand-sub {
        font-size: 0.75rem;
        color: #828B9C;
    }

    .menu-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 4px;
        color: #828B9C;
        font-weight: 500;
        cursor: pointer;
        font-size: 0.95rem;
    }

    .menu-item.active {
        background-color: #3B58F5;
        color: white;
    }

    .menu-item:hover:not(.active) {
        background-color: #1A1D29;
    }


    /* ========================================================
       PROMO CARD
       ======================================================== */

    .promo-card {
        background: linear-gradient(
            145deg,
            #1A1D29,
            #0F111A
        );

        border: 1px solid #232838;
        border-radius: 16px;
        padding: 16px;
        margin-top: 40px;
        margin-bottom: 20px;
        text-align: left;
    }

    .promo-icon {
        font-size: 30px;
        margin-bottom: 10px;
    }

    .promo-title {
        font-weight: 600;
        font-size: 0.95rem;
        color: white;
        margin-bottom: 4px;
    }

    .promo-desc {
        font-size: 0.8rem;
        color: #828B9C;
        margin-bottom: 12px;
        line-height: 1.4;
    }

    .promo-btn {
        background-color: #3B58F5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 0.8rem;
        font-weight: 500;
        width: 100%;
        cursor: pointer;
    }


    /* ========================================================
       USER PROFILE
       ======================================================== */

    .user-profile {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px;
        border-top: 1px solid #1A1D29;
        margin-top: 30px;
    }

    .up-avatar {
        width: 36px;
        height: 36px;
        background: #232838;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .up-name {
        font-size: 0.9rem;
        font-weight: 500;
        color: white;
    }

    .up-status {
        font-size: 0.75rem;
        color: #34D399;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        background: #34D399;
        border-radius: 50%;
    }


    /* ========================================================
       LOGIN
       ======================================================== */

    .login-box {
        max-width: 500px;
        margin: 100px auto;
        padding: 30px;
        background-color: #1A1D29;
        border: 1px solid #232838;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }


    /* ========================================================
       HEADER CHAT
       ======================================================== */

    .main-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        background-color: #0F111A;

        padding: 15px 5px;

        border-bottom: 1px solid #1A1D29;

        margin-bottom: 20px;

        position: sticky;
        top: 0;
        z-index: 999;
    }

    .mh-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .mh-avatar {
        width: 40px;
        height: 40px;
        background: #1A1D29;
        border-radius: 50%;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 20px;
    }

    .mh-title {
        font-weight: 600;
        font-size: 1.1rem;
        color: #FFFFFF;
        line-height: 1.2;
    }

    .mh-subtitle {
        font-size: 0.8rem;
        color: #828B9C;
    }

    .mh-right {
        color: #828B9C;
        font-size: 1.2rem;
        display: flex;
        gap: 15px;
    }


    /* ========================================================
       CHAT MESSAGE
       ======================================================== */

    [data-testid="stChatMessage"] {
        display: flex;
        gap: 12px;
        margin-bottom: 24px;

        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    [data-testid="stChatMessageContent"] {
        padding: 14px 18px;
        max-width: 80%;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    [data-testid="stChatMessageContent"] code {
        background: #0B0D14 !important;
        color: #3B58F5 !important;
    }


    /* ========================================================
       TIMESTAMP
       ======================================================== */

    .time-stamp {
        font-size: 0.7rem;
        color: #64748B;
        margin-top: 6px;

        display: flex;
        align-items: center;
        gap: 4px;
    }

    .time-stamp.user {
        justify-content: flex-end;
        color: #94A3B8;
    }


    /* ========================================================
       CHAT INPUT
       ======================================================== */

    [data-testid="stChatInput"] {
        background-color: #0B0D14;
        border: 1px solid #1A1D29;
        border-radius: 24px;
        padding: 2px 10px;
    }

    [data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
    }

    [data-testid="stChatInput"] button {
        background-color: #3B58F5 !important;
        color: white !important;
        border-radius: 50% !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. LOGIN / GATE USER
# ============================================================

if "username" not in st.session_state:

    st.markdown(
        '<div class="login-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        f"<h2>🔮 Selamat Datang di {NAMA_AI} Chat</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            color: #828B9C;
            font-size: 0.9rem;
            margin-bottom: 20px;
        ">
            Silakan masukkan nama Anda untuk memulai sesi
            asisten AI kustom.
        </p>
        """,
        unsafe_allow_html=True
    )

    input_nama = st.text_input(
        "Nama Panggilan Anda:",
        placeholder="Contoh: Vivaldi Manurung"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "Masuk Ke Ruang Chat 🚀",
        use_container_width=True
    ):

        if input_nama.strip():

            st.session_state.username = input_nama.strip()

            # Inisialisasi pesan
            st.session_state.messages = []

            st.rerun()

        else:

            st.error("Nama tidak boleh kosong!")

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# 5. HALAMAN UTAMA
# ============================================================

else:

    USER_NAME = st.session_state.username


    # ========================================================
    # 5A. SIDEBAR
    # ========================================================

    with st.sidebar:

        st.markdown(
            f"""
            <div class="sb-brand">

                <div class="sb-brand-icon">
                    🤖
                </div>

                <div>

                    <div class="sb-brand-text">
                        {NAMA_AI} Chat
                    </div>

                    <div class="sb-brand-sub">
                        Selalu ada untukmu
                    </div>

                </div>

            </div>

            <div class="menu-item active">
                💬 &nbsp; Chat
            </div>

            <div class="menu-item">
                🕒 &nbsp; Riwayat
            </div>

            <div class="menu-item">
                ⭐ &nbsp; Favorit
            </div>

            <div class="menu-item">
                ⚙️ &nbsp; Pengaturan
            </div>

            <div class="promo-card">

                <div class="promo-icon">
                    🤖
                </div>

                <div class="promo-title">
                    Ada pertanyaan lainnya?
                </div>

                <div class="promo-desc">
                    Saya siap membantu kapan saja!
                </div>

                <div class="promo-btn">
                    Mulai Chat &gt;
                </div>

            </div>

            <div class="user-profile">

                <div class="up-avatar">
                    👤
                </div>

                <div>

                    <div class="up-name">
                        {USER_NAME}
                    </div>

                    <div class="up-status">
                        <span class="status-dot"></span>
                        Online
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # Tombol hapus percakapan

        if st.button(
            "Kosongkan Percakapan",
            use_container_width=True,
            type="secondary"
        ):

            st.session_state.messages = []

            st.rerun()


        # Tombol logout

        if st.button(
            "Keluar",
            use_container_width=True
        ):

            del st.session_state.username

            if "messages" in st.session_state:
                del st.session_state.messages

            st.rerun()


    # ========================================================
    # 5B. HEADER UTAMA
    # ========================================================

    st.markdown(
        f"""
        <div class="main-header">

            <div class="mh-left">

                <div class="mh-avatar">
                    🤖
                </div>

                <div>

                    <div class="mh-title">
                        {NAMA_AI} Chat
                    </div>

                    <div class="mh-subtitle">
                        Asisten AI Anda
                        (Engine: {MODEL_NAME})
                    </div>

                </div>

            </div>

            <div class="mh-right">
                <span>☀️</span>
                <span>⋮</span>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # 5C. INISIALISASI PESAN
    # ========================================================

    if (
        "messages" not in st.session_state
        or len(st.session_state.messages) == 0
    ):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    f"Halo, {USER_NAME}! 👋\n\n"
                    f"Saya {NAMA_AI}, asisten AI yang siap "
                    "membantu kamu. Ada yang bisa saya bantu "
                    "hari ini?"
                ),
                "time": datetime.now().strftime("%H:%M")
            }
        ]


    # ========================================================
    # 5D. RENDER RIWAYAT CHAT
    # ========================================================

    for message in st.session_state.messages:

        if message["role"] == "system":
            continue

        avatar_icon = (
            "🤖"
            if message["role"] == "assistant"
            else "👤"
        )

        with st.chat_message(
            message["role"],
            avatar=avatar_icon
        ):

            st.markdown(message["content"])

            if message.get("time"):

                time_class = (
                    "time-stamp user"
                    if message["role"] == "user"
                    else "time-stamp"
                )

                check_mark = (
                    " ✓✓"
                    if message["role"] == "user"
                    else ""
                )

                st.markdown(
                    f"""
                    <div class="{time_class}">
                        {message["time"]}{check_mark}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # ========================================================
    # 5E. INPUT CHAT
    # ========================================================

    prompt = st.chat_input(
        "Ketik pesan Anda di sini..."
    )


    if prompt:

        waktu_user = datetime.now().strftime("%H:%M")


        # ----------------------------------------------------
        # Tampilkan pesan user
        # ----------------------------------------------------

        with st.chat_message(
            "user",
            avatar="👤"
        ):

            st.markdown(prompt)

            st.markdown(
                f"""
                <div class="time-stamp user">
                    {waktu_user} ✓✓
                </div>
                """,
                unsafe_allow_html=True
            )


        # Simpan pesan user

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
                "time": waktu_user
            }
        )


        # ----------------------------------------------------
        # Tampilkan area response AI
        # ----------------------------------------------------

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            placeholder = st.empty()

            full_response = ""


            with st.spinner("Mengetik..."):

                # --------------------------------------------
                # Susun history untuk Ollama
                # --------------------------------------------

                payload_messages = [
                    {
                        "role": "system",
                        "content": DESKRIPSI_SISTEM
                    }
                ]

                for message in st.session_state.messages:

                    if message["role"] in [
                        "user",
                        "assistant"
                    ]:

                        payload_messages.append(
                            {
                                "role": message["role"],
                                "content": message["content"]
                            }
                        )


                # --------------------------------------------
                # Payload Ollama
                # --------------------------------------------

                payload = {
                    "model": MODEL_NAME,
                    "messages": payload_messages,
                    "stream": False
                }


                # --------------------------------------------
                # Request ke Ollama
                # --------------------------------------------

                try:

                    response = requests.post(
                        OLLAMA_URL,
                        json=payload,
                        timeout=120
                    )


                    if response.status_code == 200:

                        result = response.json()

                        full_response = (
                            result
                            .get("message", {})
                            .get(
                                "content",
                                "Maaf, AI tidak memberikan jawaban."
                            )
                        )

                    else:

                        try:
                            error_detail = response.json()
                        except Exception:
                            error_detail = response.text

                        full_response = (
                            f"⚠️ Server {NAMA_AI} mengembalikan "
                            f"status **{response.status_code}**.\n\n"
                            f"Detail: `{error_detail}`"
                        )


                except requests.exceptions.ConnectionError:

                    full_response = (
                        f"❌ **Gagal terhubung ke Ollama.**\n\n"
                        f"Pastikan Ollama sedang berjalan di:\n"
                        f"`{OLLAMA_URL}`"
                    )


                except requests.exceptions.Timeout:

                    full_response = (
                        "⏱️ **Waktu permintaan habis.**\n\n"
                        "Model membutuhkan waktu terlalu lama "
                        "untuk memberikan respons."
                    )


                except Exception as e:

                    full_response = (
                        f"❌ **Terjadi kesalahan:**\n\n"
                        f"`{str(e)}`"
                    )


            # --------------------------------------------
            # Tampilkan response
            # --------------------------------------------

            placeholder.markdown(full_response)

            waktu_assistant = datetime.now().strftime("%H:%M")

            st.markdown(
                f"""
                <div class="time-stamp">
                    {waktu_assistant}
                </div>
                """,
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # Simpan response AI
        # ----------------------------------------------------

        if full_response:

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response,
                    "time": waktu_assistant
                }
            )
