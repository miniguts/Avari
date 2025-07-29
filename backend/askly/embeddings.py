import re

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from core.constants import SIMILARITY_THRESHOLD, TOP_K

from .genai_service import get_embedding
from .models import QuestionAnswer


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    return text


def find_similar_question_embedding(query: str) -> QuestionAnswer | None:
    query_norm = normalize_text(query)
    exact_match = QuestionAnswer.objects.filter(
        question__iexact=query_norm, valid=True
    ).first()
    if exact_match:
        return exact_match

    query_embedding = get_embedding(query_norm)
    if not query_embedding or len(query_embedding) < 10:
        return None

    valid_qas = list(QuestionAnswer.objects.filter(valid=True))
    if not valid_qas:
        return None

    embeddings = np.array([qa.embedding for qa in valid_qas])
    query_emb = np.array(query_embedding).reshape(1, -1)
    similarities = cosine_similarity(query_emb, embeddings)[0]

    top_indices = similarities.argsort()[-TOP_K:][::-1]

    for idx in top_indices:
        if similarities[idx] >= SIMILARITY_THRESHOLD:
            return valid_qas[idx]

    return None
