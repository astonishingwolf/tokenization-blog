# Tokenization research essay

Open **index.html** in a browser. No server, installation, or account is required. The page works offline; Google Fonts fall back to local fonts when unavailable.

## Editing the writing

1. Open the **texts** folder. Use descriptive lowercase filenames with hyphens, such as `background.tex` or `architecture.tex`. Section order comes from `main.tex`, not filenames.
2. Edit the writing below `\section{Your heading}`. Leave a blank line between paragraphs.
3. Run `python3 build.py` from this folder, then refresh **index.html**.

The `.tex` files are the source of truth for both HTML and LaTeX. Do not edit index.html directly: rebuilding replaces it. Save as UTF-8.

Supported formatting for both outputs:

- Subsections: `\subsection{RoboMimic}`.
- Citation keys: `\cite{titok}` renders as `[titok]` in HTML. Bibliography resolution is not configured; LaTeX requires a matching bibliography entry for a resolved citation.

- Italics: `\emph{text}` or `\textit{text}`.
- Bold: `\textbf{text}`.
- Code: `\texttt{text}`.
- Links: `\href{https://example.com}{Link label}`.
- Images: `\includegraphics[width=\linewidth]{Ttokenization_v2.png}` (project-relative file path). Click the image in the blog to view it at full size.
- Quotations: place text between `\begin{quote}` and `\end{quote}`, with no blank lines inside.
- Escape special characters: `\&`, `\%`, `\_`, `\#`, `\$`, `\{`, `\}`.
- Comments start with `%` and continue to the end of the line.

The HTML builder supports this small LaTeX subset, not arbitrary LaTeX commands, equations, tables, or packages. Unsupported commands produce an error instead of silently changing your writing.

## Compile a LaTeX PDF

Open **main.tex** in Overleaf (upload the project including `texts/`), or run `pdflatex main.tex` with a local LaTeX installation. The PDF uses standard article typography; the HTML retains the existing website fonts and layout.

To insert a section anywhere:

1. Create `texts/your-section-name.tex`, starting with `\section{Your heading}`.
2. Add `\input{texts/your-section-name.tex}` at the desired position inside the document in `main.tex`.
3. Run `python3 build.py` to update the blog. The PDF uses the same order automatically.

The first input supplies the page title. Unlisted files remain drafts and do not appear in either output. The empty `texts/benefits.txt` file is a draft; give it a `.tex` extension and a section heading before adding it to `main.tex`. Reordering inputs does not change existing section links.

## Files

- `texts/`: all essay writing, divided into sections.
- `assets/style.css`: responsive layout, typography, and print styles.
- `assets/script.js`: reading navigation and printing.
- `template.html`: page structure and author/date metadata.
- `build.py`: dependency-free Python 3 builder.
- `main.tex`: LaTeX document that includes all section files.
- `index.html`: generated, directly viewable result.

## Editorial status

The three body sections reproduce the author's supplied draft, including its wording; the supplied architecture image appears in the architecture section. The existing website title is retained. Only source line wrapping and HTML rendering are applied. Earlier expanded text is preserved in `archive/previous-texts/` and is not included in either output.

Visual styling was inspired by https://already-clean.goodfire.com/. This project is local and has not been published.
