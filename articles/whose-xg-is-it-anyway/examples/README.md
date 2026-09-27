# Replay McBaggio's metric check

Run from this directory with Python 3.9 or later. There are no dependencies or credentials.

```sh
python replay.py
python -m unittest discover -v
```

The fictional fixtures produce:

| Request by the recruitment role | Result |
|---|---|
| Screen McBaggio | Excluded: 15.92 non-penalty xG / 2,684 minutes × 90 = 0.53, below the strict > 0.55 threshold |
| Screen the Provider B-only candidate | Withheld: no approved comparison with Provider A |
| Submit a £25m offer | Denied before the local offer handler runs; zero offer calls |

The tests also cover exactly 0.55, a rate above 0.55 that rounds to 0.55, missing penalty evidence, invalid values, mismatched competition scope, an attempted policy override and an unknown role.

## What this example demonstrates

This is a local executable illustration of two boundaries: the metric service owns its calculation and policy, and the tool dispatcher checks permissions before calling a handler. The printed decision includes the evidence identifier, source/model and policy version. `passes_metric` means only that this metric and minutes check passed; it is not a full recruitment ranking.

`PERMISSIONS` is a Python allowlist, not Cedar or an AgentCore emulator. The role is fixed by the trusted harness. In the proposed AWS deployment, authenticated identity and AgentCore Gateway Policy would supply the tool-access boundary. No AWS deployment or live Policy denial is demonstrated here.

The source data is fictional and stored in `replay.py`; the evidence identifiers refer to those fixtures. The example trusts their stated season, scope and matching minutes. A production service must verify the underlying events and identity joins, enforce age, position, geography and budget criteria, handle duplicates and missing cohort coverage, and select the approved policy effective at server decision time. Here the policy is deliberately fixed to one scenario; there is no temporal policy store.

The in-memory offer handler exists only to make execution observable. It cannot send an offer or spend money.
