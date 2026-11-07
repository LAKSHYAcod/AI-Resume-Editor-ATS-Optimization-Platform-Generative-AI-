from pathlib import Path

def save_resume(text: str, filename: str) -> str:
    path = Path("generated_resumes")
    path.mkdir(exist_ok=True)
    file_path = path / filename

    file_path.write_text(text, encoding="utf-8")
    return str(file_path)
