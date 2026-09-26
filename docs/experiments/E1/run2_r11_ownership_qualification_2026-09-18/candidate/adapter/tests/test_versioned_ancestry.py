"""Synthetic committed fixtures for the production versioned binding protocol."""
from pathlib import Path
from dataclasses import replace
import json,tempfile,unittest,sys,subprocess
from unittest.mock import patch
from adapter.context_projection import canonical,digest,sha,derive,model_payload_digest
from adapter.continuation_envelope import seal,SCHEMA,TYPES,invariants,dispatch_ancestor
from adapter.governance_continuation import reference,GovernanceContinuation,verify_authorization
from adapter.context_binding import CommittedContext
from adapter.tests.test_governance_continuation import write
from adapter.tests.qualify_activation_transaction import fixture
from adapter.authorization_lifecycle import dispatch_binding
from adapter.activation_transaction import ActivationTransaction


def capture(out,paths,current=False):
    out.mkdir(parents=True,exist_ok=True);(out/'blobs').mkdir(exist_ok=True)
    rows={}
    for p in paths:
        p=Path(p);data=p.read_bytes();h=sha(data);(out/'blobs'/h).write_bytes(data)
        rows[str(p)]={'sha256':h}
    return write(out/'MANIFEST.json',{'current_inputs' if current else 'inputs':rows})


def anchored(out,auth,projection):
    op=json.loads(auth.operational_binding)
    refs={'operational_binding':write(out/'ANCHOR_OP.json',op),
        'full_context':write(out/'ANCHOR_FULL.json',projection['controller_context']),
        'projection':write(out/'ANCHOR_PROJECTION.json',projection['projection'])}
    inputs=[r['path'] for r in refs.values()]
    inputs+=list(auth.context_binding.governance.supplement['inputs'])
    refs['evidence_capture']=capture(out/'anchor-capture',inputs,current=True)
    return {'schema':2,'anchor':refs,
        **{k:op['governance'][k] for k in ('release_basis','release_decision','released_profile','clearance')},
        'authority_invariants':invariants(op,projection['projection']),
        'records':[],'approvals':[],'identities':op['governance']['identities']}


def append(out,spec,typ,path,new_bytes):
    out.mkdir(parents=True,exist_ok=True);before=path.read_bytes() if path.exists() else None
    oldsha=sha(before) if before is not None else None
    oldblob=out/'old.blob'
    if before is not None:oldblob.write_bytes(before)
    newblob=out/'new.blob';newblob.write_bytes(new_bytes)
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(new_bytes)
    artifacts=[{'path':str(path),'old_sha256':oldsha,'new_sha256':sha(new_bytes),
        'old_blob':str(oldblob) if before is not None else None,'new_blob':str(newblob)}]
    cap=capture(out/'qualification-capture',[newblob,*([oldblob] if before is not None else [])])
    evidence=write(out/'EVIDENCE.json',{'result':'PASS','classification':TYPES[typ],
        'artifacts_sha256':digest(artifacts),'authority_invariants':spec['authority_invariants'],'capture':cap})
    authority=out/'ARCHITECT.md';authority.write_text('Synthetic Architect approves this exact non-material continuation only.\n')
    body={'schema':SCHEMA,'type':typ,'sequence':len(spec['records'])+1,
        'predecessor_OperationalContextId':spec['identities']['OperationalContextId'],
        'predecessor_chain_digest':spec['identities']['continuation_chain_digest'],
        'artifacts':artifacts,'authority':reference(authority),'classification':TYPES[typ],
        'evidence':evidence,'authority_invariants':spec['authority_invariants'],'reason':'Synthetic qualification only'}
    approval=write(out/'APPROVAL.json',{'authority':'Architect','decision':'AUTHORIZE_NON_MATERIAL_CONTINUATION',
        'body_sha256':digest(body),'evidence':evidence,'authority_source':body['authority']})
    row=seal(body,approval);ref=write(out/'CONTINUATION.json',row)
    result=json.loads(canonical(spec));result['records'].append(ref);result['approvals'].append(approval)
    result['identities'].update({k:row[k] for k in ('OperationalContextId','continuation_chain_digest')})
    return result


def descendant(auth,spec):
    b=CommittedContext(auth.context_binding.path,auth.context_binding.capture_commit,spec)
    projection=derive(json.loads(auth.context_projection),b)
    op=json.loads(auth.operational_binding);op['governance']=spec
    op['context_identities']={k:projection[k] for k in ('AuthoritativeContextId','FullContextDigest','ModelProjectionDigest','ModelPayloadDigest','ModelProjectionBindingDigest')}
    return replace(auth,context_binding=b,operational_binding=canonical(op)),projection


