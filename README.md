# 🏢 Nexus HR Intelligence: AI-Powered Resume Screener

> "**Automating the first glance.** Fair, Efficient, and Explainable Talent Acquisition."

---

## 🌟 The Vision

In a world where one job posting attracts thousands of resumes, the traditional hiring funnel is broken. Recruiters spend an average of **6 seconds** per resume, leading to burnout and missed opportunities. **Nexus HR Intelligence** is an enterprise-grade AI solution that reads, scores, and ranks candidates instantly—transforming weeks of work into seconds. 

### What Makes Nexus Special?
1.  **Semantic Search (No Keywords):** We don't just count keywords. Our NLP model uses **Sentence Transformers** (Hugging Face) to understand the *meaning* of a candidate's experience, matching it to the Job Description with advanced semantic similarity.
2.  **Explainable AI:** Nexus doesn't just give a score; it generates a **radar symmetry map** for every candidate, showing exactly *why* the AI ranked them that way (e.g., strong experience, weak achievements).
3.  **Secure Multi-Tenant Auth:** Built on **MongoDB Atlas**, Nexus allows different companies (like Stark Industries or Wayne Enterprises) to securely register and manage their own isolated talent pools.

---

## 📸 Platform Tour

We believe in seeing is believing. Here is a tour of the current live platform:

### 1. Secure Corporate Login
Our platform uses a full-stack security gateway to ensure multi-tenancy. Companies can register or log in securely to access their private dashboard.

> `[REPLACE_WITH_A_SCREENSHOT_OF_YOUR_LOGIN_TAB]`
*Description: The clean, professional login/registration page using `st.tabs`.*

### 2. The Talent Dashboard & Ranking
The core innovation. This dashboard ranks all applicants by their final AI composite score. You can also toggle **"🕶️ Blind Hiring Mode"** here to anonymize candidates and eliminate bias during the first review.

> `[REPLACE_WITH_A_SCREENSHOT_OF_THE_MAIN_DASHBOARD_RANKING]`
*Description: The main `st.dataframe` showing the '🏆 Rankings' tab, complete with the green conditional formatting on the final score.*

### 3. Smart AI Deep-Dive (Explainable AI)
Select a candidate, and Nexus generates a detailed profile, including suggestions for interview questions and a dynamic **radar chart** to visualize their strengths and weaknesses.

> `[REPLACE_WITH_A_SCREENSHOT_OF_THE_CANDIDATE_PROFILE_WITH_RADAR_CHART]`
*Description: The radar chart (`px.line_polar`) and the '🤖 AI Recruiter’s Commentary' section for a single candidate.*

### 4. Advanced Talent Analytics
Nexus provides a bird's-eye view of your entire talent pipeline, with interactive distribution charts for experience and education.

> `[REPLACE_WITH_A_SCREENSHOT_OF_THE_ANALYTICS_TAB]`
*Description: The '📈 Analytics' tab showing the `st.metric` cards (Total Applicants, Avg Experience) and the pie/histogram charts.*

### 5. The ML Lab (Model Training)
For a dynamic demo, the ML Lab tab shows how our linear regression model is trained on the current database, triggering a "celebration" animation when complete.

> `[REPLACE_WITH_A_SCREENSHOT_OF_THE_ML_LAB_TAB]`
*Description: The '🤖 ML Lab' tab showing the '🚀 Start Model Training' button.*

---

## 🛠️ Tech Stack & Architecture

This is a **Full-Stack Microservices Application** built for high-performance AI inference.

* **Frontend:** Streamlit (UI, Visualizations, Auth UI, Glassmorphism CSS)
* **Database:** MongoDB Atlas (Cloud NoSQL DB for users and candidates)
* **NLP & Scoring:** Sentence Transformers (`all-MiniLM-L6-v2`) via Hugging Face
* **Data Science:** Scikit-learn (Linear Regression), Pandas, Numpy, Plotly
* **Backend:** FastAPI & Uvicorn (REST API)

### Cloud Architecture:
```mermaid
graph TD
    A[Client Browser] -->|HTTPS| B(Streamlit Community Cloud: Frontend)
    B -->|API Requests| C(Render.com: FastAPI Backend)
    C -->|AI Inference| D(Hugging Face NLP)
    C -->|Read/Write Data| E(MongoDB Atlas: Cloud Database)
    B -->|Check Auth| E
