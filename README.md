# Resume Skill Matcher

A desktop application that analyzes resumes against a set of weighted skills and provides matching scores.

## Features

- Upload a CSV file with weighted skills
- Process multiple resumes (PDF and DOCX formats)
- Extract text from documents automatically
- Match skills using both exact matching and semantic similarity
- Calculate weighted scores based on matched skills
- Export results to CSV

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/resume-skill-matcher.git
cd resume-skill-matcher
```

2. Create a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Download the required SpaCy model:
```
python -m spacy download en_core_web_sm
```

## Usage

1. Run the application:
```
python main.py
```

2. Select your skills CSV file (must have 'skills' and 'weightage' columns)
3. Select one or more resume files (PDF or DOCX)
4. Click "Process Resumes"
5. View the results in the table
6. Optionally export the results to CSV

## Skills CSV Format

The skills CSV file should have the following columns:
- `skills`: The name of the skill
- `weightage`: The weight/importance of the skill (numeric value)

Example:
```
skills,weightage
Python,10
Machine Learning,8
Data Analysis,7
```

## License

[MIT License](LICENSE)