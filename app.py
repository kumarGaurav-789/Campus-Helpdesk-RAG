import streamlit as st
import glob

from pyrebase import pyrebase

from groq import Groq

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# =====================================================
# FIREBASE CONFIG
# =====================================================

firebaseConfig = {

    "apiKey": "Your Api key",

    "authDomain": "amity-university-chatbot.firebaseapp.com",

    "projectId": "amity-university-chatbot",

    "storageBucket": "amity-university-chatbot.firebasestorage.app",

    "messagingSenderId": "336103704199",

    "appId": "1:336103704199:web:a729c34bba69b63a249a22",

    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

# =====================================================
# GROQ API
# =====================================================

client = Groq(
    api_key="YOUR_GROQ_API_KEY"
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Amity University Jharkhand Chatbot",
    page_icon="🎓",
    layout="wide"
)

# =====================================================
# SESSION STATE
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp {

    background-image:
    linear-gradient(
        rgba(5,10,30,0.92),
        rgba(5,10,30,0.92)
    ),

    url("https://i.ibb.co/tM7hgk9M/background-image-amity.jpg");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;

    color: white;
}

.login-box {

    max-width: 450px;

    margin: auto;

    margin-top: 80px;

    padding: 40px;

    background: rgba(255,255,255,0.08);

    border-radius: 20px;

    backdrop-filter: blur(20px);

    border: 1px solid rgba(255,255,255,0.1);
}

.main-title {

    text-align: center;

    font-size: 42px;

    font-weight: bold;

    color: white;
}

.subtitle {

    text-align: center;

    color: #d1d5db;

    margin-bottom: 30px;
}

.user-message {

    background: linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );

    padding: 15px;

    border-radius: 15px;

    margin-bottom: 10px;

    color: white;
}

.ai-message {

    background: rgba(255,255,255,0.08);

    padding: 15px;

    border-radius: 15px;

    margin-bottom: 10px;

    color: white;
}

.stButton button {

    width: 100%;

    border-radius: 12px;

    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    );

    color: white;

    border: none;

    padding: 12px;

    font-weight: bold;
}

.footer {

    text-align: center;

    margin-top: 40px;

    color: #d1d5db;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOGIN SCREEN
# =====================================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="login-box">',
        unsafe_allow_html=True
    )

    st.image(
        "https://i.ibb.co/MxS7vkmr/amity-logo-123.png",
        width=120
    )

    st.markdown("""
    <h1 class="main-title">
    Amity University Jharkhand
    </h1>

    <p class="subtitle">
    AI Powered University Assistant
    </p>
    """, unsafe_allow_html=True)

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    # =====================================================
    # LOGIN
    # =====================================================

    with col1:

        if st.button("Login"):

            if email == "" or password == "":

                st.warning("Please enter email and password")

            else:

                try:

                    auth.sign_in_with_email_and_password(
                        email,
                        password
                    )

                    st.session_state.logged_in = True

                    st.success("Login Successful!")

                    st.rerun()

                except:

                    st.error("Invalid email or password")

    # =====================================================
    # SIGN UP
    # =====================================================

    with col2:

        if st.button("Sign Up"):

            if email == "" or password == "":

                st.warning("Please enter email and password")

            else:

                try:

                    auth.create_user_with_email_and_password(
                        email,
                        password
                    )

                    st.success(
                        "Account created successfully!"
                    )

                except:

                    st.error("Signup failed")

    # =====================================================
    # GOOGLE LOGIN MESSAGE
    # =====================================================

    st.markdown("---")

    st.info("""
Google Sign-In popup is restricted in Streamlit local environment.

For mentor demo:
1. Use Email Login
2. Or deploy on Streamlit Cloud
3. Then Google popup will work correctly
""")

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.image(
        "https://i.ibb.co/MxS7vkmr/amity-logo-123.png",
        width=90
    )

    st.markdown("""
### University Sections

- 🎓 Admissions
- 💼 Placements
- 💰 Fees
- 🏆 Scholarships
- 🏠 Hostel
- 📚 Academics
- 📝 Exams
- 📖 Library
- 🚍 Transport
- ❓ FAQs
""")

    if st.button("Logout"):

        st.session_state.logged_in = False

        st.session_state.messages = []

        st.rerun()

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<h1 class="main-title">
🎓 Amity University Jharkhand Chatbot
</h1>

<p class="subtitle">
Admissions • Placements • Academics • Campus Support
</p>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DOCUMENTS
# =====================================================

PDF_FOLDER = "documents"

CHROMA_DB_DIR = "chroma_db"

@st.cache_resource
def load_vectorstore():

    pdf_files = glob.glob(f"{PDF_FOLDER}/*.pdf")

    documents = []

    for pdf in pdf_files:

        loader = PyPDFLoader(pdf)

        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=CHROMA_DB_DIR
    )

    return vectorstore

with st.spinner("Loading University Knowledge Base..."):

    vectorstore = load_vectorstore()

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)

# =====================================================
# AI FUNCTION
# =====================================================

def generate_answer(query, docs):

    context = "\n\n".join(
        [doc.page_content[:500] for doc in docs]
    )

    prompt = f"""
You are an AI assistant for
Amity University Jharkhand.

Answer professionally and naturally.

Question:
{query}

University Context:
{context}
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are an AI assistant for "
                    "Amity University Jharkhand."
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.4,

            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"

# =====================================================
# QUICK ACCESS
# =====================================================

st.markdown("## 🚀 Quick Access")

col1, col2, col3 = st.columns(3)

with col1:

    if st.button("🎓 MBA Admission"):

        query = "What is the admission process for MBA?"

        docs = retriever.invoke(query)

        answer = generate_answer(query, docs)

        st.session_state.messages.append(
            {"role": "user", "content": query}
        )

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        st.rerun()

with col2:

    if st.button("💼 Placements"):

        query = "Tell me about placements"

        docs = retriever.invoke(query)

        answer = generate_answer(query, docs)

        st.session_state.messages.append(
            {"role": "user", "content": query}
        )

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        st.rerun()

with col3:

    if st.button("🏠 Hostel"):

        query = "Tell me about hostel facilities"

        docs = retriever.invoke(query)

        answer = generate_answer(query, docs)

        st.session_state.messages.append(
            {"role": "user", "content": query}
        )

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        st.rerun()

# =====================================================
# CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f'<div class="user-message">{message["content"]}</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f'<div class="ai-message">{message["content"]}</div>',
            unsafe_allow_html=True
        )

# =====================================================
# CHAT INPUT
# =====================================================

query = st.chat_input(
    "Ask anything about Amity University Jharkhand..."
)

if query:

    st.session_state.messages.append(
        {"role": "user", "content": query}
    )

    docs = retriever.invoke(query)

    answer = generate_answer(query, docs)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    st.rerun()

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">
© 2025 Amity University Jharkhand AI Assistant • Powered by Groq AI
</div>
""", unsafe_allow_html=True)