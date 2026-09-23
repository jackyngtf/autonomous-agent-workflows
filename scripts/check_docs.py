"""Check local documentation links, bilingual pairs and authored SVG syntax."""
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '.venv', 'output', 'node_modules', '.playwright-cli'}


def visible_markdown(text):
    return re.sub(r'^```.*?^```\s*$', '', text, flags=re.M | re.S)


def anchors(text):
    seen = {}
    found = set()
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', visible_markdown(text), re.M):
        heading = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', heading).replace('`', '').lower()
        slug = ''.join(c for c in heading if c in '-_ ' or unicodedata.category(c)[0] in 'LN').replace(' ', '-')
        n = seen.get(slug, 0)
        found.add(f'{slug}-{n}' if n else slug)
        seen[slug] = n + 1
    return found


def main():
    errors = []
    files = [p for p in ROOT.rglob('*.md') if not set(p.relative_to(ROOT).parts) & SKIP]
    for path in files:
        text = path.read_text(encoding='utf-8-sig')
        name = path.relative_to(ROOT).as_posix()
        counterpart = path.with_name(path.name.replace('.zh-TW.md', '.md')) if path.name.endswith('.zh-TW.md') else path.with_name(path.stem + '.zh-TW.md')
        if not counterpart.exists():
            errors.append(f'{name}: missing bilingual counterpart')
        if counterpart.name not in text:
            errors.append(f'{name}: missing language-switch link')
        if len(re.findall(r'^```', text, re.M)) % 2:
            errors.append(f'{name}: unclosed code fence')
        for raw in re.findall(r'\]\(([^)]+)\)', visible_markdown(text)):
            target = raw.strip().strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            linked = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not linked.is_relative_to(ROOT) or not linked.exists():
                errors.append(f'{name}: broken local link {target}')
                continue
            if parsed.fragment and linked.suffix == '.md':
                if unquote(parsed.fragment) not in anchors(linked.read_text(encoding='utf-8-sig')):
                    errors.append(f'{name}: missing anchor {target}')
    for path in (ROOT / 'images').glob('*.svg'):
        try:
            ElementTree.parse(path)
        except ElementTree.ParseError as exc:
            errors.append(f'{path.name}: invalid SVG: {exc}')
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'PASS: {len(files)} Markdown files; language pairs, local links, anchors, fences and SVG syntax.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
