"""
Core package initialization with model loading
"""

import os
import logging

logger = logging.getLogger('resume_matcher.core')

# Create model loading indicator
MODELS_LOADED = False