Gemini said
Here is your complete, fully updated app.py file. I have gone through and replaced every single local address with your live Render cloud URL.

Copy this entire block of code, replace everything in your current app.py file, save it, and do your final git push.

Python
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
st.set_page_config(layout="wide", page_title="AI Resume Screener", page_icon="🤖")

# --- ENTERPRISE UI CSS HACK ---
st.markdown("""
<style>
    /* Style the metric cards to look like glassmorphism */
    div[data-testid="metric-container"] {
        background-color: #1A1C23; 
        border: 1px solid #2d303e;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    /* Style the main title */
    h1 {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    /* Clean up the sidebar padding */
    .css-1d391kg {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- ENTERPRISE MONGODB SECURITY GATEWAY ---
@st.cache_resource
def get_mongo_client():
    client = pymongo.MongoClient("mongodb+srv://devkanti:devkantisarkar@hackathon.uubwq89.mongodb.net/?appName=hackathon")
    return client

def hash_password(password):
    """Cryptographically hashes the password for secure database storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def render_auth_page():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        # Magic CSS to hide the Streamlit sidebar on the login page
        st.markdown("""
            <style>
                [data-testid="stSidebar"] {display: none;}
                [data-testid="collapsedControl"] {display: none;}
                .stApp > header {display: none;}
            </style>
        """, unsafe_allow_html=True)

        # Initialize Database connection
        try:
            client = get_mongo_client()
            # CRITICAL FIX: Force a ping to ensure MongoDB is actually running
            client.admin.command('ping') 
            
            db = client["hr_platform"]      
            users_col = db["recruiters"]    
        except Exception as e:
            st.error("⚠️ Could not connect to MongoDB. Is MongoDB Compass running locally?")
            return False

        # Center the UI
        col1, col2, col3 = st.columns([1, 1.2, 1])
        
        with col2:
            st.write("\n\n\n") 
            st.markdown("<h1 style='text-align: center;'>🏢 Nexus HR Intelligence</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>Enterprise Talent Acquisition Platform</p>", unsafe_allow_html=True)
            st.write("")
            
            tab_login, tab_register = st.tabs(["🔒 Member Login", "📝 Register Company"])
            
            # --- TAB 1: LOGIN ---
            with tab_login:
                with st.form("login_form"):
                    login_email = st.text_input("Email Address")
                    login_pwd = st.text_input("Password", type="password")
                    submit_login = st.form_submit_button("Authenticate 🚀", use_container_width=True)

                    if submit_login:
                        if not login_email or not login_pwd:
                            st.warning("Please fill in all fields.")
                        else:
                            user = users_col.find_one({
                                "email": login_email.lower(), 
                                "password": hash_password(login_pwd)
                            })
                            
                            if user:
                                st.session_state["authenticated"] = True
                                st.session_state["company_name"] = user.get("company_name", "Enterprise")
                                st.rerun() 
                            else:
                                st.error("🚫 Access Denied. Invalid email or password.")

            # --- TAB 2: REGISTER NEW USER ---
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
                                new_user = {
                                    "company_name": reg_company,
                                    "email": reg_email.lower(),
                                    "password": hash_password(reg_pwd)
                                }
                                users_col.insert_one(new_user)
                                st.success("✅ Account created successfully! Please switch to the Login tab.")
        
        return False
    return True

# Stop the app from loading the dashboard if not authenticated
if not render_auth_page():
    st.stop()
# --- END MONGODB SECURITY GATEWAY ---

# --- MAIN DASHBOARD APP ---

# Fetch the company name dynamically!
company = st.session_state.get("company_name", "Enterprise")

st.title(f"🚀 {company} AI Resume Screener")
st.markdown("Automated. Explainable. Fair. | **National Hackathon Edition**")

# --- UPGRADED CLEAN SIDEBAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135692.png", width=60) # Fake corporate logo
st.sidebar.markdown(f"**{company} HR Portal**")
st.sidebar.divider()

with st.sidebar.expander("⚙️ Advanced Scoring Weights"):
    st.caption("Adjust AI bias toward specific traits")
    w_exp = st.slider("Weight: Experience", 0.0, 1.0, 0.39)
    w_edu = st.slider("Weight: Education", 0.0, 1.0, 0.41)
    w_skill = st.slider("Weight: Skills Match", 0.0, 1.0, 0.71)
    w_ach = st.slider("Weight: Achievements", 0.0, 1.0, 0.80)

total_w = w_exp + w_edu + w_skill + w_ach
weights = {
    "experience": w_exp/max(total_w, 0.1), 
    "education": w_edu/max(total_w, 0.1), 
    "skills": w_skill/max(total_w, 0.1), 
    "achievements": w_ach/max(total_w, 0.1)
}

with st.sidebar.expander("📝 Job Description Setup"):
    jd_text = st.text_area("Paste the JD here:", "Looking for a Python developer with experience in Data Science, Pandas, and Streamlit.")

if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

st.sidebar.divider()
st.sidebar.header("📄 Upload Real Resumes")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs", 
    type=["pdf"], 
    accept_multiple_files=True, 
    key=f"uploader_{st.session_state.uploader_key}"
)

