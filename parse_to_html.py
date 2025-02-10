#!/usr/bin/env python3
import re
import sys

def convert_latex_to_html(content):
    """
    Wandelt den Inhalt der Challenge-Datei (LaTeX-ähnliches Format) in HTML um.
    """
    # Entferne alle Zeilen, die mit %% beginnen (Kommentare)
    lines = content.splitlines()
    filtered_lines = [line for line in lines if not line.lstrip().startswith("%%")]
    content = "\n".join(filtered_lines)

    # Ersetze \learningobjective{...} durch einen HTML-Header und Absatz
    content = re.sub(
        r'\\learningobjective\{(.+?)\}',
        r'<h1>Learning Objective</h1><p>\1</p>',
        content,
        flags=re.DOTALL
    )

    # Ersetze \chatitle{...} durch einen zweiten HTML-Header
    content = re.sub(
        r'\\chatitle\{(.+?)\}',
        r'<h2>\1</h2>',
        content,
        flags=re.DOTALL
    )

    # Ersetze \begin{challenge} und \end{challenge} durch ein div-Element
    content = content.replace(r'\begin{challenge}', '<div class="challenge">')
    content = content.replace(r'\end{challenge}', '</div>')

    # Ersetze chadescription-Umgebung durch ein div
    content = content.replace(r'\begin{chadescription}', '<div class="chadescription"><p>Description:</p>')
    content = content.replace(r'\end{chadescription}', '</div>')

    # Ersetze task-Umgebung durch ein div
    content = content.replace(r'\begin{task}', '<div class="task"><p>Task:</p>')
    content = content.replace(r'\end{task}', '</div>')

    # Ersetze questions-Umgebung durch ein div mit einer geordneten Liste
    content = content.replace(r'\begin{questions}', '<div class="questions"><p>Questions:</p><ol>')
    content = content.replace(r'\end{questions}', '</ol></div>')

    # Ersetze advice-Umgebung durch ein div
    content = content.replace(r'\begin{advice}', '<div class="advice"><p>Advice:</p><p>')
    content = content.replace(r'\end{advice}', '</p></div>')

    # Ersetze enumerate-Umgebung durch <ol>
    content = content.replace(r'\begin{enumerate}', '<ol>')
    content = content.replace(r'\end{enumerate}', '</ol>')

    # Ersetze \item: Annahme: Jede \item-Zeile enthält den kompletten Listenpunkt.
    def replace_item(match):
        item_content = match.group(1).strip()
        return f'<li>{item_content}</li>'
    content = re.sub(r'\\item\s*(.+)', replace_item, content)

    # Ersetze lstlisting-Umgebung in einen HTML-Codeblock
    content = content.replace(r'\begin{lstlisting}', '<pre><code>')
    content = content.replace(r'\end{lstlisting}', '</code></pre>')

    # Konvertiere einfache figure-Umgebung in ein HTML-Figure-Element.
    # Hier wird nur ein einfaches Muster angenommen, das \includegraphics und \caption umfasst.
    def replace_figure(match):
        figure_content = match.group(0)
        # Suche nach \includegraphics mit Optionen und Dateinamen
        img_match = re.search(r'\\includegraphics\[(.*?)\]\{(.*?)\}', figure_content)
        if img_match:
            options = img_match.group(1)
            img_file = img_match.group(2)
            # Versuche, die Breite zu extrahieren (z.B. width=0.9\textwidth)
            width = '100%'
            width_match = re.search(r'width=([0-9\.]+)\\textwidth', options)
            if width_match:
                width = f'{float(width_match.group(1)) * 100:.0f}%'
            img_html = f'<img src="{img_file}" style="width:{width};" />'
        else:
            img_html = ''
        # Suche nach \caption{...}
        caption_match = re.search(r'\\caption\{(.+?)\}', figure_content)
        caption_html = f'<figcaption>{caption_match.group(1)}</figcaption>' if caption_match else ''
        return f'<figure>{img_html}{caption_html}</figure>'
    content = re.sub(r'\\begin\{figure\}(.+?)\\end\{figure\}', replace_figure, content, flags=re.DOTALL)

    return content

def generate_html(input_filename, output_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            content = infile.read()
    except FileNotFoundError:
        print(f"Error: Datei '{input_filename}' wurde nicht gefunden.")
        sys.exit(1)

    html_body = convert_latex_to_html(content)

    # Erstelle den vollständigen HTML-Inhalt mit Kopf- und Fußbereich
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Challenge</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        .challenge {{ border: 1px solid #ccc; padding: 10px; margin-bottom: 20px; }}
        .chadescription, .task, .questions, .advice {{ margin-bottom: 15px; }}
        ol {{ margin-left: 20px; }}
        figure {{ text-align: center; margin: 15px 0; }}
        figcaption {{ font-style: italic; }}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""

    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(html_content)
    except Exception as e:
        print(f"Fehler beim Schreiben der Ausgabedatei: {e}")
        sys.exit(1)

    print(f"Erfolgreich generiert: {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python parse_to_html.py input_file output_file")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    generate_html(input_file, output_file)
