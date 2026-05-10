"""
Mutation Testing for Plan Your Study — Auth & Course modules
Manually injects mutations and runs the unit/integration tests to measure
how many mutants the test suite catches (kills).

Tested modules:
  1. backend/routers/auth.py        — Authentication logic
  2. backend/routers/courses.py     — Course CRUD
  3. backend/routers/assignments.py — Assignment CRUD

Mutation types applied:
  A. Logical operator change  (== → !=, >= → >, etc.)
  B. Return value modification (True → False, status codes)
  C. Constant alteration      (expire timedelta, HTTP status)
  D. Condition removal        (if x: → if True:)
  E. Arithmetic change        (+ → -)
"""

import subprocess
import shutil
import os
import sys
import json
import re
import time
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Test command to run against each mutant
TEST_CMD = [
    sys.executable, "-m", "pytest",
    "tests/unit/",
    "tests/integration/",
    "-x",           # stop on first failure (fast kill detection)
    "-q",
    "--tb=no",
    "--no-header",
]


@dataclass
class Mutant:
    id: int
    module: str
    description: str
    mutation_type: str
    original_code: str
    mutated_code: str
    status: str = "pending"   # pending | killed | survived | error
    test_output: str = ""


MUTANTS: List[Mutant] = [
    # ───────── auth.py mutations ─────────
    Mutant(
        id=1,
        module="backend/routers/auth.py",
        description="verify_password: return False instead of True for valid match",
        mutation_type="Return value modification",
        original_code="    return pwd_context.verify(plain_password, hashed_password)",
        mutated_code="    return not pwd_context.verify(plain_password, hashed_password)",
    ),
    Mutant(
        id=2,
        module="backend/routers/auth.py",
        description="create_access_token: use subtraction instead of addition for expire",
        mutation_type="Arithmetic change",
        original_code="        expire = datetime.utcnow() + expires_delta",
        mutated_code="        expire = datetime.utcnow() - expires_delta",
    ),
    Mutant(
        id=3,
        module="backend/routers/auth.py",
        description="get_current_user: skip email None check (always proceed)",
        mutation_type="Condition removal",
        original_code="        if email is None:\n            raise credentials_exception",
        mutated_code="        if False:\n            raise credentials_exception",
    ),
    Mutant(
        id=4,
        module="backend/routers/auth.py",
        description="register: change duplicate check operator == to !=",
        mutation_type="Logical operator change",
        original_code="    existing_user = db.query(User).filter(\n        (User.email == user_data.email) | (User.username == user_data.username)\n    ).first()",
        mutated_code="    existing_user = db.query(User).filter(\n        (User.email != user_data.email) | (User.username != user_data.username)\n    ).first()",
    ),
    Mutant(
        id=5,
        module="backend/routers/auth.py",
        description="get_current_user: change email payload key 'sub' to 'usr'",
        mutation_type="Constant alteration",
        original_code='        email: str = payload.get("sub")',
        mutated_code='        email: str = payload.get("usr")',
    ),

    # ───────── courses.py mutations ─────────
    Mutant(
        id=6,
        module="backend/routers/courses.py",
        description="create_course: return 200 instead of 201 status code",
        mutation_type="Constant alteration",
        original_code="@router.post(\"/\", response_model=CourseSchema, status_code=status.HTTP_201_CREATED)",
        mutated_code="@router.post(\"/\", response_model=CourseSchema, status_code=status.HTTP_200_OK)",
    ),
    Mutant(
        id=7,
        module="backend/routers/courses.py",
        description="get_course: change == to != in user ownership filter",
        mutation_type="Logical operator change",
        original_code="        (Course.id == course_id) & (Course.user_id == current_user.id)",
        mutated_code="        (Course.id == course_id) & (Course.user_id != current_user.id)",
    ),
    Mutant(
        id=8,
        module="backend/routers/courses.py",
        description="get_courses: remove user_id filter (return all users' courses)",
        mutation_type="Condition removal",
        original_code="    courses = db.query(Course).filter(Course.user_id == current_user.id).all()",
        mutated_code="    courses = db.query(Course).all()",
    ),

    # ───────── assignments.py mutations ─────────
    Mutant(
        id=9,
        module="backend/routers/assignments.py",
        description="get_assignment: change == to != in ownership filter",
        mutation_type="Logical operator change",
        original_code="        (Assignment.id == assignment_id) & (Assignment.user_id == current_user.id)",
        mutated_code="        (Assignment.id == assignment_id) & (Assignment.user_id != current_user.id)",
    ),
    Mutant(
        id=10,
        module="backend/routers/assignments.py",
        description="create_assignment: assign wrong user_id (0 instead of current_user.id)",
        mutation_type="Constant alteration",
        original_code="        user_id=current_user.id,",
        mutated_code="        user_id=0,",
    ),
]


