"""
Score calculation module based on matched skills
"""

import logging

logger = logging.getLogger('resume_matcher.core.scorer')

def calculate_score(weighted_skills, matched_skills):
    """
    Calculate score based on weighted skills
    
    Args:
        weighted_skills (pandas.DataFrame): DataFrame with 'skills' and 'weightage' columns
        matched_skills (list): List of matched skills
        
    Returns:
        tuple: (matched_skills, missing_skills, score)
    """
    # Convert matched_skills to set for faster operations
    matched_skills_set = set(matched_skills)
    all_skills_set = set(weighted_skills['skills'].to_list())
    
    # Find missing skills
    missing_skills = all_skills_set - matched_skills_set
    
    # Calculate score
    resume_score = 0
    acquired_skill_points = 0
    total_skill_points = int(weighted_skills['weightage'].sum())

    try:
        # Sum up weights of matched skills
        for matched_skill in matched_skills_set:
            skill_weight = weighted_skills[weighted_skills['skills'] == matched_skill]['weightage'].iloc[0]
            acquired_skill_points += int(skill_weight)
        
        # Calculate percentage score
        if total_skill_points > 0:
            resume_score = acquired_skill_points * 100 / total_skill_points
        else:
            resume_score = 0
            logger.warning("Total skill points is zero, cannot calculate percentage")
        
        logger.info(f"Resume scored {resume_score:.2f}% ({acquired_skill_points}/{total_skill_points} points)")
        
        return matched_skills_set, missing_skills, resume_score
    
    except Exception as e:
        logger.error(f"Error calculating score: {e}")
        return matched_skills_set, missing_skills, 0