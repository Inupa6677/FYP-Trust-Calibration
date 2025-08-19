import argparse
import glob
import subprocess
from pathlib import Path

from main import (
    DOMAINS,
    Barman, Blocksworld, Floortile, Grippers, Storage, Termes, Tyreworld, Manipulation
)

DOMAIN_MAP = {
    "barman": Barman,
    "blocksworld": Blocksworld,
    "floortile": Floortile,
    "grippers": Grippers,
    "storage": Storage,
    "termes": Termes,
    "tyreworld": Tyreworld,
    "manipulation": Manipulation,
}

def main():
    parser = argparse.ArgumentParser(description="LLM+P: plan validator")
    parser.add_argument('--domain', type=str, choices=DOMAINS, default="tyreworld")
    parser.add_argument('--run', type=str, default="run1")
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    # Domain instance and domain file
    domain_cls = DOMAIN_MAP[args.domain]
    domain = domain_cls()
    domain_pddl_file = domain.get_domain_pddl_file()
    if args.domain == "tyreworld":
        domain_pddl_file = domain_pddl_file.split('.pddl')[0] + "_validation.pddl"

    # Build the set of valid task IDs (e.g., {"p01", "p02", ...})
    task_ids = set()
    for t in range(len(domain)):
        suffix = domain.get_task_suffix(t)  # may be like "llm_ic_pddl/p01.pddl"
        task_ids.add(Path(suffix).stem)     # -> "p01"

    # Output file
    outdir = Path(f"experiments/{args.run}/plans/{args.domain}")
    outdir.mkdir(parents=True, exist_ok=True)
    output_path = outdir / "validation.txt"

    attempts = 0
    valids = 0
    logs = []

    # Find all .plan files in this run
    all_plans = list(Path(f"experiments/{args.run}/plans").rglob("*.plan"))
    if args.verbose:
        print(f"[DEBUG] Found {len(all_plans)} .plan file(s) in experiments/{args.run}/plans")

    # Filter to only those whose basename (stem) matches a known task id (p01, p02, ...)
    plan_files = [p for p in all_plans if p.stem in task_ids]
    if args.verbose:
        names = ", ".join(sorted(p.stem for p in plan_files))
        print(f"[DEBUG] Matching plans by task id ({len(plan_files)}): {names or 'none'}")

    for plan in plan_files:
        # Map to generated problem:
        # experiments/<run>/plans/.../pXX.plan -> experiments/<run>/problems/.../pXX.pddl
        problem = str(plan).replace(f"experiments/{args.run}/plans", f"experiments/{args.run}/problems")
        problem = str(Path(problem).with_suffix(".pddl"))

        if not Path(problem).is_file():
            msg = f"[SKIP] Problem file missing for plan:\n  plan:    {plan}\n  problem: {problem}\n"
            logs.append(msg)
            if args.verbose:
                print(msg, end="")
            continue

        cmd = ["./downward/validate", domain_pddl_file, problem, str(plan)]
        if args.verbose:
            print("[CMD]", " ".join(cmd))
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        out = res.stdout

        attempts += 1
        logs.append(f"$ {' '.join(cmd)}\n{out}\n")

        if "Plan valid" in out:
            valids += 1

    output_path.write_text("".join(logs), encoding="utf-8")
    print(f"{valids} plans are valid (out of {attempts} attempts)")
    print(f"Log written to: {output_path}")

if __name__ == "__main__":
    main()
