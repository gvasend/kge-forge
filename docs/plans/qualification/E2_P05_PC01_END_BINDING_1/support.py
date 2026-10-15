"""Independent native provenance/policy/current-definition support inspection."""
import hashlib
import json
from binding import ROOT, OUT, DOCS, P, c, m, ai, source_specs, read, pointer, equal, save, aid, ref, CALLS
from adapter.planner.selector import validate_policy


def main():
    projected=read(OUT/'END-projection.json')['projection']
    original,current=source_specs()
    models={spec['role']:c._unwire(pointer(read(ROOT/spec['source']['path']),spec['source']['pointer'])) for spec in source_specs()}
    bundle=c._unwire(read(ROOT/current['source']['path'])['bundle'])
    c._verify_sources(bundle,ROOT)
    c._check_snapshot_pins(bundle.current,bundle.sources)
    validate_policy(bundle.policy,bundle.policy_version)
    records=[]
    for spec in source_specs():
        state=models[spec['role']]
        before=c.snapshot_bytes(state)
        for action in state.actions:
            # Original temporary paths are not treated as currently loadable
            # P04 sources. Their exact qualified provenance bytes are retained
            # inside the pinned original native Snapshot.
            content=action.source.excerpt.encode()
            equal('retained Action provenance content',hashlib.sha256(content).hexdigest(),action.source.identity.sha256)
            records.append({'role':spec['role'],'ActionId':action.id.value,
                'source_provenance':c._wire(action.source),'content_hash_correspondence':'PASS',
                'source_role':'IMMUTABLE_HISTORICAL_PROVENANCE_IN_RETAINED_SNAPSHOT' if spec['role']==original['role'] else 'CURRENT_PINNED_P04_SOURCE',
                'old_temporary_source_path_promoted_to_live_source':False})
        equal('source view immutable after inspection',c.snapshot_bytes(state),before)
    versions=[]
    for record in bundle.current.installed_definitions:
        descriptor=c.parse_json(record.request.definition.descriptor_json.encode())
        if descriptor.get('definition_type')!='ACTION_DEFINITION':continue
        desc,(old,new)=ai.descriptor(record.request.definition)
        actual=next(a for a in bundle.current.actions if a.id==new.id)
        equal('exact governed current Action bytes',c._wire(actual),c._wire(new))
        equal('governed Action definition support current',ai.action_current(bundle.current,actual),True)
        event=next(e for e in bundle.events if type(e.result) is m.InstallDefinition and e.result==record.request)
        versions.append({'ActionId':new.id.value,'installed_definition_id':aid(record.id),
            'definition_id':aid(record.request.definition.id),'event_id':aid(event.identity),'sequence':event.sequence,
            'content_id':desc['content_id'],'authority_id':aid(record.request.authority.id),
            'currentness':'PASS','old_action':c._wire(old),'current_action':c._wire(new),
            'changes':json.loads(record.request.definition.provenance.excerpt)['contract']['allowed_changes']})
    equal('existing Action replacement versions only',sorted(v['ActionId'] for v in versions),['E2-FINISH','E2-REENTER'])
    equal('known native definition install boundaries',sorted(v['sequence'] for v in versions),[7,9])
    equal('no native transition/replay/commit',CALLS,[])
    save('currentness-provenance-policy.json',{'RESULT':'PASS','native_mutating_calls':CALLS,
        'original_context':c._wire(models[original['role']].context),'current_context':c._wire(bundle.current.context),
        'original_model_role':'Historical qualified baseline definition view only',
        'current_model_role':'Exact current canonical P04 definition view only',
        'Action_sources':records,'governed_Action_versions':versions,'source_pin_verification':'PASS',
        'policy':c._wire(bundle.policy),'policy_version':bundle.policy_version,'policy_validation':'PASS',
        'native_ledger_and_current_state_not_changed':True,'completed_state_not_new_execution_permission':True})
    print(json.dumps({'CURRENTNESS':'PASS','governed_Action_versions':2,'provenance_rows':len(records),'native_calls':CALLS}))


if __name__=='__main__':main()
