from langchain_core.prompts import PromptTemplate
from prompts import prompt_template
from langchain_groq import ChatGroq


class ResumeAnalyzerModel:
    def __init__(self) -> None:
        self.llm = ChatGroq(temperature=0.3, model_name="llama-3.3-70b-versatile")
        self.template = prompt_template

        self.prompt = PromptTemplate(
            input_variables=[
                "final_score",
                "interpretation",
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
            final_score=round(data["final_score"] * 100, 2),
            interpretation=data["interpretation"],
            phrase_score=round(data["phrase_score"] * 100, 2),
            keyword_score=round(data["keyword_score"] * 100, 2),
            matched_skills=", ".join(data["matched_skills"]),
            missing_skills=", ".join(data["missing_skills"]),
            resume_keywords=", ".join(data["resume_keywords"]),
            jd_keywords=", ".join(data["jd_keywords"]),
        )

        response = self.llm.invoke(prompt)

        return response.content
