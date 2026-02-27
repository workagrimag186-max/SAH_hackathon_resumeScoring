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
st.set_page_config(layout="wide", page_title="AI Resume Screener", page_icon="🤖", initial_sidebar_state="expanded")

# --- ULTIMATE GLASSMORPHISM UI CSS ---
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* Apply Font Globally */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Main App Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364) !important;
        color: #ffffff !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 32, 39, 0.85) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Glassmorphism Metric Cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
    }

    /* Form Container Glassmorphism (Login/Register) */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    }

    /* Gradient Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%) !important;
        color: #0f2027 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0, 201, 255, 0.4) !important;
        color: #000000 !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 4px 4px 0px 0px;
        color: #A0AEC0 !important;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #00C9FF !important;
        border-bottom: 2px solid #00C9FF !important;
    }

    /* Headers Text Shadow */
    h1, h2, h3 {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* Adjust DataFrame Container */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- ENTERPRISE MONGODB SECURITY GATEWAY ---
@st.cache_resource
def get_mongo_client():
    client = pymongo.MongoClient("mongodb+srv://devkanti:devkantisarkar@hackathon.uubwq89.mongodb.net/?appName=hackathon")
    return client

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def render_auth_page():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.markdown("""
            <style>
                [data-testid="stSidebar"] {display: none;}
                [data-testid="collapsedControl"] {display: none;}
                .stApp > header {display: none;}
            </style>
        """, unsafe_allow_html=True)

        try:
            client = get_mongo_client()
            client.admin.command('ping') 
            db = client["hr_platform"]      
            users_col = db["recruiters"]    
        except Exception as e:
            st.error("⚠️ Could not connect to MongoDB Database.")
            return False

        col1, col2, col3 = st.columns([1, 1.2, 1])
        
        with col2:
            st.write("\n\n\n\n") 
            st.markdown("<h1 style='text-align: center; color: #00C9FF;'>🏢 Nexus HR Intelligence</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #E2E8F0; font-size: 1.2rem;'>Enterprise Talent Acquisition Platform</p>", unsafe_allow_html=True)
            st.write("")
            
            tab_login, tab_register = st.tabs(["🔒 Member Login", "📝 Register Company"])
            
            with tab_login:
                with st.form("login_form"):
                    login_email = st.text_input("Email Address")
                    login_pwd = st.text_input("Password", type="password")
                    submit_login = st.form_submit_button("Authenticate 🚀", use_container_width=True)

                    if submit_login:
                        if not login_email or not login_pwd:
                            st.warning("Please fill in all fields.")
                        else:
                            user = users_col.find_one({"email": login_email.lower(), "password": hash_password(login_pwd)})
                            if user:
                                st.session_state["authenticated"] = True
                                st.session_state["company_name"] = user.get("company_name", "Enterprise")
                                st.rerun() 
                            else:
                                st.error("🚫 Access Denied. Invalid email or password.")

            with tab_register:
                with st.form("register_form"):
                    reg_company = st.text_input("Company Name", placeholder="e.g., Stark Industries")
                    reg_email = st.text_input("Work Email")
                    reg_pwd = st.text_input("Create Password", type="password")
                    submit_register = st.form_submit_button("Create Account ✨", use_container_width=True)

                    if submit_register:
                        if not reg_company or not reg_email or not reg_pwd:
                            st.warning("Please fill out all fields to register.")
                        else:
                            if users_col.find_one({"email": reg_email.lower()}):
                                st.error("⚠️ An account with this email already exists.")
                            else:
                                users_col.insert_one({"company_name": reg_company, "email": reg_email.lower(), "password": hash_password(reg_pwd)})
                                st.success("✅ Account created successfully! Please switch to the Login tab.")
        return False
    return True

if not render_auth_page():
    st.stop()
# --- END MONGODB SECURITY GATEWAY ---

# --- MAIN DASHBOARD APP ---
company = st.session_state.get("company_name", "Enterprise")

st.markdown(f"<h1>🚀 {company} <span style='color: #00C9FF;'>AI Resume Screener</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #A0AEC0; font-size: 1.1rem;'>Automated. Explainable. Fair. | <b>National Hackathon Edition</b></p>", unsafe_allow_html=True)
st.write("")

# --- SIDEBAR ---
st.sidebar.markdown(f"<h2 style='text-align: center; color: #00C9FF;'>{company}</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center;'>HR Intelligence Portal</p>", unsafe_allow_html=True)
st.sidebar.divider()

with st.sidebar.expander("⚙️ Advanced AI Tuning"):
    st.caption("Adjust AI bias toward specific traits")
    w_exp = st.slider("Weight: Experience", 0.0, 1.0, 0.39)
    w_edu = st.slider("Weight: Education", 0.0, 1.0, 0.41)
    w_skill = st.slider("Weight: Skills Match", 0.0, 1.0, 0.71)
    w_ach = st.slider("Weight: Achievements", 0.0, 1.0, 0.80)

total_w = w_exp + w_edu + w_skill + w_ach
weights = {"experience": w_exp/max(total_w, 0.1), "education": w_edu/max(total_w, 0.1), "skills": w_skill/max(total_w, 0.1), "achievements": w_ach/max(total_w, 0.1)}

with st.sidebar.expander("📝 Job Description Setup"):
    jd_text = st.text_area("Paste the JD here:", "Looking for a Python developer with experience in Data Science, Pandas, and Streamlit.")

if 'uploader_key' not in st.session_state: st.session_state.uploader_key = 0

st.sidebar.divider()
st.sidebar.subheader("📄 Upload Talent Data")
uploaded_files = st.sidebar.file_uploader("Upload PDF Resumes", type=["pdf"], accept_multiple_files=True, key=f"uploader_{st.session_state.uploader_key}")

st.sidebar.divider()
blind_mode = st.sidebar.checkbox("🕶️ Enable Blind Hiring Mode")

if st.sidebar.button("🚨 Clear Database", type="secondary"):
    try:
        res = requests.delete("https://sah-hackathon-resumescoring.onrender.com/clear/")
        if res.status_code == 200:
            st.session_state.processed_files = set() 
            st.session_state.uploader_key += 1 
            st.rerun() 
        else:
            st.sidebar.error("Failed to clear database.")
    except Exception as e:
        st.sidebar.error("Backend offline.")

if 'processed_files' not in st.session_state: st.session_state.processed_files = set()

if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state.processed_files:
            with st.spinner(f"AI is analyzing {file.name}..."):
                files = {"file": (file.name, file.getvalue(), "application/pdf")}
                try:
                    response = requests.post("https://sah-hackathon-resumescoring.onrender.com/upload/", files=files, data={"jd_text": jd_text})
                    if response.status_code == 200:
                        st.session_state.processed_files.add(file.name)
                        st.toast(f"Indexed {file.name}!", icon="✅")
                    else: st.error(f"Error {response.status_code}")
                except Exception as e: st.error(f"API Error: {e}")

try:
    db_response = requests.get("https://sah-hackathon-resumescoring.onrender.com/candidates/")
    if db_response.status_code == 200 and len(db_response.json()) > 0: df = pd.DataFrame(db_response.json())
    else: df = pd.DataFrame() 
except: df = pd.DataFrame()

if not df.empty:
    ranked_df = calculate_final_score(df, weights)
    
    tab1, tab2, tab3 = st.tabs(["🏆 Live Rankings", "📈 Talent Analytics", "🤖 ML Prediction Lab"])

    with tab1:
        st.markdown("### Top Shortlisted Candidates")
        display_cols = ['name', 'email', 'FINAL_SCORE', 'education_level', 'degree', 'years_experience', 'semantic_match_score', 'certificate_skills']
        existing_cols = [col for col in display_cols if col in ranked_df.columns]
        display_df = ranked_df[existing_cols].copy()

        if blind_mode:
            display_df['name'] = [f"Candidate #{i+1}" for i in range(len(display_df))]
            if 'email' in display_df.columns: display_df['email'] = "CONFIDENTIAL"

        format_dict = {"FINAL_SCORE": "{:.2f}", "years_experience": "{:.1f}", "semantic_match_score": "{:.2f}"}
        active_formats = {k: v for k, v in format_dict.items() if k in display_df.columns}
        
        # Keep the green gradient, it looks great on dark mode!
        styled_table = display_df.style.background_gradient(subset=['FINAL_SCORE'], cmap="Greens").format(active_formats)
        st.dataframe(styled_table, width='stretch', height=250)

        st.divider()
        st.markdown("### 📊 Smart AI Deep-Dive")
        selected_name = st.selectbox("Select Candidate to Profile", options=ranked_df['name'].values)
        
        if selected_name:
            cand_data = ranked_df[ranked_df['name'] == selected_name].iloc[0]
            col_radar, col_ai = st.columns([1, 1])
            
            with col_radar:
                st.markdown("**Skill Symmetry Map**")
                radar_data = pd.DataFrame({
                    'Metric': ['Experience', 'Education', 'Skill Match', 'Achievements'],
                    'Score': [
                        cand_data.get('score_exp', cand_data.get('years_experience', 0) * 10), 
                        cand_data.get('score_edu', 70), 
                        cand_data.get('score_sem', cand_data.get('semantic_match_score', 0) * 100), 
                        cand_data.get('score_ach', cand_data.get('achievements_count', 0) * 10)
                    ]
                })
                # Added template='plotly_dark' to match the theme
                fig = px.line_polar(radar_data, r='Score', theta='Metric', line_close=True, range_r=[0,100], template='plotly_dark')
                fig.update_traces(fill='toself', line_color='#00C9FF')
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, width='stretch')

            with col_ai:
                st.markdown("**🤖 AI Recruiter's Commentary**")
                st.info(f"**Objective:** {cand_data.get('career_objective', 'N/A')}")
                st.write(f"**Contact:** {cand_data.get('email', 'N/A') if not blind_mode else 'CONFIDENTIAL'}")
                st.write(f"**Education:** {cand_data.get('education_level', 'Unknown')} | {cand_data.get('degree', 'Unknown')} (Class of {cand_data.get('passing_year', 'Unknown')})")
                
                if cand_data.get('semantic_match_score', 0) > 0.75:
                    st.success(f"**High Potential:** {cand_data['name']} shows elite semantic alignment with the JD.")
                else:
                    st.warning(f"**Generalist Match:** Relevant skills present; training may be needed.")

                st.markdown("**💡 Suggested Interview Questions**")
                st.write(f"- How do your {cand_data.get('years_experience', 0)} years help you handle technical debt?")
                st.write(f"- How has your background in {cand_data.get('degree', 'your field')} shaped your problem-solving?")

    with tab2:
        st.markdown(f"### 🏢 {company} Global Talent Overview")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Candidates In Pipeline", len(ranked_df))
        m2.metric("Average Experience", f"{ranked_df['years_experience'].mean():.1f} yrs")
        m3.metric("Highest Similarity Score", f"{ranked_df['semantic_match_score'].max():.2f}")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Education Breakdown**")
            edu_col = 'degree' if 'degree' in ranked_df.columns else 'education_level'
            if edu_col in ranked_df.columns:
                fig_edu = px.pie(ranked_df, names=edu_col, hole=0.5, color_discrete_sequence=['#00C9FF', '#92FE9D', '#f39c12', '#e74c3c'], template='plotly_dark')
                fig_edu.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_edu, width='stretch')
        with c2:
            st.markdown("**Experience Distribution**")
            fig_exp = px.histogram(ranked_df, x='years_experience', nbins=10, color_discrete_sequence=['#00C9FF'], template='plotly_dark')
            fig_exp.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_exp, width='stretch')

    with tab3:
        st.markdown("### 🧠 Predictive Machine Learning Lab")
        st.write("Train the predictive model on your current proprietary database to forecast candidate success.")
        if st.button("Initialize Neural Training 🚀"):
            try:
                from train_model import train_candidate_model
                result = train_candidate_model()
                st.success(result)
            except Exception as e:
                st.error(f"Training failed: {e}")
            
        st.divider()
        if os.path.exists("candidate_model.pkl"):
            st.markdown("### 🔮 Forecast Candidate Success Probability")
            target_name = st.selectbox("Select Candidate to Predict", options=ranked_df['name'].values, key="ml_tab_select")
            person_data = ranked_df[ranked_df['name'] == target_name].iloc[0]
            
            try:
                model = joblib.load("candidate_model.pkl")
                edu_map = {"B.Sc": 1, "B.Tech": 2, "M.Tech": 3, "PhD": 4}
                edu_val = edu_map.get(person_data.get('degree', 'B.Sc'), 1)
                feat_df = pd.DataFrame([[person_data.get('years_experience', 0), edu_val, person_data.get('semantic_match_score', 0), person_data.get('achievements_count', 0)]], columns=['years_experience', 'edu_numeric', 'semantic_match_score', 'achievements_count'])
                
                pred = model.predict(feat_df)[0]
                
                # Big UI Metric for the AI Prediction
                st.markdown(f"""
                <div style="background: rgba(0, 201, 255, 0.1); border-left: 5px solid #00C9FF; padding: 20px; border-radius: 5px;">
                    <h3 style="margin:0; color: #00C9FF;">Predicted Success Rate: {pred:.2f}%</h3>
                    <p style="margin:0; color: #E2E8F0;">Based on historical firm data and candidate metrics.</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.warning("Could not run prediction. Train the model first.")
else:
    st.info("👋 Welcome to Nexus. Please upload PDF resumes in the sidebar to begin processing.")
