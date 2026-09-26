from pathlib import Path
import json
from adapter.context_projection import canonical,digest,sha,read_exact
from adapter.governance_continuation import reference,next_identity
root=Path('/home/gvasend/app/kge-forge');base=root/'docs/experiments/E1/pre_dispatch';out=base/'integrated_activation_2026-09-16';prod=base/'governance_continuation_2026-09-16/production_final'
def write(name,value):
 p=out/name;p.write_text(canonical(value));return reference(p)
op=json.loads((prod/'OPERATIONAL_BINDING.json').read_bytes());g=op['governance'];old_ids=g['identities']
full=json.loads((prod/'AUTHORITATIVE_OPERATIONAL_CONTEXT.json').read_bytes());projection=json.loads((prod/'MODEL_CONTEXT_PROJECTION.json').read_bytes())
assert digest(full)==op['context_identities']['FullContextDigest']
assert digest(projection)==op['context_identities']['ModelProjectionDigest']
old_payload=digest(projection['payload'])
# Exact six-source payload and byte ranges remain content-bound.
proof=[]
for item in projection['items']:
 data=Path(item['path']).read_bytes()
 assert sha(data)==item['current_source_sha256']
 for span in item['ranges']:
  assert sha(data[span['start_byte']:span['end_byte_exclusive']])==span['sha256']
 proof.append({'path':item['path'],'source_sha256':sha(data),'ranges':item['ranges']})
assert len(proof)==6
write('RELEASED_PAYLOAD_PRESERVATION.json',{'result':'PASS','payload_sha256':old_payload,'sources':proof})
delta=json.loads((out/'DELTA_INVENTORY.json').read_bytes())['production_delta']
body={'schema':'IMPLEMENTATION-CONTINUATION-PROPOSAL-1','sequence':len(g['chain'])+1,
 'predecessor':old_ids['OperationalContextId'],'ReleaseBasisId':old_ids['ReleaseBasisId'],
 'ReleaseDecisionId':old_ids['ReleaseDecisionId'],
 'dispatch_record':reference(base/'dispatch_authorization_2026-09-16/DISPATCH_RECORD.json'),
 'authorization_id':op['invocation_identity']['authorization_id'],
 'authority_source':reference(out/'ARCHITECT_INSTRUCTION.md'),'authority_status':'ARCHITECT_ADOPTION_REQUIRED',
 'classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','alters_released_task_authority':False,
 'delta_classification':'LOCAL_ONLY','complete_implementation_delta':delta,
 'qualification':reference(out/'APPLICABILITY_ASSESSMENT.json'),
 'released_profile_fingerprint':'b9e7f72d97525f39fbddfe92f276ab6aedd057ef6c5b7284dc163f1db9c9c328',
 'model_payload_sha256_unchanged':old_payload,'historical_authorization_and_dispatch_unchanged':True,
 'new_controller_resource':{'path':'/tmp/kge-forge-e1-invocations.jsonl.controller-lock','purpose':'exclusive controller fence only; no Programmer access','created_for_E1':False},
 'applied':False}
ordered=[]
for r in g['chain']:
 row=json.loads(read_exact(r['path'],r['sha256']));row.pop('OperationalContextId');ordered.append(digest(row))
new_id=next_identity(old_ids['ReleaseBasisId'],old_ids['ReleaseDecisionId'],old_ids['OperationalContextId'],ordered+[digest(body)])
record={**body,'OperationalContextId':new_id}
rr=write('PROPOSED_CONTINUATION_EVENT.json',record)
# A review-only specification. The existing runtime accepts only source-append
# continuations; this proposed implementation member is not installed or trusted.
proposed_g=json.loads(canonical(g));proposed_g['chain'].append(rr);proposed_g['approved_records'].append(rr['sha256'])
proposed_g['identities']={**old_ids,'OperationalContextId':new_id,'continuation_chain_digest':digest(proposed_g['approved_records'])}
supplement=json.loads(read_exact(g['implementation_supplement']['path'],g['implementation_supplement']['sha256']))
basis=json.loads(read_exact(g['release_basis']['path'],g['release_basis']['sha256']));sources=basis.get('current_inputs',basis.get('inputs'))
for row in delta:
 p=str(root/row['path']);supplement['inputs'][p]={'previous_sha256':sources.get(p,{}).get('sha256'),'sha256':row['current_sha256']}
supplement['authority_source']=reference(out/'ARCHITECT_INSTRUCTION.md')
supplement['reason']='PROPOSED ONLY: integrated activation implementation; requires Architect adoption before rebinding'
proposed_g['implementation_supplement']=write('PROPOSED_IMPLEMENTATION_SUPPLEMENT.json',supplement)
proposed_g['implementation_paths']=sorted(supplement['inputs'])
write('PROPOSED_GOVERNANCE_SPECIFICATION.json',proposed_g)
full['implementation_supplement']=supplement;full['operational_governance']=proposed_g['identities'];full['operational_specification_sha256']=digest(proposed_g)
new_full=digest(full);new_authority='E1-AUTHORITATIVE-CONTEXT-sha256:'+new_full
projection['authoritative_context_id']=new_authority;projection['operational_governance']=proposed_g['identities']
for row in projection['items']:row['continuation_chain_digest']=proposed_g['identities']['continuation_chain_digest']
assert digest(projection['payload'])==old_payload
write('PROPOSED_AUTHORITATIVE_CONTEXT.json',full);write('PROPOSED_MODEL_PROJECTION.json',projection)
summary={'status':'PROPOSED / NOT APPLIED / NOT AN AUTHORIZATION','event':rr,
 'identity_derivation':'next_identity(ReleaseBasisId, ReleaseDecisionId, predecessor OperationalContextId, ordered canonical continuation bodies excluding resulting IDs); full/projection SHA256 of canonical proposed bodies',
 'predecessor':old_ids,'proposed':{**proposed_g['identities'],'AuthoritativeContextId':new_authority,'FullContextDigest':new_full,'ModelProjectionDigest':digest(projection)},
 'released_profile_fingerprint_unchanged':body['released_profile_fingerprint'],'model_payload_sha256_unchanged':old_payload,
 'adoption_requirements':['Architect explicitly accepts this implementation continuation and its controller fence resource.',
 'Do not pass this proposal to current GovernanceContinuation as an approved record: its source-append-only schema intentionally rejects implementation-replacement members.',
 'An authorized adoption must validate implementation-member lineage and reconcile the new context with the immutable dispatch ancestor; no existing record may be overwritten. This qualification did not implement or apply that rebinding.',
 'Rerun complete dispatch validation under the approved operational binding before any real activation.'],
 'E1':'INACTIVE','E1_WP_001':'INELIGIBLE / UNDISPATCHED'}
write('PROPOSED_IMPLEMENTATION_CONTINUATION.json',summary)
print(json.dumps(summary['proposed'],indent=2))
