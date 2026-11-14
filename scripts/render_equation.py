"""Typeset one equation block in Neo Euler and export a transparent PNG.

Usage: python3 render_equation.py OUT_DIR NAME 'LATEX_BODY'
  LATEX_BODY goes inside $\\begin{aligned} ... \\end{aligned}$, e.g.
  '\\bar{x} &= \\dfrac{1}{N}\\sum_{i} x_i \\\\[10pt] \\symbf{y} &= \\symbf{A}\\symbf{x} + \\symbf{b}'
Colours available in the body: ink (default), focus (blue), muted, highlight (orange) —
e.g. \\textcolor{focus}{...}.
Writes OUT_DIR/NAME.png and prints its pixel size (keep the aspect ratio when placing it).
Stops if Neo Euler or xelatex is missing: ask the user instead of falling back to another font.
"""
import os, shutil, subprocess, sys

out, name, body = os.path.abspath(sys.argv[1]), sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
if not shutil.which("xelatex"):
    sys.exit("xelatex not found: ask the user before using any other way to typeset math")
if "Neo Euler" not in subprocess.run(["fc-list"], capture_output=True, text=True).stdout:
    sys.exit("Neo Euler not installed: download https://raw.githubusercontent.com/aliftype/euler-otf/master/euler.otf "
             "into ~/.fonts, run `fc-cache -f`, and if that fails ask the user (no silent fallback)")

TEX = r"""\documentclass[border=3pt]{standalone}
\usepackage{amsmath,xcolor}
\usepackage[math-style=upright,bold-style=upright]{unicode-math}
\setmainfont{Neo Euler}[FakeBold=1.2]
\setmathfont{Neo Euler}[FakeBold=1.2]
\definecolor{ink}{HTML}{1E1E1E}\definecolor{focus}{HTML}{2F6FD8}
\definecolor{muted}{HTML}{737373}\definecolor{highlight}{HTML}{D9731A}
\begin{document}\color{ink}\Large
$\begin{aligned}
%s
\end{aligned}$
\end{document}
"""
tex = os.path.join(out, f"{name}.tex")
open(tex, "w").write(TEX % body)
r = subprocess.run(["xelatex", "-interaction=nonstopmode", f"{name}.tex"], cwd=out, capture_output=True, text=True)
missing = [l for l in r.stdout.splitlines() if "Missing character" in l]
if r.returncode:
    sys.exit(r.stdout[-1500:])
if missing:
    print("WARNING missing glyphs:", *missing, sep="\n  ")
subprocess.run(["pdftocairo", "-png", "-transp", "-r", "600", "-singlefile", f"{name}.pdf", name], cwd=out, check=True)
from PIL import Image
print(name, Image.open(os.path.join(out, f"{name}.png")).size)
