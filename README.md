 ATS Resume Scoring System

This project is a simple web-based Applicant Tracking System (ATS) that:
- Takes a Job Description and multiple PDF resumes as input.
- Extracts key sections: Projects, Strengths, and Education.
- Computes an ATS score for each section and overall.
- Displays missing keywords from the resume compared to the job description.



Project Structure

ats-system/
│
├── app.py                       # Main Flask backend
├── templates/
│   └── index.html              # Frontend UI
├── uploads/
│   └── resumes/                # Folder to save uploaded resumes
│   └── job_description.txt     # Stores the current job description



 Features

Upload multiple **PDF resumes**
Input a **Job Description**
Extract and evaluate **Projects, Strengths, Education** from each resume
Section-wise **similarity scores**
Shows **missing keywords** from JD
Easy-to-use **web interface**


### 🚀 Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ats-system.git
cd ats-system
```

#### 2. Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt


Or manually:

```bash
pip install flask pymupdf nltk scikit-learn
```

> The first run will download NLTK stopwords automatically.

---

 🧪 Run the Application

```bash
python app.py
```

Visit `http://127.0.0.1:5000/` in your browser.
# 📤 Usage

1. Paste the **Job Description** in the text box.
2. Upload one or more **PDF resumes**.
3. Click **Submit**.
4. View:
   - Section-wise ATS scores (Projects, Strengths, Education)
   - Overall score
   - Keywords missing from each resume

---

### Example Output

```text
Resume: John_Doe.pdf
Projects Score: 72.5%
Strengths Score: 65.0%
Education Score: 80.3%
Overall ATS Score: 72.6%
Missing Keywords: python, deep, deployment, collaboration, ...
```



- Make sure your resume sections are clearly labeled (e.g., “Projects”, “Strengths”).
- Only supports **PDF** files for resume uploads.
- If section headers are not found, those sections may get scored low.

---

flask
pymupdf
scikit-learn
nltk


