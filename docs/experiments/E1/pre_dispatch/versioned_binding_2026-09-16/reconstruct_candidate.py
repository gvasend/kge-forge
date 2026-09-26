from pathlib import Path
import json,shutil
from adapter.context_projection import sha,digest,canonical,read_exact,model_payload_digest
from adapter.continuation_envelope import SCHEMA,TYPES,BODY_KEYS,RESULT_KEYS,seal,invariants,archive,historical_operation
from adapter.governance_continuation import reference
root=Path('/home/gvasend/app/kge-forge');base=root/'docs/experiments/E1/pre_dispatch';out=base/'versioned_binding_2026-09-16';candidate=out/'canonical_e1_candidate';candidate.mkdir(parents=True,exist_ok=True)
def write(name,value):
 p=candidate/name;p.write_text(canonical(value));return reference(p)
old=base/'integrated_activation_2026-09-16';capture_hash='627fc40163edea51492f1711d645b11ac72ceb6d5fa2c2ed9fc5438356a67f6f'
capref={'path':str(old/'captures'/capture_hash/'MANIFEST.json'),'sha256':capture_hash}
captured=archive(capref)
proposal=json.loads((old/'PROPOSED_IMPLEMENTATION_CONTINUATION.json').read_bytes());original= json.loads(read_exact(proposal['event']['path'],proposal['event']['sha256']))
assert captured[proposal['event']['path']]['sha256']==proposal['event']['sha256']
assert original['classification']=='NON_MATERIAL_IMPLEMENTATION_CONTINUATION'
prod=base/'governance_continuation_2026-09-16/production_final';op=json.loads((prod/'OPERATIONAL_BINDING.json').read_bytes());g=op['governance']
assert g['identities']==proposal['predecessor']
full=json.loads((prod/'AUTHORITATIVE_OPERATIONAL_CONTEXT.json').read_bytes());projection=json.loads((prod/'MODEL_CONTEXT_PROJECTION.json').read_bytes())
assert digest(full)==op['context_identities']['FullContextDigest'] and digest(projection)==op['context_identities']['ModelProjectionDigest']
profile=json.loads(read_exact(g['released_profile']['path'],g['released_profile']['sha256']))
assert digest(profile)==original['released_profile_fingerprint']
assert digest(projection['payload'])==original['model_payload_sha256_unchanged']
for ref in [g['release_basis'],g['release_decision'],g['clearance'],op['released_launch'],*g['chain'],original['dispatch_record']]:read_exact(ref['path'],ref['sha256'])
for row in projection['items']:
 data=Path(row['path']).read_bytes();assert sha(data)==row['current_source_sha256']
 for span in row['ranges']:assert sha(data[span['start_byte']:span['end_byte_exclusive']])==span['sha256']
artifacts=[];current_delta_mismatches=[]
for row in original['complete_implementation_delta']:
 path=str(root/row['path']);new=row['current_sha256'];before=row['predecessor_operational_sha256']
 assert captured[path]['sha256']==new
 new_blob=Path(capref['path']).parent/'blobs'/new;read_exact(str(new_blob),new)
 old_blob=None
 if before:
  old_blob=Path(capref['path']).parent/'blobs'/before;read_exact(str(old_blob),before)
 artifacts.append({'path':path,'old_sha256':before,'new_sha256':new,'old_blob':str(old_blob) if old_blob else None,'new_blob':str(new_blob)})
 actual=sha(Path(path).read_bytes())
 if actual!=new:current_delta_mismatches.append({'path':path,'qualified_sha256':new,'current_sha256':actual})
protected=invariants(op,projection)
evidence=write('QUALIFIED_FACTS.json',{'result':'PASS','classification':original['classification'],
 'artifacts_sha256':digest(artifacts),'authority_invariants':protected,'capture':capref,
 'original_proposal':proposal['event'],'qualification_scope':'Exact historical seven-file integrated activation delta; excludes subsequent versioned-binding implementation'})
authority=out/'ARCHITECT_AUTHORITY.md'
authority.write_text('''# Architect authority — recorded excerpts, no application\n\nThe prior Architect adoption instruction states:\n\n> The Architect accepts: integrated activation qualification: PASS; applicability classification: `NON_MATERIAL_IMPLEMENTATION_CONTINUATION`.\n\n> The proposed implementation continuation in `docs/experiments/E1/pre_dispatch/integrated_activation_2026-09-16/PROPOSED_IMPLEMENTATION_CONTINUATION.json` is authorized for adoption, subject to exact validation against evidence-capture SHA-256: `627fc40163edea51492f1711d645b11ac72ceb6d5fa2c2ed9fc5438356a67f6f`\n\nThe current instruction supersedes application authority for this step:\n\n> Do not apply the proposed implementation continuation yet.\n\n> Transform the proposed implementation continuation into the canonical representation only if all qualified facts are preserved exactly.\n\n> If synthetic qualification passes, reconstruct the previously proposed lifecycle implementation continuation using the canonical continuation envelope.\n\n> Then stop before applying it.\n\nThis record attributes the candidate encoding to the Architect's existing dispositions. It does not select a new operational head, approve additional implementation changes, or authorize activation.\n''')
body={'schema':SCHEMA,'type':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','sequence':1,
 'predecessor_OperationalContextId':g['identities']['OperationalContextId'],
 'predecessor_chain_digest':g['identities']['continuation_chain_digest'],
 'artifacts':artifacts,'authority':reference(authority),'classification':original['classification'],
 'evidence':evidence,'authority_invariants':protected,
 'reason':'Exact canonical encoding of the Architect-accepted integrated lifecycle implementation checkpoint; original qualified facts preserved; candidate only, NOT APPLIED'}
