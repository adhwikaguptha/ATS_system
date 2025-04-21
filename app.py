import os
import re
from flask import Flask, request, render_template
import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/resumes'
JOB_DESC_FILE = 'uploads/job_description.txt'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = re.sub(r'\W+', ' ', text)
    text = text.lower()
    return ' '.join([word for word in text.split() if word not in stop_words])

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_sections(text):
    sections = {'projects': '', 'strengths': '', 'education': ''}
    lines = text.split('\n')
    current_section = None
    for line in lines:
        line_lower = line.lower()
        if 'project' in line_lower:
            current_section = 'projects'
        elif 'strength' in line_lower:
            current_section = 'strengths'
        elif 'education' in line_lower:
            current_section = 'education'
        elif current_section:
            sections[current_section] += ' ' + line
    return sections

def get_similarity(jd, section_text):
    docs = [jd, section_text]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform(docs)
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()[0]
    return round(similarity * 100, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        jd_text = clean_text(request.form['jd_text'])
        resumes = request.files.getlist('resumes')

        for resume in resumes:
            filename = resume.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            resume.save(filepath)
            raw_text = extract_text_from_pdf(filepath)
            sections = extract_sections(raw_text)
            cleaned_sections = {k: clean_text(v) for k, v in sections.items()}

            scores = {
                'projects': get_similarity(jd_text, cleaned_sections['projects']),
                'strengths': get_similarity(jd_text, cleaned_sections['strengths']),
                'education': get_similarity(jd_text, cleaned_sections['education'])
            }

            overall = round(sum(scores.values()) / len(scores), 2)

            # Get missing keywords
            jd_words = set(jd_text.split())
            resume_words = set(clean_text(raw_text).split())
            missing_keywords = jd_words - resume_words

            results.append({
                'filename': filename,
                'scores': scores,
                'overall': overall,
                'missing_keywords': ', '.join(list(missing_keywords)[:15])  # show only top 15
            })

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
