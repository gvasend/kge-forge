"""Synthetic immutable history dependency scaling, not synthetic release authority."""
import sys,json,time,tempfile,statistics
from pathlib import Path
O=Path(__file__).parent;sys.path.insert(0,str(O/'candidate'))
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
from adapter.history_catalogs import historical_store,reuse_history_catalogs
rows=[]
for n in (1,4,16,64,128):
 with tempfile.TemporaryDirectory(prefix='history-scale-') as t:
  root=Path(t);records={};head=None;ids=[]
  for i in range(n):
   b=encoded({'attempt':'synthetic-'+str(i),'predecessor':head,'disposition':'CANCELLED','effects':0,'immutable_receipt':'x'*4096});head='sha256:'+sha(b);ids.append(head);records[head]={'bytes':b,'evidence':[]}
  s=ControllerAuthorityStore.materialize(root/'store',records,{}, {'authority_source':{'sha256':'0'*64},'release_identities':{'ReleaseBasisId':'synthetic','ReleaseDecisionId':'synthetic'}},{'authorization_id':'synthetic'},[str(root/'grant')]);conf={'root':str(s.root),'catalog_sha256':s.catalog_sha256,'applicability':s.applicability};s.close()
  def validate():
   for _ in range(8):
    with historical_store(conf) as store:
     store.verify_immutable_witness({k:k[7:] for k in ids});previous=None
     for k in ids:
      row=json.loads(store.resolve(k));assert row['predecessor']==previous and row['disposition']=='CANCELLED' and row['effects']==0;previous=k
     assert previous==head
  modes={}
  for name,fn in [('complete_catalog_reconstruction',validate),('operation_scoped_catalog_reuse',reuse_history_catalogs(validate))]:
   samples=[]
   for _ in range(3):
    st=time.monotonic();fn();samples.append(time.monotonic()-st)
   modes[name]={'seconds':samples,'median':statistics.median(samples)}
  rows.append({'attempts':n,'passes_per_operation':8,'data_bytes':sum(len(r['bytes']) for r in records.values()),'measurements':modes})
(O/'COMPLEXITY.json').write_text(json.dumps({'schema':'NON_AUTHORIZING_HISTORY_SCALING-1','scope':'real private resolver and complete synthetic hash-linked safe-history kernel; not full production activation','results':rows,'classification':'LINEAR_FULL_HISTORY_BYTES; catalog parsing once per unique store per operation; no constant-time checkpoint claim'},sort_keys=True))
print(json.dumps(rows))
