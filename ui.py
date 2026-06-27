import streamlit as st

def futuristic_ui():

    st.markdown("""
    <style>

    /* ==========================
       BACKGROUND
    ========================== */

    .stApp{

        background:
        linear-gradient(
            rgba(2,6,23,0.92),
            rgba(2,6,23,0.95)
        ),

        url("https://i.ibb.co/tM7hgk9M/background-image-amity.jpg");

        background-size:cover;
        background-position:center;
        background-attachment:fixed;
    }

    /* ==========================
       HEADER
    ========================== */

    .header{

        text-align:center;

        margin-top:20px;

        margin-bottom:30px;
    }

    .header img{

        width:90px;

        filter:
        drop-shadow(
        0px 0px 15px #60a5fa);
    }

    .title{

        font-size:42px;

        font-weight:700;

        margin-top:10px;

        background:
        linear-gradient(
            90deg,
            #60a5fa,
            #8b5cf6
        );

        -webkit-background-clip:text;

        -webkit-text-fill-color:transparent;
    }

    .subtitle{

        color:#d1d5db;

        font-size:18px;
    }

    /* ==========================
       GLASS CARD
    ========================== */

    .glass-card{

        background:
        rgba(255,255,255,0.08);

        backdrop-filter:blur(20px);

        border:
        1px solid rgba(255,255,255,0.15);

        border-radius:25px;

        padding:25px;

        box-shadow:
        0px 0px 25px rgba(96,165,250,.25),
        0px 0px 40px rgba(139,92,246,.20);
    }

    /* ==========================
       BUTTONS
    ========================== */

    .stButton>button{

        width:100%;

        border:none;

        border-radius:15px;

        padding:14px;

        font-size:16px;

        font-weight:bold;

        color:white;

        background:
        linear-gradient(
            135deg,
            #2563eb,
            #8b5cf6
        );

        transition:0.3s;
    }

    .stButton>button:hover{

        transform:translateY(-3px);

        box-shadow:
        0px 0px 20px #60a5fa,
        0px 0px 35px #8b5cf6;
    }

    /* ==========================
       INPUT BOX
    ========================== */

    .stTextInput input{

        background:
        rgba(255,255,255,0.08);

        color:white;

        border-radius:15px;

        border:
        1px solid rgba(255,255,255,.15);
    }

    /* ==========================
       CHAT INPUT
    ========================== */

    .stChatInput{

        border-radius:20px;
    }

    /* ==========================
       SIDEBAR
    ========================== */

    section[data-testid="stSidebar"]{

        background:
        rgba(15,23,42,0.75);

        backdrop-filter:blur(20px);
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="header">

        <img src="https://i.ibb.co/MxS7vkmr/amity-logo-123.png">

        <div class="title">
            Amity University Jharkhand
        </div>

        <div class="subtitle">
            AI Powered Campus Helpdesk Assistant
        </div>

    </div>
    """, unsafe_allow_html=True)