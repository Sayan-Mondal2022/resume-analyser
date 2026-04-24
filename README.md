# Resume Analyzer

Welcome to the Resume Analyzer! This project is an intelligent tool designed to evaluate the alignment between a candidate's resume and a specific job description. By leveraging natural language processing and advanced machine learning models, it provides objective scoring and detailed AI-driven insights to help job seekers optimize their resumes and recruiters identify the best talent.

## Project Overview
The Resume Analyzer works by parsing text from uploaded resumes and job descriptions (PDF or TXT formats). It extracts key phrases and keywords using NLP techniques, generates embeddings to understand the semantic meaning, and calculates a match score using cosine similarity. Furthermore, it integrates with a Large Language Model (LLM) via Groq to provide actionable feedback, highlighting strengths, missing skills, and recommendations for improvement.

## Demo Link
Live Demo: [Click Here](https://airesume-analyser.streamlit.app)

## Tech Stack
This project is built using the following technologies:
- **Python 3.11**
- **Streamlit**: For building the interactive web application.
- **spaCy**: For natural language processing, text preprocessing, and keyword/phrase extraction.
- **Sentence-Transformers**: For generating semantic embeddings (`all-MiniLM-L6-v2` model).
- **scikit-learn**: For computing cosine similarity between phrases.
- **LangChain & Groq API**: For generating AI-powered insights and feedback using the `llama-3.3-70b-versatile` model.
- **pdfplumber**: For robust text extraction from PDF files.
- **NumPy & PyTorch**: Core libraries for numerical computations and deep learning models.

## Key Features
- **Flexible Input Methods**: Upload files (PDF, TXT) or paste text directly for both resumes and job descriptions.
- **Semantic Phrase Matching**: Uses sentence embeddings to understand the context and semantic similarity between phrases, rather than relying solely on exact keyword matches.
- **Keyword Extraction & Scoring**: Identifies core skills (nouns, proper nouns, adjectives) and calculates an exact match score.
- **Weighted Scoring System**: Combines phrase similarity (70% weight) and keyword matching (30% weight) to provide a holistic "Match Score".
- **AI Insights & Deep Dive**: Generates comprehensive, actionable feedback using an LLM, detailing score explanations, weaknesses, suggested improvements, and recommended skills.
- **Skill Gap Analysis**: Explicitly lists matched and missing skills between the resume and the job description.

## Installation and Setup Instructions

Follow these step-by-step instructions to set up the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/Sayan-Mondal2022/resume-analyser.git
cd resume-analyser
```

### 2. Set Up a Virtual Environment (Recommended)
Make sure you have Python 3.11 installed. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
Install the required Python packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Download spaCy Model
The project requires the English core web small model for spaCy. It should be installed via the requirements, but you can also install it manually if needed:
```bash
python -m spacy download en_core_web_sm
```

### 5. Configure Environment Variables
Create a `.env` file in the root directory of the project and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 6. Run the Application
Start the Streamlit server:
```bash
streamlit run app.py
```
The application will open in your default web browser at `http://localhost:8501`.

## Future Enhancements
- **Support for More File Formats**: Add support for `.docx` and image-based PDFs (via OCR).
- **Batch Processing**: Allow recruiters to upload multiple resumes against a single job description to rank candidates.
- **Customizable Weights**: Provide a UI slider to let users adjust the weightage between phrase scoring and keyword scoring.
- **Export Reports**: Allow users to download the analysis and AI insights as a PDF report.

## Acknowledgements
This project wouldn't be possible without the following incredible open-source tools and libraries:
- [spaCy](https://spacy.io/) - Industrial-strength Natural Language Processing in Python.
- [Groq](https://groq.com/) - High-performance AI inference for fast LLM responses.
- [PDFPlumber](https://github.com/jsvine/pdfplumber) - Plumb a PDF for detailed information about each text character, rectangle, and line.
- [LangChain](https://python.langchain.com/) - A framework for developing applications powered by language models.
- [Streamlit](https://streamlit.io/) - A faster way to build and share data apps.

## Thank You
Thank you for taking the time to view and explore this project! Your interest is highly appreciated. 

## Contributing
I am always open to collaboration! If you have suggestions, feature requests, or want to contribute to the codebase, please feel free to open an issue or submit a pull request. Let's build something great together.