def apply_mutation(mutant: Mutant) -> bool:
    """Apply mutation by replacing original_code with mutated_code in module."""
    target = PROJECT_ROOT / mutant.module
    content = target.read_text()
    if mutant.original_code not in content:
        print(f"  WARNING: original code not found in {mutant.module}")
        return False
    new_content = content.replace(mutant.original_code, mutant.mutated_code, 1)
    target.write_text(new_content)
    return True


def revert_mutation(mutant: Mutant):
    """Revert mutation back to original code."""
    target = PROJECT_ROOT / mutant.module
    content = target.read_text()
    new_content = content.replace(mutant.mutated_code, mutant.original_code, 1)
    target.write_text(new_content)


def run_tests() -> tuple[bool, str]:
    """Run test suite. Returns (killed, output)."""
    result = subprocess.run(
        TEST_CMD,
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        timeout=120,
    )
    output = result.stdout + result.stderr
    killed = result.returncode != 0
    return killed, output


def module_short(module: str) -> str:
    return Path(module).stem


def print_summary(mutants: List[Mutant]):
    """Print mutation score table by module."""
    from collections import defaultdict
    by_module = defaultdict(list)
    for m in mutants:
        by_module[module_short(m.module)].append(m)

    print("\n\n" + "="*70)
    print("MUTATION TESTING RESULTS")
    print("="*70)
    print(f"\n{'Module':<22} {'Type':<30} {'Created':>8} {'Killed':>8} {'Survived':>9} {'Score':>8}")
    print("-"*80)

    total_created = total_killed = 0
    for module, module_mutants in by_module.items():
        by_type = defaultdict(list)
        for m in module_mutants:
            by_type[m.mutation_type].append(m)
        for mtype, group in by_type.items():
            created = len(group)
            killed = sum(1 for m in group if m.status == "killed")
            survived = created - killed
            score = killed / created * 100 if created > 0 else 0
            total_created += created
            total_killed += killed
            print(f"  {module:<20} {mtype:<30} {created:>8} {killed:>8} {survived:>9} {score:>7.1f}%")

    total_survived = total_created - total_killed
    total_score = total_killed / total_created * 100 if total_created > 0 else 0
    print("-"*80)
    print(f"  {'OVERALL':<50} {total_created:>8} {total_killed:>8} {total_survived:>9} {total_score:>7.1f}%")


def main():
    print("Plan Your Study — Mutation Testing")
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"\nRunning baseline tests first...")

    # Baseline: ensure tests pass before any mutation
    killed, output = run_tests()
    if killed:
        print("ERROR: Baseline test suite already failing. Fix tests before mutation testing.")
        print(output[-2000:])
        sys.exit(1)
    print("  Baseline: PASS ✓\n")

    results = []
    for mutant in MUTANTS:
        print(f"[Mutant #{mutant.id:02d}] {module_short(mutant.module)}: {mutant.description}")

        applied = apply_mutation(mutant)
        if not applied:
            mutant.status = "error"
            mutant.test_output = "Could not apply mutation (code not found)"
            print(f"  → ERROR (code not found)")
            results.append(asdict(mutant))
            continue

        try:
            killed, test_out = run_tests()
            mutant.status = "killed" if killed else "survived"
            mutant.test_output = test_out[-500:]  # keep last 500 chars
            icon = "✓ KILLED" if killed else "✗ SURVIVED"
            print(f"  → {icon}")
        except subprocess.TimeoutExpired:
            mutant.status = "error"
            mutant.test_output = "Timeout"
            print(f"  → TIMEOUT")
        finally:
            revert_mutation(mutant)

        results.append(asdict(mutant))

    # Save results
    out_path = RESULTS_DIR / "mutation_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results saved to: {out_path}")

    print_summary(MUTANTS)

    # Print surviving mutants analysis
    survived = [m for m in MUTANTS if m.status == "survived"]
    if survived:
        print(f"\n\nSURVIVING MUTANTS ANALYSIS (gaps in test coverage):")
        print("-"*70)
        for m in survived:
            print(f"  #{m.id:02d} [{module_short(m.module)}] {m.description}")
            print(f"       Mutation type: {m.mutation_type}")
            print(f"       Recommendation: Add assertions checking {m.mutation_type.lower()} behavior")
            print()

    killed_count = sum(1 for m in MUTANTS if m.status == "killed")
    score = killed_count / len(MUTANTS) * 100 if MUTANTS else 0
    print(f"\nFinal Mutation Score: {score:.1f}%  ({killed_count}/{len(MUTANTS)} mutants killed)")


if __name__ == "__main__":
    main()
