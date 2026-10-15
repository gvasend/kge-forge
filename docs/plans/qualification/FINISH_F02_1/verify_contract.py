"""Read-only F02 seal verification; no authority, installation or lifecycle operations."""
import hashlib
import json
from pathlib import Path
from adapter.planner import codec as c, installation as i, model as m, typed_proofs as t
from adapter.planner import action_installation as a
ROOT=Path('docs/plans/qualification/FINISH_F02_1')
manifest=json.loads((ROOT/'sealed-manifest.json').read_text())
checked=set()
def verify(value):
    if isinstance(value,dict):
        if 'path' in value and 'content_id' in value:
            path=Path(value['path']);ident=value['content_id']
            assert ident['namespace']=='raw-file-sha256'
            assert hashlib.sha256(path.read_bytes()).hexdigest()==ident['sha256'],path
            checked.add(str(path))
        for member in value.values():verify(member)
    elif isinstance(value,list):
        for member in value:verify(member)
verify(manifest)
for item in manifest['installable_definitions']:
    descriptor=json.loads(Path(item['path']).read_text())
    assert i.simple(i.digest(descriptor,'planner-installable-definition-v1'))==item['definition_id']
    assert c.canonical_bytes(descriptor)==Path(item['path']).read_bytes()
    assert descriptor['content_id']==item['body']['content_id']
    if descriptor['definition_type']=='ACTION_DEFINITION':
        pin=item['body'];body=Path(pin['path']).read_text()
        provenance=m.Provenance(pin['path'],i.identity(pin['content_id']),'/',body,'F02_SEALED_PROSPECTIVE_DEFINITION',manifest['binding']['scope'])
        definition=m.InstallableDefinition(i.identity(item['definition_id']),Path(item['path']).read_text(),provenance)
        _,(old,new)=a.descriptor(definition)
        assert a.same_action(old,old) and old.accepted_inventory==new.accepted_inventory
        assert not new.blocked_terminal
contracts=[]
for pin in manifest['proof_definitions']:
    wire=json.loads(Path(pin['path']).read_text())['contract'];contract=c._unwire(wire)
    m.validate_types(contract,m.TypedProofContract)
    assert contract.id==t.identity(contract)
    assert c.canonical_bytes(wire)==c.canonical_bytes(c._wire(contract))
    contracts.append(contract)
slot,root=contracts
assert slot.proof_type is m.TypedProofKind.SLOT_PROOF and root.proof_type is m.TypedProofKind.ROOT_PROOF
assert slot.provenance.identity!=root.provenance.identity
sources=[json.loads(Path(x['path']).read_text()) for x in manifest['sources']]
assert sources[0]['provenance_origin']['section']!=sources[1]['provenance_origin']['section']
assert sources[0]['proposition']['id']!=sources[1]['proposition']['id']
# A changed source/wrapper cannot retain the exact authorized content identity.
for pin in manifest['sources']:
    raw=Path(pin['path']).read_bytes()
    assert hashlib.sha256(raw+b' ').hexdigest()!=pin['content_id']['sha256']
    wrapper=c.canonical_bytes({'historical_template':json.loads(raw)})
    assert hashlib.sha256(wrapper).hexdigest()!=pin['content_id']['sha256']
print(json.dumps({'status':'PASS_OFFLINE_CONTRACT_SEALS','manifest_id':i.simple(c._identity((ROOT/'sealed-manifest.json').read_bytes(),'raw-file-sha256')),'source_identities':[x['content_id'] for x in manifest['sources']],'proof_contract_ids':[i.simple(x.id) for x in contracts],'checked_content_references':len(checked),'canonical_lifecycle_executed':False},sort_keys=True))
