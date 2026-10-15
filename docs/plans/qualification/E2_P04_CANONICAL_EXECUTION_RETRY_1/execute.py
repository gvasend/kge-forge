"""One canonical P04 execution. Consume sealed inputs; stop without repair."""
import hashlib
import json
import os
import sys
import traceback
from dataclasses import replace
from pathlib import Path

from adapter.planner import codec as c, core, gates, model as m
from adapter.planner import evidence_attestation as ea, evidence_transaction as tx
from adapter.planner import validation_transaction as vt, installation as i
from adapter.planner import proof_installation as pi, typed_proofs as tp
from adapter.tests.qualify_finish_f03 import semantic_view, save, computation_wire
from adapter.tests.qualify_p04_a09_control import view
from adapter.tests.test_planner_typed_proofs import candidate

R = Path(__file__).resolve().parents[4]
D = R / 'docs/plans'
O = Path(__file__).resolve().parent
F = D / 'qualification/FINISH_F03_1'
Q = D / 'qualification/FINISH_F02_1'
P = 'DETERMINISTIC_PLANNER_V0_1_'
STORE = O / 'canonical-store'
ENTRY = D / (P + 'E2_P04_FINAL_PREEXECUTION_CONFIGURATION_BUNDLE_1.json')
TARGET = D / (P + 'E2_P04_CANONICAL_TARGET_BUNDLE_1.json')


def read(path):
    return c.parse_json(path.read_bytes())


def uid(x):
    return x.namespace + ':' + x.sha256


def emit(name, value):
    (O / name).write_bytes(c.canonical_bytes(value))


