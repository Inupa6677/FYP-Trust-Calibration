#!/bin/bash
# Helper script to run Fast Downward planner
# Usage: ./run_planner.sh <domain> <task_number> <run_number> <alias>
# Example: ./run_planner.sh barman 01 1 lama-first

DOMAIN=${1:-barman}
TASK=${2:-01}
RUN=${3:-1}
ALIAS=${4:-lama-first}

PLAN_FILE="experiments/run${RUN}/plans/llm_ic_pddl/p${TASK}.plan"
SAS_FILE="experiments/run${RUN}/plans/llm_ic_pddl/p${TASK}.sas"
DOMAIN_FILE="domains/${DOMAIN}/domain.pddl"
PROBLEM_FILE="experiments/run${RUN}/problems/llm_ic_pddl/p${TASK}.pddl"

echo "=================================================="
echo "Running Fast Downward Planner"
echo "=================================================="
echo "Domain:  $DOMAIN"
echo "Task:    p${TASK}"
echo "Run:     run${RUN}"
echo "Alias:   $ALIAS"
echo "=================================================="

python3 downward/fast-downward.py \
    --alias "$ALIAS" \
    --plan-file "$PLAN_FILE" \
    --sas-file "$SAS_FILE" \
    "$DOMAIN_FILE" \
    "$PROBLEM_FILE"

echo "=================================================="
if [ $? -eq 0 ]; then
    echo "✓ Plan generated successfully!"
    echo "Plan file: $PLAN_FILE"
else
    echo "✗ Planning failed!"
fi
echo "=================================================="
