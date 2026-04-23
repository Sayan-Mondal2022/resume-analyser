import os
import streamlit as st
from dotenv import load_dotenv
from preprocessor import extract_keywords, extract_phrases
from parser import process_file
from embedder import Embedder
from scorer import Scorer
from model import ResumeAnalyzerModel


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


@st.cache_resource
def load_embedder():
    return Embedder()


@st.cache_resource
def load_model():
    return ResumeAnalyzerModel()


embedder = load_embedder()
scorer = Scorer()


st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.markdown(
    """
    <h1 style='text-align: center;'>Resume Analyzer</h1>
    <h2 style='text-align: center;'>Upload Resume and Job Description to analyze match.</h2>""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Resume upload")
    resume_input_mode = st.radio(
        "Choose Resume Input Method", ["Upload File", "Paste Text"]
    )

    if resume_input_mode.lower() == "upload file":
        resume_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])
        resume_text_file = None
    else:
        resume_text_file = st.text_area("Paste the Resume").strip()
        resume_file = None


with col2:
    st.subheader("Job Description upload")
    jd_input_mode = st.radio(
        "Choose Job Description Input Method", ["Upload File", "Paste Text"]
    )

    if jd_input_mode.lower() == "upload file":
        jd_file = st.file_uploader("Upload Job Description", type=["pdf", "txt"])
        jd_text_file = None
    else:
        jd_text_file = st.text_area("Paste the Job Description").strip()
        jd_file = None


if (resume_file or resume_text_file) and (jd_file or jd_text_file):
    if st.button("Analyze"):
        if not resume_text_file and not resume_file:
            st.warning("Please upload or paste a Resume before analyzing.")
        elif not jd_text_file and not jd_file:
            st.warning("Please upload or paste a Job Description before analyzing.")
        else:
            with st.spinner("Processing..."):
                try:
                    if resume_file is not None:
                        resume_text = process_file(resume_file)
                    else:
                        resume_text = process_file(resume_text_file)

                    if jd_file is not None:
                        jd_text = process_file(jd_file)
                    else:
                        jd_text = process_file(jd_text_file)

                    # Preprocess
                    resume_keywords = extract_keywords(resume_text)
                    jd_keywords = extract_keywords(jd_text)

                    resume_phrases = extract_phrases(resume_text)
                    jd_phrases = extract_phrases(jd_text)

                    # Embeddings (PHRASES)
                    resume_emb = embedder.encode_batch(resume_phrases)
                    jd_emb = embedder.encode_batch(jd_phrases)

                    # Scores
                    phrase_score = scorer.get_score(resume_emb, jd_emb)
                    keyword_score = scorer.keyword_score(resume_keywords, jd_keywords)

                    # Final Score
                    final_score = scorer.final_score(phrase_score, keyword_score)
                    result = scorer.interpret(final_score)

                    # Skill gap
                    missing_skills = jd_keywords - resume_keywords
                    matched_skills = jd_keywords & resume_keywords

                    st.session_state["analysis"] = {
                        "final_score": str(round(final_score * 100, 2)),
                        "interpretation": result.upper(),
                        "phrase_score": str(round(phrase_score * 100, 2)),
                        "keyword_score": str(round(keyword_score * 100, 2)),
                        "matched_skills": list(matched_skills),
                        "missing_skills": list(missing_skills),
                        "resume_keywords": list(resume_keywords),
                        "jd_keywords": list(jd_keywords),
                        "resume_phrases": resume_phrases,
                        "jd_phrases": jd_phrases,
                    }
                except Exception as e:
                    st.error(f"An ERROR occurred: {e}")

    if "analysis" in st.session_state and st.session_state["analysis"]:
        st.success("Analysis Complete!")
        tab1, tab2, tab3 = st.tabs(["Overview", "AI Insights", "Deep Dive"])

        with tab1:
            st.subheader("Final Score")
            st.metric(
                "Match Score",
                f"{st.session_state['analysis']['final_score']} %",
            )
            st.subheader(
                f"Final remarks: {st.session_state['analysis']['interpretation'].upper()}"
            )

            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Phrase Score",
                    f"{st.session_state['analysis']['phrase_score']} %",
                )

            with col2:
                st.metric(
                    "Keyword Score",
                    f"{st.session_state['analysis']['keyword_score']} %",
                )

        with tab2:
            if st.button("Get AI Insights"):
                with st.spinner("Generating Insights..."):
                    model = load_model()
                    data = {
                        "final_score": st.session_state["analysis"]["final_score"],
                        "interpretation": st.session_state["analysis"][
                            "interpretation"
                        ],
                        "phrase_score": st.session_state["analysis"]["phrase_score"],
                        "keyword_score": st.session_state["analysis"]["keyword_score"],
                        "matched_skills": st.session_state["analysis"][
                            "matched_skills"
                        ],
                        "missing_skills": st.session_state["analysis"][
                            "missing_skills"
                        ],
                        "resume_keywords": st.session_state["analysis"][
                            "resume_keywords"
                        ],
                        "jd_keywords": st.session_state["analysis"]["jd_keywords"],
                    }
                    response = model.get_insights(data)

                    st.subheader("AI Insights are:")
                    st.write(response)

        with tab3:
            st.write("Matched Skills", st.session_state["analysis"]["matched_skills"])
            st.write("Missing Skills", st.session_state["analysis"]["missing_skills"])

            with st.expander("View Extracted Data"):
                st.write(
                    "Resume Keywords:",
                    st.session_state["analysis"]["resume_keywords"],
                )
                st.write("JD Keywords:", st.session_state["analysis"]["jd_keywords"])
                st.write(
                    "Resume Phrases:",
                    st.session_state["analysis"]["resume_phrases"],
                )
                st.write("JD Phrases:", st.session_state["analysis"]["jd_phrases"])
else:
    st.session_state["analysis"] = {}
