"""Select sealed source operands without invoking any native transaction."""
from common import *
inv = read(DOCS/'qualification/E2_P05_END_INTERFACE_CLOSURE_1/six-interface-inventory.json')['interfaces'][3]
equal('T01 ordinal', inv['ORDINAL'],4); equal('T01 input',inv['INTERFACE_ID'],INPUT)
check_refs(inv)
man=read(SOURCE/'checkpoint-manifests.json')['post-a09']
bundle_path=Path(man['path'])
raw=read(bundle_path)['bundle']; cmd=read(SOURCE/'a09-command.json')
sel=dict(schema='T01-END-SOURCE-SELECTION-1', primary_sources=inv['PROVENANCE'],
    native_bundle=ref(bundle_path), restore_manifest={k:v for k,v in man.items() if k!='semantic_oracle'},
    command=ref(SOURCE/'a09-command.json'), boundary_oracle=ref(SOURCE/'boundary-checks.json','/A09'),
    independent_oracle=ref(ROOT/man['oracle_source']), capability=ref(DOCS/(PREFIX+'E2_T01_VALIDATION.json')),
    api=['adapter.planner.codec.restore','adapter.planner.codec.admit_external_evidence','EvidenceSourceAdmission','ExternalEvent:EVIDENCE_RECEIVED'],
    native_code=[ref(p) for p in sorted((ROOT/'adapter/planner').glob('*.py'))],
    context=raw['current']['context'], policy=raw['policy'],
    authoritative_context=[ref(p) for p in sorted(DOCS.glob('*CANONICAL*EXPERIMENT*')) if p.is_file()],
    lifecycle=[ref(DOCS/(PREFIX+n)) for n in ['E2_T04_RESULT.json','E2_P03_T01_A_ATTESTOR_AUTHORITY_RESULT.json','E2_P03_T01_A_ATTESTOR_AUTHORITY_DOSSIER_1.json','E2_P03_T01_B_EVENT_ANCESTRY_RESULT.json','GENESIS_G04_RESULT.json','E2_P03_T01_TRUST_ANCESTRY_CLOSURE_1.json','E2_P03_T01_C_SOURCE_PROVENANCE_RESULT.json','EVIDENCE_E01_MATERIALIZER_RESULT.json','EVIDENCE_E02_ATTESTATION_RESULT.json','E2_P03_T01_D_LIVE_ADMISSION_RESULT.json']],
    acceptance_matrix=[ref(p) for p in sorted(DOCS.glob('*ACCEPTANCE*')) if p.is_file()])
save('source-selection.json',sel)
contract=dict(T01_INTERFACE_ID=inv['INTERFACE_ID'], T01_PURPOSE=inv['PURPOSE'],
    SOURCE_TYPE='Qualified native ingress capability plus retained event-bearing canonical post-A09 PersistenceBundle',
    REQUIRED_SOURCE=inv['REQUIRED_INPUT'], RESTORE_REQUIREMENT='Fresh native restore of exact retained post-A09 bundle, source pins, ledger artifacts and Snapshot; no Evidence transaction',
    END_CONSUMER=inv['CONSUMER'],END_INPUT=inv['INTERFACE_ID'],PROCESS=inv['PROCESS'],
    SATISFACTION_RULE=inv['REQUIRED_OUTPUT'],CURRENTNESS_RULE=inv['CURRENTNESS'],
    SCOPE=inv['SCOPE'],LINEAGE=inv['LINEAGE'],PROVENANCE=inv['PROVENANCE'],recovered_declaration=inv,
    post_restore_explanation='Original E2-T01 qualified cold-restored waiting-state admission capability. Sealed END interface consumes its actual canonical A09 input/post-state witness. This work restores the retained complete receipt boundary, without repeating admission.',
    terminal_boundary='Canonical P04 retry-1 post-a09: events 10 EvidenceSourceAdmission and 11 EVIDENCE_RECEIVED; before A10 validation/support',
    earlier_T01_D='Historical P03 receipt bundle 245c3516... is lifecycle provenance only; it is not the sealed current A09 operand')
save('recovered-contract.json',contract)
defn=dict(schema='T01-END-EXPLICIT-COLD-RESTORE-PROCESS-1',consumer=INPUT,
    recovered_process=inv['PROCESS'],steps=['retained canonical event-bearing post-A09 bundle','native codec.restore in fresh reader','bounded post-restore projection','explicit invocation/input manifest','independent term-by-term oracle comparison','E2-END dependency 3'],
    restore=dict(api='adapter.planner.codec.restore',path=sel['native_bundle'],expected_bundle=man['bundle_id'],repo_root=str(ROOT)),
    code=[ref(OUT/n) for n in ['common.py','binding.py','oracle.py','prepare.py','qualify.py']],
    native_code=sel['native_code'],interpreter=dict(path=sys.executable,version=sys.version),
    environment=dict(PYTHONDONTWRITEBYTECODE='1',PYTHONPATH='.',PYTHONHASHSEED=[0,1,7,101]),
    invocation=[sys.executable,str((OUT/'binding.py').relative_to(ROOT)),'reader','PRESENTATION'],
    unordered_presentations=['original','reversed','rotated'],readers_per_seed_presentation=2,
    native_mutating_calls=[],historical_replay='Read-only native restore validates committed history; no transaction/commit/install/authority issuance')
save('process-binding.json',dict(definition=defn,identity=qid('process',defn)))
print('SOURCE_CONTRACT_AND_PROCESS_PINNED')
