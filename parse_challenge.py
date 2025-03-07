import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import typer
from pydantic import BaseModel
from to_md import json_to_markdown
from to_html import json_to_html
from to_latex import json_to_latex

app = typer.Typer()

# === Pydantic Models ===

class ChallengeData(BaseModel):
    chatitle: str
    challenge_description: str
    tasks: List[str]
    questions: List[str]
    advice: Optional[str] = None

class StemgraphChallenge(BaseModel):
    meta: Dict[str, Any]  # Arbitrary key-value pairs
    learningobjective: str
    challenge: ChallengeData

# === Typer Application ===

@app.command()
def parse_json(
    input: Path = typer.Option(..., "-i", "--input", help="Path to the .json file"),
    outputs: List[Path] = typer.Option(
        None,
        "-o",
        "--output",
        help="Output file(s) (.md, .html, and .tex supported). Multiple outputs are allowed."
    )
):
    """
    Load and parse a STEMgraph challenge JSON file.
    If --output includes .md, it generates Markdown.
    If --output includes .html, it generates HTML.
    If --output includes .tex, it generates LaTeX.
    Multiple outputs can be generated in one run.
    """
    try:
        content = input.read_text(encoding="utf-8")
        challenge_data = json.loads(content)  # Load JSON data
    except Exception as e:
        typer.echo(f"Error reading JSON file: {e}")
        raise typer.Exit(1)

    try:
        parsed = StemgraphChallenge(**challenge_data)
        
        if outputs:
            for output in outputs:
                if output.suffix == ".md":
                    json_to_markdown(parsed.model_dump(), output)
                elif output.suffix == ".html":
                    json_to_html(parsed.model_dump(), output)
                elif output.suffix == ".tex":
                    json_to_latex(parsed.model_dump(), output)
                else:
                    typer.echo(f"Error: Unsupported output format '{output.suffix}'. Only .md, .html, and .tex are allowed.")
                    raise typer.Exit(1)
        else:
            # Default behavior: print JSON to console
            typer.echo(json.dumps(parsed.model_dump(), indent=2))
    
    except Exception as e:
        typer.echo(f"Error parsing JSON structure: {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
