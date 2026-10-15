"""D01 generic durable qualification; never uses or executes prospective A04."""
import tempfile
import unittest
from dataclasses import fields, replace
from pathlib import Path
from unittest.mock import patch

from adapter.planner import codec as c, dossier_transaction as dt, model as m
from adapter.tests import dossier_fixture as f

ZERO = c._identity(b'wrong', 'planner-snapshot-v1')


class DossierTransactionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.before, self.artifacts = f.create(self.root)
        self.expected = c.bundle_id(self.before)
        self.producer = dt.register_producer(f.BUILD, f.produce)
        self.store = self.root / 'store'

    def prepare(self, operation=None):
        producer = self.producer if operation is None else dt.register_producer(f.BUILD, operation)
        return dt.prepare(self.before, self.expected, producer, self.artifacts, self.root, postcondition=f.oracle)

    def positive(self):
        candidate = self.prepare()
        after, bid, noop = dt.commit(candidate, self.store, self.root)
        self.assertFalse(noop)
        return candidate, after, bid

    def changed(self, candidate, *, result=None, after=None, **event_fields):
        old = candidate.updated.events[-1]
        after = after or candidate.updated.current
        event = replace(old, result=result or old.result, after_snapshot=c.snapshot_id(after), **event_fields)
        event = replace(event, identity=c._event_identity(event.sequence, event.parent_snapshot, event.parent_event,
                                                        event.result, event.after_snapshot, event.resume_binding))
        binding = replace(candidate.updated.dossier_materializations[-1], event_identity=event.identity)
        bundle = replace(candidate.updated, current=after, events=candidate.updated.events[:-1] + (event,),
                         dossier_materializations=(binding,))
        return bundle, dt.memory_resolver((after,))

    def test_complete_native_result_and_independent_identity_oracle(self):
        expected, eid = f.expected(self.before, self.artifacts)
        candidate, after, bid = self.positive()
        self.assertEqual(c.snapshot_id(after.current), c.snapshot_id(expected.current))
        self.assertEqual(after.events[-1].identity, expected.events[-1].identity)
        self.assertEqual(bid, eid)
        self.assertEqual(c.bundle_bytes(after, snapshot_resolver=candidate.resolve), c._bundle_bytes_admitted(expected))
        self.assertEqual(after.events[-1].sequence, 2)
        self.assertEqual(after.events[-1].parent_event, self.before.events[-1].identity)
        self.assertEqual(after.events[0], self.before.events[0])
        self.assertEqual(c._prefix_bundle(after, 1, snapshot_resolver=candidate.resolve), self.before)
        self.assertEqual(len(after.dossier_materializations), 1)
        self.assertEqual(len(after.current.validation_instances), 6)
        self.assertEqual(after.current.context, self.before.current.context)
        self.assertFalse(self.before.current.validation_instances)
        self.assertEqual(len(self.before.events), 1)
        self.assertNotIn('validation_instances', {x.name for x in fields(m.SuppliedResult)})
        self.assertNotIn('dossier_materializations', {x.name for x in fields(m.ExecutionEvent)})

    def test_no_raw_or_boolean_live_execution_context(self):
        candidate = self.prepare()
        for value in (True, candidate.supplied, candidate.updated.current, {}, c._wire(candidate.supplied),
                      replace(candidate), dt.Producer(f.BUILD, f.produce)):
            with self.subTest(type=type(value)), self.assertRaises(m.PlannerError):
                dt.commit(value, self.store, self.root)
        with self.assertRaises(m.PlannerError):
            dt.prepare(self.before, self.expected, dt.Producer(f.BUILD, f.produce), self.artifacts, self.root)
        with self.assertRaises(m.PlannerError):
            dt.prepare(self.before, self.expected, True, self.artifacts, self.root)
        self.assertFalse((self.store / 'HEAD.json').exists())

    def test_wrong_native_result_and_output_inventory(self):
        supplied, vs = f.produce(self.before.current, self.artifacts)
        changes = [replace(supplied, result=m.ActionResult.FAIL), replace(supplied, action=f.REVIEW),
                   replace(supplied, expected_snapshot=ZERO), replace(supplied, knowledge=()),
                   replace(supplied, knowledge=supplied.knowledge+supplied.knowledge),
                   replace(supplied, knowledge=(replace(supplied.knowledge[0], statement='wrong'),)),
                   replace(supplied, dossier=None)]
        for bad in changes:
            with self.subTest(result=bad), self.assertRaises(m.PlannerError):
                self.prepare(lambda state, artifacts: (bad, vs))
        with self.assertRaises(m.PlannerError):
            self.prepare(lambda state, artifacts: True)

    def test_validation_subject_inputs_membership_and_currentness(self):
        supplied, vs = f.produce(self.before.current, self.artifacts)
        cases = {'dossier': ZERO, 'predicate': m.PredicateId('foreign'), 'proposition': 'generic TRUE',
                 'inputs': vs[0].inputs[::-1], 'scope': 'foreign', 'lineage': 'foreign',
                 'result': m.ValidationOutcome.FAIL, 'currentness': m.ValidationState.REJECTED,
                 'provenance': replace(vs[0].provenance, section='/wrong')}
        for field, value in cases.items():
            bad = (replace(vs[0], **{field: value}),) + vs[1:]
            with self.subTest(field=field), self.assertRaises(m.PlannerError):
                self.prepare(lambda state, artifacts: (supplied, bad))
        for bad in (True, list(vs), vs[:-1], vs + vs[:1], ()):
            with self.subTest(tuple=bad), self.assertRaises(m.PlannerError):
                self.prepare(lambda state, artifacts: (supplied, bad))

    def test_wrong_source_and_pre_bundle(self):
        pin, raw = self.artifacts[0]
        with self.assertRaises(m.PlannerError):
            dt.prepare(self.before, replace(self.expected, sha256='0'*64), self.producer, self.artifacts, self.root)
        for artifacts in (((pin, raw+b' '),), ((replace(pin, path='../escape.json'), raw),),
                          ((replace(pin, profile=m.HashProfile.PLANNER_JSON), raw),), self.artifacts+self.artifacts):
            with self.subTest(artifacts=artifacts), self.assertRaises(m.PlannerError):
                dt.prepare(self.before, self.expected, self.producer, artifacts, self.root)

    def test_wrong_event_parent_position_payload_and_identity(self):
        candidate = self.prepare()
        for change in ({'parent_event': ZERO}, {'parent_snapshot': ZERO}, {'sequence': 3}, {'resume_binding': ZERO}):
            bad, resolver = self.changed(candidate, **change)
            with self.subTest(change=change), self.assertRaises(m.PlannerError):
                c._replay(bad, snapshot_resolver=resolver)
        bad = replace(candidate.updated.events[-1], identity=ZERO)
        with self.assertRaises(m.PlannerError):
            c._replay(replace(candidate.updated, events=candidate.updated.events[:-1]+(bad,)), snapshot_resolver=candidate.resolve)
        payload = c._wire(candidate.supplied)
        payload['validated'] = True
        with self.assertRaises(m.PlannerError):
            c._unwire(payload)

    def test_archive_missing_wrong_and_no_latest_snapshot_fallback(self):
        candidate, after, bid = self.positive()
        archive = self.store / ('snapshot-'+c.snapshot_id(after.current).sha256+'.json')
        with self.assertRaises(m.PlannerError):
            c._replay(after)
        with self.assertRaises(m.PlannerError):
            c._replay(after, snapshot_resolver=lambda identity: self.before.current)
        original = archive.read_bytes()
        archive.write_bytes(c.snapshot_bytes(self.before.current))
        with self.assertRaises(m.PlannerError):
            c.restore(self.store / ('bundle-'+bid.sha256+'.json'), bid, self.root)
        archive.unlink()
        with self.assertRaises(m.PlannerError):
            c.restore(self.store / ('bundle-'+bid.sha256+'.json'), bid, self.root)
        archive.write_bytes(original)
        self.assertEqual(c.snapshot_id(c.restore(self.store / ('bundle-'+bid.sha256+'.json'), bid, self.root).current),
                         c.snapshot_id(after.current))

    def test_rehashed_tampered_state_still_fails_historical_projection(self):
        candidate = self.prepare()
        changes = [replace(candidate.updated.current,
                        actions=tuple(replace(a, accepted_inventory=tuple(replace(k, statement='forged prerequisite')
                            for k in a.accepted_inventory)) if a.id == f.ACQUIRE else a
                            for a in candidate.updated.current.actions),
                        knowledge=tuple(replace(k, statement='forged prerequisite')
                            if k.producer == f.ACQUIRE else k for k in candidate.updated.current.knowledge)),
                   replace(candidate.updated.current, context=replace(candidate.updated.current.context, generation='foreign'))]
        for after in changes:
            bad, resolver = self.changed(candidate, after=after)
            with self.subTest(after=c.snapshot_id(after)), self.assertRaises(m.PlannerError):
                c._replay(bad, snapshot_resolver=resolver)
        member = candidate.updated.current.validation_instances[0]
        after = replace(candidate.updated.current, validation_instances=(replace(member, inputs=(ZERO, member.inputs[1])),)
                        + candidate.updated.current.validation_instances[1:])
        bad, resolver = self.changed(candidate, after=after)
        with self.assertRaises(m.PlannerError):
            c._replay(bad, snapshot_resolver=resolver)

    def test_binding_missing_tampered_duplicate_orphan_and_extra_source(self):
        candidate = self.prepare()
        binding = candidate.updated.dossier_materializations[0]
        cases = [(), (replace(binding, expected_bundle=ZERO),), (replace(binding, event_identity=ZERO),),
                 (binding, binding), (replace(binding, source_additions=()),)]
        for bs in cases:
            with self.subTest(bindings=bs), self.assertRaises(m.PlannerError):
                c._replay(replace(candidate.updated, dossier_materializations=bs), snapshot_resolver=candidate.resolve)
        pin = m.ArtifactPin('unrelated.json', c._identity(b'{}','raw-file-sha256'))
        bad = replace(candidate.updated, sources=candidate.updated.sources+(pin,),
                dossier_materializations=(replace(binding, source_additions=binding.source_additions+(pin,)),))
        with self.assertRaises(m.PlannerError):
            c._replay(bad, snapshot_resolver=candidate.resolve)

    def test_exact_retry_before_producer_and_after_descendants(self):
        calls = []
        producer = dt.register_producer(f.BUILD, lambda state, artifacts: (calls.append(1) or f.produce(state, artifacts)))
        after, bid, noop = dt.execute(self.before, self.expected, producer, self.artifacts, self.store, self.root, postcondition=f.oracle)
        again, same, noop = dt.execute(self.before, self.expected, producer, self.artifacts, self.store, self.root)
        self.assertTrue(noop); self.assertEqual(same, bid); self.assertEqual(calls, [1])
        invalidation = m.SourceInvalidation((self.artifacts[0][0].identity,), c.snapshot_id(after.current))
        later, lid = c.commit_event(after, invalidation, self.store, self.root)
        current, original, noop = dt.execute(self.before, self.expected, producer, self.artifacts, self.store, self.root)
        self.assertTrue(noop); self.assertEqual(original, bid); self.assertEqual(calls, [1])
        self.assertEqual(c.snapshot_id(current.current), c.snapshot_id(later.current))
        self.assertEqual(len(current.events), 3)
        self.assertNotEqual(current.current.validation_instances[0].currentness, m.ValidationState.ACCEPTED)
        restored = c.restore(self.store / ('bundle-'+lid.sha256+'.json'), lid, self.root)
        self.assertEqual(c.snapshot_id(restored.current), c.snapshot_id(later.current))
        self.assertTrue((self.store / ('snapshot-'+after.events[-1].after_snapshot.sha256+'.json')).is_file())

    def test_conflicting_retry_and_foreign_or_stale_head(self):
        candidate, after, bid = self.positive()
        # A different legitimate authored dossier under the same intent conflicts.
        pin, raw = self.artifacts[0]
        data = c.parse_json(raw); data['question'] = 'A different bounded question'
        new_raw = c.canonical_bytes(data)
        artifacts = ((replace(pin, identity=c._identity(new_raw,'raw-file-sha256')), new_raw),)
        conflict = dt.prepare(self.before, self.expected, self.producer, artifacts, self.root)
        with self.assertRaises(m.PlannerError):
            dt.commit(conflict, self.store, self.root)
        with self.assertRaises(m.PlannerError):
            dt.execute(self.before, self.expected, self.producer, artifacts, self.store, self.root)
        # A current-parent relabel cannot execute the completed Action again.
        with self.assertRaises(m.PlannerError):
            dt.prepare(after, bid, self.producer, self.artifacts, self.root, snapshot_resolver=candidate.resolve)
        self.assertEqual(c.bundle_id(c._read_head(self.store, self.before, self.root), snapshot_resolver=c.snapshot_resolver(self.store)), bid)

    def test_replay_is_read_only_and_cannot_create_second_occurrence(self):
        candidate, after, bid = self.positive()
        contents = {p.name:p.read_bytes() for p in self.store.iterdir() if p.is_file()}
        resolver = c.snapshot_resolver(self.store)
        with patch.object(dt, 'register_producer', side_effect=AssertionError('no live registration')), \
             patch.object(dt, 'prepare', side_effect=AssertionError('no live execution')), \
             patch.object(c, '_publish_head', side_effect=AssertionError('replay cannot publish')):
            for _ in range(3):
                cold = c.restore(self.store / ('bundle-'+bid.sha256+'.json'), bid, self.root)
                self.assertEqual(c.snapshot_id(c._replay(cold,snapshot_resolver=resolver)), c.snapshot_id(after.current))
        self.assertEqual(contents, {p.name:p.read_bytes() for p in self.store.iterdir() if p.is_file()})
        self.assertEqual(c.append_event(after, after.events[-1], snapshot_resolver=resolver), after)
        with self.assertRaises(m.PlannerError):
            c.record_result(after, candidate.supplied, snapshot_resolver=resolver)

    def test_failure_injection_old_or_complete_new_and_clean_retry(self):
        stages = ('after_producer', 'after_validations', 'after_result_application', 'after_snapshot', 'after_event_binding',
                  'after_source_stage', 'after_archive_stage', 'after_event_stage', 'after_bundle_stage',
                  'after_files_fsync', 'before_head_replace', 'after_head_replace')
        before = c.bundle_bytes(self.before)
        for stage in stages:
            store = self.root / ('failure-'+stage)
            def fail(value):
                if value == stage:
                    raise OSError('injected ' + stage)
            with self.subTest(stage=stage):
                with self.assertRaises(OSError):
                    dt.execute(self.before,self.expected,self.producer,self.artifacts,store,self.root,failure_hook=fail)
                recovered = c._read_head(store,self.before,self.root)
                if stage == 'after_head_replace':
                    self.assertEqual(len(recovered.events), 2)
                    self.assertEqual(len(recovered.current.validation_instances), 6)
                else:
                    self.assertEqual(c.bundle_bytes(recovered), before)
                    self.assertFalse((store/'HEAD.json').exists())
                final, bid, noop = dt.execute(self.before,self.expected,self.producer,self.artifacts,store,self.root)
                self.assertEqual(len(final.events), 2)
                self.assertEqual(noop, stage == 'after_head_replace')
                self.assertEqual(c.bundle_bytes(self.before), before)

    def test_atomic_replace_io_failure_and_immutable_conflict(self):
        candidate = self.prepare()
        original = c.os.replace
        def fail(source, target):
            if str(target).endswith('HEAD.json'):
                raise OSError('head replace failed')
            return original(source, target)
        with patch.object(c.os,'replace',side_effect=fail), self.assertRaises(OSError):
            dt.commit(candidate,self.store,self.root)
        self.assertFalse((self.store/'HEAD.json').exists())
        dt.commit(candidate,self.store,self.root)
        other = self.root/'conflict'; other.mkdir()
        (other/('snapshot-'+c.snapshot_id(candidate.updated.current).sha256+'.json')).write_bytes(b'not a snapshot')
        with self.assertRaises(m.PlannerError):
            dt.commit(candidate,other,self.root)
        self.assertFalse((other/'HEAD.json').exists())

    def test_unchanged_old_wire_and_default_omission(self):
        wire = c._wire(self.before)
        self.assertNotIn('dossier_materializations',wire)
        self.assertEqual(c._bundle_bytes_admitted(c._unwire(wire)),c._bundle_bytes_admitted(self.before))
        self.assertEqual(c._bundle_bytes_admitted(self.before),c.bundle_bytes(self.before))
        candidate = self.prepare()
        for field in ('validation_instances','executed','permission'):
            value=c._wire(candidate.updated.dossier_materializations[0]);value[field]=True
            with self.assertRaises(m.PlannerError):c._unwire(value)

    def test_unordered_permutations_preserve_all_native_identities(self):
        expected, eid = f.expected(self.before,self.artifacts)
        for mode in ('original','reverse','rotate'):
            producer=dt.register_producer(f.BUILD,lambda state, artifacts: f.produce(state,artifacts,mode))
            candidate=dt.prepare(self.before,self.expected,producer,self.artifacts,self.root)
            self.assertEqual(c.bundle_id(candidate.updated,snapshot_resolver=candidate.resolve),eid)
            self.assertEqual(candidate.updated.events[-1].identity,expected.events[-1].identity)
            self.assertEqual(c.snapshot_id(candidate.updated.current),c.snapshot_id(expected.current))

    def test_trusted_ledger_head_and_source_tampering(self):
        candidate, after, bid = self.positive()
        path = self.store / ('bundle-'+bid.sha256+'.json')
        with self.assertRaises(m.PlannerError):
            c.restore(path,self.expected,self.root)
        head = self.store/'HEAD.json'
        original = head.read_bytes()
        data = c.parse_json(original)
        data['previous'] = c._wire(ZERO)
        head.write_bytes(c.canonical_bytes(data))
        with self.assertRaises(m.PlannerError):
            dt.commit(candidate,self.store,self.root)
        head.write_bytes(original)
        source = self.root/self.artifacts[0][0].path
        raw = source.read_bytes()
        source.write_bytes(raw+b' ')
        with self.assertRaises(m.PlannerError):
            c.restore(path,bid,self.root)
        with self.assertRaises(m.PlannerError):
            dt.commit(candidate,self.store,self.root)
        source.write_bytes(raw)
        self.assertEqual(c.bundle_id(c._read_head(self.store,self.before,self.root),
                                     snapshot_resolver=c.snapshot_resolver(self.store)),bid)

    def test_missing_historical_archive_after_invalidation(self):
        candidate, after, bid = self.positive()
        later, lid = c.commit_event(after,m.SourceInvalidation((self.artifacts[0][0].identity,),
                                  c.snapshot_id(after.current)),self.store,self.root)
        archive = self.store/('snapshot-'+after.events[-1].after_snapshot.sha256+'.json')
        archive.unlink()
        with self.assertRaises(m.PlannerError):
            c.restore(self.store/('bundle-'+lid.sha256+'.json'),lid,self.root)
        with self.assertRaises(m.PlannerError):
            c._replay(later)

    def test_conflicting_validation_retry_and_physical_closure(self):
        candidate, after, bid = self.positive()
        pin, raw = self.artifacts[0]
        supplied, vs = f.produce(self.before.current,self.artifacts)
        check = supplied.dossier.checks[0]
        new_provenance = replace(check.provenance,section='/different-authored-rule')
        dossier = replace(supplied.dossier,checks=(replace(check,provenance=new_provenance),)+supplied.dossier.checks[1:])
        did = c._identity(c.canonical_bytes(c._wire(dossier)),'planner-dossier-sha256')
        vs = tuple(replace(v,dossier=did,provenance=new_provenance if v.predicate==check.predicate else v.provenance) for v in vs)
        conflict = self.prepare(lambda state, artifacts: (replace(supplied,dossier=dossier),vs))
        with self.assertRaises(m.PlannerError):
            dt.commit(conflict,self.store,self.root)
        event_path = self.store/('event-'+after.events[-1].identity.sha256+'.json')
        event_path.unlink()
        with self.assertRaises(m.PlannerError):
            c.restore(self.store/('bundle-'+bid.sha256+'.json'),bid,self.root)

    def test_inapplicable_operation_never_invokes_producer(self):
        calls=[]
        producer=dt.register_producer(f.REVIEW,lambda state, inputs:(calls.append(1) or f.produce(state,inputs)))
        with self.assertRaises(m.PlannerError):
            dt.prepare(self.before,self.expected,producer,self.artifacts,self.root)
        self.assertEqual(calls,[])
        with self.assertRaises(m.PlannerError):
            dt.execute(self.before,self.expected,producer,self.artifacts,self.store,self.root)
        self.assertEqual(calls,[])
        self.assertFalse((self.store/'HEAD.json').exists())

    def test_foreign_append_head_stops_before_operation(self):
        changed=m.SourceInvalidation((self.before.sources[0].identity,),c.snapshot_id(self.before.current))
        c.commit_event(self.before,changed,self.store,self.root)
        calls=[]
        producer=dt.register_producer(f.BUILD,lambda state, inputs:(calls.append(1) or f.produce(state,inputs)))
        with self.assertRaises(m.PlannerError):
            dt.execute(self.before,self.expected,producer,self.artifacts,self.store,self.root)
        self.assertEqual(calls,[])

    def test_partial_result_event_bundle_and_orphan_files_are_not_head(self):
        candidate=self.prepare()
        missing_result=replace(candidate.updated.events[-1],result=None)
        with self.assertRaises(m.PlannerError):
            c._replay(replace(candidate.updated,events=candidate.updated.events[:-1]+(missing_result,)),
                      snapshot_resolver=candidate.resolve)
        missing_event=replace(candidate.updated,events=self.before.events,dossier_materializations=())
        with self.assertRaises(m.PlannerError):
            c._replay(missing_event,snapshot_resolver=candidate.resolve)
        # A pre-HEAD crash can leave perfectly encoded immutable files. Their
        # availability does not advance the accepted native transaction head.
        pin,raw=self.artifacts[0];(self.root/pin.path).write_bytes(raw)
        c.save_bundle(candidate.updated,self.store,self.root,snapshot_resolver=candidate.resolve)
        self.assertFalse((self.store/'HEAD.json').exists())
        self.assertEqual(c.bundle_bytes(c._read_head(self.store,self.before,self.root)),c.bundle_bytes(self.before))

    def test_archive_symlink_and_noncanonical_bytes_fail_closed(self):
        candidate,after,bid=self.positive()
        archive=self.store/('snapshot-'+after.events[-1].after_snapshot.sha256+'.json')
        original=archive.read_bytes()
        archive.write_bytes(original+b'\n')
        with self.assertRaises(m.PlannerError):
            c.restore(self.store/('bundle-'+bid.sha256+'.json'),bid,self.root)
        foreign=self.root/'foreign-snapshot.json';foreign.write_bytes(original)
        archive.unlink();archive.symlink_to(foreign)
        with self.assertRaises(m.PlannerError):
            c.restore(self.store/('bundle-'+bid.sha256+'.json'),bid,self.root)


if __name__ == '__main__':
    unittest.main()
