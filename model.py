from langchain_core.prompts import PromptTemplate
from prompts import prompt_template
from langchain_groq import ChatGroq


class ResumeAnalyzerModel:
    def __init__(self) -> None:
        # self.llm = ChatGroq(temperature=0.3, model_name="llama-3.3-70b-versatile")
        self.llm = ChatGroq(temperature=0.3, model_name="llama-3.1-8b-instant")
        self.template = prompt_template

        self.prompt = PromptTemplate(
            input_variables=[
                "final_score",
                "phrase_score",
                "keyword_score",
                "matched_skills",
                "missing_skills",
                "resume_keywords",
                "jd_keywords",
            ],
            template=self.template,
        )

    def get_insights(self, data: dict) -> str:

        prompt = self.prompt.format(
            final_score=data["final_score"],
            phrase_score=data["phrase_score"],
            keyword_score=data["keyword_score"],
            matched_skills=", ".join(data["matched_skills"]),
            missing_skills=", ".join(data["missing_skills"]),
            resume_keywords=", ".join(data["resume_keywords"]),
            jd_keywords=", ".join(data["jd_keywords"]),
        )

        response = self.llm.invoke(prompt)

        return response.content
