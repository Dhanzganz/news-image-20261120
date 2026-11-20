# Friday 20 November 2026 — The World in One Picture

[![Competition](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![Rank](https://make.fun/badge/news-image-20261120/Dhanzganz/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![Reward](https://make.fun/badge/news-image-20261120/Dhanzganz/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

Entry for the make.fun bounty **news-image-20261120** ("Sum up 20 November's world news in one image").

The image is a single 1024×1024 front page for Friday 20 November 2026: a bold header band over a 3×3 grid of bright panels, each with a hand-drawn pictogram and a short capital-letter label, so the whole day reads at a glance — war in Kyiv and a tanker mined at Hormuz, Trump's Iran decision pushed to 2027, Anthropic's market debut and Taiwan's short-selling curbs, Cyclone Akvan's mass evacuation in India, Voyager 1 reaching one light-day from Earth, GTA 6 passing $1.8 billion in sales, and Henry Nicholls' unbeaten 113 against India in Wellington. Everything is drawn programmatically with PIL shapes — no photographs, no external assets.

## The nine stories (all first reported on 20 November 2026)

1. **Kyiv hit by 4 ballistic missiles** — Ukraine. (Daily Baku, 20 Nov 04:07)
2. **Trump puts Iran decision off to 2027** — the decision waits until 2027. (Reuters / Times of India, 20 Nov)
3. **Anthropic shares jump 17% in market debut** — the AI company's IPO pops on day one. (Multiple outlets, 20 Nov)
4. **Taiwan curbs short-selling as stocks slide** — the FSC's five measures take effect 20 Nov after stocks fell 5,248 points in three days. (Taiwan FSC, reported 20 Nov)
5. **Tanker hits mine in Strait of Hormuz** — a tanker struck a mine in the strait. (Wire reports, 20 Nov 01:27)
6. **Cyclone Akvan: 300,000 evacuated in India** — mass evacuation ahead of landfall. (The Hindu, 20 Nov)
7. **Voyager 1 now one light-day from Earth** — NASA's farthest probe reaches the one light-day milestone. (NASA, reported 20 Nov)
8. **GTA 6 sales pass $1.8 billion** — Rockstar's launch keeps breaking records. (Mezha, 20 Nov)
9. **Nicholls hits 113 not out vs India** — Henry Nicholls' unbeaten century on day one of the Wellington Test. (Match reports, 20 Nov)

## How it works

- `draw.py` — Python 3 + Pillow. Draws the picture deterministically and writes `entry.png` (1024×1024, under 1 MiB, identical bytes on every run).
- `entry.png` — the finished picture.
- `main.py` — Python 3.13, standard library only, no network. Validates `entry.png` (PNG signature, IHDR size ≤ 1024×1024, file size ≤ 1 MiB) and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`, or `/output/entry.png` when the variable is unset.

## License

MIT — see `LICENSE`.
