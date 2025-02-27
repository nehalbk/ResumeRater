"""
Utility functions for the Resume Skill Matcher application
"""

import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('resume_matcher')

def setup_logging(log_file=None):
    """Set up logging to file and console"""
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)

def ensure_directory(directory):
    """Ensure directory exists, create if not"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")
    return directory

def is_valid_file(filepath, allowed_extensions=None):
    """Check if file exists and has allowed extension"""
    if not os.path.isfile(filepath):
        return False
    
    if allowed_extensions:
        _, ext = os.path.splitext(filepath)
        return ext.lower() in allowed_extensions
    
    return True

def cleanup_text(text):
    """Clean up text by removing excessive whitespace and normalizing newlines"""
    # Replace multiple newlines with a single newline
    text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
    
    # Replace multiple spaces with a single space
    text = ' '.join(text.split())
    
    return text