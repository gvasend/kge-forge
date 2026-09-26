"""Read-only prefix cost comparison, not production authority selection."""
import json,sys,time,copy
from pathlib import Path
from unittest.mock import patch
O=Path(__file__).parent;pub=json.loads((O/'PREPARED_PUBLICATION.json').read_bytes());sys.path.insert(0,pub['runtime_root'])
from adapter import attempt_chain as chain
from adapter.context_projection import canonical
full=json.loads((O/'R10_AUTHENTICATED_CAPTURE.json').read_bytes())
prior=copy.deepcopy(full['governance']['run6']['predecessor'])
prior['publication']=full['governance']['run6']['amendment']['predecessor_publication']
rows=[]
for label,proof in [('through_r9',prior),('through_r10',full)]:
 for iteration in range(3):
  start=time.monotonic()
  with patch.object(chain,'read',return_value=proof):
   chain.historical_capture({'predecessor_capture':'SYNTHETIC_READ_ONLY_PREFIX_REFERENCE','predecessor_publication':proof['publication']})
  rows.append({'prefix':label,'iteration':iteration,'seconds':time.monotonic()-start})
(O/'HISTORY_PREFIX_TIMING.json').write_text(canonical({'mode':'READ_ONLY_MICROBENCHMARK_NOT_AUTHORITY','measurements':rows,'constant_time_claim':False,'current_mutable_ownership_not_cached':True}))
print(canonical(rows))
