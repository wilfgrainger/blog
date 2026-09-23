# Reproduce the fictional shortlist

Use Python 3.10 or later. From the article directory, run:

```sh
python3 example/recruitment.py
python3 -m unittest discover -s example -v
```

The first ranking deliberately uses **total xG/90** and mixes models. McBaggio leads at 0.64, although his supplied 7.27 total xG includes 2.37 from three fictional penalties (an average of 0.79; the fixture contains aggregates, not individual shots). The corrected screen computes `(7.27 - 2.37) * 90 / 1020 = 0.43` npxG/90. Ward is 0.60 and tops the **validated, comparable subset**; McBaggio fails the strict `> 0.55` condition. Kovac's Provider B/v1 evidence is **withheld under this Provider A/v3 policy**, not declared universally incomparable or numerically excluded. Because evidence is withheld, the example makes no best-overall claim. The final run switches every record to Provider B/v1 to illustrate a complete refusal: all three are withheld and there is no ranking.

`players.csv` supplies record IDs, age at the screen date, position, European-region flag, affordable flag, qualifying league minutes, xG components and penalty count, plus provider/model, season, competition scope, denominator, penalty-treatment and metric identifiers. The explicit policy ID is printed with each decision. A record ranks only if the source fields are present and valid, its provenance exactly matches the policy, it passes the supplied pre-screen (age under 23, forward, Europe, affordable, at least 900 league minutes), and its **unrounded Decimal** npxG/90 exceeds 0.55. Failed criteria are reported as excluded; missing, invalid, duplicated or incompatible evidence is withheld.

This is a tiny deterministic illustration, not production scouting or an LLM evaluation. Age, budget, position and region are supplied facts, not independently checked. It assumes xG aggregates and minutes refer to the same qualifying appearances. The code checks internal shape and arithmetic; it does not validate source truth, reconcile shot events, establish audit completeness, or build an event-level graph. No network, LLM, external package or live data is used.
