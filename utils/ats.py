import re


# -------------------------------
# Clean and tokenize text
# -------------------------------
def tokenize(text: str):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return set(words)


# -------------------------------
# Extract important keywords
# -------------------------------
def extract_keywords(job_description: str):
    """
    Extracts important words from job description
    """
    words = tokenize(job_description)

    # Remove common useless words
    stop_words = {
        "with", "and", "the", "for", "you", "are", "will",
        "this", "that", "from", "have", "has", "our",
        "your", "job", "role", "team", "work", "experience"
    }

    keywords = words - stop_words

    return keywords


# -------------------------------
# ATS Score Calculator
# -------------------------------
def calculate_ats_score(resume_text: str, job_description: str):
    resume_words = tokenize(resume_text)
    job_keywords = extract_keywords(job_description)

    if not job_keywords:
        return {
            "score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "suggestions": ["No job keywords found"]
        }

    matched = resume_words.intersection(job_keywords)
    missing = job_keywords - resume_words

    keyword_score = (len(matched) / len(job_keywords)) * 70  # 70% weight

    # Resume length check (ideal between 400–1200 words)
    word_count = len(resume_text.split())

    if 400 <= word_count <= 1200:
        length_score = 20
    else:
        length_score = 10

    # Basic structure check (education/experience presence)
    structure_score = 0
    lower_resume = resume_text.lower()

    if "experience" in lower_resume:
        structure_score += 5
    if "education" in lower_resume:
        structure_score += 5

    total_score = round(keyword_score + length_score + structure_score, 2)

    suggestions = []

    if missing:
        suggestions.append(
            f"Consider adding these missing keywords: {', '.join(list(missing)[:10])}"
        )

    if word_count < 400:
        suggestions.append("Resume is too short. Add more project or experience details.")

    if word_count > 1200:
        suggestions.append("Resume is too long. Try keeping it concise.")

    return {
        "score": total_score,
        "matched_keywords": list(matched)[:15],
        "missing_keywords": list(missing)[:15],
        "suggestions": suggestions
    }