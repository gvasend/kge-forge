# Released supervisor binding

Classification: **PROCESS_INSTANCE_IDENTITY**, at the granularity of the exact
process tuple recorded in the released profile. This is not a qualified
interchangeable supervisor/service identity.

## Evidence chain

1. The live host observation in
   `../pd05_final_evidence/HOST_RECEIPT.json` records PID 57950, PPID 57949,
   UID 1000, `/usr/bin/python -m adapter.supervisor_server /tmp/a21m.sock`,
   executable `/usr/bin/python3.11`, executable SHA-256
   `415cab36dc0bc818be4f6915fd7997103ab10753c878f01d28484a9fcf218b04`,
   cwd `/home/gvasend/app/kge-forge`, and the complete cgroup-membership string.
   The authoritative receipt bytes have SHA-256
   `87b83b45033e830f9d14fd398eb614b76c59d113757a589a19a075e470b0210b`.
2. `../pd05_final_evidence/prepare_evidence.py:38` copies the receipt's
   `supervisor` array into the proposed profile's `supervisor_binding`.
   The PD05 final qualification report identifies this existing process as the
   supervisor used for live governed execution; it was not replaced or restarted.
3. The PD06 execution receipt
   `../pd06_release_evidence/execution/HOST_RECEIPT.json` has SHA-256
   `26a1c404f24888b1d7012c22b35269f2e1d171f5a441992474d817df1ec0e258`.
   Its supervisor tuple, both intervening proposed profiles, and the released
   `../pd06_context_separation/PRODUCTION_PROFILE.json` agree exactly.
4. The unchanged ReleaseBasisId
   `E1-RELEASE-BASIS-sha256:bc176574817f6b7fe06fdcf87a71c57b2a8bfe74e55ed20f2aa55ad5d4fa5181`
   captures both host receipts, qualification report, proposed profiles, and the
   exact released profile. The unchanged ReleaseDecisionId
   `E1-RELEASE-DECISION-sha256:43ab22254604a29f3cf2164152803ee5f689f7540e2006c43d27ded87d83d8c0`
   binds the canonical released-profile fingerprint
   `b9e7f72d97525f39fbddfe92f276ab6aedd057ef6c5b7284dc163f1db9c9c328`.
5. `adapter/activation_transaction.py` selects the sole supervisor tuple from
   that released profile. `_host` reads `/proc/<expected pid>` and compares the
   entire observed tuple with the expected tuple. A different PID, PPID, UID,
   executable path/hash, argv, cwd, or cgroup string fails. Socket ownership,
   mode, cgroup availability and quiescence checks are additional requirements.
   The integrated activation qualification includes this exact comparison in its
   archived production implementation; the authority-store continuation retains
   it unchanged.

The executable hash identifies the Python interpreter, not by itself the loaded
supervisor module. Source/implementation qualification is separately preserved.
The binding contains no boot ID, process start time or pidfd identity. Therefore
the classification describes the released, enforced tuple, not a claim that the
tuple cryptographically distinguishes every possible PID reuse. PID reuse is
not authorization to substitute a new process.

## Reconciliation boundary

The qualified host-prerequisite record reports `/proc/57950/stat` absent from an
observation outside the coding sandbox's PID namespace. This adoption performs
no new host intervention and does not infer host absence from sandbox visibility.

An ordinary host restart with a different PID cannot satisfy the unchanged
released tuple. There is no currently qualified supervisor-rebinding operation
that allows this continuation to substitute a process while preserving its
released-profile invariant. Editing the private profile or ignoring PID/PPID
would invalidate authority; neither is an available reconciliation.

The smallest next host step is a separately authorized, read-only reconciliation
of the recorded process, socket, cgroup and outstanding scopes. If the original
process still exists and only visibility/access is wrong, restore that host
prerequisite without changing the binding. If its death is confirmed, a
replacement requires a narrowly scoped Architect-authorized binding amendment
and qualification, followed by host-authorized startup and fresh readiness
validation. That is a forward authority change, with the current release and
dispatch retained as historical ancestry; the present non-material implementation
continuation cannot authorize it. A restart alone is not the remaining solution.

No replacement process was started, no supervisor field was changed, and no
production activation validation or E1 activation was attempted here.
