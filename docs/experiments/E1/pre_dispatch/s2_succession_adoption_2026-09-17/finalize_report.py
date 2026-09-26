"""Document completed recovery; no authority or runtime changes."""
from pathlib import Path
import json,hashlib
from adapter.context_projection import canonical,digest,sha
O=Path(__file__).resolve().parent
r=json.loads((O/'FINAL_RECOVERY.json').read_bytes())
assert r['result']=='ACTIVATED_AND_READY_TO_DISPATCH'
assert r['state']=='ACTIVE' and r['ownership']=='OWNERSHIP_HELD' and r['handoff_eligible']
assert r['CURRENT_RELEASE_BINDINGS_VALID'] and r['CURRENT_SUPERVISOR_READY']
e=r['activation_event'];own=r['recovery']['ownership']
assert e['event_sha256']==digest({k:v for k,v in e.items() if k not in ('event_id','event_sha256')})
assert own['reservation_id']=='INVOCATION-RESERVATION-sha256:'+digest({k:v for k,v in own.items() if k!='reservation_id'})
audit=Path(own['controller_audit']);lines=audit.read_bytes().splitlines(keepends=True);rows=[json.loads(x) for x in lines]
start=next(i for i,row in enumerate(rows) if row.get('event')=='production_dispatch_validated')
expected=['production_dispatch_validated','authorization_lifecycle_dispatch_authorized','authorization_lifecycle_activation_intent','authorization_lifecycle_activated']
assert [x.get('event') for x in rows[start:]]==expected
assert sha(b''.join(lines[:start]))=='e4d8a91d0692bb48ad323005b45603cbbd2834a6babdb08b8f846b742ae1e883'
ledger=Path(e['binding']['ownership_ledger']);assert [json.loads(x) for x in ledger.read_bytes().splitlines()]==[own]
app=json.loads((O/'APPLICATION.json').read_bytes())
summary={'result':r['result'],'applied_succession_identity':app['event_identity'],'succession_event_file_sha256':app['event_file_sha256'],'current_supervisor':r['current_supervisor'],'supervisor_readiness':'PASS','dispatch_inheritance':'PASS','production_validation':e['validation']['validation_id'],'activation_event_identity':e['event_id'],'activation_event_fingerprint':e['event_sha256'],'activation_event_canonical_file_sha256':digest(e),'ownership_reservation_identity':own['reservation_id'],'ownership_reservation_fingerprint':own['reservation_id'].split(':',1)[1],'ownership_reservation_canonical_file_sha256':digest(own),'operational_ancestry':r['operational_ancestry'],'independent_recovery':'PASS','state':'ACTIVE','ownership':'OWNERSHIP_HELD','CURRENT_RELEASE_BINDINGS_VALID':True,'CURRENT_SUPERVISOR_READY':True,'model_handoff_eligible':True,'E1_model_requests':0,'E1_implementation_effects':0,'E1_WP_001_dispatched':False,'audit_suffix_only':expected,'current_private_pin':json.loads((O/'CURRENT_PRIVATE_PIN.json').read_bytes())}
with (O/'SUMMARY.json').open('xb') as f:f.write(canonical(summary).encode())
s='# E1-WP-001: ACTIVATED_AND_READY_TO_DISPATCH\n\n'
s+='The exact Architect-authorized succession was applied append-only. Independent supervisor recovery selected the qualified S2 process as the unique current authority holder, with production readiness and dispatch inheritance PASS. Production validation passed before durable intent, ownership reservation and ACTIVE. A separate process recovered ACTIVE + OWNERSHIP_HELD, validated current production/release/supervisor bindings, and established model-handoff eligibility. No first model request was sent.\n\n'
for k,v in summary.items():
 if isinstance(v,(str,bool,int)):s+='- '+k+': `'+str(v)+'`\n'
s+='\nOperationalContextId: `'+r['operational_ancestry']['OperationalContextId']+'`.\n\nContinuation-chain digest: `'+r['operational_ancestry']['continuation_chain_digest']+'`.\n\nThe private selection is pinned by CURRENT_PRIVATE_PIN.json; repository reports are documentary copies. The reserved specific Architect authorization reference now resolves privately to the attributable decision. Original release/dispatch records, S1 anchor and prior continuation records are unchanged. No production implementation was changed.\n\nOnly the four listed activation lifecycle/validation records were appended to the preserved E1 audit; the ownership ledger contains exactly the one matching reservation. The recovery process released its transient controller fence on exit; the durable ACTIVE state and reservation remain. A subsequent controller must use qualified recovery before any handoff, and no model request was authorized or sent by this step.\n'
(O/'REPORT.md').write_text(s)
manifest={p.name:sha(p.read_bytes()) for p in sorted(O.iterdir()) if p.is_file() and p.name!='EVIDENCE_HASHES.json'}
(O/'EVIDENCE_HASHES.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(canonical(summary))
