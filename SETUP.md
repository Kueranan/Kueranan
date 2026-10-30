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
- The name and identity remain visible throughout the loop.
- `assets/terminal-header.png` is a static alternative. Change the README image extension from `.gif` to `.png` to disable motion.
- Badges and footer are local SVG images with no scripts, external fonts, or network requests.
- GitHub controls the surrounding page theme. Images retain their black background in light and dark modes; README text uses the visitor's GitHub theme.
- Work, education, and skills are based on the supplied resume. Project repository links were not supplied, so none were invented. A phone number and a copy of the resume PDF are not included.

## Regenerate the artwork

Python 3 and Pillow are required. The generator supports macOS, Linux, and Windows font locations. For another font installation, set `PROFILE_MONO_FONT` and `PROFILE_TITLE_FONT` to font file paths.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python scripts/generate_assets.py
```

Generated assets are included alongside the README, so visitors do not need to run the generator. The `scripts/` directory and this guide are only needed for maintenance.
