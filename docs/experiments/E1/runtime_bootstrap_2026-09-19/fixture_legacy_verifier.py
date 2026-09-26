"""Synthetic fixture only; never selected as a production legacy verifier."""
import json,sys,hashlib
from pathlib import Path
r=json.load(sys.stdin)
assert hashlib.sha256(Path(r['sentinel']).read_bytes()).hexdigest()==r['sha256']
print(json.dumps(r['expected']))
