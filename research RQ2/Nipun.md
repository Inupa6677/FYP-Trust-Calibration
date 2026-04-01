Theme 1: Object / Resource Allocation Issues

Definition: This theme captures problems related to missing, insufficient, or incorrectly allocated objects / resources in the LLM-generated plans.

Codes under this theme:

Missing objects / resources


Object allocation errors


Object count variations


Severe allocation problems


Evidence Table

Analysis:

Barmen domain is highly susceptible to object allocation issues


The LLM struggles with correctly identifying required quantities (shot glasses)


Severity ranges from minor (plan still works) to severe (complete failure)


4 out of 5 Barmen plans exhibited this issue


Only Grippers sample 1 showed this issue outside Barmen, but it was non-critical




Theme 2: Initial State Validity Problems

Definition: This theme encompasses issues where the LLM-generated initial state is corrupted, invalid, or contains pre-existing conditions that should not exist.

Codes under this theme:

Corrupted initial state


Invalid initial state


Pre-existing conditions (pre-made cocktails)


Evidence Table

Analysis:

Exclusive to Barmen domain - suggests domain-specific complexity


LLM incorrectly adds pre-existing cocktails in initial state


This indicates the LLM may not fully understand the "clean slate" requirement


Corrupted initial states directly cause INV (Invariant) failures


Even when MF passes, invalid initial states cause cascading failures



Theme 3: Goal Specification Errors

Definition: This theme captures problems where goals are incorrectly specified, incomplete, or completely mismatched with the intended objectives.

Codes under this theme:

Wrong goal specifications


Incomplete goal definitions


Complete goal mismatch


Goal specification errors


Evidence Table



Analysis:

Appears in 2 domains: Barmen and Floortile


Barmen: Goal errors combined with other issues (catastrophic)


Floortile: Goal errors are the sole cause of failure (INV still passes)



Theme 4: Minor Non-Critical Variations

Definition: This theme captures superficial differences in the LLM output that do not affect functional correctness, including naming conventions, formatting, and minor structural deviations.

Codes under this theme:

Object naming inconsistencies


Structural variations


Formatting differences


Naming convention deviations


Configuration deviations


Evidence Table

Analysis:

100% of plans with this theme passed all metrics


Dominant theme in Blocksworld (5/5 samples) and Grippers (4/5 samples)


Expert consistently uses qualifier words: "minor", "slight", "small", "trivial"


These variations are cosmetic and don't impact plan validity





Theme 5: Successful Well-Structured Generation

Definition: This theme captures instances where the LLM successfully generated well-formed, correctly specified, and properly structured planning problems.

Codes under this theme:

Well-structured problem


Clean implementation


Correct specifications


Proper configuration


Successful execution


Clear execution path


Evidence Table



Analysis:

Storage domain achieved 100% success with all samples exhibiting this theme


Floortile showed this theme in 3 out of 5 samples


Key indicators of success:


"Well-structured" / "Well-defined"


"Clean implementation"


"Properly specified"


"Correct" specifications



6. Key Insights and Findings

6.1 Critical Failure Patterns

Finding 1: The Barmen domain exhibits a unique combination of all three failure themes (Object Allocation + Initial State + Goal Specification), indicating:

Domain-specific complexity that challenges LLM understanding


Cascading failures when multiple issues compound


Finding 2: Goal specification errors appear across domains with different severity:

In Barmen: Combined with other errors → catastrophic (Trust 1)


In Floortile: Isolated error → recoverable (Trust 2)


6.2 Success Patterns

Finding 3: Domains with simpler object relationships (Storage, Blocksworld, Grippers) achieve higher success rates:

Storage: 100% success, purely positive comments


Blocksworld/Grippers: 100% success with only cosmetic variations


Finding 4: The presence of Theme 4 (Minor Variations) is a strong positive indicator - all plans with this theme passed all metrics.







