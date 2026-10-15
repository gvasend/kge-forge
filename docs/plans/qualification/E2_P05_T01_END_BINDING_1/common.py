"""Read-only documentary binding; native restore validates retained history."""
import hashlib
import json
import sys
from dataclasses import fields, is_dataclass, replace
from pathlib import Path
from adapter.planner import codec as c, core, model as m

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
DOCS = ROOT / 'docs/plans'
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'
SOURCE = DOCS / 'qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1'
INPUT = 'E2-END#/dependencies/3'

def read(path):
    return json.loads(Path(path).read_bytes())

def ref(path, pointer=''):
    path = Path(path)
    return dict(path=str(path.relative_to(ROOT)), pointer=pointer,
                raw_sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def save(name, value):
    (OUT / name).write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')

def qid(kind, value):
    return 'qualification-T01-END-' + kind + '-v1:' + hashlib.sha256(c.canonical_bytes(value)).hexdigest()

def equal(name, actual, expected):
    if actual != expected:
        raise m.PlannerError(name + ': term mismatch')

def check_refs(value):
    if isinstance(value, dict):
        if set(('path','raw_sha256')).issubset(value):
            equal('source pin ' + value['path'], ref(ROOT / value['path'])['raw_sha256'], value['raw_sha256'])
        for child in value.values(): check_refs(child)
    elif isinstance(value, list):
        for child in value: check_refs(child)

def contract():
    return read(OUT / 'recovered-contract.json')

def process():
    return read(OUT / 'process-binding.json')

def selection():
    return read(OUT / 'source-selection.json')

def permutation(value, form):
    """Permute only fields declared unordered by the native codec."""
    if is_dataclass(value):
        updates = {}
        for f in fields(value):
            item = permutation(getattr(value, f.name), form)
            if f.name in c.SET_FIELDS.get(type(value), set()) and isinstance(item, tuple):
                if form == 'reversed': item = tuple(reversed(item))
                if form == 'rotated' and item: item = item[1:] + item[:1]
            updates[f.name] = item
        return replace(value, **updates)
    if isinstance(value, tuple): return tuple(permutation(x, form) for x in value)
    return value

def restore(form='original'):
    sel = selection()
    check_refs(sel)
    man = sel['restore_manifest']
    b = c.restore(ROOT / sel['native_bundle']['path'], c._unwire(man['bundle_id']), ROOT)
    equal('T01 exact Snapshot', c._wire(c.snapshot_id(b.current)), man['state_id'])
    equal('T01 event count', len(b.events), man['event_count'])
    equal('T01 append head', c._wire(b.events[-1].identity), man['head'])
    return permutation(b, form)

def metadata():
    return dict(contract=contract(), process=process(), source_selection=selection(),
                consumer=INPUT, kind='QUALIFICATION_EVIDENCE_ONLY',
                currentness='Exact retained A09 boundary; verified current source/policy/code pins; historical occurrence is not permission',
                excluded=['A10 validation/support/accepted observation', 'A11 proof/reentry',
                          'A12 Knowledge/Action result', 'A13 root/slot/FINISH'],
                semantic_order='Native SET_FIELDS canonicalized; event ancestry strictly ordered')

def envelope(terms):
    body = dict(metadata(), terms=terms)
    return dict(body=body, identity=qid('projection', body))

def rows(projection, values):
    sel = selection()
    result = []
    for name, typ, artifact, value in values:
        result.append(dict(INPUT_ID=name, EXPECTED_TYPE=typ, SOURCE_ARTIFACT=artifact,
            SOURCE_IDENTITY=artifact.get('raw_sha256', projection['identity']), EXPECTED_VALUE=value,
            RESTORE_SOURCE=sel['native_bundle'], PROJECTION_IDENTITY=projection['identity'],
            CONSUMER=INPUT, PROCESS=process()['identity'], SCOPE=contract()['SCOPE'],
            LINEAGE=sel['context'], PROVENANCE=sel['primary_sources'],
            CURRENTNESS=projection['body']['currentness']))
    body = dict(consumer=INPUT, process=process()['identity'], inputs=result)
    return dict(body=body, identity=qid('manifest', body))

def manifest(projection):
    sel = selection(); t = projection['body']['terms']
    values = [('RETAINED_BUNDLE', 'PersistenceBundle', sel['native_bundle'], t['bundle']),
        ('QUALIFIED_API', 'PinnedNativeAdmissionCapability', sel['capability'], sel['api']),
        ('SEALED_END_CONTRACT', 'RecoveredENDInterfaceContract', ref(OUT/'recovered-contract.json'), contract()),
        ('A09_COMMAND', 'EvidenceSourceAdmission', sel['command'], t['ingress_operand']),
        ('A09_SNAPSHOT', 'SnapshotIdentity', sel['native_bundle'], t['snapshot']),
        ('EVIDENCE', 'GraphEntity:EVIDENCE', sel['native_bundle'], t['evidence']),
        ('ATTESTATION', 'EvidenceAttestationOperand', sel['command'], t['attestation_operand']),
        ('RECEIPT', 'ReceiptAdmission', sel['native_bundle'], t['receipt']),
        ('EVENT_ANCESTRY', 'OrderedExecutionEvents', sel['native_bundle'], t['ancestry']),
        ('LEDGER_ROOT_HEAD', 'LedgerRootAndAppendHead', sel['native_bundle'], [t['ledger_root'],t['append_head']]),
        ('SOURCE_POLICY_PINS', 'CanonicalUnorderedArtifactPins', sel['native_bundle'], [t['sources'],t['policy']]),
        ('POST_RESTORE_ORACLE', 'T01ReceivedBoundaryOracle', sel['boundary_oracle'], t['post_restore']),
        ('CONTEXT', 'EvaluationContext', sel['native_bundle'], t['context']),
        ('END_PROJECTION', 'QualificationProjection', ref(OUT/'source-selection.json'), projection['identity']),
        ('PROCESS_BINDING', 'ExplicitColdRestoreProcess', ref(OUT/'process-binding.json'), process())]
    return rows(projection, values)
