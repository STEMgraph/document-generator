import json
from pathlib import Path
from typing import Dict, Any

def json_to_latex(json_data: Dict[str, Any], output_file: Path):
    """
    Convert JSON challenge data into a structured LaTeX document.
    Uses 'template.tex' and inserts content into 'content.tex'.
    """
    # Paths for template and content files
    template_path = Path("./latex-template/template.tex")
    styles_path = Path("./latex-template/styles.sty")
    content_path = output_file.with_name("content.tex")

    # Ensure template and styles exist
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")
    if not styles_path.exists():
        raise FileNotFoundError(f"Styles file not found: {styles_path}")

    # Convert tasks into LaTeX enumerated list
    tasks_latex = "\\begin{enumerate}\n"
    for task in json_data["challenge"]["tasks"]:
        tasks_latex += f"  \\item {task}\n"
    tasks_latex += "\\end{enumerate}"

    # Convert questions into LaTeX enumerated list
    questions_latex = "\\begin{questions}\n"
    for question in json_data["challenge"]["questions"]:
        questions_latex += f"  \\item {question}\n"
    questions_latex += "\\end{questions}"

    # Advice section
    advice_text = json_data["challenge"].get("advice", "")

    # Prepare LaTeX content for content.tex
    content_tex = f"""
\\learningobjective{{{json_data["learningobjective"]}}}

\\begin{{challenge}}{{{json_data["challenge"]["chatitle"]}}}
{json_data["challenge"]["challenge_description"]}
\\end{{challenge}}

\\section*{{Tasks}}
{tasks_latex}

\\section*{{Questions}}
{questions_latex}

\\section*{{Advice}}
\\begin{{advice}}
{advice_text}
\\end{{advice}}
"""

    # Write structured LaTeX content
    content_path.write_text(content_tex, encoding="utf-8")

    # Copy template.tex to output location
    template_output_path = output_file.with_name(output_file.stem + "_template.tex")
    template_output_path.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"LaTeX files saved: {template_output_path}, {content_path}")

# Example usage
if __name__ == "__main__":
    input_json_path = Path("challenge.json")
    output_tex_path = Path("challenge.tex")

    with input_json_path.open(encoding="utf-8") as f:
        json_data = json.load(f)

    json_to_latex(json_data, output_tex_path)
