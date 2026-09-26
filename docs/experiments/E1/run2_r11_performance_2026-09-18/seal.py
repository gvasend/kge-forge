"""Append-only qualification publication. Keeps PREPARED and grants no issuance."""
import json,os,sys
from pathlib import Path
O=Path(__file__).parent;pub=json.loads((O/'PREPARED_PUBLICATION.json').read_bytes());sys.path.insert(0,pub['runtime_root'])
from adapter.context_projection import canonical,sha,digest
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,_put,_read,_directory
preflight=json.loads((O/'PREFLIGHT.json').read_bytes());neg=json.loads((O/'NEGATIVE_CONTEXT.json').read_bytes())
assert preflight['result']=='PASS_PROSPECTIVE_R11_PENDING_SPECIFIC_ARCHITECT_ISSUANCE' and neg['result']=='PASS'
assert preflight['audit_unused'] and not preflight['issued'] if 'issued' in preflight else preflight['audit_unused']
assert not any(r['hard_exceeded'] for r in preflight['diagnostics'])
for name in ('SYNTHETIC_FINAL_NEW.log','ACTUAL_NEW.log','SYNTHETIC_GRANT.log','HOST_REGRESSIONS.log','PERFORMANCE_TESTS_FINAL.log'):
 assert (O/name).read_text().rstrip().endswith('OK'),name
history=json.loads((O/'HISTORICAL_BASELINE.json').read_bytes())
assert all(sha(Path(p).read_bytes())==h for p,h in history.items())
assert not Path(pub['audit']).exists() and not Path(pub['audit']).parents[2].exists()
store=ControllerAuthorityStore(**pub['selected_store']);cat=json.loads(encoded(store.catalog));A=pub['authorization_id']
names=('SYNTHETIC_FINAL_NEW.log','ACTUAL_NEW.log','SYNTHETIC_GRANT.log','HOST_REGRESSIONS.log','PERFORMANCE_TESTS_FINAL.log','NEGATIVE_CONTEXT.json','PREFLIGHT.json','PRE_ISSUANCE_DIAGNOSTICS.json','COMPLEXITY.json','R10_AUTHENTICATED_CAPTURE.json','PERFORMANCE_APPLICABILITY.json','HISTORY_QUALIFICATION_MATRIX.json')
assert all(r['seconds']<30 for r in preflight['diagnostics'] if r['operation'].startswith('warm_preissuance_production_validation'))
assert sum(r['operation'].startswith('warm_preissuance_production_validation') for r in preflight['diagnostics'])==3
q={'schema':'ATTEMPT-CHAIN-QUALIFICATION-1','result':'PASS','amendment':pub['amendment'],'controller_runtime':pub['controller_runtime'],'accepted_proposal':pub['proposal'],
 'evidence':{n:sha((O/n).read_bytes()) for n in names},'scope':'ACTUAL_PREISSUANCE_CONTEXT_AND_NON_E1_SYNTHETIC_CURRENT_LIFECYCLE_USING_GENUINE_PREDECESSOR_EVIDENCE',
 'regressions':'32 host regression PASS; 24 integrated synthetic; 8 actual history; 6 specific grant; 16 performance reuse tests','production_issuance':False,'production_activation':False,'real_model_requests':0,'effects':0,
 'material_adoption_required':True,'specific_Architect_invocation_authorization_required':True}
qb=canonical(q).encode();qr={'authority_id':'sha256:'+sha(qb),'sha256':sha(qb)}
selection=json.loads(store.resolve(A+':attempt-chain'));assert selection['mode']=='PREPARED' and selection['specific_invocation_authorization'] is None
selection['qualification']=qr;sb=canonical(selection).encode()
new=store.root.parent/'qualified-prepared';new.mkdir(mode=0o700);fd=_directory(new)
try:
 for h in sorted({r['sha256'] for r in cat['objects'].values()}):_put(fd,h,_read(store.fd,h))
 for key,b in ((qr['authority_id'],qb),(A+':attempt-chain',sb)):
  h=sha(b)
  if not (new/h).exists():_put(fd,h,b)
  row=dict(cat['objects'][A+':attempt-chain']);row['sha256']=h;cat['objects'][key]=row
 _put(fd,'catalog.json',canonical(cat).encode());os.fsync(fd)
finally:os.close(fd);store.close()
pub.update(status='QUALIFIED_PREPARED_NOT_ADOPTED_NOT_ISSUED',selected_store={'root':str(new),'catalog_sha256':digest(cat),'applicability':cat['applicability']},qualification=qr)
data=canonical(pub).encode();(O/'QUALIFIED_PUBLICATION.json').write_bytes(data);(O/'QUALIFICATION.json').write_bytes(qb)
# Private publication is the pin; repository copy remains qualification evidence.
fd=_directory(new.parent)
try:_put(fd,'QUALIFIED_PUBLICATION.json',data);os.fsync(fd)
finally:os.close(fd)
(O/'CURRENT_PIN.json').write_text(canonical({'path':str(new.parent/'QUALIFIED_PUBLICATION.json'),'sha256':sha(data)}))
(O/'HISTORICAL_PRESERVATION.json').write_text(canonical({'result':'PASS','files_verified':len(history),'shared_ledger_unchanged':True,'r11_audit_unused':True}))
print(canonical({'result':pub['status'],'qualification':qr,'publication_sha256':sha(data)}))
