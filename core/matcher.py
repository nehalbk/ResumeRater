"""
Skill matching module using NLP techniques
"""

import logging
import spacy
from sentence_transformers import SentenceTransformer, util

# Initialize logger
logger = logging.getLogger('resume_matcher.core.matcher')

# Load models
logger.info("Loading NLP models...")
try:
    nlp = spacy.load("en_core_web_sm")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    MODELS_LOADED = True
    logger.info("NLP models loaded successfully")
except Exception as e:
    logger.error(f"Error loading NLP models: {e}")
    MODELS_LOADED = False
    raise

def tokenize_resume(text):
    """
    Tokenizes resume text into meaningful phrases for better skill matching.
    
    Args:
        text (str): Resume text content
        
    Returns:
        list: List of tokenized phrases and keywords
    """
    doc = nlp(text)
    
    # Extract noun chunks (e.g., "data analysis", "machine learning")
    phrases = set(chunk.text.lower() for chunk in doc.noun_chunks)
    
    # Extract important keywords (ignore stopwords, punctuation, etc.)
    keywords = set(token.text.lower() for token in doc 
                if not token.is_stop and not token.is_punct and token.is_alpha)

    # Combine both
    tokens = phrases.union(keywords)
    return list(tokens)

def match_skills(resume_text, skill_list, similarity_threshold=0.75):
    """
    Matches resume skills using embeddings for better accuracy and exact matches.
    
    Args:
        resume_text (str): Resume text content
        skill_list (list): List of skills to match against
        similarity_threshold (float): Threshold for semantic similarity matching
        
    Returns:
        list: Sorted list of matched skills
    """
    if not MODELS_LOADED:
        logger.error("NLP models not loaded. Cannot match skills.")
        return []
    
    resume_tokens = tokenize_resume(resume_text)
    logger.info(f"Tokenized resume into {len(resume_tokens)} tokens")

    # Exact skill match
    matched_skills = set()
    for skill in skill_list:
        # Check for exact match (case-insensitive)
        if skill.lower() in resume_text.lower():
            matched_skills.add(skill)
    
    logger.info(f"Found {len(matched_skills)} exact skill matches")
    
    # Compute embeddings for tokenized skills and resume for similarity matching
    resume_embeddings = embedder.encode(resume_tokens, convert_to_tensor=True)
    skill_embeddings = embedder.encode(skill_list, convert_to_tensor=True)
    
    # Compute similarity scores
    similarity_scores = util.pytorch_cos_sim(resume_embeddings, skill_embeddings)
    
    # Matching skills based on similarity score
    semantic_matches = 0
    for i, resume_token in enumerate(resume_tokens):
        for j, skill in enumerate(skill_list):
            if similarity_scores[i][j] > similarity_threshold:
                matched_skills.add(skill)
                semantic_matches += 1
    
    logger.info(f"Found {semantic_matches} semantic skill matches")
    
    return sorted(matched_skills)