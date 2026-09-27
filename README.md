# Blog

Source repository for Wilfred Grainger's long-form essays. Substack is the
publication; this repository holds the editable source, figures and
publishing copy.

## Current essay

[Whose xG Is It Anyway?](articles/whose-xg-is-it-anyway/article.md) is the
canonical draft. Its football example uses a fictional full season: 19.08
total xG, four penalties worth 3.16 xG, 2,684 minutes and **0.53 non-penalty
xG per 90** against a strict **> 0.55** screen. Earlier three-penalty and
0.43 versions are superseded.

Within the [article directory](articles/whose-xg-is-it-anyway/):

| File | Role |
| --- | --- |
| `article.md` | Edit this source. Relative figure links work on any branch. |
| `substack.md` | Generated paste-ready body; do not edit directly. Title and subtitle go in Substack's fields. |
| `publishing-kit.md` | Title, description, image order and final publication checks. |
| `linkedin-launch.md` | Optional promotional draft; replace its article-link placeholder before use. |
| `images/*.svg` | Editable figure sources. |
| `images/*.png` | Rendered figures for Substack and other image uploads. |

## Before publishing

From the repository root:

```sh
python3 articles/whose-xg-is-it-anyway/scripts/build-substack.py
python3 articles/whose-xg-is-it-anyway/scripts/build-substack.py --check
python3 articles/whose-xg-is-it-anyway/scripts/render-images.py --check
```

If an SVG changes, regenerate all three PNGs at 1,600 pixels wide with
Inkscape, then inspect them:

```sh
python3 articles/whose-xg-is-it-anyway/scripts/render-images.py
```

The render manifest lets CI catch changed SVGs or PNGs without matching
exports. Inspect at phone width, then rebuild `substack.md` if the article
changed. The exporter converts local image references to
absolute PNG links on `main`, so merge the reviewed changes before copying
the body into Substack. Upload the PNGs in the Substack editor if pasted
Markdown does not embed them. Publication and subscriber email remain a
deliberate final action in Substack.
