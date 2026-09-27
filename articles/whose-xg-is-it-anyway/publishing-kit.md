# Publishing kit — Whose xG Is It Anyway?

## Substack title
Whose xG Is It Anyway?

## Subtitle
Five green ticks. One player on the wrong shortlist.

## Preview / social description
A fictional striker looks like a find at 0.64 xG per 90. Mark asks whether the agent removed four penalties. It didn't, and the non-penalty rate is 0.53—below the club's 0.55 cut-off. The arithmetic worked. The feedback around the decision didn't. What would it take to build a screen that can show its evidence, admit when players cannot be compared, and stop before an unauthorised offer?

## Hero
https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/01-hero.png

## Image sequence
1. Hero — below the title/subtitle.
2. Five green ticks — after “Why everything looked green”.
3. McBaggio calculation — after the excluded/withheld distinction.
4. Authority / ambiguity — after “How much can the agent assume?”

## Pull quotes
> The agent hasn't made up a player or invented a number. That is what makes the mistake easy to miss.

> A shared definition that nobody can challenge will become another green tick.

> The greater the authority to act, the less room there is to guess.

## Suggested tags
AI agents · Football analytics · Systems thinking · Data architecture · Financial services

## Publish check
- The player, club, season dossier and investment mandate are fictional. Keep that clear in promotion.
- Run `python3 scripts/build-substack.py` from this directory to rebuild `substack.md`, then run it with `--check` to verify. Set the title and subtitle in Substack's own fields.
- Keep four images and their alt text. The PNGs sit beside the editable SVGs. Check readability on mobile and upload the PNGs in the editor if pasted Markdown leaves links instead of images.
- The generated image and replay links target `main`; merge the reviewed PR before publishing those links.
- The local replay is a demonstration of the metric and permission boundary, not a live AgentCore deployment.
- Leave the final watchlist decision and last sentence as the ending. No added call to action.
