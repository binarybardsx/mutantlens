"""Throwaway: one command. Score each suite, then show every surviving mutant."""

import argparse
import difflib
from pathlib import Path

from run import evaluate, line_coverage


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("toy")
    ap.add_argument("--tests", action="append", required=True)
    args = ap.parse_args()

    toy = Path(args.toy).resolve()
    for tests in args.tests:
        test_file = Path(tests).name
        original, results = evaluate(toy, test_file)
        killed = sum(r["outcome"].startswith("killed") for r in results)
        survivors = [r for r in results if r["outcome"] == "survived"]
        total = len(results)
        cov = line_coverage(toy, test_file, "shapes.py")
        print(f"== {tests}")
        print(f"{total} mutants, {killed} killed, {len(survivors)} survived, "
              f"score {100 * killed / total:.0f}% | line coverage {cov}")
        for r in survivors:
            print()
            print("\n".join(difflib.unified_diff(
                original, r["mutated"], "original", f"mutant {r['n']} (line {r['line']})",
                lineterm="", n=0,
            )))
        print()


if __name__ == "__main__":
    main()