def report_value(value):
    if isinstance(value, bytes):
        return {'sha256': hashlib.sha256(value).hexdigest(), 'byte_length': len(value)}
    if isinstance(value, dict):
        return {k: report_value(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [report_value(x) for x in value]
    if value is None or type(value) in (str, bool, int):
        return value
    return computation_wire(value)


class Divergence(Exception):
    pass


class Run:
    def __init__(self):
        self.bundle = None
        self.stage = 'ENTRY'
        self.trace = []
        self.manifests = {}
        self.checks = {}
        self.first = None
        self.refs = read(F / 'isolated-checkpoints.json')
        self.oracles = read(Q / 'boundary-oracles.json')['oracles']

    def need(self, name, expected, actual):
        passed = expected == actual
        self.checks.setdefault(self.stage, {})[name] = {'expected': report_value(expected), 'actual': report_value(actual), 'pass': passed}
        if not passed:
            self.first = {'stage': self.stage, 'FIRST_COUNTEREXAMPLE': name,
                          'EXPECTED': report_value(expected), 'ACTUAL': report_value(actual),
                          'STATE': uid(c.snapshot_id(self.bundle.current)) if self.bundle else None,
                          'EVENT': uid(self.bundle.events[-1].identity) if self.bundle else None,
                          'CLASSIFICATION': 'SEALED_ORACLE_DIVERGENCE'}
            raise Divergence(name)

    def compare_reference(self, name, bundle):
        man = self.refs[name]
        raw = Path(man['path']).read_bytes()
        self.need('trusted_F03_reference_bytes', man['bundle_id'], c._wire(c._identity(raw, 'planner-bundle-v1')))
        self.need('exact_qualified_snapshot', man['state_id'], c._wire(c.snapshot_id(bundle.current)))
        self.need('exact_qualified_append_head', man['head'], c._wire(bundle.events[-1].identity))
        self.need('exact_qualified_bundle_bytes', raw, c._bundle_bytes_admitted(bundle))
        oracle = read(F / ('reader-manifests/' + name + '.json'))['semantic_oracle']
        self.need('complete_sealed_Computation_sources_policy_context', oracle, semantic_view(bundle))

    def checkpoint(self, name, before, after, operands=None):
        self.bundle = after
        self.compare_reference(name, after)
        path = O / 'checkpoints' / name / (name + '.json')
        path.parent.mkdir(parents=True, exist_ok=True)
        man = save(after, path)
        man['semantic_oracle'] = read(F / ('reader-manifests/' + name + '.json'))['semantic_oracle']
        man['oracle_source'] = str((F / ('reader-manifests/' + name + '.json')).relative_to(R))
        man['writer_terminated'] = True  # Readers run only after this writer exits.
        self.manifests[name] = man
        self.trace.append({'stage': self.stage, 'checkpoint': name,
            'pre_state': uid(c.snapshot_id(before.current)), 'post_state': uid(c.snapshot_id(after.current)),
            'parent': uid(before.events[-1].identity), 'head': uid(after.events[-1].identity),
            'events': [c._wire(e) for e in after.events[len(before.events):]],
            'operands': operands, 'control': core.recompute(after.current).control.value,
            'checks': self.checks[self.stage], 'canonical_commit': True})
        emit('execution-trace.json', self.trace)
        emit('checkpoint-manifests.json', self.manifests)
        emit('boundary-checks.json', self.checks)
        print(self.stage + ' PASS ' + uid(after.events[-1].identity), flush=True)

    def boundary(self, label, bundle):
        expected = self.oracles[label]
        s = bundle.current
        comp = core.recompute(s)
        fin = next(a for a in s.actions if a.id.value == 'E2-FINISH')
        st = next(x for x in comp.statuses if x.id == fin.id)
        self.need(label + '.control', expected['control'], comp.control.value)
        self.need(label + '.slot', expected['slot'], s.slots[0].state.value)
        self.need(label + '.root', expected['root'], s.roots[0].state.value)
        self.need(label + '.proofs', sorted(x['sha256'] for x in expected['typed_proofs']), sorted(x.id.sha256 for x in s.typed_proofs))
        self.need(label + '.goals', expected['goal_inventory'], c._wire(s.goals))
        self.need(label + '.source_configuration_current', True, all(i.current(bundle, x) for x in pi.records(s, 'ROOT_SLOT_CONFIGURATION_SET')))
        self.need(label + '.proof_usability', True, all(tp.usable(s, x) for x in s.typed_proofs))
        self.need(label + '.actual_REENTER_completed', True, gates.current_completion(s, m.ActionId('E2-REENTER')))
        reenter = next(a for a in s.actions if a.id.value == 'E2-REENTER')
        self.need(label + '.actual_K_REENTER', c._wire(reenter.accepted_inventory[0]),
                  c._wire(next(k for k in s.knowledge if k.id.value == 'E2-K-REENTER')))
        self.need(label + '.unrelated_completed', True, all(x.state is m.ActionState.COMPLETED for x in s.statuses if x.id != fin.id))
        if label in ('POST_A12_PRE_SUPPORT', 'POST_SUPPORT', 'POST_SLOT_PROOF'):
            self.need(label + '.nonterminal_FINISH_hold', True,
                      st.state is m.ActionState.BLOCKED and not st.terminal_failure and not fin.blocked_terminal)
            self.need(label + '.FINISH_not_executed', False, gates.current_completion(s, fin.id))
        elif label in ('POST_ROOT_PROOF', 'POST_ROOT_SATISFACTION', 'PRE_FINISH'):
            self.need(label + '.FINISH_selected', 'E2-FINISH', comp.selection.selected.value)
            self.need(label + '.FINISH_not_executed', False, gates.current_completion(s, fin.id))
        else:
            self.need(label + '.FINISH_completed', True, gates.current_completion(s, fin.id))
            self.need(label + '.actual_K_FINISH', expected['knowledge_added'],
                      c._wire(tuple(k for k in s.knowledge if k.id.value == 'E2-K-FINISH')))
            self.need(label + '.all_declared_goals_proven', True,
                      all(g.target in {r.id for r in s.roots if r.state is m.ConditionState.SATISFIED} for g in s.goals))
            self.need(label + '.all_actions_completed', True, all(x.state is m.ActionState.COMPLETED for x in s.statuses))
            self.need(label + '.no_further_action', [], c._wire(comp.actionable))

    def install(self, index):
        b = self.bundle
        step = read(Q / 'bounded-installation-workflow.json')['steps'][index]
        r = c._unwire(read(F / ('install-request-' + str(index) + '.json')))
        audit = read(D / 'qualification/E2_P04_DEFERRED_INSTALLATION_RECONCILIATION_1/authorization-verification.json')
        witness = audit['deferred_install_audits'][index - 2]
        expected = step['definition']
        descriptor, body = pi.descriptor(r.definition)
        self.need('exact_deferred_definition', expected['definition_id'], i.simple(r.definition.id))
        self.need('exact_deferred_body_content', expected['body']['content_id'], descriptor['content_id'])
        self.need('exact_deferred_type', expected['definition_type'], descriptor['definition_type'])
        self.need('exact_operation', 'INSTALL', r.operation.value)
        self.need('exact_old_reference', None, r.expected_old_reference)
        self.need('already_issued_exact_authority', witness['existing_qualified_authority_id'], uid(r.authority.id))
        self.need('exact_existing_authority_receipt', read(F / ('install-authority-' + str(index) + '.json')),
                  c.parse_json(r.authority.admission_provenance.excerpt.encode()))
        self.need('actual_current_parent', r.expected_parent_event, b.events[-1].identity)
        self.need('actual_current_prestate', r.expected_snapshot, c.snapshot_id(b.current))
        self.need('actual_current_bundle', r.expected_bundle, c.bundle_id(b))
        self.need('exact_scope_lineage_generation', [descriptor[k] for k in ('scope', 'lineage', 'generation')],
                  [getattr(b.current.context, k) for k in ('scope', 'lineage', 'generation')])
        i.validate_authority(r, b.current.context)
        i.validate_prefix(b, r)
        self.need('authority_and_parent_preflight', True, True)
        # This consumes existing F03 authority/receipt; no admit_authority call.
        result, bid, noop = i.commit(b, r, STORE, R, expected_authority=r.authority.id,
                                    expected_decision=i.identity(c.parse_json(r.authority.grant_json.encode())['decision_id']))
        self.bundle = result
        self.need('exactly_one_new_INSTALL_event', 1, len(result.events) - len(b.events))
        self.need('not_duplicate_retry', False, noop)
        self.need('installed_contract_current', True, pi.contract_current(result.current, c._unwire(body['contract'])))
        self.need('proof_count_unchanged', len(b.current.typed_proofs), len(result.current.typed_proofs))
        self.need('no_Action_state_change', c._wire(b.current.statuses), c._wire(result.current.statuses))
        self.need('no_slot_root_satisfaction_change', c._wire((b.current.slots, b.current.roots)),
                  c._wire((result.current.slots, result.current.roots)))
        name = 'slot-contract' if index == 2 else 'root-contract'
        self.checkpoint(name, b, result, c._wire(r))
        # Read-only same-process restore additionally checks publication; cold
        # independent readers run after the canonical writer has terminated.
        restored = c.restore(STORE / ('bundle-' + bid.sha256 + '.json'), bid, R)
        self.need('published_install_bundle_restore', c._bundle_bytes_admitted(result), c._bundle_bytes_admitted(restored))
        self.bundle = restored

    def execute(self):
        self.need('entry_reader_25_checks', True, all(read(O / 'entry-reader.json')['checks'].values()))
        recon = read(D / (P + 'E2_P04_DEFERRED_INSTALLATION_RECONCILIATION_1.json'))
        self.need('reconciliation_PASS', 'PASS', recon['RESULT'])
        self.need('reconciled_readiness', 'YES', recon['P04_EXECUTION_READY'])
        self.need('exact_two_allowed_steps', [3, 4], recon['RETRY_CONTRACT']['allowed_installation_ordinals'])
        self.need('empty_canonical_execution_store', False, (STORE / 'HEAD.json').exists())
        self.need('canonical_target_not_already_present', False, TARGET.exists())
        f03 = read(D / (P + 'FINISH_F03_RESULT.json'))
        b = c.restore(ENTRY, c._unwire(f03['configuration_bundle']['bundle_id']), R)
        self.bundle = b
        entry_count = len(b.events)
        self.manifests['final-preexecution'] = dict(read(F / 'reader-manifests/final-preexecution.json'))

        self.stage = 'A09'
        prepared = read(D / 'qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1/evidence-binding.json')
        binding = m.SemanticNativeBinding(**{k: c._unwire(v) for k, v in prepared['binding']['fields'].items()})
        template = c._unwire(read(F / 'fresh-a09-candidate.json'))
        request = replace(template, expected_bundle=c.bundle_id(b), expected_snapshot=c.snapshot_id(b.current),
                          expected_parent_event=b.events[-1].identity)
        args = dict(vars(template.attestation_operand.attestation)); args.pop('attestation_id')
        request = tx.bind(request, ea.materialize(**args), binding)
        raw = {p.path: (R / p.path).read_bytes() for p in request.source_additions}
        emit('a09-command.json', c._wire(request))
        trial = c.preflight_external_evidence(b, request, raw, R, expected_binding=binding)
        tx.check_receipt_postcondition(tx.receipt_oracle(b.current, request), trial.current)
        self.compare_reference('post-a09', trial)
        received, _, noop = c.admit_external_evidence(b, request, raw, STORE, R, expected_binding=binding)
        self.bundle = received
        self.need('actual_A09_not_retry', False, noop)
        self.need('preflight_execution_equality', c.snapshot_id(trial.current), c.snapshot_id(received.current))
        self.need('A09_EVIDENCE_NOT_EVALUATED', 'NOT_EVALUATED', next(e for e in received.current.entities if e.id == request.entity.id).validation.value)
        self.need('A09_received_control', 'EXTERNAL_WAIT', core.recompute(received.current).control.value)
        self.need('A09_no_Proof_instances', [], c._wire(received.current.typed_proofs))
        self.need('A09_C03_ineligible', False, core.resume_eligibility(received, R).allowed)
        self.checkpoint('post-a09', b, received, c._wire(request))

        self.stage = 'A10'
        b = self.bundle
        definition = next(r for r in b.current.installed_definitions if i.descriptor(r.request.definition)[0]['definition_type'] == 'VALIDATION_SUPPORT_DEFINITION_SET')
        operand, trial = vt.prepare(b, vt.command(b, request.entity.id, definition.id), R)
        self.compare_reference('post-a10', trial)
        validated, _, noop = vt.commit(b, operand, STORE, R)
        self.bundle = validated
        self.need('actual_A10_not_retry', False, noop)
        self.need('A10_actual_validation_outcome', 'PASS', operand.validation_result.outcome.value)
        self.need('A10_actual_support_accepted', True, operand.support.observation.accepted)
        self.need('A10_C03_ineligible', False, core.resume_eligibility(validated, R).allowed)
        self.need('A10_no_Proof_instances', [], c._wire(validated.current.typed_proofs))
        self.checkpoint('post-a10', b, validated, c._wire(operand))

        self.stage = 'A11'
        b = self.bundle
        proof = gates.obligation_proof(b.current, m.EvidenceId('E2-EXTERNAL-REQUIREMENT'))
        self.need('typed_obligation_Proof', 'PROVED', proof.state.value)
        self.need('pre_event_C03_ineligible', False, core.resume_eligibility(b, R).allowed)
        external_operand = m.ExternalEvent(m.GateId('E2-GATE'), m.ExternalStage.DEPENDENT_ACTION_REENTRY, c.snapshot_id(b.current))
        external, _ = c.commit_event(b, external_operand, STORE, R)
        self.bundle = external
        decision = next(d for d in external.current.decisions if m.ActionId('E2-REENTER') in d.downstream)
        decision_operand = m.DecisionReentry(decision.action, c.snapshot_id(external.current))
        eligible, _ = c.commit_event(external, decision_operand, STORE, R)
        self.bundle = eligible
        resume = core.resume_eligibility(eligible, R)
        self.need('C03_named_resume_actions', ['E2-REENTER'], [a.value for a in resume.actions])
        self.need('E2_REENTER_selected', 'E2-REENTER', core.recompute(eligible.current).selection.selected.value)
        self.need('E2_REENTER_not_executed', False, gates.current_completion(eligible.current, m.ActionId('E2-REENTER')))
        self.checkpoint('post-a11', b, eligible, {'Proof': computation_wire(proof),
                        'events': c._wire((external_operand, decision_operand)), 'C03': c._wire(resume)})

        self.stage = 'A12'
        b = self.bundle
        self.need('current_C03_before_REENTER', ['E2-REENTER'], [a.value for a in core.resume_eligibility(b, R).actions])
        action = next(a for a in b.current.actions if a.id == core.recompute(b.current).selection.selected)
        self.need('native_selected_action', 'E2-REENTER', action.id.value)
        self.need('native_permitted_result', 'PASS', action.accepted_result.value)
        self.need('native_permitted_output', ['E2-K-REENTER'], [k.id.value for k in action.accepted_inventory])
        # Canonical matrix A12 prescribes selected supplied-permitted-result ->
        # append_event. No separate executor/entity identity is invented.
        supplied = m.SuppliedResult(action.id, action.accepted_result, action.accepted_inventory, c.snapshot_id(b.current))
        post, _ = c.commit_event(b, supplied, STORE, R)
        self.bundle = post
        self.need('actual_REENTER_completed', True, gates.current_completion(post.current, action.id))
        self.boundary('POST_A12_PRE_SUPPORT', post)
        self.checkpoint('post-a12', b, post, c._wire(supplied))

        self.stage = 'SLOT_INSTALL'
        self.install(2)
        self.boundary('POST_SUPPORT', self.bundle)

        self.stage = 'SLOT_PROOF'
        b = self.bundle
        sc = next(x for x in b.current.proof_contracts if x.proof_type is m.TypedProofKind.SLOT_PROOF)
        p = candidate(sc)
        self.need('actual_knowledge_support_fingerprint', sc.support_identities[0], tp.support_identity(b.current, sc.supports[0]))
        self.need('slot_proof_oracle', True, tp.usable(b.current, p))
        operand = m.TypedProofAdmission(p, c.snapshot_id(b.current))
        slot, _ = c.commit_event(b, operand, STORE, R)
        self.bundle = slot
        self.boundary('POST_SLOT_PROOF', slot)
        self.checkpoint('post-slot-proof', b, slot, c._wire(operand))

        self.stage = 'ROOT_INSTALL'
        self.install(3)

        self.stage = 'ROOT_PROOF'
        b = self.bundle
        config = pi.records(b.current, 'ROOT_SLOT_CONFIGURATION_SET')[0]
        self.need('independent_root_source_and_semantic_configuration', True, pi.support_current(b.current, config))
        # configuration() verifies the full sealed source roles/content/origins.
        pi.configuration(config.request)
        rc = next(x for x in b.current.proof_contracts if x.proof_type is m.TypedProofKind.ROOT_PROOF)
        p = candidate(rc)
        self.need('actual_slot_support_fingerprint', rc.support_identities[0], tp.support_identity(b.current, rc.supports[0]))
        self.need('root_proof_oracle', True, tp.usable(b.current, p))
        root, _ = c.commit_event(b, m.TypedProofAdmission(p, c.snapshot_id(b.current)), STORE, R)
        self.bundle = root
        self.boundary('POST_ROOT_PROOF', root)
        self.boundary('POST_ROOT_SATISFACTION', root)
        self.boundary('PRE_FINISH', root)
        self.checkpoint('post-root-proof', b, root, c._wire(p))

        self.stage = 'FINISH'
        b = self.bundle
        action = next(a for a in b.current.actions if a.id == core.recompute(b.current).selection.selected)
        self.need('selected_FINISH', 'E2-FINISH', action.id.value)
        self.need('permitted_FINISH_result', 'PASS', action.accepted_result.value)
        self.need('permitted_FINISH_output', ['E2-K-FINISH'], [k.id.value for k in action.accepted_inventory])
        supplied = m.SuppliedResult(action.id, action.accepted_result, action.accepted_inventory, c.snapshot_id(b.current))
        target, _ = c.commit_event(b, supplied, STORE, R)
        self.bundle = target
        self.boundary('POST_FINISH', target)
        self.boundary('P04_TARGET', target)
        installs = [e for e in target.events[entry_count:] if type(e.result) is m.InstallDefinition]
        self.need('exact_two_INSTALLs', [16, 18], [e.sequence for e in installs])
        self.need('no_additional_INSTALLs', 2, len(installs))
        self.need('original_entry_prefix_retained', ENTRY.read_bytes(), c._bundle_bytes_admitted(c._prefix_bundle(target, entry_count)))
        self.checkpoint('isolated-p04-target', b, target, c._wire(supplied))
        # The comparison label is the existing F03 seal's name; this checkpoint
        # is an actual canonical execution, not another isolated lifecycle.
        manifest = save(target, TARGET)
        manifest['semantic_oracle'] = read(F / 'reader-manifests/isolated-p04-target.json')['semantic_oracle']
        manifest['writer_terminated'] = True
        emit('final-target-manifest.json', manifest)
        emit('boundary-checks.json', self.checks)
        emit('writer-result.json', {'RESULT': 'PASS', 'P04_EXIT_PREDICATE': True,
             'E2_P04_RESULT': 'PASS', 'entry_count': entry_count, 'final': manifest,
             'INSTALL_DEFINITION_EVENT_COUNT': len(installs), 'UNAUTHORIZED_INSTALLATIONS': 0,
             'new_authority_issuance_calls': 0, 'all_lifecycle_committed_once': True,
             'Action_result_protocol': 'Native selected SuppliedResult and result admission, as canonical A12/A13 and F03; no external executor identity fabricated.',
             'writer_pid': os.getpid(), 'writer_pid_namespace': os.readlink('/proc/self/ns/pid')})
        print('P04_EXIT_PREDICATE TRUE; WRITER COMPLETE', flush=True)

    def stop(self, error):
        if self.first is None:
            self.first = {'stage': self.stage, 'FIRST_COUNTEREXAMPLE': type(error).__name__,
                'EXPECTED': 'Complete native operation and sealed oracle PASS', 'ACTUAL': str(error),
                'STATE': uid(c.snapshot_id(self.bundle.current)) if self.bundle else None,
                'EVENT': uid(self.bundle.events[-1].identity) if self.bundle else None,
                'CLASSIFICATION': 'NATIVE_OPERATION_OR_EXECUTION_HARNESS_FAILURE; NO_REPAIR'}
        # Never continue/retry a lifecycle step after a reported failure.
        emit('first-counterexample.json', self.first)
        emit('boundary-checks.json', self.checks)
        emit('writer-result.json', {'RESULT': 'BLOCKED', 'P04_EXIT_PREDICATE': False,
            'E2_P04_RESULT': 'BLOCKED', 'first_counterexample': self.first,
            'completed_checkpoints': list(self.manifests), 'new_authority_issuance_calls': 0})
        print('STOP ' + str(error), flush=True)
        traceback.print_exc()


if __name__ == '__main__':
    run = Run()
    try:
        run.execute()
    except Exception as error:
        run.stop(error)
        sys.exit(1)
