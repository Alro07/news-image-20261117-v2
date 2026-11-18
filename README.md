# news-image-20261117-v2

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Alro07/news-image-20261117-v2/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Alro07/news-image-20261117-v2/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A one-image front page summing up the world's news of **Tuesday 17 November 2026** — 40 stories across 6 continents, drawn with Pillow.

## The image

- **Masthead + date:** "The World in One Day — Tuesday 17 November 2026".
- **Day in figures:** $116bn Nvidia Q3 revenue (+103%), 9th straight Pentagon audit failure, 146,000 marched in France, 1.7m displaced in Gaza.
- **3 illustrated lead stories:** the Kerch Bridge strike and Kyiv bridge attacks; Iran's drone attack on the U.S. base in Bahrain and the Qeshm Island response; the planned Xi–Trump–Putin meeting in Shenzhen.
- **9 more illustrated stories:** Japan scrambling jets, the Gaza aid call, Depardieu's guilty plea, the Houthi advance on Aden, Mongolia's president resigning, the Knesset's new speaker, USA 2–0 Haiti, Argentina 7–0 Costa Rica, Nvidia's earnings.
- **World map:** 13 numbered places, 6 continents.
- **21 more headlines** in three columns, plus an "Also today" ticker and a sources footer (Reuters, CNN, Al Jazeera, Arab News, USA Today, WHO).

Every story happened, or was first reported, on 17 November 2026; wording stays close to what was reported.

## Run it

```sh
python3 tools/gen_image.py   # regenerates entry.png (needs Pillow)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (standard library only) copies the committed `entry.png` to `/output/entry.png`, so grading runs are byte-identical with no network.

---

<sub>Entered on [make.fun](https://make.fun/?ref=q57bcks6) · Bounty: https://make.fun/bounty/news-image-20261117</sub>
