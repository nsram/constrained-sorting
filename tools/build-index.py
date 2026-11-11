#!/usr/bin/env python3
"""Refresh the static deck links and reward previews in index.html."""

from html import escape
import json
from pathlib import Path
import re
from urllib.parse import quote


def replace_block(page, name, lines):
    start = f"<!-- {name}:start -->"
    end = f"<!-- {name}:end -->"
    if page.count(start) != 1 or page.count(end) != 1:
        raise ValueError(f"Expected one {name} block in index.html")
    before, remainder = page.split(start)
    _, after = remainder.split(end)
    indent = before.rsplit("\n", 1)[-1]
    return before + start + "\n" + "\n".join(lines) + "\n" + indent + end + after


def reward_previews(root, deck):
    names = deck.get("preview", [])
    if not names:
        return []
    manifest = root / deck["rewards"]
    rewards = json.loads(manifest.read_text(encoding="utf-8"))
    previews = []
    for name in names:
        reward = rewards[name]
        image = reward.get("image")
        src = ""
        if image:
            path = (manifest.parent / image).resolve()
            if not path.is_file():
                raise ValueError(f"Missing preview image {path}")
            src = quote(path.relative_to(root).as_posix())
        label = name[:1].upper() + name[1:]
        previews.append((label, reward.get("fact") or reward.get("detail") or "", src))
    return previews


def preview_image(src, css="", lazy=False):
    if not src:
        return ""
    class_attr = f' class="{css}"' if css else ""
    loading = ' loading="lazy"' if lazy else ""
    return f'<img{class_attr} src="{escape(src)}" width="128" height="128" alt=""{loading} decoding="async">'


def preview_caption(name, fact):
    label = f'<span class="preview-name">{escape(name)}</span>'
    if fact:
        label += f'<span class="preview-fact">{escape(fact)}</span>'
    return label


def deck_tile(deck_id, deck, previews, indent):
    title = escape(deck["title"])
    description = escape(deck["description"])
    lines = [f'{indent}<a class="deck-tile" href="play.html?deck={deck_id}">']
    if previews:
        name, fact, src = previews[0]
        if src:
            lines.append(f'{indent}  {preview_image(src, "tile-art", lazy=True)}')
    lines.extend([
        f'{indent}  <div>',
        f'{indent}    <h4>{title}</h4>',
        f'{indent}    <p class="description">{description}</p>',
    ])
    if previews:
        lines.append(f'{indent}    <p>{preview_caption(name, fact)}</p>')
    lines.extend([
        f'{indent}  </div>',
        f'{indent}  <span class="tile-arrow" aria-hidden="true">↗</span>',
        f'{indent}</a>',
    ])
    return lines


def main():
    root = Path(__file__).resolve().parents[1]
    catalog = json.loads((root / "decks.json").read_text(encoding="utf-8"))
    decks = catalog["decks"]
    sections = catalog["sections"]
    groups = {section: [] for section in sections}
    previews = {}
    for deck_id, deck in decks.items():
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", deck_id):
            raise ValueError(f"Invalid deck ID: {deck_id}")
        if not (root / "games" / deck_id / "deck.json").is_file():
            raise ValueError(f"Missing games/{deck_id}/deck.json")
        previews[deck_id] = reward_previews(root, deck)
        if deck_id != "demo":
            groups[deck["section"]].append((deck_id, deck))

    nav = []
    blocks = []
    for section, title in sections.items():
        entries = groups[section]
        if not entries:
            continue
        if not re.fullmatch(r"[a-z][a-z0-9-]*", section):
            raise ValueError(f"Invalid section ID: {section}")
        title = escape(title)
        nav.append(f'          <a href="#{section}">{title}</a>')
        grid = len(entries) > 1
        wide = " deck-section--wide" if grid or any(previews[deck_id] for deck_id, _ in entries) else ""
        blocks.extend([
            f'        <section class="deck-section{wide}" id="{section}" aria-labelledby="{section}-title">',
            f'          <h3 id="{section}-title">{title}</h3>',
        ])
        if grid:
            blocks.append('          <div class="deck-grid">')
        indent = "            " if grid else "          "
        for deck_id, deck in entries:
            blocks.extend(deck_tile(deck_id, deck, previews[deck_id], indent))
        if grid:
            blocks.append("          </div>")
        blocks.append("        </section>")

    home = root / "index.html"
    page = home.read_text(encoding="utf-8")
    demo_title = escape(decks["demo"]["title"])
    page = replace_block(page, "deck-demo", [
        f'        <a class="demo-link" href="play.html?deck=demo">Play the {demo_title.lower()} <span aria-hidden="true">→</span></a>',
    ])
    page = replace_block(page, "demo-previews", [
        '          <figure class="demo-sample">'
        + preview_image(src)
        + f'<figcaption>{preview_caption(name, fact)}</figcaption></figure>'
        for name, fact, src in previews["demo"]
    ])
    page = replace_block(page, "deck-navigation", nav)
    page = replace_block(page, "deck-sections", blocks)
    home.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
