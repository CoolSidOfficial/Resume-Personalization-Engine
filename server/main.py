from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
import subprocess
import shutil

app = FastAPI()

TEMPLATE_TEX = "minimalist_ats.tex"

# In-memory skills store (can later move to DB)
skills = {
    "Frontend": ["React", "Next.js", "TypeScript", "Tailwind CSS", "JavaScript"],
    "Backend": ["FastAPI", "Node.js", "Express", "Flask", "Python", "REST APIs", "JWT Authentication"],
    "Databases": ["PostgreSQL", "MongoDB", "Redis"],
    "ML & AI": ["Scikit-Learn", "Pandas", "LangChain", "Ollama"],
    "DevOps": ["Docker", "Nginx", "Azure", "WebSockets"]
}

# ----------------------------
# MODELS
# ----------------------------
class SkillRequest(BaseModel):
    category: str
    skill: str

class CompanyRequest(BaseModel):
    company: str


# ----------------------------
# UTILS
# ----------------------------
def generate_skills_block():
    latex = "\\begin{itemize}[leftmargin=0.15in, label={}]\n"

    for category, items in skills.items():
        latex += f"    \\item \\textbf{{{category}:}} " + ", ".join(items) + "\n"

    latex += "\\end{itemize}"
    return latex


def create_custom_tex(company: str):
    if not os.path.exists(TEMPLATE_TEX):
        raise HTTPException(status_code=500, detail="Template file missing")

    with open(TEMPLATE_TEX, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "% SKILLS_START"
    end_tag = "% SKILLS_END"

    start_index = content.find(start_tag)
    end_index = content.find(end_tag)

    if start_index == -1 or end_index == -1:
        raise HTTPException(status_code=500, detail="Missing SKILLS tags in template")

    start_index += len(start_tag)

    new_block = "\n" + generate_skills_block() + "\n"

    updated_content = (
        content[:start_index] +
        new_block +
        content[end_index:]
    )

    output_tex = f"{company}.tex"

    with open(output_tex, "w", encoding="utf-8") as f:
        f.write(updated_content)

    return output_tex


def compile_pdf(tex_file: str, company: str):
    try:
        for _ in range(2):
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )

        pdf_name = tex_file.replace(".tex", ".pdf")
        final_pdf = f"{company}.pdf"

        if os.path.exists(pdf_name):
            shutil.move(pdf_name, final_pdf)
            return final_pdf

        raise HTTPException(status_code=500, detail="PDF not generated")

    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="LaTeX compilation failed")


# ----------------------------
# ROUTES
# ----------------------------

@app.get("/")
def home():
    return {"message": "Resume Builder API Running"}


@app.get("/skills")
def get_skills():
    return skills


@app.post("/skills/add")
def add_skill(req: SkillRequest):
    if req.category not in skills:
        skills[req.category] = []

    if req.skill not in skills[req.category]:
        skills[req.category].append(req.skill)

    return {"message": "Skill added", "skills": skills}


@app.post("/skills/remove")
def remove_skill(req: SkillRequest):
    if req.category in skills and req.skill in skills[req.category]:
        skills[req.category].remove(req.skill)
        return {"message": "Skill removed", "skills": skills}

    raise HTTPException(status_code=404, detail="Skill not found")


@app.post("/build")
def build_resume(req: CompanyRequest):
    company = req.company.lower().replace(" ", "_")

    # Save JSON snapshot
    with open(f"{company}_skills.json", "w") as f:
        json.dump(skills, f, indent=4)

    tex_file = create_custom_tex(company)
    pdf_file = compile_pdf(tex_file, company)

    return {
        "message": "Resume generated",
        "tex_file": tex_file,
        "pdf_file": pdf_file
    }