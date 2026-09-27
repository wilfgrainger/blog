"""Local metric/permission replay. No AWS calls, authentication or real offers."""

import json
from decimal import Decimal, InvalidOperation

# Trusted service configuration, fixed to the current policy for this fixture.
POLICY = {"version": "recruitment-v1", "source": "A/v3.4",
          "season": "2025/26", "scope": "domestic_league",
          "minimum_minutes": 2000, "threshold": Decimal("0.55")}
MCBAGGIO = dict(player_id="mcbaggio-21", source="A/v3.4",
               season="2025/26", scope="domestic_league",
               evidence="season-2025-26-mcbaggio",
               minutes=2684, total_xg="19.08", penalty_xg="3.16")
FIXTURES = {"mcbaggio-21": MCBAGGIO,
            "provider-b-only": MCBAGGIO | {"player_id": "provider-b-only",
                "source": "B/v1", "evidence": "season-2025-26-provider-b"}}
PERMISSIONS = {"recruitment": {"screen_recruits"}}
OFFERS = []  # Local in-memory sink only; there is no external transaction.


def screen_record(record):
    result = {"player_id": record.get("player_id"), "policy": POLICY["version"],
              "source": record.get("source"), "evidence": record.get("evidence"),
              "status": "withheld"}
    if record.get("source") != POLICY["source"]:
        return result | {"reason": "no approved provider comparison"}
    if any(record.get(key) != POLICY[key] for key in ("season", "scope")):
        return result | {"reason": "incompatible season or competition scope"}
    try:
        total, penalty, minutes = (Decimal(str(record[key]))
                                   for key in ("total_xg", "penalty_xg", "minutes"))
        if (not all(x.is_finite() for x in (total, penalty, minutes))
                or not 0 <= penalty <= total or minutes <= 0
                or not record.get("evidence")):
            raise ValueError("invalid evidence")
    except (KeyError, InvalidOperation, ValueError):
        return result | {"reason": "missing or invalid evidence"}
    npxg = total - penalty
    rate = npxg / minutes * 90
    passed = minutes >= POLICY["minimum_minutes"] and rate > POLICY["threshold"]
    return result | {"status": "passes_metric" if passed else "excluded",
                     "total_xg": str(total), "penalty_xg": str(penalty),
                     "eligible_minutes": str(minutes), "npxg": str(npxg),
                     "npxg_per_90": f"{rate:.2f}",
                     "reason": "metric and minutes pass" if passed else
                         "requires at least 2000 minutes and NPxG/90 > 0.55"}


def screen_recruits(player_id):
    record = FIXTURES.get(player_id)
    if record is None:
        return {"status": "withheld", "reason": "unknown player"}
    return screen_record(record)


def submit_offer(**offer):
    OFFERS.append(offer)
    return {"status": "recorded_locally"}


def invoke(role, tool, arguments):
    # 'role' is supplied by this trusted harness, never by the agent's arguments.
    if tool not in PERMISSIONS.get(role, set()):
        return {"status": "denied", "reason": f"{role} role lacks permission"}
    if tool == "screen_recruits" and set(arguments) != {"player_id"}:
        return {"status": "rejected_request", "reason": "only player_id is accepted"}
    handlers = {"screen_recruits": screen_recruits, "submit_offer": submit_offer}
    return handlers[tool](**arguments)


if __name__ == "__main__":
    for tool, arguments in [
        ("screen_recruits", {"player_id": "mcbaggio-21"}),
        ("screen_recruits", {"player_id": "provider-b-only"}),
        ("submit_offer", {"player_id": "mcbaggio-21", "GBP": 25000000}),
    ]:
        print(json.dumps({"tool": tool, "result": invoke("recruitment", tool, arguments)}, indent=2))
    print(f"Offer function calls: {len(OFFERS)}")
