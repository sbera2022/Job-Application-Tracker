
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = {
    "python",
    "c",
    "c++",
    "java",
    "javascript",
    "typescript",
    "react",
    "flask",
    "fastapi",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "git",
    "github",
    "html",
    "css",
}
def compare_skills(resume_text, job_description):
    resume_skills = set(
        extract_basic_keywords(resume_text)
    )

    job_skills = set(
        extract_basic_keywords(job_description)
    )

    matching_skills = sorted(
        resume_skills & job_skills
    )

    missing_skills = sorted(
        job_skills - resume_skills
    )

    return {
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
    }


def extract_basic_keywords(text):
    text = text.lower()

    found = []

    for skill in SKILLS:
        if skill in text:
            found.append(skill)

    return sorted(found)

def calculate_match_score(resume_text, job_description):
    if not resume_text or not job_description:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words="english")

        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])

        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        return round(float(similarity[0][0]) * 100, 2)

    except ValueError:
        return 0.0

def analyze_resume(resume_text, job_description):
    match_score = calculate_match_score(
        resume_text,
        job_description
    )

    skills = compare_skills(
        resume_text,
        job_description
    )

    return {
        "match_score": match_score,
        **skills,
    }