# backend.py (updated)
import os
import uuid
import io
import tempfile
import sqlite3
import openai
from datetime import datetime
from fpdf import FPDF
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import streamlit as st
# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize database
def init_db():
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS resumes
                 (id TEXT PRIMARY KEY,
                  name TEXT,
                  email TEXT,
                  phone TEXT,
                  score INTEGER,
                  created_at TIMESTAMP)''')
    conn.commit()
    conn.close()
# Add these functions/classes ABOVE process_resume_data()

class ResumeGenerator:
    def __init__(self, form_data):
        self.data = form_data
        self.pdf = FPDF()
        self.filename = f"resume_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        self._setup_fonts()

    def _setup_fonts(self):
        try:
            self.pdf.add_font('Arial', '', 'arial.ttf', uni=True)
            self.pdf.add_font('Arial', 'B', 'arialbd.ttf', uni=True)
        except:
            self.pdf.set_font("Helvetica", size=12)

    def _create_header(self):
        self.pdf.set_font("Arial", 'B', 16)
        self.pdf.cell(200, 10, txt=self.data['personal_info']['name'], ln=1, align='C')
        self.pdf.set_font("Arial", '', 12)
        self.pdf.cell(200, 10, txt=f"{self.data['personal_info']['email']} | {self.data['personal_info']['phone']}", ln=1, align='C')

    def _create_section(self, title, content):
        self.pdf.set_font("Arial", 'B', 14)
        self.pdf.cell(200, 10, txt=title, ln=1)
        self.pdf.set_font("Arial", '', 12)
        self.pdf.multi_cell(0, 10, txt=content)
        self.pdf.ln(5)

    def generate_pdf(self):
        try:
            self.pdf.add_page()
            self._create_header()
            
            sections = [
                ("Education", f"{self.data['education']['degree']}\n{self.data['education']['years']}"),
                ("Work Experience", f"{self.data['experience']['job_title']} at {self.data['experience']['company']}\n{self.data['experience']['description']}"),
                ("Skills", ", ".join(self.data['skills']) if isinstance(self.data['skills'], list) else self.data['skills']),
                ("Projects", self.data['projects'])
            ]
            
            for title, content in sections:
                if content.strip():
                    self._create_section(title, content)
            
            filepath = os.path.join(tempfile.gettempdir(), self.filename)
            self.pdf.output(filepath)
            return filepath
        except Exception as e:
            raise RuntimeError(f"PDF generation failed: {str(e)}")
def analyze_resume_quality(resume_data):
    # Calculate quality score
    score = 0
    feedback = []
    
    # Check for essential components
    essential_fields = ['name', 'email', 'phone']
    for field in essential_fields:
        if resume_data['personal_info'].get(field):
            score += 1
        else:
            feedback.append(f"Missing {field.replace('_', ' ')}")
    
    # Experience analysis
    exp_length = len(resume_data['experience']['description'])
    if exp_length > 50:
        score += 2
    elif exp_length > 20:
        score += 1
    else:
        feedback.append("Add more details to work experience")
    
    # Skills analysis
    if len(resume_data['skills']) >= 5:
        score += 2
    elif len(resume_data['skills']) >= 3:
        score += 1
    else:
        feedback.append("Add more skills")
    
    # Education validation
    if resume_data['education']['degree']:
        score += 2
    
    # Cap score at 10
    score = min(score, 10)
    
    # Generate feedback
    if not feedback:
        feedback.append("Good structure! Consider adding more details for higher score")
    
    return {'score': score, 'feedback': " | ".join(feedback)}

def generate_ai_content(form_data):
    prompt = f"""Generate professional resume suggestions based on:
    Name: {form_data.get('name', '')}
    Education: {form_data.get('education', '')}
    Experience: {form_data.get('experience', '')}
    Skills: {form_data.get('skills', '')}
    Projects: {form_data.get('projects', '')}
    
    Suggest improvements for:"""
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional career coach"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    
    return response.choices[0].message['content']

def parse_pdf(file):
    """Extract text from PDF files"""
    try:
        pdf = PdfReader(io.BytesIO(file.read()))
        return "\n".join(page.extract_text() for page in pdf.pages)
    except Exception as e:
        raise ValueError(f"PDF parsing error: {str(e)}")

def extract_info_from_pdf(text):
    """Extract structured data from PDF text"""
    info = {
        'name': '',
        'email': '',
        'phone': '',
        'education': [],
        'experience': []
    }
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    for i, line in enumerate(lines):
        if '@' in line and '.' in line:
            info['email'] = line
        elif any(c.isdigit() for c in line) and len(line) >= 10:
            info['phone'] = line
        elif 'education' in line.lower():
            info['education'].extend(lines[i+1:i+4])
        elif 'experience' in line.lower():
            info['experience'].extend(lines[i+1:i+6])
    
    info['name'] = lines[0] if lines else ''
    return info

def save_to_database(resume_data):
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    resume_id = str(uuid.uuid4())
    score = analyze_resume_quality(resume_data)['score']  # Get quality score
    
    c.execute("INSERT INTO resumes VALUES (?,?,?,?,?,?)",  # 6 placeholders
              (resume_id,
               resume_data['personal_info']['name'],
               resume_data['personal_info']['email'],
               resume_data['personal_info']['phone'],
               score,  # Add quality score
               datetime.now()))
    conn.commit()
    conn.close()
    return resume_id
def process_resume_data(form_data):
    try:
        # Validate required fields
        required = {'name', 'email', 'phone'}
        missing = required - form_data['personal_info'].keys()
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        # Handle PDF input if present
        if 'document' in st.session_state and st.session_state.document:
            if st.session_state.document.type == "application/pdf":
                pdf_text = parse_pdf(st.session_state.document)
                pdf_info = extract_info_from_pdf(pdf_text)
                
                # Merge PDF data with form data
                form_data['personal_info'] = {**pdf_info, **form_data['personal_info']}
                form_data['education'] = {**form_data['education'], 'degree': '\n'.join(pdf_info['education'])}
                form_data['experience'] = {**form_data['experience'], 'description': '\n'.join(pdf_info['experience'])}

        # Generate PDF
        generator = ResumeGenerator(form_data)
        pdf_path = generator.generate_pdf()
        
        # Save to database
        save_to_database(form_data)
        
        return {
            "success": True,
            "pdf_path": pdf_path,
            "filename": generator.filename
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Keep other backend functions same as previous version with font fixes