def qualify(out,host_identity=None):
    root,auth,audit,ref,projection=fixture(out/'fixture',supervisor_identity=host_identity)
    original_dispatch=json.loads(Path(ref['path']).read_bytes())
    exact=dispatch_binding(auth,audit,ref)
    spec=anchored(out/'canonical',auth,projection)
    root_auth,root_projection=descendant(auth,spec)
    dispatch_binding(root_auth,audit,ref)
    gspec=append(out/'governance',spec,'GOVERNANCE_CONTINUATION',root/'public.txt',
        (root/'public.txt').read_bytes()+b'LOCAL_ONLY_CANONICAL_GOVERNANCE\n')
    ga,gp=descendant(auth,gspec);dispatch_binding(ga,audit,ref)
    ispec=append(out/'implementation',gspec,'NON_MATERIAL_IMPLEMENTATION_CONTINUATION',root/'adapter/probe.py',b'# synthetic controller implementation\n')
    current,now=descendant(auth,ispec);result=dispatch_binding(current,audit,ref)
    assert model_payload_digest(projection['projection']['payload'])==gp['ModelPayloadDigest']==now['ModelPayloadDigest']
    assert projection['ModelProjectionBindingDigest']!=gp['ModelProjectionBindingDigest']!=now['ModelProjectionBindingDigest']
    assert now['ModelProjectionDigest']==projection['ModelProjectionDigest']
    assert now['FullContextDigest']!=projection['FullContextDigest']
    assert now['projection']['payload']==projection['projection']['payload']
    # A dispatch issued at the authenticated intermediate governance node also
    # inherits through the later implementation node; it is not root-only logic.
    intermediate=json.loads(canonical(original_dispatch));gop=json.loads(ga.operational_binding)
    intermediate.update(gop['governance']['identities']);intermediate.update(gop['context_identities'])
    intermediate['all_authorized_bindings']['operational_binding_sha256']=digest(gop)
    intermediate_ref=write(out/'INTERMEDIATE_DISPATCH.json',intermediate)
    dispatch_binding(current,audit,intermediate_ref)
    denials={}
    def deny(name,fn):
        try:fn()
        except (RuntimeError,ValueError,KeyError,OSError,TypeError) as exc:denials[name]=type(exc).__name__+': '+str(exc)
        else:raise AssertionError('permitted '+name)
    for name in ('missing','reordered','replay','branch','predecessor','material','unknown','malformed','evidence','approval'):
        bad=json.loads(canonical(ispec))
        if name=='missing':bad['records'].pop();bad['approvals'].pop()
        elif name=='reordered':bad['records'].reverse();bad['approvals'].reverse()
        elif name=='replay':bad['records'].append(bad['records'][-1]);bad['approvals'].append(bad['approvals'][-1])
        else:
            row=json.loads(Path(bad['records'][-1]['path']).read_bytes())
            if name=='branch':row['reason']='unauthorized competing branch'
            if name=='predecessor':row['predecessor_OperationalContextId']='substituted'
            if name=='material':row['classification']='MATERIAL_TO_RELEASE_AUTHORITY'
            if name=='unknown':row['type']='UNRECOGNIZED'
            if name=='malformed':row.pop('artifacts')
            if name=='evidence':row['evidence']=dict(row['evidence'],sha256='0'*64)
            if name=='approval':bad['approvals'][-1]=dict(bad['approvals'][-1],sha256='0'*64)
            bad['records'][-1]=write(out/('BAD_'+name+'.json'),row)
        deny(name,lambda:GovernanceContinuation(bad))
    # Re-sealing a NON_MATERIAL label cannot substitute MATERIAL evidence.
    bad=json.loads(canonical(ispec));row=json.loads(Path(bad['records'][-1]['path']).read_bytes())
    evidence=json.loads(Path(row['evidence']['path']).read_bytes());evidence['classification']='MATERIAL_TO_RELEASE_AUTHORITY'
    body={k:row[k] for k in __import__('adapter.continuation_envelope',fromlist=['BODY_KEYS']).BODY_KEYS}
    body['evidence']=write(out/'MATERIAL_EVIDENCE.json',evidence)
    approval=write(out/'MATERIAL_RELABEL_APPROVAL.json',{'authority':'Architect','decision':'AUTHORIZE_NON_MATERIAL_CONTINUATION',
        'body_sha256':digest(body),'evidence':body['evidence'],'authority_source':body['authority']})
    resealed=seal(body,approval);bad['records'][-1]=write(out/'MATERIAL_RELABEL.json',resealed);bad['approvals'][-1]=approval
    bad['identities'].update({k:resealed[k] for k in ('OperationalContextId','continuation_chain_digest')})
    deny('material_evidence_relabelled',lambda:GovernanceContinuation(bad))
    # Even re-authored, separately approved wrapper evidence cannot erase a
    # MATERIAL classification in the underlying immutable qualification capture.
    bad=json.loads(canonical(ispec));row=json.loads(Path(bad['records'][-1]['path']).read_bytes())
    evidence=json.loads(Path(row['evidence']['path']).read_bytes());cap=Path(evidence['capture']['path'])
    material_cap=json.loads(cap.read_bytes());material_cap['classification']='MATERIAL_TO_RELEASE_AUTHORITY'
    evidence['capture']=write(cap.parent/'MATERIAL_CAPTURE.json',material_cap)
    body={k:row[k] for k in __import__('adapter.continuation_envelope',fromlist=['BODY_KEYS']).BODY_KEYS}
    body['evidence']=write(out/'RELABELLED_CAPTURE_EVIDENCE.json',evidence)
    approval=write(out/'RELABELLED_CAPTURE_APPROVAL.json',{'authority':'Architect','decision':'AUTHORIZE_NON_MATERIAL_CONTINUATION',
        'body_sha256':digest(body),'evidence':body['evidence'],'authority_source':body['authority']})
    resealed=seal(body,approval);bad['records'][-1]=write(out/'RELABELLED_CAPTURE.json',resealed);bad['approvals'][-1]=approval
    bad['identities'].update({k:resealed[k] for k in ('OperationalContextId','continuation_chain_digest')})
    deny('material_capture_relabelled',lambda:GovernanceContinuation(bad))
    evidence_path=Path(json.loads(Path(ispec['records'][-1]['path']).read_bytes())['evidence']['path'])
    saved=evidence_path.with_suffix('.temporarily-missing');evidence_path.rename(saved)
    try:deny('missing_evidence_file',lambda:GovernanceContinuation(ispec))
    finally:saved.rename(evidence_path)
    for rel,name in [('adapter/probe.py','implementation_hash'),('task.txt','task_identity'),('public.txt','payload_identity')]:
        p=root/rel;data=p.read_bytes();p.write_bytes(data+b'UNAUTHORIZED')
        try:deny(name,lambda:descendant(auth,ispec))
        finally:p.write_bytes(data)
    for key in ('released_profile','clearance'):
        refp=ispec[key];p=Path(refp['path']);data=p.read_bytes();p.write_bytes(data+b' ')
        try:deny(key,lambda:descendant(auth,ispec))
        finally:p.write_bytes(data)
    for key in ('destination','ModelPayloadDigest','transmission'):
        bad=json.loads(canonical(ispec));bad['authority_invariants'][key]='changed'
        deny(key,lambda:GovernanceContinuation(bad))
    wrong=json.loads(canonical(original_dispatch));wrong['OperationalContextId']='unrelated-ancestor'
    deny('unrelated_dispatch_ancestor',lambda:dispatch_ancestor(current,wrong))
    wrong=dict(original_dispatch,ModelPayloadDigest='0'*64)
    deny('dispatch_payload_mismatch',lambda:dispatch_ancestor(current,wrong))
    for key in ('ModelPayloadDigest','ModelProjectionBindingDigest','FullContextDigest'):
        altered=json.loads(current.operational_binding);altered['context_identities'][key]='0'*64
        deny('operational_'+key,lambda:dispatch_binding(replace(current,operational_binding=canonical(altered)),audit,ref))
    initial_audit=audit.read_bytes();p=root/'local.txt';data=p.read_bytes();p.write_bytes(data+b'UNAUTHORIZED')
    try:deny('activation_requires_valid_ancestry',lambda:ActivationTransaction.activate(current,audit,ref))
    finally:p.write_bytes(data)
    assert audit.read_bytes()==initial_audit
    # Independently encoded restart identity, without re-authoring context.
    restored,rebuilt=descendant(auth,json.loads(canonical(ispec)))
    assert rebuilt==now and dispatch_binding(restored,audit,ref)==result
    # Implementation-only ancestry from a separate committed context.
    r2,a2,au2,d2,p2=fixture(out/'implementation_only_fixture',supervisor_identity=host_identity)
    s2=anchored(out/'implementation_only_anchor',a2,p2)
    s2=append(out/'implementation_only',s2,'NON_MATERIAL_IMPLEMENTATION_CONTINUATION',r2/'adapter/probe.py',b'# implementation-only\n')
    a2,p2after=descendant(a2,s2);dispatch_binding(a2,au2,d2)
    report={'result':'PASS','denials':denials,'exact_dispatch':exact,'descendant_dispatch':result,
        'identities_before':{k:projection[k] for k in ('FullContextDigest','ModelProjectionDigest','ModelPayloadDigest','ModelProjectionBindingDigest')},
        'identities_after':{k:now[k] for k in ('FullContextDigest','ModelProjectionDigest','ModelPayloadDigest','ModelProjectionBindingDigest')},
        'chain':ispec,'restart':'PASS','payload_byte_identical':True,'E1_effects':0,'model_calls':0}
    write(out/'REPORT.json',report)
    return current,audit,ref,now,report


class VersionedAncestryTests(unittest.TestCase):
    def test_synthetic_ancestry_and_negatives(self):
        with tempfile.TemporaryDirectory(prefix='ancestry-unit-') as raw:
            out=Path(raw)
            with patch('adapter.activation_transaction._host',return_value={'unit_host':'mocked; not live evidence'}):
                auth,audit,ref,projection,report=qualify(out,{'unit_host':'mocked'})
                from adapter.tests.test_controller_authority_store import private_fixture
                store=private_fixture(auth,audit,ref,out/'private-authority')
                try:
                    with store.session():
                        ref='E1-ARCHITECT-DISPATCH-sha256:'+ref['sha256']
                        tx=ActivationTransaction.activate(auth,audit,ref);tx.close()
                        tx=ActivationTransaction.recover(auth,audit,ref)
                        self.assertTrue(tx.recovery['handoff_eligible']);tx.close()
                finally:store.close()


if __name__=='__main__':unittest.main()