st.sidebar.divider()
blind_mode = st.sidebar.checkbox("🕶️ Enable Blind Hiring Mode")

if st.sidebar.button("🚨 Clear All Candidates", type="primary"):
    try:
        res = requests.delete("https://sah-hackathon-resumescoring.onrender.com/clear/")
        if res.status_code == 200:
            st.session_state.processed_files = set() 
            st.session_state.uploader_key += 1 
            st.rerun() 
        else:
            st.sidebar.error("Failed to clear database.")
    except Exception as e:
        st.sidebar.error("Backend offline. Please check Render!")

if 'processed_files' not in st.session_state:
    st.session_state.processed_files = set()

if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state.processed_files:
            with st.spinner(f"AI is reading {file.name}..."):
                files = {"file": (file.name, file.getvalue(), "application/pdf")}
                data = {"jd_text": jd_text}
                try:
                    response = requests.post("https://sah-hackathon-resumescoring.onrender.com/upload/", files=files, data=data)
                    if response.status_code == 200:
                        st.session_state.processed_files.add(file.name)
                        st.toast(f"Successfully Indexed {file.name}!", icon="✅")
                    else:
                        st.error(f"Backend Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"API Connection Error. Is Backend running? Details: {e}")

try:
    db_response = requests.get("https://sah-hackathon-resumescoring.onrender.com/candidates/")
    if db_response.status_code == 200 and len(db_response.json()) > 0:
        df = pd.DataFrame(db_response.json())
    else:
        df = pd.DataFrame() 
except Exception as e:
    df = pd.DataFrame()

if not df.empty:
    ranked_df = calculate_final_score(df, weights)
    
    tab1, tab2, tab3 = st.tabs(["🏆 Rankings", "📈 Analytics", "🤖 ML Lab"])

    with tab1:
        st.subheader("Top Shortlisted Talent")
        display_cols = [
            'name', 'email', 'FINAL_SCORE', 'education_level', 'degree', 'passing_year', 
            'years_experience', 'semantic_match_score', 'certificate_skills', 
            'online_links', 'career_objective'
        ]
        existing_cols = [col for col in display_cols if col in ranked_df.columns]
        display_df = ranked_df[existing_cols].copy()

        if blind_mode:
            display_df['name'] = [f"Candidate #{i+1}" for i in range(len(display_df))]
            if 'email' in display_df.columns:
                display_df['email'] = "CONFIDENTIAL"

        format_dict = {"FINAL_SCORE": "{:.2f}", "years_experience": "{:.1f}", "semantic_match_score": "{:.2f}"}
        active_formats = {k: v for k, v in format_dict.items() if k in display_df.columns}
        styled_table = display_df.style.background_gradient(subset=['FINAL_SCORE'], cmap="Greens").format(active_formats)
        st.dataframe(styled_table, width='stretch')

        st.divider()
        st.subheader("📊 Smart AI Deep-Dive")
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
                fig = px.line_polar(radar_data, r='Score', theta='Metric', line_close=True, range_r=[0,100])
                fig.update_traces(fill='toself', line_color='#1f77b4')
                st.plotly_chart(fig, width='stretch')

            with col_ai:
                st.markdown("**🤖 AI Recruiter's Commentary**")
                st.info(f"**Objective:** {cand_data.get('career_objective', 'N/A')}")
                st.write(f"**Contact Email:** {cand_data.get('email', 'N/A') if not blind_mode else 'CONFIDENTIAL'}")
                st.write(f"**Links:** {cand_data.get('online_links', 'None Detected')}")
                st.write(f"**Education:** {cand_data.get('education_level', 'Unknown')} | {cand_data.get('degree', 'Unknown')} (Class of {cand_data.get('passing_year', 'Unknown')})")
                
                if cand_data.get('semantic_match_score', 0) > 0.75:
                    st.success(f"**High Potential:** {cand_data['name']} shows elite semantic alignment.")
                else:
                    st.warning(f"**Generalist Match:** Relevant skills present; training may be needed.")

                st.markdown("**💡 Suggested Interview Questions**")
                st.write(f"1. How do your {cand_data.get('years_experience', 0)} years help you handle technical debt?")
                st.write(f"2. How has your background in {cand_data.get('degree', 'your field')} shaped your problem-solving?")

    with tab2:
        st.subheader(f"🏢 {company} Talent Overview")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Applicants", len(ranked_df))
        m2.metric("Avg Experience", f"{ranked_df['years_experience'].mean():.1f} yrs")
        m3.metric("Highest AI Match Score", f"{ranked_df['semantic_match_score'].max():.2f}")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Education Diversity**")
            edu_col = 'degree' if 'degree' in ranked_df.columns else 'education_level'
            if edu_col in ranked_df.columns:
                fig_edu = px.pie(ranked_df, names=edu_col, hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
                st.plotly_chart(fig_edu, width='stretch')
        with c2:
            st.markdown("**Experience Distribution**")
            fig_exp = px.histogram(ranked_df, x='years_experience', nbins=10, color_discrete_sequence=['#2ecc71'])
            st.plotly_chart(fig_exp, width='stretch')

    with tab3:
        st.subheader("🤖 Machine Learning Lab")
        st.write("Train the model on the current database.")
        if st.button("🚀 Start Model Training"):
            try:
                from train_model import train_candidate_model
                result = train_candidate_model()
                st.success(result)
                st.balloons() # Added the celebration animation!
            except Exception as e:
                st.error(f"Training failed: {e}")
            
        st.divider()
        if os.path.exists("candidate_model.pkl"):
            st.write("### Predict Success Probability")
            target_name = st.selectbox("Select Candidate to Predict", options=ranked_df['name'].values, key="ml_tab_select")
            person_data = ranked_df[ranked_df['name'] == target_name].iloc[0]
            
            try:
                model = joblib.load("candidate_model.pkl")
                edu_map = {"B.Sc": 1, "B.Tech": 2, "M.Tech": 3, "PhD": 4}
                edu_val = edu_map.get(person_data.get('degree', 'B.Sc'), 1)
                
                feat_df = pd.DataFrame([[
                    person_data.get('years_experience', 0), 
                    edu_val, 
                    person_data.get('semantic_match_score', 0), 
                    person_data.get('achievements_count', 0)
                ]], columns=['years_experience', 'edu_numeric', 'semantic_match_score', 'achievements_count'])
                
                pred = model.predict(feat_df)[0]
                st.metric(f"ML Success Score for {target_name}", f"{pred:.2f}%")
            except Exception as e:
                st.warning("Could not run prediction. Train the model first.")
else:
    st.info("👋 Welcome! Please upload PDF resumes in the sidebar to begin processing. (Ensure backend is running!)")
The Final Push to GitHub:
Once you have saved this app.py, just run these three commands in your terminal:

Bash
git add app.py
git commit -m "Final Update: Connected to live Render backend"
git push origin main
