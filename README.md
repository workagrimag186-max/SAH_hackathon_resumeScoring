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

> <img width="1919" height="924" alt="image" src="https://github.com/user-attachments/assets/192e1dcb-42b4-4a76-a6b9-3d4a9ccdacbb" />
<img width="1919" height="928" alt="image" src="https://github.com/user-attachments/assets/5cf1deea-3134-4ad4-9c9b-0a90e3075c33" />


*Description: The clean, professional login/registration page using `st.tabs`.*

### 2. The Talent Dashboard & Ranking
The core innovation. This dashboard ranks all applicants by their final AI composite score. You can also toggle **"🕶️ Blind Hiring Mode"** here to anonymize candidates and eliminate bias during the first review.

> <img width="1919" height="928" alt="image" src="https://github.com/user-attachments/assets/1b413365-e4bd-4944-bf94-2a072dde22e2" />
<img width="1919" height="931" alt="image" src="https://github.com/user-attachments/assets/560ddbc6-a673-4646-8341-bac107a3e9c1" />



*Description: The main `st.dataframe` showing the '🏆 Rankings' tab, complete with the green conditional formatting on the final score.*

### 3. Smart AI Deep-Dive (Explainable AI)
Select a candidate, and Nexus generates a detailed profile, including suggestions for interview questions and a dynamic **radar chart** to visualize their strengths and weaknesses.

> <img width="1919" height="924" alt="image" src="https://github.com/user-attachments/assets/5c4ac10c-cc7e-4d9b-8d9b-a11200bbeb3f" />

*Description: The radar chart (`px.line_polar`) and the '🤖 AI Recruiter’s Commentary' section for a single candidate.*

### 4. Advanced Talent Analytics
Nexus provides a bird's-eye view of your entire talent pipeline, with interactive distribution charts for experience and education.

> <img width="1919" height="924" alt="image" src="https://github.com/user-attachments/assets/955ca225-4bde-46d5-9082-bb47d6b114a6" />

*Description: The '📈 Analytics' tab showing the `st.metric` cards (Total Applicants, Avg Experience) and the pie/histogram charts.*

### 5. The ML Lab (Model Training)
For a dynamic demo, the ML Lab tab shows how our linear regression model is trained on the current database, triggering a "celebration" animation when complete.

> <img width="1885" height="929" alt="image" src="https://github.com/user-attachments/assets/e638ced4-837c-447b-a83a-40450ef43cb1" />

*Description: The '🤖 ML Lab' tab showing the '🚀 Start Model Training' button.*

---

## 🛠️ Tech Stack & Architecture

This is a **Full-Stack Microservices Application** built for high-performance AI inference.

* **Frontend:** Streamlit (UI, Visualizations, Auth UI, Glassmorphism CSS)
* **Database:** MongoDB Atlas (Cloud NoSQL DB for users and candidates)
* **NLP & Scoring:** Sentence Transformers (`all-MiniLM-L6-v2`) via Hugging Face
* **Data Science:** Scikit-learn (Linear Regression), Pandas, Numpy, Plotly
* **Backend:** FastAPI & Uvicorn (REST API)

🚀 How to Run Locally
If you wish to run the development environment on your machine:

Deployed Website Link:
https://analyserresume.streamlit.app/


1. Clone the repository:

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

2. Install dependencies:

We recommend using a virtual environment (venv).

pip install -r requirements.txt

3. Set up the environment variables:
   
Create a .env file in the root directory and add:
MONGO_URI=your_mongodb_atlas_connection_string

5. Start the Backend:

uvicorn api:app --reload

5. Start the Frontend (New Terminal):

streamlit run app.py


👥 The Team (SAH_Hackathon)
Devkanti Sarkar- Resume Parsing and Extraction Engineer

Mohar Gorai - Scoring Algorithm and Data Processing Engineer

Agrima Gupta - System Integration and UI developer

### Cloud Architecture:
```mermaid
graph TD
    A[Client Browser] -->|HTTPS| B(Streamlit Community Cloud: Frontend)
    B -->|API Requests| C(Render.com: FastAPI Backend)
    C -->|AI Inference| D(Hugging Face NLP)
    C -->|Read/Write Data| E(MongoDB Atlas: Cloud Database)
    B -->|Check Auth| E
