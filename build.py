"""Render the supported LaTeX subset in texts/ to a standalone HTML essay."""
from pathlib import Path
from html import escape
import re
ROOT = Path(__file__).resolve().parent

def group(text, pos):
    if pos >= len(text) or text[pos] != '{':
        raise ValueError('Expected a braced LaTeX argument')
    start = pos + 1
    depth = 1
    pos += 1
    while pos < len(text):
        if text[pos] == '\\':
            pos += 2
            continue
        if text[pos] == '{': depth += 1
        if text[pos] == '}': depth -= 1
        if not depth: return text[start:pos], pos + 1
        pos += 1
    raise ValueError('Unclosed LaTeX argument')

def inline(text):
    result = []
    pos = 0
    while pos < len(text):
        char = text[pos]
        if char != '\\':
            if char in '{}$':
                raise ValueError('Escape literal braces/dollar signs; HTML math rendering is not configured.')
            result.append(escape(char))
            pos += 1
            continue
        pos += 1
        if pos >= len(text): raise ValueError('Incomplete LaTeX command')
        if text[pos] in '&%$#_{}':
            result.append(escape(text[pos])); pos += 1; continue
        match = re.match(r'[A-Za-z]+', text[pos:])
        if not match: raise ValueError('Unsupported LaTeX escape')
        command = match[0]
        pos += len(command)
        value, pos = group(text, pos)
        if command == 'href':
            label, pos = group(text, pos)
            if not value.startswith('https://'): raise ValueError('Only HTTPS links are supported')
            result.append(f'<a href="{escape(value, quote=True)}">{inline(label)}</a>')
        elif command in ('emph', 'textit', 'textbf', 'texttt'):
            tag = {'emph':'em','textit':'em','textbf':'strong','texttt':'code'}[command]
            result.append(f'<{tag}>{inline(value)}</{tag}>')
        elif command in ('textasciitilde', 'textasciicircum', 'textbackslash'):
            result.append({'textasciitilde':'~','textasciicircum':'^','textbackslash':'\\'}[command])
        else:
            raise ValueError(f'Unsupported HTML command: {command}')
    return ''.join(result)

def paragraphs(text):
    result = []
    for block in re.split(r'\n\s*\n', text.strip()):
        if not block: continue
        image = re.fullmatch(r'\\includegraphics(?:\[width=\\linewidth\])?\{([^{}]+)\}', block.strip())
        if image:
            image_path = image[1]
            resolved = (ROOT / image_path).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.is_file():
                raise ValueError(f'Image must be an existing project file: {image_path}')
            url = escape(image_path, quote=True)
            result.append(
                f'<div class="architecture-image"><a href="{url}" '
                f'aria-label="Open tokenizer architecture image at full size">'
                f'<img src="{url}" alt="Action tokenizer architecture showing '
                f'the encoder, FSQ quantization, and decoder" loading="lazy"></a></div>'
            )
        elif block.strip().startswith(r'\subsection{'):
            heading, end = group(block.strip(), len(r'\subsection'))
            result.append('<h3>' + inline(heading) + '</h3>')
            remainder = block.strip()[end:].strip()
            if remainder:
                result.append(paragraphs(remainder))
        elif block.startswith(r'\begin{quote}') and block.endswith(r'\end{quote}'):
            body = block[len(r'\begin{quote}'):-len(r'\end{quote}')].strip()
            result.append('<blockquote>' + inline(body.replace('\n', ' ')) + '</blockquote>')
        else:
            result.append('<p>' + inline(block.replace('\n', ' ')) + '</p>')
    return '\n'.join(result)

files = sorted((ROOT / 'texts').glob('[0-9][0-9]-*.tex'))
sections, nav = [], []
for i, file in enumerate(files):
    # Remove LaTeX comments, preserving escaped percent signs.
    source = re.sub(r'(?<!\\)%[^\n]*', '', file.read_text()).strip()
    if not source.startswith(r'\section{'): raise ValueError(f'{file.name}: start with a section title')
    title, end = group(source, len(r'\section'))
    body = source[end:]
    if i == 0:
        hero = '<h1>' + inline(title) + '</h1>' + paragraphs(body)
        continue
    slug = file.stem[3:]
    nav.append(f'<a href="#{slug}"><span>{i:02}</span>{inline(title)}</a>')
    sections.append(f'<section id="{slug}"><div class="section-label">{i:02} /</div><h2>{inline(title)}</h2>{paragraphs(body)}</section>')
words = sum(len(f.read_text().split()) for f in files)
template = (ROOT / 'template.html').read_text()
for key, value in {'HERO': hero, 'NAV': '\n'.join(nav), 'SECTIONS': '\n'.join(sections), 'MINUTES': str(max(1, round(words / 210)))}.items():
    template = template.replace('{{' + key + '}}', value)
(ROOT / 'index.html').write_text(template)
print(f'Built index.html from {len(files)} LaTeX section files.')
