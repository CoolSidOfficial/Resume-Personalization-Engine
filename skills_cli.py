import os
import json
import subprocess
import shutil

TEMPLATE_TEX = "minimalist_ats.tex"

skills = {
    "Frontend": ["React", "Next.js", "TypeScript", "Tailwind CSS", "JavaScript"],
    "Backend": ["FastAPI", "Node.js", "Express", "Flask", "Python", "REST APIs", "JWT Authentication"],
    "Databases": ["PostgreSQL", "MongoDB", "Redis"],
    "ML & AI": ["Scikit-Learn", "Pandas", "LangChain", "Ollama"],
    "DevOps": ["Docker", "Nginx", "Azure", "WebSockets"]
}

# ----------------------------
# GENERATE SKILLS BLOCK (ONLY ITEMIZE)
# ----------------------------
def generate_skills_block():
    latex = "\\begin{itemize}[leftmargin=0.15in, label={}]\n"

    for category, items in skills.items():
        latex += f"    \\item \\textbf{{{category}:}} " + ", ".join(items) + "\n"

    latex += "\\end{itemize}"
    return latex


# ----------------------------
# CREATE NEW TEX FILE
# ----------------------------
def create_custom_tex(company):
    with open(TEMPLATE_TEX, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "% SKILLS_START"
    end_tag = "% SKILLS_END"

    start_index = content.find(start_tag)
    end_index = content.find(end_tag)

    if start_index == -1 or end_index == -1:
        print("❌ ERROR: Add % SKILLS_START and % SKILLS_END in your .tex file")
        return None

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


# ----------------------------
# COMPILE PDF
# ----------------------------
def compile_pdf(tex_file, company):
    print("\n⚙️ Compiling PDF...\n")

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
            print(f"✅ Final PDF: {final_pdf}")

    except subprocess.CalledProcessError:
        print("❌ Compilation failed. Run manually:")
        print(f"pdflatex {tex_file}")


# ----------------------------
# SAVE VERSION
# ----------------------------
def save_version():
    company = input("\nEnter company name: ").lower().replace(" ", "_")

    with open(f"{company}_skills.json", "w") as f:
        json.dump(skills, f, indent=4)

    tex_file = create_custom_tex(company)

    if tex_file:
        compile_pdf(tex_file, company)


# ----------------------------
# CLI
# ----------------------------
def display_skills():
    print("\n=== CURRENT SKILLS ===\n")
    idx = 1
    mapping = {}

    for category, items in skills.items():
        print(f"\n{category}:")
        for skill in items:
            print(f"  {idx}. {skill}")
            mapping[idx] = (category, skill)
            idx += 1

    return mapping


def remove_skill(mapping):
    num = int(input("\nEnter number to REMOVE: "))
    if num in mapping:
        category, skill = mapping[num]
        skills[category].remove(skill)
        print(f"Removed: {skill}")


def add_skill():
    category = input("\nEnter category: ")
    skill = input("Enter skill: ")

    if category not in skills:
        skills[category] = []

    skills[category].append(skill)
    print(f"Added: {skill}")


# ----------------------------
# MAIN LOOP
# ----------------------------
def main():
    while True:
        mapping = display_skills()

        print("\nOptions:")
        print("1. Remove skill")
        print("2. Add skill")
        print("3. Build Resume 🚀")
        print("4. Exit")

        choice = input("\nChoose: ")

        if choice == "1":
            remove_skill(mapping)
        elif choice == "2":
            add_skill()
        elif choice == "3":
            save_version()
        elif choice == "4":
            break


if __name__ == "__main__":
    main()