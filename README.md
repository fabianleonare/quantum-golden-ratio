Project: quantum-golden-ratio

This folder contains a script to build a Word document (`manuscript.docx`) from the provided manuscript text and figure.

Files:
- `build_docx.py` : Python script that creates `manuscript.docx`. It will insert `figure.png` if present; otherwise it generates a placeholder image and embeds it.
- `manuscript.md` : Markdown version of the manuscript text.
- `requirements.txt` : Python dependencies.

How to build the Word file (Windows / macOS / Linux):

1. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Place your high-resolution figure image in this folder and name it `figure.png`. If you prefer, keep the provided placeholder; the script will use it.

4. Run the builder:

```bash
python build_docx.py
```

This will produce `manuscript.docx` in the same folder.

GitHub commit instructions (replace with your remote URL):

```bash
git init
git add .
git commit -m "Add manuscript builder and manuscript text"
git remote add origin https://github.com/<your-username>/quantum-golden-ratio.git
git push -u origin main
```

Note: You need push permissions on the target repository. If the repository already exists on GitHub, set the correct remote URL and push. If you want, provide a GitHub access token and I can show the exact curl/git commands, but I cannot push on your behalf from this environment.

Repository link to include in the manuscript: https://github.com/fabianleonare/quantum-golden-ratio
