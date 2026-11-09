#!/usr/bin/env python3
"""Build the single-file UI demo from the app and its small JSON deck."""

import argparse
import json
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Destination HTML file")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    app = (root / "index.html").read_text(encoding="utf-8")
    deck = json.loads((root / "games/demo/deck.json").read_text(encoding="utf-8"))
    embedded = json.dumps(deck, ensure_ascii=False).replace("<", "\\u003c")
    app, count = re.subn(
        r'(<select[^>]+id="domain"[^>]*>).*?(</select>)',
        r'\1\n        <option value="demo">Quick demo</option>\n      \2',
        app,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise ValueError("Domain picker was not found")
    app = app.replace(
        "  <script>\n    \"use strict\";",
        f'  <script type="application/json" id="embedded-demo">{embedded}</script>\n'
        '  <script>\n    "use strict";',
        1,
    )
    app = app.replace(
        '      <p class="detail"><a href="constrained-sorting-history.html">Project history</a></p>\n',
        "",
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(app, encoding="utf-8")
    print(args.output.resolve())


if __name__ == "__main__":
    main()
