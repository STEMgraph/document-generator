#!/usr/bin/env python3
import re
import sys

def convert_latex_to_md(content):
    """
    Wandelt den Inhalt der Challenge-Datei (LaTeX-ähnliches Format)
    in Markdown um.
    """
    # Entferne Kommentarzeilen, die mit %% beginnen
    lines = content.splitlines()
    filtered_lines = [line for line in lines if not line.lstrip().startswith("%%")]
    content = "\n".join(filtered_lines)

    # Ersetze \learningobjective{...} durch eine Markdown-Überschrift und Absatz
    content = re.sub(
        r'\\learningobjective\{(.+?)\}',
        r'# Learning Objective\n\n\1\n',
        content,
        flags=re.DOTALL
    )

    # Ersetze \chatitle{...} durch eine Markdown-Überschrift (Ebene 2)
    content = re.sub(
        r'\\chatitle\{(.+?)\}',
        r'## \1\n',
        content,
        flags=re.DOTALL
    )

    # Entferne die Umgebung "challenge" (optional: man könnte auch eine Überschrift hinzufügen)
    content = content.replace(r'\begin{challenge}', '## Challenge\n')
    content = content.replace(r'\end{challenge}', '\n')

    # Ersetze die "chadescription"-Umgebung durch eine Überschrift "Description"
    content = content.replace(r'\begin{chadescription}', '### Description\n')
    content = content.replace(r'\end{chadescription}', '\n')

    # Ersetze die "task"-Umgebung durch eine Überschrift "Task"
    content = content.replace(r'\begin{task}', '### Task\n')
    content = content.replace(r'\end{task}', '\n')

    # Ersetze die "questions"-Umgebung durch eine Überschrift "Questions"
    content = content.replace(r'\begin{questions}', '### Questions\n')
    content = content.replace(r'\end{questions}', '\n')

    # Ersetze die "advice"-Umgebung durch eine Überschrift "Advice"
    content = content.replace(r'\begin{advice}', '### Advice\n')
    content = content.replace(r'\end{advice}', '\n')

    # Entferne die "enumerate"-Umgebung (die Listenelemente werden separat verarbeitet)
    content = content.replace(r'\begin{enumerate}', '')
    content = content.replace(r'\end{enumerate}', '')

    # Ersetze \item durch Markdown-Listenelemente (verwende "-" für jeden Punkt)
    content = re.sub(r'\\item\s*(.*)', r'- \1', content)

    # Ersetze lstlisting-Umgebung durch Markdown-Codeblöcke (triple backticks)
    content = content.replace(r'\begin{lstlisting}', '```\n')
    content = content.replace(r'\end{lstlisting}', '\n```')

    # Ersetze figure-Umgebung durch Markdown-Bildsyntax
    def replace_figure(match):
        figure_content = match.group(1)
        # Suche nach \includegraphics (mit oder ohne Optionen)
        img_match = re.search(r'\\includegraphics(?:\[[^\]]*\])?\{(.*?)\}', figure_content)
        caption_match = re.search(r'\\caption\{(.+?)\}', figure_content)
        img_path = img_match.group(1) if img_match else ''
        caption = caption_match.group(1) if caption_match else ''
        # Markdown-Syntax: ![Caption](Bildpfad)
        return f'![{caption}]({img_path})\n'
    content = re.sub(r'\\begin\{figure\}(.+?)\\end\{figure\}', replace_figure, content, flags=re.DOTALL)

    return content

def generate_md(input_filename, output_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            content = infile.read()
    except FileNotFoundError:
        print(f"Error: Datei '{input_filename}' nicht gefunden.")
        sys.exit(1)

    md_content = convert_latex_to_md(content)

    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(md_content)
    except Exception as e:
        print(f"Fehler beim Schreiben der Ausgabedatei: {e}")
        sys.exit(1)

    print(f"Markdown-Datei erfolgreich generiert: {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python parse_to_md.py input_file output_file")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    generate_md(input_file, output_file)
