# Constrained Sorting

Sort cards into named categories and use immediate feedback to revise the board. The game grew out of *The Method of Constrained Sorting*, an unpublished 1999 manuscript by N. Sriram and Troy J. Thevathasan at the National University of Singapore. The [project history](constrained-sorting-history.html) tells the research and design story.

## Play

Select one or more cards, then click or tap a category box. Select a placed card and tap the Tray to bring it back. If the Tray is empty, selecting a placed card reveals **Return to tray**. With nothing selected, tap a filled category’s heading or background to select its cards.

A card scores two points when correctly placed on its first move, one on its second, and zero thereafter. Moving a card out of its correct category removes its points. Efficiency is the number currently placed divided by the number of card moves. The clock starts on the first placement and stops the first time every card is placed.

The project home links directly to Quick demo, the Singapore and soccer decks, and each cricket deck. Which Neighbourhood? has 30 Singapore landmarks across six neighbourhoods. Soccer - Premier League A has 50 players from 10 clubs. The four cricket decks contain 76 Test, 70 ODI, 58 T20I, and 99 IPL cards. The international decks cover India’s men’s team. The IPL deck includes Indian and overseas players. The Test deck includes selected players who debuted before the original 1971 cutoff. Each deck assigns one intended category per card. Switching decks starts a fresh round.

## Run locally

Serve the extracted folder over HTTP so the page can load its JSON decks. From the folder containing `index.html`:

```sh
python3 -m http.server 8000
```

Open [localhost:8000](http://localhost:8000/). The app and its data are static and have no third-party runtime dependencies.

For a direct-open UI demo, generate one file and open it in a browser:

```sh
python3 tools/build-demo.py ../constrained-sorting-demo.html
```

## Source layout

| Path | Purpose |
| --- | --- |
| `index.html` | Project home with direct deck links |
| `play.html` | Game UI, scoring, interaction, and synthesized audio |
| `consort-mark.svg` | Sorting-card logo and browser icon |
| `games/demo/deck.json` | Quick demo |
| `games/singapore/deck.json` | Which Neighbourhood? Singapore landmarks |
| `games/premier-league-a/deck.json` | Soccer - Premier League A |
| `games/tests/deck.json`, `games/odi/deck.json`, `games/t20i/deck.json`, `games/ipl/deck.json` | Four cricket decks |
| `tools/build-demo.py` | Generates the standalone demo from the app and demo JSON |
| `constrained-sorting-history.html` | Research background, design decisions, and technical checkpoints |
| `constrained-sorting-first-release.jpg` | First-release screenshot displayed on the history page |
| `constrained-sorting-tests.jpg` | India Tests screenshot displayed on the home page |
| `constrained-sorting-git-diffs.zip` | Replayable prototype-to-release diffs and checksums |

Each `deck.json` is an object whose keys are the category labels in display order. Each value is an array of unique card labels, written either as a single string or as a two-string name split for display. A card label belongs to one category per deck. Edit the relevant deck file to revise its answer key.

## Singapore deck sources

- Bedok draws on the [Bedok Heritage Trail](https://www.roots.gov.sg/-/media/Roots/Files/bedok-trail/nhb_bedok-heritage-trail_v3.pdf), the [NEA hawker-centre listing](https://www.nea.gov.sg/our-services/hawker-management/overview), and [Golden Village's account of the former Princess Theatre](https://media.gv.com.sg/Booking/movies/images/press/GOLDEN_VILLAGE_BEDOK.pdf).
- Queenstown, Tiong Bahru, and Toa Payoh draw on their [Queenstown](https://www.roots.gov.sg/places/places-landing/trails/my-queenstown-heritage-trail), [Tiong Bahru](https://www.roots.gov.sg/places/places-landing/trails/tiong-bahru-heritage-trail), and [Toa Payoh](https://www.roots.gov.sg/places/places-landing/trails/Toa%20Payoh%20Heritage%20Trail) heritage trails.
- Serangoon Gardens draws on [NHB's Chomp Chomp history](https://www.roots.gov.sg/stories-landing/stories/Hawker-Centres/Chomp-Chomp-Food-Centre), [DP Architects' myVillage profile](https://www.dpa.com.sg/projects/myvillage-serangoon-garden/), and the sites for the [Church of St Francis Xavier](https://www.sfxchurch.sg/) and [Chartwell Drive Park](https://www.nparks.gov.sg/visit/parks/park-detail/chartwell-drive-park).
- Tampines draws on the [Tampines heritage trail booklet](https://www.roots.gov.sg/-/media/Roots/Files/tampines-heritage-trail/nhb_tampines_trail-booklet.ashx) and [NParks' Sun Plaza Park profile](https://www.nparks.gov.sg/visit/parks/park-detail/sun-plaza-park).

## Premier League deck sources

The club order comes from the 2026–27 standings after Matchweek 10, as of 9 November 2026. Each club has its designated captain, a goalkeeper, and three selected first-team players. The answer key uses this season's squads and stays fixed when the table or squads change. See the [Matchweek 10 standings](https://sport-minute.com/en/football/premier-league-2026-27-matchweek-10), the [Premier League squad numbers](https://www.premierleague.com/en/news/4725682/all-20-premier-league-clubs-squad-numbers-for-202627-season), and the [league’s captain list](https://www.premierleague.com/en/news/4706912/premier-league-club-captains-for-202627-season).

## Contribute a deck

Start with the [Bass demo JSON](games/demo/deck.json), the same twelve cards used by Quick demo.

```json
{
  "Fish": ["bass", "trout", "salmon", "cod"],
  "Instruments": ["flute", "cello", "clarinet", "trumpet"],
  "Birds": ["robin", "heron", "sparrow", "finch"]
}
```

1. Save your deck as `games/<deck-name>/deck.json`, using a short folder name such as `garden-birds`.
2. To try it, use a separate local copy of the project. Put your JSON at `games/demo/deck.json`, run the local server described above, and play it through in **Quick demo**.
3. Submit your new deck folder in a pull request. Include a proposed display title, a short description of the subject, and any sources or reasoning that would help a reviewer understand the categories.

## Historical diffs

The [diff archive](constrained-sorting-git-diffs.zip) covers the recoverable checkpoints through the first-push source. Its README describes the provenance, gaps, and replay commands. The [GitHub commit history](https://github.com/nsram/constrained-sorting/commits/main/) follows the project from its first public release.

## First push

For an empty `constrained-sorting` repository, extract the first-push ZIP and run these commands from inside the extracted `constrained-sorting` folder. Replace `YOUR_REPOSITORY_REMOTE` with its Git remote.

```sh
git init -b main
git add .
git commit -m "Add Constrained Sorting"
git remote add origin YOUR_REPOSITORY_REMOTE
git push -u origin main
```

To serve from GitHub Pages, select the `main` branch and `/(root)` as the publishing source. The app uses paths relative to the repository root. [GitHub Pages setup](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
