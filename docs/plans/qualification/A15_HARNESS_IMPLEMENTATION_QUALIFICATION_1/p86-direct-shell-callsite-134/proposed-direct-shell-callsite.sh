# DO NOT EXECUTE — NOT AUTHORIZED
# Package134 inert non-runnable annotated specification only.
# UNBOUND: clear-and-rebuild environment before first native exec.
# UNBOUND: actual operator cwd and exactsource127 context verification.
# UNBOUND: Bash pre-first-exec descriptor closure and safe standard endpoints.
# UNBOUND: qualified bounded stdout/stderr collector, independent exit/timeout evidence.
# UNBOUND: selected resource enforcement, scratch/aggregate controls and permissions.
# UNBOUND: exact future evidence root/writer/durability and grant/consumption guard.
# No runnable callsite is supplied. Do not strip comments or paste this vector.
# Retained quoted argv-only source vector follows, for static comparison only:
# SOURCE_VECTOR_TEXT /usr/bin/prlimit --cpu=60:60 --as=268435456:268435456 --nofile=64:64 -- /bin/bash --noprofile --norc -c 'umask 077
# SOURCE_VECTOR_TEXT "$@"
# SOURCE_VECTOR_TEXT result=$?
# SOURCE_VECTOR_TEXT printf "P127_PARENT_EXIT=%s\n" "$result" >&2
# SOURCE_VECTOR_TEXT exit "$result"
# SOURCE_VECTOR_TEXT ' P127_FIXED_PARENT /usr/bin/timeout --signal=KILL 200s /usr/bin/bwrap --unshare-user --uid 1000 --gid 1000 --unshare-pid --unshare-net --unshare-ipc --unshare-uts --cap-drop ALL --die-with-parent --dir /bin --dir /lib --dir /lib/x86_64-linux-gnu --dir /lib64 --dir /dev --dir /proc --dir /work --ro-bind /bin/findmnt /bin/findmnt --ro-bind /lib/x86_64-linux-gnu/ld-2.31.so /lib/x86_64-linux-gnu/ld-linux-x86-64.so.2 --ro-bind /lib/x86_64-linux-gnu/libblkid.so.1.1.0 /lib/x86_64-linux-gnu/libblkid.so.1 --ro-bind /lib/x86_64-linux-gnu/libc-2.31.so /lib/x86_64-linux-gnu/libc.so.6 --ro-bind /lib/x86_64-linux-gnu/libdl-2.31.so /lib/x86_64-linux-gnu/libdl.so.2 --ro-bind /lib/x86_64-linux-gnu/libmount.so.1.1.0 /lib/x86_64-linux-gnu/libmount.so.1 --ro-bind /usr/lib/x86_64-linux-gnu/libpcre2-8.so.0.9.0 /lib/x86_64-linux-gnu/libpcre2-8.so.0 --ro-bind /lib/x86_64-linux-gnu/libpthread-2.31.so /lib/x86_64-linux-gnu/libpthread.so.0 --ro-bind /lib/x86_64-linux-gnu/libselinux.so.1 /lib/x86_64-linux-gnu/libselinux.so.1 --ro-bind /lib/x86_64-linux-gnu/libsmartcols.so.1.1.0 /lib/x86_64-linux-gnu/libsmartcols.so.1 --ro-bind /lib/x86_64-linux-gnu/libudev.so.1.6.17 /lib/x86_64-linux-gnu/libudev.so.1 --ro-bind /lib/x86_64-linux-gnu/ld-2.31.so /lib64/ld-linux-x86-64.so.2 --proc /proc --remount-ro /proc --tmpfs /work --remount-ro / --chdir /work --setenv PATH /bin --setenv LC_ALL C --setenv LANG C -- /bin/findmnt --json --output TARGET,SOURCE,FSTYPE,OPTIONS
# Outcome: PARTIAL; one prospective attempt; automatic retries0; no executionauthority.