approval=write('CANDIDATE_APPROVAL_ENCODING.json',{'authority':'Architect','decision':'AUTHORIZE_NON_MATERIAL_CONTINUATION',
 'body_sha256':digest(body),'evidence':evidence,'authority_source':body['authority']})
row=seal(body,approval);rowref=write('CANONICAL_CONTINUATION.json',row)
anchor_cap=base/'governance_continuation_2026-09-16/captures/4f4e0ceec6e2d3349a58a71f59c47d11ca42b905ad42b268a01c122870b3dec5/MANIFEST.json'
anchor={'operational_binding':reference(prod/'OPERATIONAL_BINDING.json'),
 'full_context':reference(prod/'AUTHORITATIVE_OPERATIONAL_CONTEXT.json'),
 'projection':reference(prod/'MODEL_CONTEXT_PROJECTION.json'),'evidence_capture':reference(anchor_cap)}
archive(anchor['evidence_capture'])
spec={'schema':2,'anchor':anchor,**{k:g[k] for k in ('release_basis','release_decision','released_profile','clearance')},
 'authority_invariants':protected,'records':[rowref],'approvals':[approval],
 'identities':{**g['identities'],**{k:row[k] for k in ('OperationalContextId','continuation_chain_digest')}}}
write('CANDIDATE_SPECIFICATION.json',spec)
supplement=json.loads(read_exact(g['implementation_supplement']['path'],g['implementation_supplement']['sha256']))
basis=json.loads(read_exact(g['release_basis']['path'],g['release_basis']['sha256']));sources=basis.get('current_inputs',basis.get('inputs'))
for a in artifacts:supplement['inputs'][a['path']]={'previous_sha256':sources.get(a['path'],{}).get('sha256'),'sha256':a['new_sha256']}
proposed=historical_operation(op,full,projection,spec,supplement)
write('PROPOSED_OPERATIONAL_BINDING_CHECKPOINT.json',proposed)
# Exact current drift is deliberately not silently incorporated into the old record.
all_delta=[]
for p in sorted((root/'adapter').glob('*.py')):
 oldhash=captured.get(str(p),{}).get('sha256');newhash=sha(p.read_bytes())
 if oldhash!=newhash:all_delta.append({'path':str(p),'previous_qualified_sha256':oldhash,'current_sha256':newhash})
dispatch=json.loads(Path(original['dispatch_record']['path']).read_bytes())
audit=Path(dispatch['all_authorized_bindings']['audit']);ledger=Path(dispatch['all_authorized_bindings']['ownership_ledger'])
assert sha(audit.read_bytes())=='e4d8a91d0692bb48ad323005b45603cbbd2834a6babdb08b8f846b742ae1e883'
assert ledger.read_bytes()==b'' and not Path(str(ledger)+'.controller-lock').exists()
report={'status':'RECONSTRUCTED CANDIDATE / NOT APPLIED','canonical_continuation':rowref,
 'continuation_id':row['continuation_id'],'evidence_capture_sha256':capture_hash,
 'qualified_facts_preserved':True,'qualified_artifact_count':len(artifacts),
 'predecessor':g['identities'],'proposed':{**spec['identities'],**proposed['context_identities']},
 'ModelPayloadDigest_before':model_payload_digest(projection['payload']),
 'ModelPayloadDigest_after':protected['ModelPayloadDigest'],
 'released_ModelProjectionDigest_preserved':digest(projection),
 'profile_fingerprint_preserved':digest(profile),'existing_dispatch_record_unchanged':original['dispatch_record'],
 'current_files_differing_from_original_seven_file_checkpoint':current_delta_mismatches,
 'additional_binding_mechanism_delta_since_qualification':all_delta,
 'current_tip_adoption_ready':False,
 'limitation':'This exact old checkpoint does not include the new binding implementation. Its present-day current-byte verification fails closed; any adoption on this tree must separately account for the additional qualified binding delta. No old/new hash was substituted.',
 'continuation_applied':False,'E1':'INACTIVE','E1_WP_001':'INELIGIBLE / UNDISPATCHED',
 'E1_activation_events_created':0,'E1_ownership_acquired':False,'model_requests':0,'E1_effects':0}
write('RECONSTRUCTION_REPORT.json',report)
print(json.dumps({'candidate':rowref,'identities':report['proposed'],'current_delta_mismatches':len(current_delta_mismatches),'additional_binding_files':len(all_delta)},indent=2))
