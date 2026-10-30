# Profile setup

An English GitHub profile README with a green-and-black terminal theme. All images are stored locally in `assets/`; no external badge or animation service is required.

## Display it on your GitHub profile

This artwork was prepared in `Kueranan/Resume-Profile`. GitHub displays a personal profile README from a **public repository named exactly like the account**: `Kueranan/Kueranan`.

1. Create the public repository `Kueranan/Kueranan`, or rename this repository to `Kueranan` if that name is available.
2. Copy `README.md` and the entire `assets/` directory into its default branch. Keep the README at the repository root.
3. Open `https://github.com/Kueranan` to see the profile.

If `Kueranan/Kueranan` already exists, review its contents before replacing anything. Relative image paths work in either repository as long as the assets stay beside the README.

Official documentation: [Managing your profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).

## Design and animation

- The header is a looping GIF with a typing terminal, moving data streams, and a scanning neural network.
- Sections 01–06 are compact animated notebook cards with data curves, scatter plots, and heatmaps. These graphics are decorative, not measured model results or Kaggle statistics.
- The skills card groups monochrome technology logos into Machine Learning & Data Science, Development & Tools, and Analytics & Reporting. Logo sources and license notices are in `assets/icons/`.
- A collapsed plain-text profile and descriptive image alternatives keep the content available without loading the artwork.
- The name and identity remain visible throughout the loop.
- Every GIF has a matching PNG. Replace `.gif` with `.png` in the README image paths to disable motion.
- Badges and footer are local SVG images with no scripts, external fonts, or network requests.
- GitHub controls the surrounding page theme. Images retain their black background in light and dark modes; README text uses the visitor's GitHub theme.
- Work, education, and skills are based on the supplied resume, with Codex, Excel, and Power BI added at the owner's request. Project repository links were not supplied, so none were invented. A phone number and a copy of the resume PDF are not included.

## Regenerate the artwork

Python 3, Pillow, CairoSVG, and the system Cairo library are required. The generator supports macOS, Linux, and Windows font locations. For another font installation, set `PROFILE_MONO_FONT` and `PROFILE_TITLE_FONT` to font file paths.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python scripts/generate_assets.py
.venv/bin/python scripts/generate_sections.py
```

Edit section copy and skill groups in `scripts/generate_sections.py`; it regenerates the section artwork and README together. Generated assets are included alongside the README, so visitors do not need to run the generator. The `scripts/` directory and this guide are only needed for maintenance.
