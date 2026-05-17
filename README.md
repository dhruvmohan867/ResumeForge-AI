# ResumeForge AI ⚡

A modern AI-powered resume builder with ATS optimization, intelligent parsing, and professional PDF generation.

## Features

- **🧠 AI Resume Parsing** — Upload a PDF and let GPT-4o-mini extract structured data
- **🎯 ATS Analysis** — Semantic job description matching with gap analysis
- **✨ AI Enhancement** — XYZ formula bullet rewriting and summary optimization
- **📄 Multi-Template PDF** — Three professional templates with dynamic layouts
- **🌙 Dark/Light Mode** — Modern SaaS-quality UI with glassmorphism design

## Architecture

```
app/
├── main.py                  # Application entry point
├── config.py                # Environment & configuration
├── models/
│   └── resume_schema.py     # Pydantic data models
├── services/
│   ├── ai_service.py        # OpenAI API wrapper
│   ├── parser_service.py    # PDF parsing pipeline
│   ├── ats_service.py       # ATS analysis engine
│   ├── enhance_service.py   # Content enhancement
│   └── pdf_service.py       # PDF generation engine
├── database/
│   └── db.py                # SQLite persistence
├── ui/
│   ├── dashboard.py         # Tab orchestration
│   ├── form_sections.py     # Form input sections
│   ├── sidebar.py           # Navigation sidebar
│   ├── components.py        # Reusable UI components
│   └── styles.py            # CSS theme system
└── utils/
    ├── constants.py          # Prompts & constants
    ├── helpers.py            # Utility functions
    └── validators.py         # Input validation
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Minor_project_6th
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate     # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   # Create .env file in root
   OPENAI_API_KEY=your_api_key_here
   ```

5. **Run the application:**
   ```bash
   streamlit run app/main.py
   ```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit + Custom CSS |
| AI | OpenAI GPT-4o-mini |
| Validation | Pydantic v2 |
| PDF | FPDF2 |
| Database | SQLite |
| Parsing | PyPDF2 |

## Key Engineering Decisions

- **Pydantic schemas** enforce data integrity across all layers
- **Reusable AI service** with retry logic and structured JSON extraction
- **Decoupled forms** prevent Streamlit state reset issues
- **CSS custom properties** enable seamless dark/light theme switching
- **Modular architecture** keeps files focused and maintainable

## License

MIT
