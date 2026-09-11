# Demonstration service — Human vision

Source: Forge baseline E1-ARCH-1, commit `411cb5a9fabc71e482a414ed58387de0ff557e93`.
Local source repository: `/home/gvasend/app/kge-forge`.
The original human answers and frozen source remain retrievable at that commit.

The following is the human-provided Experiment 1 selection, preserved verbatim.
Later service clarifications are reflected in REQUIREMENTS.md and remain recorded
in the Forge elicitation source.

The first KGE Forge experiment should engineer a new, non-trivial software system from a human-provided vision rather than extend an existing complex system.

The demonstration system should be a resilient task-execution service. At a conceptual level, the system accepts units of work, executes them, records their progress and results, handles failures according to defined policy, and can recover from interruption without losing the ability to determine the authoritative state of submitted work.

The purpose of selecting this problem is not the task-execution capability itself. It is to provide a compact but architecturally meaningful engineering problem involving state, lifecycle, authority, persistence, failure handling, recovery, observable behavior, and verification.

The initial human description should intentionally avoid prescribing implementation technologies or detailed architecture. Those decisions should be derived through the KGE Forge architecture process.

The final deliverable should be a complete software repository containing:

* A working implementation of the system.
* The authoritative engineering knowledge developed during the project.
* Automated tests and other evidence sufficient to demonstrate conformance with the derived requirements and acceptance criteria.
* Traceability sufficient to understand how major architectural decisions relate to the original vision and implementation.
* A final Architect assessment explaining whether the engineered system satisfies the original human intent and identifying any material unresolved uncertainty.

The experiment ends when the Architect determines that the derived acceptance criteria have been satisfied with adequate evidence and presents the result for human acceptance.

Deployment into a production environment, large-scale performance, distributed multi-host execution, and production operational support are not required unless the architecture process determines that some limited form is necessary to demonstrate the stated system behavior.

The human should judge the final result primarily by whether the resulting system behaves as intended and whether Forge reached that result without requiring the human to continuously engineer the solution.
