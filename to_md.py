import json
import re
from pathlib import Path
from typing import Dict, Any

def json_to_markdown(json_data: Dict[str, Any], output_file: Path):
    """
    Convert the JSON challenge structure into a Markdown file.
    - Step 1: Generate rough Markdown layout
    - Step 2: Replace LaTeX figures with Markdown image syntax
    - Step 3: Replace lstlisting with fenced code blocks, ensuring a blank line before and after them
    """
    
    # Step 1: Generate rough Markdown layout
    markdown = []

    # Metadata
    markdown.append(f"# {json_data['challenge']['chatitle']}\n")
    markdown.append(f"**Author:** {json_data['meta'].get('author', 'Unknown')}\n")
    markdown.append(f"**Date:** {json_data['meta'].get('date', 'Unknown')}\n")
    markdown.append(f"**Tags:** {', '.join(json_data['meta'].get('tags', []))}\n")

    # Learning Objective
    markdown.append("\n## Learning Objective\n")
    markdown.append(json_data["learningobjective"] + "\n")

    # Challenge Description
    markdown.append("\n## Challenge Description\n")
    markdown.append(json_data["challenge"]["challenge_description"] + "\n")

    # Tasks
    markdown.append("\n## Tasks\n")
    for idx, task in enumerate(json_data["challenge"]["tasks"], 1):
        markdown.append(f"{idx}. {task}")

    # Questions
    markdown.append("\n## Questions\n")
    for question in json_data["challenge"]["questions"]:
        markdown.append(f"- {question}")

    # Advice (if present)
    if json_data["challenge"].get("advice"):
        markdown.append("\n## Advice\n")
        markdown.append(json_data["challenge"]["advice"])

    # Convert list to single string
    md_content = "\n".join(markdown)

    # Step 2: Replace \begin{figure} with Markdown images
    def replace_figure(match):
        """
        Extracts image path and caption from LaTeX \begin{figure} blocks
        and replaces them with Markdown image syntax.
        """
        content = match.group(1)
        image_match = re.search(r'\\includegraphics\[.*?\]\{(.*?)\}', content)
        caption_match = re.search(r'\\caption\{(.*?)\}', content)
        
        image_path = image_match.group(1) if image_match else "unknown.png"
        caption = caption_match.group(1) if caption_match else "Image"
        
        return f"![{caption}]({image_path})"

    md_content = re.sub(r'\\begin\{figure\}(.*?)\\end\{figure\}', replace_figure, md_content, flags=re.DOTALL)

    # Step 3: Replace \begin{lstlisting} with fenced code blocks, ensuring line breaks
    md_content = re.sub(r'\\begin\{lstlisting\}', "\n```\n", md_content)  # Add a blank line before
    md_content = re.sub(r'\\end\{lstlisting\}', "\n```\n", md_content)   # Add a blank line after

    # Save to file
    output_file.write_text(md_content, encoding="utf-8")
    print(f"Markdown file saved: {output_file}")

# Example usage
if __name__ == "__main__":
    # Load JSON
    input_json_path = Path("challenge.json")
    output_md_path = Path("challenge.md")

    with input_json_path.open(encoding="utf-8") as f:
        json_data = json.load(f)

    # Convert to Markdown
    json_to_markdown(json_data, output_md_path)
