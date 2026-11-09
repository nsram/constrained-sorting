#!/usr/bin/env python3
"""Build the single-file UI demo from the app and its small JSON deck."""

import argparse
from base64 import b64encode
import json
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Destination HTML file")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    app = (root / "play.html").read_text(encoding="utf-8")
    logo = b64encode((root / "consort-mark.svg").read_bytes()).decode("ascii")
    app = app.replace('"consort-mark.svg"', f'"data:image/svg+xml;base64,{logo}"')
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
    app = re.sub(r'      <nav class="project-links"[^>]*>.*?</nav>\n', "", app, count=1, flags=re.S)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(app, encoding="utf-8")
    print(args.output.resolve())


if __name__ == "__main__":
    main()
