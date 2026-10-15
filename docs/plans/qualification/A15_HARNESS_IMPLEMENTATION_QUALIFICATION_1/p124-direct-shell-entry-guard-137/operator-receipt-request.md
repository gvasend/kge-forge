# Package 137 — read-only operator receipt request

Not an execution or host-inspection grant. Use only your independently permitted metadata access in the nominated interactive Bash on ubuntu01. Do not run the Package135 recipe, create the capture root, write a guard/claim, apply limits or run bwrap/findmnt.

First provide the birth-bound shell receipt below. Stop if caller PID is not3235408, the boot/start tuple differs, the executable differs, or a required read fails. Do not substitute another shell.

```bash
printf 'caller_pid=%s\n' "$$"
/bin/cat /proc/sys/kernel/hostname /proc/sys/kernel/random/boot_id /proc/3235408/stat /proc/3235408/status /proc/3235408/limits /proc/3235408/cgroup
/bin/readlink -- /proc/3235408/exe /proc/3235408/cwd /proc/3235408/ns/user /proc/3235408/ns/mnt /proc/3235408/ns/pid /proc/3235408/ns/net /proc/3235408/ns/ipc /proc/3235408/ns/uts
/bin/ls -l -- /proc/3235408/fd
/bin/cat /proc/3235408/fdinfo/0 /proc/3235408/fdinfo/1 /proc/3235408/fdinfo/2 /proc/3235408/fdinfo/255
/bin/cat /proc/sys/kernel/random/boot_id /proc/3235408/stat
```

Expected boot: `7c592fd0-8c66-476f-ab0d-548882a9f53e`; start ticks218282664, field22 after the closing process-name parenthesis in stat; UID/GID1000. Historical FD targets/flags are comparison context, not fresh facts. 02002 means RDWR|APPEND; 02002002 adds CLOEXEC. Extra FDs need target/flag review; do not dump full environment or credentials.

If the birth check passes, complete the root/filesystem/FD and before-after reads in [the exact request](fresh-operator-receipt-request.json), then independent review of permissions, pinned tools/libraries, safe context, exact root/prefix and current revocation/unused attempt. Errors or inaccessible records remain incomplete. Provide only nonsecret receipt evidence under applicable publication permission; this request does not grant a write destination.

A missing root requires separate applicable provisioning permission; no mkdir/cleanup here. A completed packet is not permission to launch. The final entry guard must be freshly reassessed immediately before the separately authorized one attempt.


The observed current shell cwd may differ from `/`; record it without changing it. The sealed launch block itself binds child cwd `/`. Do not cd, clear the environment, close FDs or alter limits as part of this receipt request.
