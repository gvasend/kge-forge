"""Recover interface contracts only; no binding or Planner operation is applied."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
DOCS = ROOT / 'docs/plans'
P = 'DETERMINISTIC_PLANNER_V0_1_'
REC = ROOT / 'docs/plans/qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1'
QUAL = ROOT / 'docs/plans/qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1'


def read(path):
    return json.loads(Path(path).read_bytes())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ref(path, pointer='', line=None):
    if not Path(path).is_absolute():path=ROOT/path
    value={'path':str(Path(path).relative_to(ROOT)),'pointer':pointer,'raw_sha256':sha(path)}
    if line is not None:value['line']=line
    return value


def save(name,value):
    path=OUT/name
    raw=(json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
    if path.exists():assert path.read_bytes()==raw,name
    else:path.write_bytes(raw)


def inventory_usage():
    # Complete retained reference search, not an assertion that every textual
    # match is an operative current binding or an actual executed consumer.
    args=['rg','-l','E2_PC01|E2-PC01','docs/plans','adapter/tests','adapter/planner',
          '-g','*.json','-g','*.md','-g','*.py']
    found=subprocess.run(args,cwd=str(ROOT),capture_output=True,text=True,check=True).stdout.splitlines()
    hits=[]
    retained_before_work=set(read(OUT/'baseline.json')['files'])
    for name in sorted(set(found)):
        if name not in retained_before_work:continue
        path=ROOT/name
        text=path.read_text()
        if 'E2_PC01' in path.name:
            category='PC01_PRODUCER_OR_OWN_QUALIFICATION'
        elif '/negative' in name or 'negative' in path.name:
            category='ISOLATED_NEGATIVE_OR_MUTATION_REFERENCE'
        elif path.name.startswith(('bundle-','event-','snapshot-')) or path.name.endswith('_BUNDLE_1.json'):
            category='RETAINED_NATIVE_ARTIFACT_REFERENCE; not current END interface by itself'
        elif path.suffix=='.py':
            category='QUALIFICATION_OR_MATERIALIZATION_PROGRAM_REFERENCE'
        else:
            category='LATER_QUALIFICATION_DECLARATION_RESULT_OR_PIN_REFERENCE'
        lines=[]
        for i,line in enumerate(text.splitlines(),1):
            if 'E2-PC01' in line or 'E2_PC01' in line:
                lines.append(i)
        hits.append({'source':ref(path),'reference_lines':lines,'classification':category,
                     'operative_consumption_not_inferred_from_text':True})
    value={'search':args,'matching_artifacts':len(hits),'artifacts':hits,
           'later_consumers_count':sum(h['classification']!='PC01_PRODUCER_OR_OWN_QUALIFICATION' for h in hits),
           'provenance_strings_and_template_copies_not_promoted_to_current_bindings':True,
           'closed_bridge_qualifications_reexecuted':False}
    save('PC01-reference-consumer-inventory.json',value)
    return value


def main():
    oracle=read(REC/'END-qualification-oracle.json')
    interface=read(DOCS/(P+'E2_PC04_END.json'))
    expected=oracle['six_interfaces_and_process_inputs']['interfaces']
    assert expected==interface['dependencies'] and len(expected)==6
    graph=read(REC/'qualified-evidence-graph.json')['graph']
    edges=[e for e in graph['edges'] if e['relationship']=='DECLARED_PC04_INTERFACE']
    assert [e['source'] for e in edges]==expected
    current=read(QUAL/'END-oracle-results.json')
    missing=[e for e in current['edge_terms'] if e['RESULT']=='FAIL_NOT_BOUND']
    assert [e['edge_id'] for e in missing]==[e['edge_id'] for e in edges]
    closed=read(DOCS/(P+'E2_P05_COMPOSITE_END_QUALIFICATION_1.json'))
    assert closed['STAGE_BINDINGS']=='13/13' and closed['AGGREGATE_N12_MAPPING']==closed['AGGREGATE_N13_MAPPING']=='PASS'
    assert closed['SCOPE_AUTHENTICATION']=='PASS'

    source_files=[
        ['E2_PC01_SOURCES.json','E2_PC01_FIXTURES.json','E2_PC01_EXIT_RECONCILIATION_1.json','E2_P02_INITIAL_SNAPSHOT.json'],
        ['E2_PC02_FIXTURES.json','E2_PC02_VALIDATION.json','E2_P04_CANONICAL_TARGET_BUNDLE_1.json'],
        ['E2_PC03_FIXTURES.json','E2_PC03_VALIDATION.json','FINISH_F03_RESULT.json'],
        ['E2_T01_RESULT.md','EVIDENCE_E07_INGRESS_INTEGRATION_RESULT.md','E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT.json'],
        ['E2_PC04_D01.json','E2_P05_COMPOSITE_END_QUALIFICATION_1.json'],
        ['REENTRY_R01_A11_CONTRACT.md','INSTALLATION_I05_RESULT.json','FINISH_F03_RESULT.json','E2_P04_CANONICAL_TARGET_BUNDLE_1.json'],
    ]
    purposes=[
        'Supply the complete canonical six-Action definition/model contract to END stage and model evaluation',
        'Supply independently source-bound proof, authority, decision and external lifecycle contracts',
        'Supply independent state, mutation, persistence and cold-reader comparison contracts',
        'Supply qualified ordinary Evidence admission/receipt capability and its actual post-restore consumer evidence',
        'Supply determinism dimensions, supported native identity comparisons and fresh-process runner inputs',
        'Supply actual native REENTER result continuation, independent root/slot proofs, reevaluation and FINISH contract',
    ]
    producer=['E2-PC01 FIXTURE package and definition/whole-model oracles',
        'E2-PC02 fixture/oracle package; later P04 governed typed contracts',
        'E2-PC03 phase/oracle/process package; later sealed F03/current lifecycle boundary oracles',
        'E2-T01 qualified native ingress capability; E07/current canonical A09 transaction',
        'E2-PC04 D01 interface and the current deterministic qualification harnesses',
        'Canonical A11/A12/A13 definitions/capabilities; I05/F03/P04 actual qualification']
    process=[
        'Read-only qualification projection/aggregation of the exact six Action definitions and model boundary into an END input/process manifest',
        'Read-only consumer projection of qualified typed source/authority/proof/lifecycle contracts; native operations later retain their own bounds',
        'Bind independent comparison oracles to exact current phase/checkpoint/mutation operands and writer/reader manifests',
        'Bind the qualified native admission API, pinned code/contracts and exact A09 consumer input/post-state evidence; no new receipt transaction here',
        'Bind seed/permutation/writer/reader/identity comparison inputs to the selected END method; later D01 execution remains separate',
        'Bind ordinary REENTER and root/slot/FINISH continuation contracts, exact event/state sequence and current independent boundary oracles',
    ]
    input_types=['Native six-Action model/Snapshot plus complete prospective source definitions and policy/reference contracts',
        'Typed proof/authority/dossier/gate/receipt/source contracts at declared native consumer boundaries',
        'Independent expected full-state oracles and pinned native phase/mutation/checkpoint candidates',
        'Qualified ingress contract/API plus exact existing source/authentication and actual canonical admission witness',
        'Supported semantic-state inputs, code/oracle pins, seeds and permitted unordered/key presentations, independent process inputs',
        'Current A11 inputs/eligibility boundary, admitted A12 result/Knowledge, A13 definitions/source/proof/FINISH requirements']
    lineage=[
        'Historical E2-CANONICAL-BASELINE-1; current included component contexts retained separately',
        'Historical baseline fixture; P04 active definitions/E2-P03-PROSPECTIVE-QUALIFICATION-1 for its native consumers',
        'Historical baseline phase fixture; current scoped A03/A04/A06/P03/P04 oracle contexts separately',
        'Capability/code pins have no one inherited lifecycle lineage; native A09 event has its exact P04 context',
        'Protocol is experiment-scoped; each writer/reader input must retain its own native lineage',
        'Actual canonical P04 tail context; no cross-lineage state splice']
    records=[]
    for i,name in enumerate(expected):
        sources=[ref(DOCS/(P+suffix)) for suffix in source_files[i]]
        dimensions={
            'SOURCE_DEFINITION':'PASS','SOURCE_INSTANCE':'PASS' if i not in (2,4) else 'AMBIGUOUS',
            'CONSUMER_DEFINITION':'PASS','CONSUMER_BINDING':'MISSING',
            'PROCESS_DEFINITION':'PASS','PROCESS_BINDING':'MISSING','CURRENTNESS':'MISSING',
            'SCOPE':'PASS','LINEAGE':'PASS','PROVENANCE':'PASS'}
        notes={
            'SOURCE_DEFINITION':'Declarative canonical fixture/capability/oracle interface exists and is retained at its qualified scope',
            'SOURCE_INSTANCE':'Existing qualified native/fixture source instances are present; existence does not establish exact current END operands',
            'CONSUMER_DEFINITION':'END experiment acceptance case and ordered interface declaration exist; it is not a native Action/input-slot API',
            'CONSUMER_BINDING':'Only dependency-name selector exists. No exact current source/native projection is attached to this END input',
            'PROCESS_DEFINITION':'Contract-level projection/runner/comparison obligation exists; no native process entity required',
            'PROCESS_BINDING':'No current concrete process/input/reader invocation manifest for this declared interface',
            'CURRENTNESS':'Binding currentness cannot pass while the current binding is absent; source age alone is not staleness',
            'SCOPE':'Known E2 qualification-only scope and selected composite decision are recorded; no binding authority is inferred from a source hash',
            'LINEAGE':'Actual source contexts are known and remain distinct. This is not a requirement that every component adopt one lineage',
            'PROVENANCE':'Existing sources/result/native selectors have pinned provenance; missing interface relation is not fabricated from them'}
        if i==2:notes['SOURCE_INSTANCE']='Historical generic PC03 phase specimens differ from current F03/P04 boundaries; current local oracles exist but the exact END oracle/operand/process collection is unselected'
        if i==4:notes['SOURCE_INSTANCE']='Qualified protocol and local deterministic reader histories exist; complete current END/native positive/negative/process input matrix is not yet an identified instance'
        records.append({'INTERFACE_ID':'E2-END#/dependencies/'+str(i),'DECLARED_NATIVE_INTERFACE_ID':None,
            'ORDINAL':i+1,'SOURCE':name,'TARGET':'E2-END','PURPOSE':purposes[i],
            'PRODUCER':producer[i],'CONSUMER':'E2-END experiment acceptance-case comparison/runner harness',
            'PROCESS':process[i],'REQUIRED_INPUT':input_types[i],
            'REQUIRED_OUTPUT':'Exact pinned current END-consumer projection and process/input binding with independently reviewed comparison obligations; not future PASS evidence',
            'SCOPE':'E2-QUALIFICATION-ONLY; qualification acceptance only','LINEAGE':lineage[i],
            'CURRENTNESS':'Exact source/policy/code/definition support at the stated consumer/checkpoint; completed history is not current execution permission',
            'PROVENANCE':sources,'CONSUMER_DECLARATION':ref(DOCS/(P+'E2_PC04_END.json'),'/dependencies/'+str(i)),
            'SEALED_EDGE_ID':edges[i]['edge_id'],'SEALED_REQUIRED_ASSURANCE':edges[i]['required_assurance'],
            'STATUS':dimensions,'STATUS_EXPLANATIONS':notes,'current_interface_oracle':'FAIL_NOT_BOUND',
            'first_failure_dimensions':['CONSUMER_BINDING','PROCESS_BINDING']})
    save('six-interface-inventory.json',{'count':6,'authoritative_order':expected,'interfaces':records,
        'allowed_dimension_statuses':['PASS','MISSING','STALE','INAPPLICABLE','AMBIGUOUS','NOT_REQUIRED'],
        'dimension_PASS_for_scope_lineage_provenance_does_not_assert_binding_EXISTS':True})

    # Recover PC01 producer and later evolution; do not execute its historical
    # temporary-fixture constructor or any current native planner path.
    source=read(DOCS/(P+'E2_PC01_SOURCES.json'))
    native_initial=read(DOCS/(P+'E2_P02_INITIAL_SNAPSHOT.json'))['snapshot']
    target=read(DOCS/(P+'E2_P04_CANONICAL_TARGET_BUNDLE_1.json'))['bundle']
    action_ids=[a['id']['value'] for a in native_initial['actions']]
    assert sorted(action_ids)==sorted(d['id'] for d in source['declarations']) and len(action_ids)==6
    native_actions=[{'ActionId':a['id']['value'],'native_selector':ref(DOCS/(P+'E2_P02_INITIAL_SNAPSHOT.json'),'/snapshot/actions/'+str(i)),
                     'definition_provenance':a['source']} for i,a in enumerate(native_initial['actions'])]
    installed=[]
    for index,event in enumerate(target['events']):
        if event['result'].get('$type')=='InstallDefinition':
            installed.append({'sequence':event['sequence'],'event_identity':event['identity'],
                'event':ref(DOCS/(P+'E2_P04_CANONICAL_TARGET_BUNDLE_1.json'),'/bundle/events/'+str(index)),
                'definition':event['result']['definition'],'authority':event['result']['authority']})
    save('PC01-current-artifact-search.json',{
        'source_definition':ref(DOCS/(P+'E2_PC01_SOURCES.json')),
        'source_definition_registry':ref(DOCS/(P+'E2_PC01_SOURCE_ROLES.json')),
        'native_Action_candidates':ref(DOCS/(P+'E2_PC01_FIXTURES.json'),'/native_actions'),
        'historical_baseline_identity_report':ref(DOCS/(P+'E2_PC01_COMPLETION_1_WHOLE_MODEL.json')),
        'historical_reported_snapshot_id':'planner-snapshot-v1:2e37f24a86b2a5e5f03d23a33a90973d2f19008a2eeb1d385085a385f68a2e2d',
        'historical_report_is_a_native_Snapshot_body':False,
        'retained_original_canonical_source_instance':ref(DOCS/(P+'E2_P02_INITIAL_SNAPSHOT.json'),'/snapshot'),
        'retained_original_canonical_Snapshot_id':'planner-snapshot-v1:'+sha(DOCS/(P+'E2_P02_INITIAL_SNAPSHOT.json')),
        'retained_actions':native_actions,
        'current_qualified_P04_model_source':ref(DOCS/(P+'E2_P04_CANONICAL_TARGET_BUNDLE_1.json'),'/bundle/current'),
        'current_P04_Snapshot_id':'planner-snapshot-v1:046fdc270a0060503729151368a68672f76af122830b86e65d372e6bc5d7dea4',
        'historical_baseline_is_current_P04_Snapshot':False,'governed_configuration_history':installed,
        'consumer_definition':ref(DOCS/(P+'E2_PC04_END.json')),
        'historical_dependency_audit':ref(DOCS/(P+'E2_PC04_RESULT.md')),
        'producer_process_code':ref(DOCS/(P+'E2_PC01_WHOLE_MODEL_ORACLE.py')),
        'historical_generic_evidence_binding_code':ref(ROOT/'docs/plans/qualification/E2_P05_END_INPUT_BINDING_1/bind_artifacts.py'),
        'current_consumer_binding_found':False,'current_process_binding_found':False,
        'current_interface_first_failure':records[0],
        'minimum_closure_is_not_fixture_rebuild_or_native_install':True})
    pc01={'PC01_ID':'E2-PC01','PC01_TYPE':'FIXTURE / qualification preparation package, not a native Planner Action',
        'earliest_definition':ref(DOCS/(P+'E2_P01_REMAINING_BLOCKERS_1.md'),line=120),
        'PC01_PURPOSE':'Close E2-G02/G03: six full O01/native prospective definitions plus source/identity/policy registry and baseline model composition',
        'PC01_PRODUCER':'Definition/source authorship and pinned definition/whole-model qualification oracles',
        'PC01_OUTPUT':['six complete native Action definitions','78 O01 cells','canonical model/reference closure',
                       'supported policy and baseline source-role registry','definition/model admission and identity evidence'],
        'PC01_SEMANTICS':'Prospective result inventories are definitions; no actual Knowledge/result/event/authority follows from their presence',
        'PC01_AUTHORITY':'Bounded E2 qualification-only source/definition authorship; no native Action/Architect/INSTALL/USE grant issued by PC01',
        'PC01_SCOPE':source['scope'],'PC01_LINEAGE':source['lineage'],'generation':source['generation'],
        'PC01_PROVENANCE':ref(DOCS/(P+'E2_PC01_SOURCES.json')),
        'historical_qualification_evolution':[
            ref(DOCS/(P+'E2_PC01_RESULT.md')),ref(DOCS/(P+'E2_PC01_COMPLETION_1.md')),
            ref(DOCS/(P+'E2_PC01_EXIT_RECONCILIATION_1.json')),ref(DOCS/(P+'E2_P01_RETRY_1_RESULT.json'))],
        'definition_exists':True,'native_source_instance_exists':True,'current_END_process_binding_exists':False}
    save('PC01-definition.json',pc01)

    consumer={'END_INPUT_ID':'E2-END#/dependencies/0','END_TYPE':'EXPERIMENT_ACCEPTANCE_CASE',
        'EXPECTED_TYPE':'canonical definitions/model: complete six-Action O01/native model projection plus source/policy/reference support',
        'EXPECTED_SOURCE':records[0]['SOURCE'],'EXPECTED_PROCESS':records[0]['PROCESS'],
        'consumer_authority_sources':[ref(DOCS/(P+'E2_PC04_END.json'),'/dependencies/0'),
            ref(REC/'END-qualification-oracle.json','/six_interfaces_and_process_inputs'),
            ref(ROOT/'docs/plans/qualification/E2_P05_END_INPUT_BINDING_1/dependency-DAG.json')],
        'SATISFACTION_RULE':'Exact current source/model projection bound to this declared END interface and selected composite acceptance, with concrete process/input manifest; READY/source presence alone fails',
        'CURRENTNESS_RULE':'Source/action-definition/policy support current at their exact historical or current consumer boundary; changed governed Action definitions must be resolved through their actual installation history',
        'SCOPE_RULE':'Use the exact already-qualified E2-only source/consumer scopes and selected aggregate mapping; no new native permissions',
        'LINEAGE_RULE':'Retain original baseline and each authorized component/P04 context; never retag, splice or equate same-name native records',
        'PROVENANCE_RULE':'Native Snapshot/Action/event selectors and source/code/policy hashes; report/prose inventory IDs do not replace native source instances',
        'native_END_input_slot_API_exists':False,'native_END_ledger_event_required':False}
    save('END-PC01-consumer-contract.json',consumer)
    process_contract={'kind':'READ_ONLY_QUALIFICATION_PROJECTION_AND_AGGREGATION',
        'NATIVE_PROCESS_ID':None,'PROCESS_ID_DEFINED_BY_EARLIEST_CONTRACT':False,
        'process_identity_domains':'Source-code/content hashes and qualification invocation/input manifest identities; not native Action/Event/Authority IDs',
        'producer_function_is_not_END_consumer_process':'PC01 whole-model oracle build/qualify produces/checks a fixture; running it again does not supply an END consumer binding',
        'existing_capabilities':['JSON/native closed typed representation','native model/type/policy/source validation where required',
            'canonical Snapshot/content identity and ordinary qualification source/pointer manifests',
            'read-only evidence graph aggregation and independent process/hash comparisons'],
        'input':'Exact PC01 definition source, included retained model projection(s), authoritative current END input definition, selected aggregate scope and independent comparison contract',
        'output':'One documentary current consumer/process binding manifest and its independent comparisons; no Planner mutation',
        'minimum_steps':['pin exact authoritative source and consumer identities','select qualified native Action/model boundaries without creating a new model',
            'record all six Action-definition/source/reference/policy identities at each required consumer boundary',
            'account for actual authorized definition transitions via existing P04 config events',
            'bind projection to END dependency 0 under the exact aggregate scope',
            'bind executable read-only harness/code hash and exact input/output/reader invocation allowlist',
            'compare source/provenance/scope/currentness and identity independently; reject out-of-scope substitutions'],
        'does_not_include':['native result admission','INSTALL_DEFINITION','proof admission','P05 execution','full native lineage manufacture'],
        'process_binding_current_status':'MISSING','generic_native_adapter_required':False,
        'contract_detail_type':'Minimum future fixture/process contract recovered from current END requirements; not an applied binding or newly executed process'}
    save('PC01-process-contract.json',process_contract)
    authority={'semantic_acceptance':{'status':'EXISTING_APPLIES_WITHIN_BOUNDARY',
        'capture':ref(QUAL/'scope-authentication.json'),
        'option':'AUTHORIZE_COMPOSITE_P05_END_QUALIFICATION_MAPPING',
        'subject':'qualification-scope-subject-v1:12b2e68bea4d28c8da2cd35e15b9cb704b153288df40360ed0dc33e414402256',
        'limit':'Document/pin a required interface projection from already included qualified sources without changing graph/stages/four bridges/claims/exclusions'},
        'INSTALL_configuration':{'status':'NOT_REQUIRED','reason':'No native definition/current Action/state change is needed to create a documentary END interface manifest'},
        'runtime_USE_or_execution':{'status':'NOT_REQUIRED','reason':'The read-only consumer/process binding is not a native permission, result, event or Action'},
        'new_authority_required':False,'authority_issued':False,
        'must_stop_for_new_authority_or_contract_change':'If new source semantics, unqualified model generation, different graph/bridge/evidence subject or new native grant/state installation is required, existing scope does not apply'}
    save('PC01-authority-requirement.json',authority)
    minimum={'STATUS':'CONTRACT_ONLY_NOT_MATERIALIZED_OR_APPLIED',
        'source':{'definition':ref(DOCS/(P+'E2_PC01_SOURCES.json')),
            'included_native_original_model':ref(DOCS/(P+'E2_P02_INITIAL_SNAPSHOT.json'),'/snapshot'),
            'included_canonical_current_model':ref(DOCS/(P+'E2_P04_CANONICAL_TARGET_BUNDLE_1.json'),'/bundle/current'),
            'selection_rule':'Choose the exact included definition/model projection(s) needed by the consumer; preserve each native context and do not run a constructor to replace retained source bytes'},
        'consumer':consumer,'process':process_contract,
        'binding':'Computed read-only qualification evidence manifest with exact native selectors plus source/code/policy/consumer and reader process inputs; not a native persisted entity',
        'identity':{'source_identities':'Exact raw content and native Snapshot/Action definition identities retained above',
            'consumer_edge_id':edges[0]['edge_id'],
            'consumer_selector':ref(DOCS/(P+'E2_PC04_END.json'),'/dependencies/0'),
            'composite_base_graph_id':'qualification-END-evidence-graph-v1:d3979240252a12139aac34db1bb1cb2396c6860af371084b94118740ec23af15',
            'selected_acceptance_mapping_id':'qualification-composite-END-acceptance-v1:6c37715a38233e9f556279e182bb3a13d5f03579257e20d787a858c5d246941c',
            'future_manifest_identity_rule':'Canonical qualification-manifest content comparison; include all selected source/consumer/process/input facts; no actual binding identity is minted in this contract-only package'},
        'scope':'E2-QUALIFICATION-ONLY / exact existing aggregate acceptance scope',
        'lineage':'Record each source/presentation/consumer native context explicitly; the manifest has documentary qualification identity, no synthesized native lineage',
        'provenance':'Exact original/native/governed version source selectors and read-only program/input/expected comparison file roles',
        'currentness':'Complete consumer-specific definition/version/source/policy applicability at exact boundaries; no blanket old-baseline retagging or required-currentness inferred from completed Action state',
        'authority':authority,
        'minimum_manifest_fields':['declared interface selector and edge ID','consumer graph/scope authentication identity',
            'source definition bytes/selector/content identity','retained native model/Snapshot selector/identity/context',
            'all six exact Action definition/reference/result-contract/source projections','supported policy source/version/content identity',
            'actual governed definition version/history refs where applicable','historical/current consumer role for each projection',
            'read-only process code/version/content pin and exact invocation','writer/input/expected comparison/reader allowlists and trusted identities',
            'independent type/model/currentness/source/provenance comparisons','declaration/result/selection/permission separation and exclusion labels'],
        'independent_negative_oracles':['wrong source/model identity','wrong native identity domain','missing/extra Action','wrong Action definition version',
            'historical source promoted to different current context','wrong policy pin/version','wrong scope/lineage/provenance',
            'changed prerequisite or result contract hidden in projection','expected comparator used as Planner input',
            'producer oracle output used as its own consumer oracle','missing concrete invocation/reader input','native permission/result/ledger inferred from manifest'],
        'no_code_or_binding_created_here':True,'implementation_required':False,'new_native_binding_adapter_required':False,
        'future_fixture_manifest_and_harness_glue_authoring':'Required ordinary qualification input preparation using existing primitives; does not establish a new native capability requirement',
        'advance_rule':'After PC01 is separately materialized and independently qualifies, rerun all six interface dimensions in their authoritative order and advance only to the next first failure'}
    save('minimum-PC01-closure-contract.json',minimum)
    save('remaining-five-classification.json',{'classification':[
        {'interface':r['SOURCE'],'dimensions':r['STATUS'],'common_generic_need':'Exact documentary consumer/process manifest, source identity/context/currentness projection',
         'independent_contract_need':r['PROCESS'],'first_failure':'CONSUMER_AND_PROCESS_BINDING_MISSING',
         'additional_specific_limit':'Phase oracle/current-state compatibility requires separate selection; old POST_REENTRY scaffold is not silently substituted for current deferred-install boundary' if r['ORDINAL']==3 else
             'Full positive/negative process operands and current reader inputs remain independently required' if r['ORDINAL']==5 else
             'Qualified capability instance/history remains consumer-bound; no native execution authorized by manifest',
         'no_repair_performed':True} for r in records[1:]],
        'one_common_native_adapter_defect_proven':False,'generic_framework_is_documentary_manifest_composition':True,
        'same_structure_does_not_make_all_independent_native_contracts_equal':True})
    usage=inventory_usage()
    save('root-cause-and-readiness.json',{'RESULT':'PASS_CONTRACT_RECOVERY_ONLY','FIRST_UNRESOLVED_INTERFACE':'E2-PC01 -> E2-END',
        'FIRST_FAILING_BINDING_TERM':'CONSUMER_BINDING_MISSING; no exact current PC01 source-instance/model projection attached to declared END dependency 0',
        'related_process_failure':'PROCESS_BINDING_MISSING; no concrete current invocation/input/reader manifest',
        'primary_classification':'CONSUMER_AND_PROCESS_BINDING_MISSING','ROOT_CAUSE':'MISSING_FIXTURE_BINDING',
        'historical_PC01_END_relation_exists':True,'historical_relation_kind':'PC04 dependency/preflight audit and earlier package consumption; not a current concrete END consumer/process manifest',
        'old_snapshot_hash_or_same_name_not_current_binding':True,'binding_representation':'COMPUTED_DOCUMENTARY_QUALIFICATION_MANIFEST',
        'native_END_binding_API_or_new_Object_required':False,'INSTALL_required':False,
        'AUTHORITY_REQUIREMENT':authority,'GENERIC_CAPABILITY_IMPACT':'No generic runtime/INSTALL defect established. Missing exact qualification fixture/process operands are shared, while native interface contracts remain distinct.',
        'DECISION_REQUIRED':'NO','DECISION_READY':'NO_NOT_REQUIRED','IMPLEMENTATION_REQUIRED':'NO',
        'IMPLEMENTATION_READY':'NO_NOT_REQUIRED; ordinary fixture manifest preparation remains future work',
        'PC01_later_reference_artifacts_inventoried':usage['matching_artifacts'],
        'P05_STAGE_BINDINGS':'13/13','FOUR_SEMANTIC_BRIDGES':'PASS','AGGREGATE_N12':'PASS','AGGREGATE_N13':'PASS',
        'closed_qualification_results_revisited_or_reexecuted':False,'COMPOSITE_P05_END_QUALIFICATION':'FAIL',
        'P05_EXECUTION_READY':'NO','P05_EXECUTED':'NO','P06_EXECUTED':'NO','bindings_modified':0,
        'RUNTIME_MODIFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','N_REAL_SATISFIED':'NO',
        'NEXT_PACKAGE':'E2-P05 PC01 -> END CURRENT QUALIFICATION-MANIFEST MATERIALIZATION + INDEPENDENT PREFLIGHT'})
    print(json.dumps({'RESULT':'PASS_CONTRACT_ONLY','interfaces':6,'first_interface':'E2-PC01 -> E2-END',
        'root_cause':'MISSING_FIXTURE_BINDING','implementation_required':'NO','decision_required':'NO','PC01_reference_artifacts':usage['matching_artifacts'],
        'bindings_modified':0,'P05_EXECUTION_READY':'NO'}))


if __name__=='__main__':main()
