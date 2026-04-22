import numpy as np
from numpy import ndarray, float32
from sklearn.metrics.pairwise import cosine_similarity


class Scorer:

    def __init__(self, phrase_weight=0.7, keyword_weight=0.3):
        self.phrase_weight = phrase_weight
        self.keyword_weight = keyword_weight

    def get_score(
        resume_embeddings: list[ndarray], jd_embeddings: list[ndarray]
    ) -> float32:
        score_matrix = cosine_similarity(resume_embeddings, jd_embeddings)

        best_matches = np.max(score_matrix, axis=1)

        return best_matches.mean()

    def final_score(self, phrase_score: float32, keyword_score: float32) -> float32:
        return self.phrase_weight * phrase_score + self.keyword_weight * keyword_score
