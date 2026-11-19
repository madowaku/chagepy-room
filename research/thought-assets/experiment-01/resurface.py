"""Thought Asset Lab: condition-based revival candidate detector.

No LLM or third-party dependencies. A match means RETEST, not acceptance.
"""
import argparse
import json
from pathlib import Path

CARDS = Path(__file__).with_name("revival_cards.json")


def satisfied(condition, scenario):
    field = condition["field"]
    if field not in scenario:  # Unknown is not proof that a premise changed.
        return False
    actual, expected = scenario[field], condition["value"]
    op = condition["op"]
    if op == "==":
        return type(actual) is type(expected) and actual == expected
    if op == ">":
        return (type(actual) in (int, float) and type(expected) in (int, float)
                and actual > expected)
    raise ValueError(f"Unsupported operator: {op}")


def resurface(cards, scenario):
    result = []
    for card in cards:
        matched = [rule for rule in card["revisit_if_any"]
                   if satisfied(rule, scenario)]
        if matched:
            result.append({"id": card["id"], "name": card["name"],
                           "matched_conditions": matched,
                           "action": card["next_test"],
                           "decision": "再検証候補（採用の証拠ではない）"})
    return result


def self_test(cards):
    assert resurface(cards, {"board_width": 3, "has_fixed_walls": False,
                             "placeable_blocker": False}) == []
    assert [c["id"] for c in resurface(cards, {"board_width": 4})] == ["REV-001"]
    assert [c["id"] for c in resurface(cards, {"placeable_blocker": True})] == ["REV-002"]
    assert len(resurface(cards, {"board_width": 4,
                                  "placeable_blocker": True})) == 2
    assert resurface(cards, {}) == []
    assert not satisfied({"field": "placeable_blocker", "op": "==", "value": True},
                         {"placeable_blocker": 1})  # Bool/int must not be conflated.


def main():
    parser = argparse.ArgumentParser(description="Surface old ideas when their rejection premises change")
    parser.add_argument("--scenario", help="JSON object: e.g. '{\"board_width\":4}'")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    cards = json.loads(CARDS.read_text(encoding="utf-8"))
    if args.self_test:
        self_test(cards)
        print("PASS: six deterministic test cases")
    if args.scenario:
        scenario = json.loads(args.scenario)
        if not isinstance(scenario, dict):
            parser.error("scenario must be a JSON object")
        print(json.dumps(resurface(cards, scenario), indent=2, ensure_ascii=False))
    elif not args.self_test:
        parser.print_help()


if __name__ == "__main__":
    main()
