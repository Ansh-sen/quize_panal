import streamlit as st
import qrcode
import pandas as pd
from PIL import Image
from io import BytesIO
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="QuizQuest Portal", page_icon="🚀", layout="centered")

# --- CUSTOM CSS FOR "FUN EDUCATION" THEME ---
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Card styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 15px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: white;
        border-radius: 10px;
        color: #5b0082;
        font-weight: bold;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(to right, #ff416c, #ff4b2b);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
    }

    /* Text Inputs */
    input {
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DB LOGIC ---
DB_FILE = "students.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Email", "Paid"]).to_csv(DB_FILE, index=False)

# --- APP HEADER ---
st.title("🚀 QuizQuest Student Portal")
st.markdown("##### *Master your knowledge, unlock your potential!*")

tab1, tab2 = st.tabs(["✨ Student Access", "🔐 Teacher Admin"])

# --- TAB 1: STUDENT VIEW ---
with tab1:
    st.markdown("### 📝 Ready to start the Quiz?")
    st.info("Scan the code below using your phone or tablet to join the arena!")
    
    # In a real scenario, the admin sets this code
    current_game_code = st.text_input("Enter the Access Key provided by your teacher", placeholder="e.g., 882910")
    
    if st.button("Unlock My Quiz! 🔓"):
        if current_game_code:
            # Generate fun QR
            quiz_url = f"https://quizizz.com{current_game_code}"
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(quiz_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#4b0082", back_color="white")
            
            buf = BytesIO()
            img.save(buf, format="PNG")
            
            st.success("✅ Access Granted! Go get 'em, Genius!")
            st.image(buf, width=300)
        else:
            st.error("Please enter your Access Key first!")

# --- TAB 2: ADMIN VIEW ---
with tab2:
    st.markdown("### 🛠 Teacher Control Center")
    password = st.text_input("Admin PIN", type="password")
    
    if password == "stars": # Fun simple password
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Log New Payment")
            with st.form("pay_form"):
                new_email = st.text_input("Student Email")
                if st.form_submit_button("Verify Payment"):
                    df = pd.read_csv(DB_FILE)
                    new_row = pd.DataFrame([[new_email, "Yes"]], columns=["Email", "Paid"])
                    pd.concat([df, new_row]).to_csv(DB_FILE, index=False)
                    st.toast(f"Student {new_email} is now Active!", icon='⭐')

        with col2:
            st.markdown("#### 📊 Quiz Stats")
            df = pd.read_csv(DB_FILE)
            st.metric("Paid Heroes", len(df))
            if st.checkbox("Show Enrollment List"):
                st.dataframe(df)
    else:
        st.warning("Please enter the Teacher PIN to manage students.")

# --- FOOTER ---
st.markdown("---")
st.caption("Powered by QuizQuest Engine • 2024 Education Suite")
