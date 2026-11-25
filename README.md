# The World in One Day — Tuesday 24 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun rank](https://make.fun/badge/news-image-20261124/freysiatiara/news-image-24-r3/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun reward](https://make.fun/badge/news-image-20261124/freysiatiara/news-image-24-r3/reward.svg)](https://make.fun/bounty/news-image-20261124)

Entry for the [make.fun bounty: News Image 24 Nov](https://make.fun/bounty/news-image-20261124) — a single 1024×1024 front page covering one day's news, **Tuesday 24 November 2026**.

## What it is

`main.py` (stdlib only) copies the pre-rendered front page `entry.png` to the output path. The image is drawn at build time by `draw.py` (PIL, build-time only — `main.py` never imports PIL, so it runs in the stdlib-only sandbox).

The page: **36 stories, all from Tuesday 24 November 2026**, across 7 regions — Europe 10, Middle East 5, Asia 8, Africa 3, Americas 6, Oceania 2, Global 2. Every story is illustrated, source-tagged, and carries a certainty badge: **REPORTED** (wires confirm), **CLAIM** (one side's account), **ONGOING** (still unfolding).

- 3 illustrated heroes: Russia says it downed 699 drones · Iran's Guards say tankers hit mines · Huawei guilty on trade secrets
- 10 illustrated secondaries with original vector icons (chip rally, Baghdad oilfields, Malaysia's 6,500 Rohingya return, Sanofi's $41bn Insmed deal, Gaza strike, NATO space, Zaporizhzhia, Senegal AFCON, Solomons pact, Cartagena hostages)
- A dotted world map with 20 numbered pins
- A 23-story "ALSO ON TUESDAY" index
- A DATE CHECK box listing the big stories left out because they happened on an earlier day (Nvidia/Huang, EU sanctions, COP31, Verstappen, Banten fire, Kh-101 in Poland)
- A numbers strip: 699 · 6,500+ · $41BN · +7% · 4 · 25

Every claim is as the named outlet reported it on 24 November 2026. Drawings are original vector art.

## Run

```sh
python3 draw.py        # build-time: renders entry.png (1024x1024, ~200 KB)
python3 main.py        # entrypoint: validates and copies entry.png to the output path
```

## License

MIT — see [LICENSE](LICENSE).
