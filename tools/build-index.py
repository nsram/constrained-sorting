#!/usr/bin/env python3
"""Refresh the static deck links in index.html from decks.json."""

from html import escape
import json
from pathlib import Path
import re


def replace_block(page, name, lines):
    start = f"<!-- {name}:start -->"
    end = f"<!-- {name}:end -->"
    if page.count(start) != 1 or page.count(end) != 1:
        raise ValueError(f"Expected one {name} block in index.html")
    before, remainder = page.split(start)
    _, after = remainder.split(end)
    indent = before.rsplit("\n", 1)[-1]
    return before + start + "\n" + "\n".join(lines) + "\n" + indent + end + after


def main():
    root = Path(__file__).resolve().parents[1]
    catalog = json.loads((root / "decks.json").read_text(encoding="utf-8"))
    decks = catalog["decks"]
    sections = catalog["sections"]
    groups = {section: [] for section in sections}
    for deck_id, deck in decks.items():
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", deck_id):
            raise ValueError(f"Invalid deck ID: {deck_id}")
        if not (root / "games" / deck_id / "deck.json").is_file():
            raise ValueError(f"Missing games/{deck_id}/deck.json")
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
        nav.append(f'      <a href="#{section}">{title}</a>')
        blocks.extend([
            f'    <section id="{section}" aria-labelledby="{section}-title">',
            f'      <h2 id="{section}-title">{title}</h2>',
        ])
        grid = len(entries) > 1
        if grid:
            blocks.append('      <div class="grid decks">')
        indent = "        " if grid else "      "
        for deck_id, deck in entries:
            title = escape(deck["title"])
            description = escape(deck["description"])
            blocks.append(
                f'{indent}<a class="tile" href="play.html?deck={deck_id}">'
                f'<h3>{title}</h3><p>{description}</p></a>'
            )
        if grid:
            blocks.append("      </div>")
        blocks.append("    </section>")

    home = root / "index.html"
    page = home.read_text(encoding="utf-8")
    demo_title = escape(decks["demo"]["title"])
    page = replace_block(page, "deck-demo", [
        f'          <a class="button" href="play.html?deck=demo">Play {demo_title}</a>',
    ])
    page = replace_block(page, "deck-navigation", nav)
    page = replace_block(page, "deck-sections", blocks)
    home.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
