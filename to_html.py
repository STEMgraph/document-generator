import json
import re
from pathlib import Path
from typing import Dict, Any

def json_to_html(json_data: Dict[str, Any], output_file: Path):
    """
    Convert the JSON challenge structure into an HTML file.
    - Step 1: Generate rough HTML layout
    - Step 2: Replace LaTeX figures with <img> tags
    - Step 3: Replace lstlisting with <pre><code> blocks
    """

    # Step 1: Generate rough HTML layout
    html = []

    # Start HTML Document
    html.append("<!DOCTYPE html>")
    html.append("<html lang='en'>")
    html.append("<head>")
    html.append("  <meta charset='UTF-8'>")
    html.append("  <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
    html.append("  <title>{}</title>".format(json_data['challenge']['chatitle']))
    html.append("  <style>")
    html.append("    body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: auto; }")
    html.append("    h1, h2, h3 { color: #333; }")
    html.append("    pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }")
    html.append("    img { max-width: 100%; height: auto; display: block; margin: 10px 0; }")
    html.append("  </style>")
    html.append("</head>")
    html.append("<body>")

    # Metadata
    html.append(f"<h1>{json_data['challenge']['chatitle']}</h1>")
    html.append(f"<p><strong>Author:</strong> {json_data['meta'].get('author', 'Unknown')}</p>")
    html.append(f"<p><strong>Date:</strong> {json_data['meta'].get('date', 'Unknown')}</p>")
    html.append(f"<p><strong>Tags:</strong> {', '.join(json_data['meta'].get('tags', []))}</p>")

    # Learning Objective
    html.append("<h2>Learning Objective</h2>")
    html.append(f"<p>{json_data['learningobjective']}</p>")

    # Challenge Description
    html.append("<h2>Challenge Description</h2>")
    html.append(f"<p>{json_data['challenge']['challenge_description']}</p>")

    # Tasks
    html.append("<h2>Tasks</h2>")
    html.append("<ul>")
    for task in json_data["challenge"]["tasks"]:
        html.append(f"<li>{task}</li>")
    html.append("</ul>")

    # Questions
    html.append("<h2>Questions</h2>")
    html.append("<ul>")
    for question in json_data["challenge"]["questions"]:
        html.append(f"<li>{question}</li>")
    html.append("</ul>")

    # Advice (if present)
    if json_data["challenge"].get("advice"):
        html.append("<h2>Advice</h2>")
        html.append(f"<p>{json_data['challenge']['advice']}</p>")

    # Convert list to a single HTML string
    html_content = "\n".join(html)

    # Step 2: Replace LaTeX \begin{figure} with <img> tags
    def replace_figure(match):
        """
        Extracts image path and caption from LaTeX \begin{figure} blocks
        and replaces them with HTML <img> tags.
        """
        content = match.group(1)
        image_match = re.search(r'\\includegraphics\[.*?\]\{(.*?)\}', content)
        caption_match = re.search(r'\\caption\{(.*?)\}', content)
        
        image_path = image_match.group(1) if image_match else "unknown.png"
        caption = caption_match.group(1) if caption_match else "Image"

        return f'<figure><img src="{image_path}" alt="{caption}"><figcaption>{caption}</figcaption></figure>'

    html_content = re.sub(r'\\begin\{figure\}(.*?)\\end\{figure\}', replace_figure, html_content, flags=re.DOTALL)

    # Step 3: Replace \begin{lstlisting} with <pre><code> blocks
    html_content = re.sub(r'\\begin\{lstlisting\}', "<pre><code>", html_content)
    html_content = re.sub(r'\\end\{lstlisting\}', "</code></pre>", html_content)

    # Close HTML Document
    html_content += "\n</body>\n</html>"

    # Save to file
    output_file.write_text(html_content, encoding="utf-8")
    print(f"HTML file saved: {output_file}")

# Example usage
if __name__ == "__main__":
    # Load JSON
    input_json_path = Path("challenge.json")
    output_html_path = Path("challenge.html")

    with input_json_path.open(encoding="utf-8") as f:
        json_data = json.load(f)

    # Convert to HTML
    json_to_html(json_data, output_html_path)
