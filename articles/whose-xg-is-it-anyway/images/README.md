# Article visuals

Four images carry four different jobs: introduce the red-herring metaphor, expose the metric error, show the enforced boundary, and demonstrate how a stale relationship changes a decision. The three explanatory figures are native SVGs with titles and extended descriptions, exported as PNGs for publishing. The cover is an original generated editorial illustration.

| File | Purpose |
| --- | --- |
| `01-cover.jpg` | A shortlisted striker casts a red-herring shadow across a recruitment desk. |
| `02-metric-dissection.png` | A shared numerical axis shows exactly how subtracting penalties moves McBaggio from 0.64 total xG/90 to 0.43 npxG/90. |
| `03-decision-boundary.png` | The agent must pass through a deterministic screening service; rank, exclude and withhold are distinct outcomes. |
| `04-ownership-timeline.png` | Effective time, publication time and decision time accompany an ownership change that turns separate £6m and £3m exposures into a £9m group against an £8m limit. |

Warm ivory, pitch green, cobalt and vermilion connect the cover and figures. Nimbus Roman headlines and Nimbus Sans labels give the data figures an editorial character. The chart, architecture diagram and ownership timeline use different forms because they explain different relationships.

## Data and interpretation

The football records and financial mandate are fictional. Figure 1 uses unrounded rates for bar lengths and rounded labels for reading. The three penalties sum to 2.37 xG; their 0.79 average is not a universal penalty value. The strict threshold applies to non-penalty xG/90 only.

The boundary diagram describes the screening policy in the article. The companion Python fixture demonstrates that boundary on supplied aggregates; it does not authenticate providers or reconcile individual shot events. In the financial illustration, amounts and currency are fixed so that only the effective parent relationship changes the decision. No empirical risk curve is implied.

## Editing and exporting

Edit the three SVG sources, then run `node scripts/render-visuals.mjs` from the article directory. The renderer requires the `sharp` Node package and Nimbus Roman / Nimbus Sans fonts. It also supports the preinstalled ChatGPT Work runtime. PNGs export at twice the SVG dimensions. The cover remains 1,672 × 941 pixels and is not changed by the renderer.

Inspect exports at article and phone widths. Preserve proportional bars, explicit fictional-data labels, the three distinct screening outcomes and the three different times. The Markdown includes descriptive alt text and captions independently of the SVG metadata.

## Cover art direction

Generated with the built-in image-generation tool and exported as a high-quality JPEG for publishing. The direction is a tactile magazine illustration: a forest-green football tactics board, a cut-paper striker in an unbranded ivory-and-cobalt kit, and a vermilion fish-shaped shadow. Scouting sheets carry green checkmarks while an analyst pauses with a pencil. Subtle screenprint grain; no text or real club marks. The red herring is a story metaphor, not a data diagram.

The full generation prompt is retained in `01-hero-prompt.txt`. The three precise figures were drawn as SVGs, not generated as raster illustrations.
