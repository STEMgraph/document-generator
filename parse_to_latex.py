#!/usr/bin/env python3
import sys

def parse_challenge(input_filename, output_filename):
    """
    Reads a challenge template file, removes comment lines starting with '%%',
    replaces all occurrences of '.svg' with '.png', and writes the remaining content
    into a valid LaTeX document.
    """
    try:
        with open(input_filename, "r", encoding="utf-8") as infile:
            lines = infile.readlines()
    except FileNotFoundError:
        print(f"Error: The file {input_filename} was not found.")
        sys.exit(1)

    # Filter out lines that start with '%%' and replace '.svg' with '.png'
    filtered_lines = []
    for line in lines:
        if line.lstrip().startswith("%%"):
            continue
        # Replace all occurrences of '.svg' with '.png'
        modified_line = line.replace(".svg", ".png")
        filtered_lines.append(modified_line)

    # Updated preamble: the 'questions' environment now creates an enumerate list.
    preamble = r"""\documentclass{scrartcl}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{listings}
\usepackage{enumitem}
% Custom command and environment definitions:
\newcommand{\learningobjective}[1]{\section*{Learning Objective}\textit{#1}}
\newcommand{\chatitle}[1]{\subsection*{#1}}
\newenvironment{challenge}{\section*{Challenge}}{\vspace{1em}}
\newenvironment{chadescription}{\paragraph{Description:}}{\medskip}
\newenvironment{task}{\paragraph{Task:}}{\medskip}
% Updated questions environment with enumerate to properly handle \item commands:
\newenvironment{questions}{%
    \paragraph{Questions:}%
    \begin{enumerate}[label=\arabic*.]
}{%
    \end{enumerate}
}
\newenvironment{advice}{\paragraph{Advice:}}{\medskip}
\begin{document}
"""

    postamble = r"""
\end{document}
"""

    try:
        with open(output_filename, "w", encoding="utf-8") as outfile:
            outfile.write(preamble + "\n")
            outfile.write("".join(filtered_lines))
            outfile.write("\n" + postamble)
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    print(f"Successfully generated {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python parse_challenge.py input_file output_file")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    parse_challenge(input_file, output_file)
