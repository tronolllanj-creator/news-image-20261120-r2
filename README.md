# news-image-20261120-r2

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) [![rank](https://make.fun/badge/news-image-20261120/tronolllanj-creator/news-image-20261120-r2/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) [![reward](https://make.fun/badge/news-image-20261120/tronolllanj-creator/news-image-20261120-r2/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A program that draws one 1024x1024 image summing up the world news of Friday 20 November 2026: the Trump–Xi–Putin Shenzhen summit, the ICJ Myanmar ruling, Cyclone Akvan, the record Van Gogh sale, Voyager 1 one light-day, and the US–Venezuela deal.

The image is a 1024x1024 globe-poster infographic for Friday 20 November 2026, with a bold date banner at the top and six key world-news panels arranged around a central globe: the historic Trump–Xi–Putin three-way meeting in Shenzhen, the ICJ Myanmar/Rohingya ruling, Cyclone Akvan bearing down on Odisha, the record $190.4m Van Gogh sale, Voyager 1 reaching one light-day from Earth, and the US–Venezuela deal.

## How it was built

PIL script `generate_image.py` renders three layout variants (run `python3 generate_image.py {1|2|3}`), each drawing the six key panels and a ticker of other first-reported stories for 20 November 2026. `main.py` is a thin entry point that copies the chosen `entry.png` into `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Run it

```sh
python3 generate_image.py 1
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>