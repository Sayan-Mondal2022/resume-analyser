import numpy as np
from numpy import ndarray, float32
from sklearn.metrics.pairwise import cosine_similarity


class Scorer:

    def __init__(self, phrase_weight=0.7, keyword_weight=0.3) -> None:
        self.phrase_weight = phrase_weight
        self.keyword_weight = keyword_weight

    def get_score(
        self, resume_embeddings: list[ndarray], jd_embeddings: list[ndarray]
    ) -> float:
        score_matrix = cosine_similarity(resume_embeddings, jd_embeddings)

        best_matches = np.max(score_matrix, axis=1)

        return float(best_matches.mean())

    def keyword_score(self, resume_keywords: set[str], jd_keywords: set[str]) -> float:
        common_skills = resume_keywords & jd_keywords
        score = len(common_skills) / len(jd_keywords)
        return float(score)

    def final_score(self, phrase_score: float32, keyword_score: float32) -> float:
        score = self.phrase_weight * phrase_score + self.keyword_weight * keyword_score
        return float(score)

    def interpret(self, score) -> str:
        if score >= 0.8:
            return "Excellent Match"
        elif score >= 0.6:
            return "Good Match"
        elif score >= 0.4:
            return "Moderate Match"
        else:
            return "Low Match"
