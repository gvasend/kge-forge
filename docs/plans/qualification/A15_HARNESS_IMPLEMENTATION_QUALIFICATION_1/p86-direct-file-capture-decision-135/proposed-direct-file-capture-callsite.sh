# DO NOT EXECUTE — NOT AUTHORIZED
# Inert specification; file mode is non-executable. No grant is issued here.
# Use only the nominated interactive Bash after independently PASSed effective-grant/fresh-entry guard.
# Required non-exported input bindings: P135_GRANT_IDENTITY_SHA256, P135_APPROVED_SUBJECT_SHA256,
# P135_GUARD_SHA256, P135_EXPECTED_CLAIM_SHA256. Each comes from the authenticated issued instrument/guard.
# Values are future typed-identity digests, not authority tokens that may be freely invented.
(
  export 'LC_ALL=C' 'LANG=C' 'PATH=/bin' 'HOME=/nonexistent'
  grant=${P135_GRANT_IDENTITY_SHA256-}
  subject=${P135_APPROVED_SUBJECT_SHA256-}
  guard=${P135_GUARD_SHA256-}
  expected_claim=${P135_EXPECTED_CLAIM_SHA256-}
  [[ $grant =~ ^[0-9a-f]{64}$ && $subject =~ ^[0-9a-f]{64}$ && $guard =~ ^[0-9a-f]{64}$ && $expected_claim =~ ^[0-9a-f]{64}$ ]] || exit 125
  cd -- / || exit 125
  umask 077
  set -C
  # Lower soft limits with existing Bash builtins before any new executable or capture write.
  # POSIX mode is disabled here so -f units are exactly1024 bytes; hard caps are set by pinned prlimit.
  set +o posix
  ulimit -S -t 60 || exit 125
  ulimit -S -v 262144 || exit 125
  ulimit -S -n 64 || exit 125
  ulimit -S -f 4227 || exit 125
  root=/var/tmp/kge-forge/p124-direct-file-capture-135
  prefix="$root/grant-$grant"
  [[ -d $root && ! -L $root ]] || exit 125
  [[ ! -e "$prefix.claim.json" && ! -L "$prefix.claim.json" && ! -e "$prefix.stdout.bin" && ! -L "$prefix.stdout.bin" && ! -e "$prefix.stderr.bin" && ! -L "$prefix.stderr.bin" && ! -e "$prefix.observer.json" && ! -L "$prefix.observer.json" ]] || exit 125
  # Record is reserved with Bash noclobber in qualified private root; partial/unknown state forbids reuse.
  printf '{"attempt":1,"grant_identity_sha256":"%s","guard_sha256":"%s","host":"ubuntu01","profile_sha256":"2f36be1b7123770d889be302a090cfef16149b270140a9ea901ba992095f46ca","schema":"P135-CONSUMPTION-1","subject_sha256":"%s","witness_sha256":"bdd87d58cb628c40ade59324668b83689075645e4ef003817bb2832c5cce8d1c"}
' "$grant" "$guard" "$subject" > "$prefix.claim.json" || exit 125
  '/usr/bin/env' '-i' 'PATH=/bin' 'LC_ALL=C' 'LANG=C' 'HOME=/nonexistent' '/usr/bin/prlimit' '--cpu=60:60' '--as=268435456:268435456' '--nofile=64:64' '--fsize=4329436:4329436' '--' '/usr/bin/timeout' '--signal=KILL' '200s' '/bin/bash' '--noprofile' '--norc' '-c' 'set -C
umask 077
grant=$1
subject=$2
guard=$3
expected_claim=$4
root=/var/tmp/kge-forge/p124-direct-file-capture-135
prefix="$root/grant-$grant"
/bin/sync -- "$prefix.claim.json" "$root" || exit 125
actual_guard=$(/usr/bin/sha256sum -- "$prefix.guard.json") || exit 125
[[ ${actual_guard:0:64} == "$guard" ]] || exit 125
actual_claim=$(/usr/bin/sha256sum -- "$prefix.claim.json") || exit 125
[[ ${actual_claim:0:64} == "$expected_claim" ]] || exit 125
printf '"'"'{"attempt":1,"grant_identity_sha256":"%s","guard_sha256":"%s","no_retry":true,"schema":"P135-LAUNCH-1","subject_sha256":"%s"}
'"'"' "$grant" "$guard" "$subject" > "$prefix.launch.json" || exit 125
/bin/sync -- "$prefix.launch.json" "$root" || exit 125
'"'"'/usr/bin/env'"'"' '"'"'-i'"'"' '"'"'PATH=/bin'"'"' '"'"'LC_ALL=C'"'"' '"'"'LANG=C'"'"' '"'"'HOME=/nonexistent'"'"' '"'"'/usr/bin/prlimit'"'"' '"'"'--cpu=60:60'"'"' '"'"'--as=268435456:268435456'"'"' '"'"'--nofile=64:64'"'"' '"'"'--'"'"' '"'"'/bin/bash'"'"' '"'"'--noprofile'"'"' '"'"'--norc'"'"' '"'"'-c'"'"' '"'"'umask 077
"$@"
result=$?
printf "P127_PARENT_EXIT=%s\n" "$result" >&2
exit "$result"
'"'"' '"'"'P127_FIXED_PARENT'"'"' '"'"'/usr/bin/timeout'"'"' '"'"'--signal=KILL'"'"' '"'"'200s'"'"' '"'"'/usr/bin/bwrap'"'"' '"'"'--unshare-user'"'"' '"'"'--uid'"'"' '"'"'1000'"'"' '"'"'--gid'"'"' '"'"'1000'"'"' '"'"'--unshare-pid'"'"' '"'"'--unshare-net'"'"' '"'"'--unshare-ipc'"'"' '"'"'--unshare-uts'"'"' '"'"'--cap-drop'"'"' '"'"'ALL'"'"' '"'"'--die-with-parent'"'"' '"'"'--dir'"'"' '"'"'/bin'"'"' '"'"'--dir'"'"' '"'"'/lib'"'"' '"'"'--dir'"'"' '"'"'/lib/x86_64-linux-gnu'"'"' '"'"'--dir'"'"' '"'"'/lib64'"'"' '"'"'--dir'"'"' '"'"'/dev'"'"' '"'"'--dir'"'"' '"'"'/proc'"'"' '"'"'--dir'"'"' '"'"'/work'"'"' '"'"'--ro-bind'"'"' '"'"'/bin/findmnt'"'"' '"'"'/bin/findmnt'"'"' '"'"'--ro-bind'"'"' '"'"'/lib/x86_64-linux-gnu/ld-2.31.so'"'"' '"'"'/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2'"'"' '"'"'--ro-bind'"'"' '"'"'/lib/x86_64-linux-gnu/libblkid.so.1.1.0'"'"' '"'"'/lib/x86_64-linux-gnu/libblkid.so.1'"'"' '"'"'--ro-bind'"'"' '"'"'/lib/x86_64-linux-gnu/libc-2.31.so'"'"' '"'"'/lib/x86_64-linux-gnu/libc.so.6'"'"' '"'"'--ro-bind'"'"' '"'"'/lib/x86_64-linux-gnu/libdl-2.31.so'"'"' '"'"'/lib/x86_64-linux-gnu/libdl.so.2'"'"' '"'"'--ro-bind'"'"' '"'"'/lib/x86_64-linux-gnu/libmount.so.1.1.0'"'"' '"'"'/lib/x86_64-linux-gnu/libmount.so.1'"'"' '"'"'--ro-bind'"'"' '"'"'/usr/lib/x86_64-linux-gnu/libpcre2-8.so.0.9.0'"'"' '"'"'/lib/x86_64-linux-gnu/libpcre2-8.so.0'"'"' '"'"'--ro-bind'"'"' '"'"'/lib/x86_64-linux-gnu/libpthread-2.31.so'"'"' '"'"'/lib/x86_64-linux-gnu/libpthread.so.0'"'"' '"'"'--ro-bind'"'"' '"'"'/lib/x86_64-linux-gnu/libselinux.so.1'"'"' '"'"'/lib/x86_64-linux-gnu/libselinux.so.1'"'"' '"'"'--ro-bind'"'"' '"'"'/lib/x86_64-linux-gnu/libsmartcols.so.1.1.0'"'"' '"'"'/lib/x86_64-linux-gnu/libsmartcols.so.1'"'"' '"'"'--ro-bind'"'"' '"'"'/lib/x86_64-linux-gnu/libudev.so.1.6.17'"'"' '"'"'/lib/x86_64-linux-gnu/libudev.so.1'"'"' '"'"'--ro-bind'"'"' '"'"'/lib/x86_64-linux-gnu/ld-2.31.so'"'"' '"'"'/lib64/ld-linux-x86-64.so.2'"'"' '"'"'--proc'"'"' '"'"'/proc'"'"' '"'"'--remount-ro'"'"' '"'"'/proc'"'"' '"'"'--tmpfs'"'"' '"'"'/work'"'"' '"'"'--remount-ro'"'"' '"'"'/'"'"' '"'"'--chdir'"'"' '"'"'/work'"'"' '"'"'--setenv'"'"' '"'"'PATH'"'"' '"'"'/bin'"'"' '"'"'--setenv'"'"' '"'"'LC_ALL'"'"' '"'"'C'"'"' '"'"'--setenv'"'"' '"'"'LANG'"'"' '"'"'C'"'"' '"'"'--'"'"' '"'"'/bin/findmnt'"'"' '"'"'--json'"'"' '"'"'--output'"'"' '"'"'TARGET,SOURCE,FSTYPE,OPTIONS'"'"'
inner_status=$?
out_bytes=$(/usr/bin/stat --format='"'"'%s'"'"' -- "$prefix.stdout.bin") || exit 125
err_bytes=$(/usr/bin/stat --format='"'"'%s'"'"' -- "$prefix.stderr.bin") || exit 125
[[ $out_bytes =~ ^[0-9]{1,7}$ && $err_bytes =~ ^[0-9]{1,7}$ ]] || exit 125
[[ $out_bytes -le 4329436 && $err_bytes -le 4329436 ]] || exit 125
classification=FAIL
[[ $inner_status -eq 0 ]] && classification=OBSERVED
[[ $inner_status -eq 124 || $inner_status -eq 137 ]] && classification=UNKNOWN
[[ $out_bytes -eq 4329436 || $err_bytes -eq 4329436 ]] && classification=INCOMPLETE
printf '"'"'{"classification":"%s","grant_identity_sha256":"%s","guard_sha256":"%s","inner_status":%s,"schema":"P135-RESULT-1","stderr_bytes":%s,"stdout_bytes":%s,"subject_sha256":"%s"}
'"'"' "$classification" "$grant" "$guard" "$inner_status" "$err_bytes" "$out_bytes" "$subject" > "$prefix.result.json" || exit 125
/bin/sync -- "$prefix.stdout.bin" "$prefix.stderr.bin" "$prefix.result.json" "$root" || exit 125
exit "$inner_status"
' 'P135_FIXED_CONTROL' "$grant" "$subject" "$guard" "$expected_claim" < /dev/null > "$prefix.stdout.bin" 2> "$prefix.stderr.bin"
  outer_status=$?
  # Outside-workload status writer: one fixed record, no payload permission or retry restored.
  printf '{"grant_identity_sha256":"%s","guard_sha256":"%s","no_retry":true,"outer_status":%s,"schema":"P135-OUTER-OBSERVER-1","subject_sha256":"%s"}
' "$grant" "$guard" "$outer_status" "$subject" > "$prefix.observer.json" || exit 125
  # Observer record has only successful-write assurance here; durable post-review publication is a separate selected step.
  exit "$outer_status"
)
