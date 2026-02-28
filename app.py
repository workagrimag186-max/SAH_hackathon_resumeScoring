import requests
import streamlit as st
import plotly.express as px
import pandas as pd
import joblib
import os
from scorer import calculate_final_score
import pymongo
import hashlib

# Make the webpage wide and set professional theme
st.set_page_config(layout="wide", page_title="Nexus HR Intelligence", page_icon="🌌", initial_sidebar_state="expanded")

# --- MASTER TOGGLE SWITCH ---
LOCAL_TESTING = False # Change to False when you push to Render for the judges!
BASE_URL = "http://127.0.0.1:8000" if LOCAL_TESTING else "https://sah-hackathon-resumescoring.onrender.com"

# --- DEEP NEBULA GLASSMORPHISM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif !important; }
    .stApp { background: linear-gradient(135deg, #050505, #120d1f, #1e1332) !important; color: #ffffff !important; }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes pulseGlow { 0% { box-shadow: 0 0 15px rgba(189, 147, 249, 0.2); } 50% { box-shadow: 0 0 25px rgba(189, 147, 249, 0.4); } 100% { box-shadow: 0 0 15px rgba(189, 147, 249, 0.2); } }
    .block-container { animation: fadeInUp 0.8s ease-out forwards; }
    [data-testid="stSidebar"] { background: rgba(5, 5, 5, 0.85) !important; backdrop-filter: blur(20px) !important; border-right: 1px solid rgba(189, 147, 249, 0.2) !important; }
    div[data-testid="metric-container"] { background: rgba(255, 255, 255, 0.03) !important; backdrop-filter: blur(15px) !important; border: 1px solid rgba(189, 147, 249, 0.2) !important; border-radius: 15px !important; padding: 20px !important; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important; transition: transform 0.3s ease, box-shadow 0.3s ease; }
    div[data-testid="metric-container"]:hover { transform: translateY(-5px); box-shadow: 0 10px 40px 0 rgba(189, 147, 249, 0.3) !important; }
    [data-testid="stForm"] { background: rgba(255, 255, 255, 0.03) !important; backdrop-filter: blur(20px) !important; border: 1px solid rgba(189, 147, 249, 0.3) !important; border-radius: 20px !important; padding: 35px !important; animation: pulseGlow 4s infinite; }
    div.stButton > button { background: linear-gradient(90deg, #8E2DE2 0%, #4A00E0 100%) !important; color: #ffffff !important; border: none !important; border-radius: 8px !important; font-weight: 700 !important; letter-spacing: 0.5px; transition: all 0.3s ease !important; }
    div.stButton > button:hover { transform: scale(1.02) !important; box-shadow: 0 5px 20px rgba(142, 45, 226, 0.6) !important; color: #ffffff !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { background-color: transparent !important; border-radius: 4px 4px 0px 0px; color: #8b9eb3 !important; font-size: 1.1rem; font-weight: 600; transition: color 0.3s ease; }
    .stTabs [aria-selected="true"] { color: #bd93f9 !important; border-bottom: 3px solid #bd93f9 !important; }
    .hero-title { background: -webkit-linear-gradient(45deg, #bd93f9, #8be9fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 2px 2px 20px rgba(189, 147, 249, 0.3); font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# --- ENTERPRISE MONGODB SECURITY GATEWAY ---
@st.cache_resource
def get_mongo_client():
    client = pymongo.MongoClient("mongodb+srv://devkanti:devkantisarkar@hackathon.uubwq89.mongodb.net/?appName=hackathon")
    return client

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def render_footer():
    st.markdown("""
        <div style='text-align: center; color: #6b7280; padding-top: 50px; padding-bottom: 20px; font-size: 0.85rem;'>
            &copy; 2026 Future Innovators. All rights reserved.
        </div>
    """, unsafe_allow_html=True)

def render_auth_page():
    if "authenticated" not in st.session_state: st.session_state["authenticated"] = False
    if not st.session_state["authenticated"]:
        st.markdown("""<style>[data-testid="stSidebar"], [data-testid="collapsedControl"], .stApp > header {display: none;}</style>""", unsafe_allow_html=True)
        try:
            client = get_mongo_client()
            client.admin.command('ping') 
            db = client["hr_platform"]      
            users_col = db["recruiters"]    
        except Exception as e:
            st.error("⚠️ Could not connect to Database Network.")
            return False

        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            st.write("\n\n\n\n") 
            st.markdown("<h1 class='hero-title' style='text-align: center; font-size: 3.5rem;'>NEXUS</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #b9c1cb; font-size: 1.2rem; margin-bottom: 30px;'>The Future of AI-Powered Talent Acquisition.</p>", unsafe_allow_html=True)
            tab_login, tab_register = st.tabs(["🔒 Secure Login", "📝 Onboard Company"])
            
            with tab_login:
                with st.form("login_form"):
                    st.markdown("<h3 style='text-align: center; margin-bottom: 20px; color: white;'>Welcome Back</h3>", unsafe_allow_html=True)
                    login_email = st.text_input("Corporate Email")
                    login_pwd = st.text_input("Password", type="password")
                    st.write("")
                    submit_login = st.form_submit_button("Authenticate 🚀", use_container_width=True)
                    if submit_login:
                        if not login_email or not login_pwd: st.warning("Please fill in all fields.")
                        else:
                            user = users_col.find_one({"email": login_email.lower(), "password": hash_password(login_pwd)})
                            if user:
                                st.session_state["authenticated"] = True
                                st.session_state["company_name"] = user.get("company_name", "Enterprise")
                                st.rerun() 
                            else: st.error("🚫 Access Denied. Invalid credentials.")

            with tab_register:
                with st.form("register_form"):
                    st.markdown("<h3 style='text-align: center; margin-bottom: 20px; color: white;'>Join the Network</h3>", unsafe_allow_html=True)
                    reg_company = st.text_input("Organization Name", placeholder="e.g., Stark Industries")
                    reg_email = st.text_input("Corporate Email")
                    reg_pwd = st.text_input("Create Password", type="password")
                    st.write("")
                    submit_register = st.form_submit_button("Initialize Account ✨", use_container_width=True)
                    if submit_register:
                        if not reg_company or not reg_email or not reg_pwd: st.warning("Please fill out all fields.")
                        else:
                            if users_col.find_one({"email": reg_email.lower()}): st.error("⚠️ An account with this email already exists.")
                            else:
                                users_col.insert_one({"company_name": reg_company, "email": reg_email.lower(), "password": hash_password(reg_pwd)})
                                st.success("✅ Account created! Please switch to Secure Login.")
        render_footer()
        return False
    return True

if not render_auth_page(): st.stop()

# --- MAIN DASHBOARD APP ---
company = st.session_state.get("company_name", "Enterprise")

# Header Section
st.markdown(f"<h1 style='font-size: 2.5rem;'>🚀 {company} <span class='hero-title'>Intelligence Hub</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #b9c1cb; font-size: 1.1rem; margin-bottom: 20px;'>Automated. Explainable. Fair. | Endpoint: {BASE_URL}</p>", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown(f"<h2 class='hero-title' style='text-align: center; font-size: 2rem;'>{company}</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #8b9eb3;'>Command Center</p>", unsafe_allow_html=True)
st.sidebar.divider()

with st.sidebar.expander("⚙️ Advanced AI Matrix Tuning"):
    w_exp = st.slider("Weight: Experience", 0.0, 1.0, 0.39)
    w_edu = st.slider("Weight: Education", 0.0, 1.0, 0.41)
    w_skill = st.slider("Weight: Skills Match", 0.0, 1.0, 0.71)
    w_ach = st.slider("Weight: Achievements", 0.0, 1.0, 0.80)

total_w = w_exp + w_edu + w_skill + w_ach
weights = {"experience": w_exp/max(total_w, 0.1), "education": w_edu/max(total_w, 0.1), "skills": w_skill/max(total_w, 0.1), "achievements": w_ach/max(total_w, 0.1)}

with st.sidebar.expander("📝 Target Job Profile (JD)"):
    jd_text = st.text_area("Paste JD:", "Looking for a Python developer with experience in Data Science, Pandas, and Streamlit.", height=150)

if 'uploader_key' not in st.session_state: st.session_state.uploader_key = 0

st.sidebar.divider()
st.sidebar.subheader("📄 Data Ingestion")
uploaded_files = st.sidebar.file_uploader("Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True, key=f"uploader_{st.session_state.uploader_key}")

st.sidebar.divider()
blind_mode = st.sidebar.checkbox("🕶️ Enable Bias-Free Hiring Mode")

if st.sidebar.button("🚨 Purge System Data", type="secondary"):
    try:
        res = requests.delete(f"{BASE_URL}/clear/")
        if res.status_code == 200:
            st.session_state.processed_files = set() 
            st.session_state.uploader_key += 1 
            st.rerun() 
        else: st.sidebar.error("Failed to clear database.")
    except Exception as e: st.sidebar.error("Backend offline. Is Uvicorn running?")

if 'processed_files' not in st.session_state: st.session_state.processed_files = set()

if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state.processed_files:
            with st.spinner(f"Neural Engine analyzing {file.name}..."):
                files = {"file": (file.name, file.getvalue(), "application/pdf")}
                try:
                    response = requests.post(f"{BASE_URL}/upload/", files=files, data={"jd_text": jd_text})
                    if response.status_code == 200:
                        st.session_state.processed_files.add(file.name)
                        st.toast(f"Successfully processed {file.name}!", icon="✅")
                    else: st.error(f"Error {response.status_code}: Server crashed while reading PDF.")
                except Exception as e: st.error(f"API Connection Error. Is your Backend running? {e}")

try:
    db_response = requests.get(f"{BASE_URL}/candidates/")
    if db_response.status_code == 200 and len(db_response.json()) > 0: df = pd.DataFrame(db_response.json())
    else: df = pd.DataFrame() 
except: df = pd.DataFrame()

if not df.empty:
    ranked_df = calculate_final_score(df, weights)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Candidates", len(ranked_df))
    m2.metric("Avg. Experience", f"{ranked_df['years_experience'].mean():.1f} yrs")
    m3.metric("Highest AI Match", f"{ranked_df['semantic_match_score'].max():.2f}")
    m4.metric("Avg. AI Match", f"{ranked_df['semantic_match_score'].mean():.2f}")
    st.write("")

    st.markdown("### 🏆 Live Talent Leaderboard")
    display_cols = ['name', 'email', 'online_links', 'FINAL_SCORE', 'semantic_match_score', 'years_experience', 'education_level', 'degree', 'passing_year', 'certificate_skills', 'career_objective']
    existing_cols = [col for col in display_cols if col in ranked_df.columns]
    display_df = ranked_df[existing_cols].copy()

    if blind_mode:
        display_df['name'] = [f"Candidate #{i+1}" for i in range(len(display_df))]
        if 'email' in display_df.columns: display_df['email'] = "CONFIDENTIAL"

    format_dict = {"FINAL_SCORE": "{:.2f}", "years_experience": "{:.1f}", "semantic_match_score": "{:.2f}"}
    active_formats = {k: v for k, v in format_dict.items() if k in display_df.columns}
    
    styled_table = (display_df.style
                    .background_gradient(subset=['FINAL_SCORE'], cmap="Purples")
                    .background_gradient(subset=['semantic_match_score'], cmap="Blues")
                    .bar(subset=['years_experience'], color='#bd93f9', vmin=0)
                    .format(active_formats))
    st.dataframe(styled_table, use_container_width=True, height=350)
    st.divider()

    tab1, tab2, tab3 = st.tabs(["🧠 AI Profile Deep-Dive", "📈 Global Pipeline Analytics", "🔮 ML Prediction Lab"])

    with tab1:
        col_select, col_space = st.columns([1, 2])
        with col_select: selected_name = st.selectbox("Select Candidate for Forensic Profiling", options=ranked_df['name'].values)
        
        if selected_name:
            cand_data = ranked_df[ranked_df['name'] == selected_name].iloc[0]
            col_radar, col_ai = st.columns([1, 1])
            with col_radar:
                st.markdown("**Skill Symmetry Map**")
                radar_data = pd.DataFrame({
                    'Metric': ['Experience', 'Education', 'Skill Match', 'Achievements'],
                    'Score': [cand_data.get('score_exp', cand_data.get('years_experience', 0) * 10), cand_data.get('score_edu', 70), cand_data.get('score_sem', cand_data.get('semantic_match_score', 0) * 100), cand_data.get('score_ach', cand_data.get('achievements_count', 0) * 10)]
                })
                fig = px.line_polar(radar_data, r='Score', theta='Metric', line_close=True, range_r=[0,100], template='plotly_dark')
                fig.update_traces(fill='toself', line_color='#bd93f9')
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

            with col_ai:
                st.markdown("**🤖 AI Recruiter's Commentary**")
                st.info(f"**Objective:** {cand_data.get('career_objective', 'N/A')}")
                st.write(f"**Contact:** {cand_data.get('email', 'N/A') if not blind_mode else 'CONFIDENTIAL'}")
                st.write(f"**Links:** {cand_data.get('online_links', 'None detected')}")
                st.write(f"**Education:** {cand_data.get('education_level', 'Unknown')} | {cand_data.get('degree', 'Unknown')} (Class of {cand_data.get('passing_year', 'Unknown')})")
                
                if cand_data.get('semantic_match_score', 0) > 0.75: st.success(f"**High Potential:** {cand_data['name']} shows elite semantic alignment.")
                elif cand_data.get('semantic_match_score', 0) > 0.50: st.warning(f"**Generalist Match:** Core skills present, but training may be required.")
                else: st.error(f"**Low Alignment:** Candidate profile deviates significantly from the target JD.")

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Education Breakdown**")
            edu_col = 'degree' if 'degree' in ranked_df.columns else 'education_level'
            if edu_col in ranked_df.columns:
                fig_edu = px.pie(ranked_df, names=edu_col, hole=0.5, color_discrete_sequence=['#bd93f9', '#8be9fd', '#ff79c6', '#f1fa8c'], template='plotly_dark')
                fig_edu.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_edu, use_container_width=True)
        with c2:
            st.markdown("**Experience Distribution**")
            fig_exp = px.histogram(ranked_df, x='years_experience', nbins=10, color_discrete_sequence=['#bd93f9'], template='plotly_dark')
            fig_exp.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_exp, use_container_width=True)

    with tab3:
        st.write("Train the predictive model on your current proprietary database to forecast candidate success.")
        if st.button("Initialize Neural Training 🚀"):
            try:
                from train_model import train_candidate_model
                result = train_candidate_model()
                st.success(result)
            except Exception as e: st.error(f"Training failed: {e}")
            
        st.divider()
        if os.path.exists("candidate_model.pkl"):
            st.markdown("### 🔮 Forecast Candidate Success Probability")
            target_name_ml = st.selectbox("Select Candidate to Evaluate", options=ranked_df['name'].values, key="ml_tab_select")
            person_data_ml = ranked_df[ranked_df['name'] == target_name_ml].iloc[0]
            try:
                model = joblib.load("candidate_model.pkl")
                edu_map = {"B.Sc": 1, "B.Tech": 2, "M.Tech": 3, "PhD": 4}
                edu_val = edu_map.get(person_data_ml.get('degree', 'B.Sc'), 1)
                feat_df = pd.DataFrame([[person_data_ml.get('years_experience', 0), edu_val, person_data_ml.get('semantic_match_score', 0), person_data_ml.get('achievements_count', 0)]], columns=['years_experience', 'edu_numeric', 'semantic_match_score', 'achievements_count'])
                pred = model.predict(feat_df)[0]
                st.markdown(f"""<div style="background: rgba(189, 147, 249, 0.1); border-left: 5px solid #bd93f9; padding: 20px; border-radius: 5px; animation: fadeInUp 0.5s ease-out;"><h3 style="margin:0; color: #bd93f9;">Predicted Success Rate: {pred:.2f}%</h3><p style="margin:0; color: #E2E8F0;">Based on historical firm data and real-time candidate metrics.</p></div>""", unsafe_allow_html=True)
            except Exception as e: st.warning("Could not run prediction. Data mismatch.")
else: st.info("👋 Welcome to Nexus. Please upload PDF resumes in the sidebar to begin processing.")

render_footer()
