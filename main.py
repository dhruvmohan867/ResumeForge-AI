# main.py
import streamlit as st
import time
from styles import inject_custom_css
from header import show_header
from form_sections import *
from backend import process_resume_data, analyze_resume_quality, generate_ai_content
def main():
    st.set_page_config(page_title="AI Resume Builder", page_icon="🤖", layout="wide")
    st.markdown(inject_custom_css(), unsafe_allow_html=True)
    
    show_header()
    
    with st.form(key='resume_form'):
        personal_info_section()
        education_section()
        work_experience_section()
        skills_section()
        projects_section()
        
        # AI Suggestions Section
        with st.container():
            st.markdown("<div class='section'><h2>🧠 AI Suggestions</h2>", unsafe_allow_html=True)
            if st.button("Get AI-Powered Suggestions"):
                with st.spinner("Generating AI suggestions..."):
                    try:
                        suggestions = generate_ai_content(st.session_state)
                        st.success("AI Suggestions Generated!")
                        st.markdown(f"<div class='ai-suggestion'>{suggestions}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"AI service unavailable: {str(e)}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("✨ Generate Final Resume")
    
    if submitted:
        with st.spinner("Analyzing and Generating Resume..."):
            # Collect form data
            form_data = {
                "personal_info": {
                    "name": st.session_state.name,
                    "email": st.session_state.email,
                    "phone": st.session_state.phone
                },
                "education": {
                    "degree": st.session_state.education,
                    "years": st.session_state.education_years
                },
                "experience": {
                    "job_title": st.session_state.job_title,
                    "company": st.session_state.company,
                    "description": st.session_state.experience
                },
                "skills": [skill.strip() for skill in st.session_state.skills.split(',')],
                "projects": st.session_state.projects
            }

            # Analyze resume quality
            quality_result = analyze_resume_quality(form_data)
            
            # Process data through backend
            result = process_resume_data(form_data)
            
            if result['success']:
                # Show quality assessment
                st.markdown(f"""
                <div class='quality-report'>
                    <h3>Resume Quality Score: {quality_result['score']}/10</h3>
                    <p>{quality_result['feedback']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Download section
                with open(result['pdf_path'], "rb") as f:
                    pdf_bytes = f.read()
                
                st.download_button(
                    label="Download Professional Resume",
                    data=pdf_bytes,
                    file_name=result['filename'],
                    mime="application/pdf"
                )
            else:
                st.error(f"⚠️ Error: {result['error']}")

    # Footer
    st.markdown("""
    <div class="footer">
        <p>🚀 Powered by AI Resume Builder | Professional Resume Crafting</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()