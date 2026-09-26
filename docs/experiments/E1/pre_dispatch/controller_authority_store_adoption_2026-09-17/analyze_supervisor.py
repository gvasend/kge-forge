"""Trace supervisor semantics from adopted private release bytes; no host calls."""
from pathlib import Path
import ast
import json
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.context_projection import canonical, sha
from verify_adoption import BASE, Q, OUT, load, ref, exact

pin=Path('/tmp/kge-forge-controller-authority/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39/adoption-2026-09-17/ADOPTION_RECORD.json')
data=exact({'path':str(pin),'sha256':'420b41640db490b2fc33500cd02ffc52a55245c8b7c730b307a513502d2efa77'})
selection=json.loads(data)['selected_store']
store=ControllerAuthorityStore(**selection)
try:
    op=json.loads(store.resolve(selection['applicability']['OperationalContextId']))
    profile=json.loads(store.resolve('sha256:'+op['governance']['released_profile']['sha256']))
    basis=json.loads(store.resolve(op['governance']['identities']['ReleaseBasisId']))
    release=json.loads(store.resolve(op['governance']['identities']['ReleaseDecisionId']))
    sources=basis.get('current_inputs',basis.get('inputs'))
    traced=[]
    for rel in ('pd05_final_evidence/HOST_RECEIPT.json','pd06_release_evidence/execution/HOST_RECEIPT.json',
                'pd05_final_evidence/PROPOSED_PRODUCTION_PROFILE.json','pd06_release_evidence/PROPOSED_PRODUCTION_PROFILE.json'):
        path=BASE/rel;h=sources[str(path)]['sha256']
        data=store.resolve('sha256:'+h)
        value=json.loads(data)
        assert (value.get('supervisor') or value.get('supervisor_binding'))==profile['supervisor_binding']
        traced.append({'evidence_path':str(path),'private_content_identity':'sha256:'+h,'tuple_equal':True})
    source=BASE.parents[3]/'adapter/activation_transaction.py'
    old_hash=load(Q/'IMPLEMENTATION_BEFORE.json')[str(source)]
    old=exact({'path':str(Q/'before'/old_hash),'sha256':old_hash})
    def host_ast(b):
        return ast.dump(next(n for n in ast.parse(b).body if isinstance(n,ast.FunctionDef) and n.name=='_host'))
    assert host_ast(old)==host_ast(source.read_bytes())
    report={'classification':'PROCESS_INSTANCE_IDENTITY','granularity':'Exact released process tuple; no boot ID, process start time or pidfd is bound.',
        'released_supervisor_binding':profile['supervisor_binding'],
        'why_pid_57950':'Captured live qualified supervisor instance; copied from host receipt into profile, then bound by immutable release profile fingerprint.',
        'traced_private_evidence':traced,'release_basis':op['governance']['identities']['ReleaseBasisId'],
        'release_decision':op['governance']['identities']['ReleaseDecisionId'],
        'released_profile':op['governance']['released_profile'],'release_decision_canonical_profile_fingerprint':release['released_profile_sha256'],
        'validator_source':ref(source),'prior_validator_sha256':old_hash,'host_validator_AST_unchanged':True,
        'host_prerequisite_evidence':ref(BASE/'controller_authority_store_2026-09-17/HOST_PREREQUISITE.json'),
        'qualified_interchangeable_supervisor_binding':False,'qualified_rebinding_operation_available':False,
        'smallest_next_host_step':'Separately host-authorized read-only reconciliation. If original instance is absent, replacement additionally needs explicit Architect-authorized forward binding amendment and qualification. Ordinary restart alone cannot satisfy the released tuple.',
        'host_intervention_performed':False,'supervisor_started':False,'supervisor_binding_changed':False}
finally:store.close()
with (OUT/'SUPERVISOR_BINDING.json').open('x') as f:f.write(canonical(report)+'\n')
print(canonical(report))
