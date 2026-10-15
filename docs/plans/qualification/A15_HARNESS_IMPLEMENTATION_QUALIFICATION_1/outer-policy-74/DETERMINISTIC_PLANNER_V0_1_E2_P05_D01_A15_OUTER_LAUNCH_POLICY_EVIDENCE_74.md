# A15 outer-launch policy evidence assessment — Package 74

`PACKAGE_RESULT = PARTIAL` · `SAME_HOST_COMPATIBILITY = UNDETERMINED`

The bounded read-only review is complete. The immediate current launcher and supplied policy profile are identified. The actual policy owner's designation, the rejecting socket rule and an authorised compatible same-host context are not established. No socket/confinement attempt or test was repeated, no configuration/source changed, and no campaign resumed.

The current process chain ends at PID1 running the packaged Codex executable in `/home/gvasend/.codex/packages/app-server-daemon/releases/0.162.0-x86_64-unknown-linux-musl/bin/codex`. Its command entrypoint is `codex-linux-sandbox`. The relevant prefix explicitly supplies the repository cwd, a `managed` permission profile with `network: restricted`, restricted filesystem access, and `--apply-seccomp-then-exec`. Executable bytes are pinned in [outer-launch-context.json](outer-launch-context.json). The shell command body, environment and credentials were deliberately not copied.

Current process metadata shows inherited `Seccomp: 2`, `NoNewPrivs: 1`, and no effective/bounding capabilities throughout the visible chain. This establishes an active outer enforcement layer. It makes the Codex network/seccomp path a concrete hypothesis for Package72's route-netlink EPERM; it does **not** expose the installed BPF decision for AF_NETLINK16/type0x80003/protocol0 or prove that this rule rejected the historical child. Package72 did not capture that child's outer argv/filter assignment, host PID mapping or a matching audit decision. These current observations must not be substituted for missing historical evidence.

[Configuration observations](launch-configuration-observations.json) inspected only allowlisted policy keys, not credentials. The readable user config supplies no selected policy setting establishing a different permitted context. `/etc/codex/requirements.toml`, `/etc/codex/managed_config.toml` and the inspected user requirements path are absent in the current view. Their absence does not rule out service-supplied or other managed policy. The launcher argv is the concrete current profile evidence.

[Denial-log assessment](existing-denial-log-assessment.json) found no matching usable audit record: the inspected Codex log directories and audit log are absent; the readable kernel log has no relevant entry; loaded AppArmor profiles cannot actually be read despite an access check. No privileged trace/filter dump, inaccessible-directory traversal or restriction bypass was attempted. Lack of a log does not support compatibility.

The visible implementation/provider is Codex. The responsible evidence handoff is to the **administrator/operator supplying this app-server's managed permission profile and Linux sandbox security policy**. That is a control-plane role, not an authenticated named person or organisation. Installation pathname, UID1000, config-file ownership and the project's qualification charter do not designate that policy owner or confer power to alter it. An actual owner assignment remains missing; if the Codex operator identifies a host/LSM/container layer as the rejecting policy, its authorised owner must be identified in the same handoff.

Official [OpenAI configuration documentation](https://learn.chatgpt.com/docs/config-file/config-reference) describes admin-enforced/managed requirements and policy precedence. That explains why a user config alone is not authoritative permission evidence. The documentation is general product context, not an attestation of this installed0.162.0 binary or the failed syscall. The OpenAI Docs skill was used for this Codex-specific review; no API credentials or external application actions were used.

The [missing-evidence register](missing-policy-evidence.json) identifies four precise gaps: effective filter/rule action for the socket arguments; original managed-profile source/owner assignment; correlated denial audit or authoritative rule explanation; and an exact approved context preserving the confinement contract. Each is assigned to the applicable Codex/control-plane or host-security owner role. No individual owner or permission value is invented.

The current failed context is not supported as compatible. Same-host compatibility as a whole remains **UNDETERMINED**: a different authorised same-host launch context is neither evidenced nor ruled out. A dedicated compatible Linux host/VM remains the unqualified candidate described by Package73's minimum profile; none was provisioned, migrated to or tested. No alternative mechanism is selected or automatically substituted.

**Single recommended next action:** ask the administrator/operator of the Codex app-server managed launch profile for one authoritative, credential-free policy/denial evidence bundle naming the actual policy owner, explaining the Package72 route-netlink socket decision, and identifying any approved same-host qualification context. This is an evidence request only—no probe, setting change or campaign approval is implied. No message was sent on the user's behalf.

The original grant, Package72/73 seals, six source files and stopped journal remain byte-identical. The original campaign cannot resume automatically. Future execution requires separate explicit approval and exact current grant/journal binding; the fixed original grant token and stopped journal issues documented in Package73 remain. Package75 was not initiated. The report is inside the authorised evidence directory, and `git diff --check = PASS`.

```text
WORK_PACKAGE = E2-P05-D01-A15-OUTER-LAUNCH-POLICY-EVIDENCE-74
PACKAGE_RESULT = PARTIAL
BOUNDED_REVIEW_COMPLETE = YES
SAME_HOST_COMPATIBILITY = UNDETERMINED
CURRENT_LAUNCH_LAYER_IDENTIFIED = YES: packaged Codex linux-sandbox with managed network=restricted profile
SECURITY_POLICY_OWNER_IDENTIFIED = ROLE/CONTROL_PLANE_LOCUS ONLY; actual authorised individual/organization not evidenced
DENYING_SOCKET_RULE_ESTABLISHED = NO
PERMITTED_SAME_HOST_CONTEXT_ESTABLISHED = NO
DEDICATED_HOST_VM = UNQUALIFIED CANDIDATE; not provisioned or tested
SINGLE_RECOMMENDED_NEXT_ACTION = Ask the administrator/operator of the Codex app-server managed launch profile for one authoritative, credential-free policy/denial evidence bundle identifying the actual policy owner, the decision for the Package72 route-netlink socket call, and any approved same-host qualification context. No probe or configuration change.
FUTURE_CAMPAIGN_AUTHORITY = Separate explicit approval plus exact grant/journal binding required
ADAPTER_SOURCE_FILES_MODIFIED = 0
SOCKET_RETRIES = 0
CONFINEMENT_TESTS_EXECUTED = 0
FAKE_PROTOCOL_TESTS_EXECUTED = 0
NATIVE_SYNTHETIC_TESTS_EXECUTED = 0
A15_EXECUTED = NO
CAMPAIGN_RESUMED = NO
SECURITY_SETTINGS_CHANGED = NO
PACKAGE75_INITIATED = NO
TOTAL_REFERENCES = 161
TOTAL_RESOLVED = 109
TOTAL_UNRESOLVED = 52
PRODUCTION_EFFECT = NO
GIT_DIFF_CHECK = PASS
```
