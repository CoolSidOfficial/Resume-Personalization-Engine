# 🧠 Resume Personalization Engine (LaTeX + Python)

A CLI-based tool to dynamically customize and generate ATS-friendly resumes using a LaTeX template.  
This project allows you to modify technical skills interactively and generate company-specific resumes in PDF format.

---

## 🚀 Features

- ✏️ Add / remove skills via CLI
- 📄 Automatically inject updated skills into LaTeX template
- 🧾 Generates a new `.tex` file per company
- 📦 Compiles LaTeX into a clean PDF resume
- 💾 Saves skill configurations as JSON snapshots
- 🔒 Keeps original template untouched

---

## 📂 Project Structure
├── minimalist_ats.tex # Base LaTeX template
├── script.py # Main Python script
├── <company>.tex # Generated LaTeX file
├── <company>.pdf # Final resume output
├── <company>_skills.json # Skills snapshot



---

## ⚙️ Requirements

- Python 3.x  
- LaTeX distribution:
  - Windows: MiKTeX  
  - Linux: TeX Live  
  - Mac: MacTeX  

Make sure `pdflatex` is available in your system PATH.

---

Ensure your LaTeX template (minimalist_ats.tex) contains the following markers:

\section{Technical Skills}

% SKILLS_START
\begin{itemize}
    ...
\end{itemize}
% SKILLS_END