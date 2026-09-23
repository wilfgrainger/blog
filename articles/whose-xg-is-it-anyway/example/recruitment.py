"""Local fictional evidence: a metric mistake, then a fail-closed screen."""

import csv
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path


POLICY_ID = "u23_europe_forward_npxg90_2025_26_v1"
METRIC_ID = "xg_components_v1"
SCOPE = "fictional_league"
SEASON = "2025-26"
APPROVED = {
    "provider": "Provider A",
    "model": "v3",
    "season": SEASON,
    "competition_scope": SCOPE,
    "denominator": "qualifying_league_minutes",
    "penalty_treatment": "subtract_reported_penalty_xg",
    "metric_id": METRIC_ID,
}
REQUIRED = (
    "record_id", "name", "age", "position", "region", "affordable",
    "league_minutes", "total_xg", "penalty_xg", "penalty_count", *APPROVED,
)
THRESHOLD = Decimal("0.55")


@dataclass(frozen=True)
class Decision:
    record_id: str
    name: str
    score: Decimal | None
    reason: str
    evidence: dict[str, str]


@dataclass(frozen=True)
class ScreenResult:
    ranked: tuple[Decision, ...]
    excluded: tuple[Decision, ...]
    withheld: tuple[Decision, ...]

    @property
    def complete_cohort(self):
        return not self.withheld


def read_records(path):
    """Read supplied CSV facts; this does not authenticate the source."""
    with open(path, newline="", encoding="utf-8") as data:
        return list(csv.DictReader(data))


def _decision(record, score=None, reason=""):
    keys = ("record_id", *APPROVED)
    evidence = {key: record.get(key, "") or "?" for key in keys}
    evidence["policy_id"] = POLICY_ID
    return Decision(record.get("record_id", "?") or "?", record.get("name", "?") or "?",
                    score, reason, evidence)


def _quantities(record):
    try:
        age = int(record["age"])
        minutes = int(record["league_minutes"])
        count = int(record["penalty_count"])
        total = Decimal(record["total_xg"])
        penalties = Decimal(record["penalty_xg"])
    except (ValueError, InvalidOperation, TypeError, KeyError) as exc:
        raise ValueError("malformed age, minutes, xG or penalty count") from exc
    if not total.is_finite() or not penalties.is_finite() or age < 0 or minutes <= 0 or count < 0:
        raise ValueError("non-finite or negative values, or non-positive minutes")
    if penalties < 0 or penalties > total:
        raise ValueError("penalty xG must be between zero and total xG")
    if (count == 0 and penalties != 0) or (count > 0 and penalties == 0):
        raise ValueError("penalty count contradicts reported penalty xG")
    if record["affordable"] not in ("true", "false"):
        raise ValueError("affordable must be true or false")
    return age, minutes, total, penalties


def flawed_shortlist(records):
    """Intentional bug: rank pre-screened players on TOTAL xG and mix models."""
    candidates = []
    for record in records:
        age, minutes, total, _ = _quantities(record)
        if (age < 23 and minutes >= 900 and record["position"] == "forward"
                and record["region"] == "Europe" and record["affordable"] == "true"):
            wrong_score = total * 90 / minutes
            if wrong_score > THRESHOLD:
                candidates.append(_decision(record, wrong_score,
                                            "total xG includes penalties; provenance ignored"))
    return tuple(sorted(candidates, key=lambda item: (-item.score, item.record_id)))


def screen(records):
    """Rank only comparable evidence; distinguish failed filters from withheld data."""
    ranked, excluded, withheld = [], [], []
    counts = Counter(record.get("record_id") for record in records)
    for record in records:
        missing = [key for key in REQUIRED if not (record.get(key) or "").strip()]
        if missing:
            withheld.append(_decision(record, reason="missing evidence: " + ", ".join(missing)))
            continue
        if counts[record["record_id"]] > 1:
            withheld.append(_decision(record, reason="duplicate record_id"))
            continue
        mismatch = [key for key, value in APPROVED.items() if record[key] != value]
        if mismatch:
            withheld.append(_decision(record, reason="incompatible evidence: " + ", ".join(mismatch)))
            continue
        try:
            age, minutes, total, penalties = _quantities(record)
        except ValueError as exc:
            withheld.append(_decision(record, reason="invalid evidence: " + str(exc)))
            continue
        failed = []
        if age >= 23:
            failed.append("age must be under 23")
        if record["position"] != "forward":
            failed.append("position must be forward")
        if record["region"] != "Europe":
            failed.append("region must be Europe")
        if record["affordable"] != "true":
            failed.append("supplied affordable flag must be true")
        if minutes < 900:
            failed.append("qualifying league minutes must be at least 900")
        if failed:
            excluded.append(_decision(record, reason="fails supplied pre-screen: " + "; ".join(failed)))
            continue
        score = (total - penalties) * 90 / minutes
        if score > THRESHOLD:
            ranked.append(_decision(record, score, "meets strict npxG/90 threshold"))
        else:
            excluded.append(_decision(record, score, "npxG/90 does not exceed 0.55"))
    ranked.sort(key=lambda item: (-item.score, item.record_id))
    return ScreenResult(tuple(ranked), tuple(excluded), tuple(withheld))


def _show(decision, show_evidence=True):
    score = f" {decision.score:.2f}" if decision.score is not None else ""
    fields = decision.evidence if show_evidence else {"record_id": decision.record_id}
    provenance = " ".join(f"{key}={value}" for key, value in fields.items())
    print(f"  {decision.name}{score} | {decision.reason} | {provenance}")


def main():
    records = read_records(Path(__file__).with_name("players.csv"))
    print("Flawed total xG/90 shortlist (intentionally ignores penalties and model compatibility)")
    for decision in flawed_shortlist(records):
        _show(decision, show_evidence=False)
    result = screen(records)
    print("Corrected npxG/90 ranked subset (approved comparable evidence only)")
    for decision in result.ranked:
        _show(decision)
    print("Excluded on supplied criteria")
    for decision in result.excluded:
        _show(decision)
    print("Withheld under this policy (neither ranked nor numerically excluded)")
    for decision in result.withheld:
        _show(decision)
    if not result.complete_cohort:
        print("Incomplete cohort: no best-overall claim.")

    print("Full-cohort failure (illustration: every provider/model changed to Provider B/v1)")
    all_b = [{**record, "provider": "Provider B", "model": "v1"} for record in records]
    failure = screen(all_b)
    if not failure.ranked:
        print("No ranking: no approved comparable evidence under this policy.")
    print("Withheld under this policy")
    for decision in failure.withheld:
        _show(decision)


if __name__ == "__main__":
    main()
