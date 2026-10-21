"""Throwaway: run a test file against every mutant of toy/shapes.py."""

import argparse
import ast
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mutate import mutants  # noqa: E402

TIMEOUT = 10
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


def copy_project(src, dst):
    # Skip caches so a stale .pyc can never shadow the mutated source.
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", ".coverage"))


def run_pytest(cwd, test_file):
    # -x: one failing test is enough to kill the mutant.
    cmd = [sys.executable, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", test_file]
    try:
        r = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return "killed (timeout)"
    if r.returncode == 0:
        return "survived"
    if r.returncode == 1:
        return "killed"
    return f"ERROR (pytest exit {r.returncode})"


def line_coverage(toy, test_file, module):
    # Measured in a temp copy so no .coverage file lands in the repo.
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "toy"
        copy_project(toy, work)
        subprocess.run(
            [sys.executable, "-m", "coverage", "run", "--include", module, "-m", "pytest", "-q", "-p", "no:cacheprovider", test_file],
            cwd=work, env=ENV, capture_output=True, text=True, check=True,
        )
        r = subprocess.run(
            [sys.executable, "-m", "coverage", "report", "--include", module],
            cwd=work, env=ENV, capture_output=True, text=True, check=True,
        )
    return r.stdout.strip().splitlines()[-1].split()[-1]  # TOTAL row, last column


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("toy")
    ap.add_argument("--tests", required=True)
    args = ap.parse_args()

    toy = Path(args.toy).resolve()
    test_file = Path(args.tests).name
    module = "shapes.py"
    tree = ast.parse((toy / module).read_text())
    original = ast.unparse(tree).splitlines()

    killed = survived = errors = 0
    print(f"suite: {args.tests}")
    for n, (lineno, t) in enumerate(mutants(tree), 1):
        mutated = ast.unparse(t).splitlines()
        changed = next(m.strip() for o, m in zip(original, mutated) if o != m)
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "toy"
            copy_project(toy, work)
            (work / module).write_text(ast.unparse(t) + "\n")
            outcome = run_pytest(work, test_file)
        killed += outcome.startswith("killed")
        survived += outcome == "survived"
        errors += outcome.startswith("ERROR")
        print(f"  mutant {n:2d} line {lineno:2d}  {changed:55s} {outcome}")

    total = killed + survived + errors
    cov = line_coverage(toy, test_file, module)
    print(f"{total} mutants, {killed} killed, {survived} survived, {errors} errors, "
          f"kill rate {100 * killed / total:.0f}% | line coverage {cov}")


if __name__ == "__main__":
    main()
