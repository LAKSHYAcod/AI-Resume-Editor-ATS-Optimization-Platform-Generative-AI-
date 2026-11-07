from utils.openrouter_client import generate_text


def generate_resume(profile: dict, job_description: str) -> str:
    """
    Generates an ATS-optimized resume based on
    user profile and job description.
    """

    name = profile.get("name", "")
    email = profile.get("email", "")
    linkedin = profile.get("linkedin", "")
    github = profile.get("github", "")
    experience = profile.get("experience", "")
    skills = profile.get("skills", [])

    skills_text = ", ".join(skills) if isinstance(skills, list) else skills

    prompt = f"""
    Create a professional, ATS-optimized resume.

    Candidate Information:
    Name: {name}
    Email: {email}
    LinkedIn: {linkedin}
    GitHub: {github}
    Experience: {experience} years
    Skills: {skills_text}

    Match the following job description:

    {job_description}

    Format the resume with:
    - Professional Summary
    - Skills Section
    - Experience Section
    - Projects Section
    - Education Section

    Make it strong, impactful, and keyword-optimized.
    """

    return generate_text(prompt)