"""Independent bounded wire reader of retained predicates; no native imports or replay.
Fail closed on shapes outside the sealed two-variant scenario. This is not a
replacement general-purpose Planner evaluator.
"""
import json, hashlib

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()
def key(x): return canonical(x) if x is not None else None
def enum(x, default=None): return x['value'] if x is not None else default
def find(rows, identity): return next(x for x in rows if x['id']==identity)
def derive(bundle, actionable, blocked):
    s=bundle['current']; ctx=s['context']; used=[]
    assert s['assertions']==[], 'Reader requires sealed assertion-free scenario'
    # Only the provenance SOURCE entity is stale; no edge can propagate its
    # unavailability into the receipt or recorded-decision predicates.
    stale=[x['id'] for x in s['entities'] if enum(x.get('validation'),'ACCEPTED')=='STALE']
    for collection in ('knowledge','actions','roots','slots'):
        for x in s[collection]:
            assert enum(x.get('validation'),'ACCEPTED')!='STALE'
            assert enum(x.get('qualification'),'ACCEPTED')!='STALE'
            assert enum(x.get('state'))!='STALE'
            assert not x.get('evidence',[])
    for p in s['predicates']:
        assert not any(x in stale for x in [p.get(k) for k in ('entity','other','condition','action','knowledge')]+p.get('operands',[]))
    for a in s['actions']:
        assert not any(g['target'] in stale for g in a['prerequisites'])
        assert a.get('authority') not in stale
    def usable(e):
        assert e['id'] not in stale and e['produced'] and e['validated']
        assert enum(e.get('validation'),'ACCEPTED')=='ACCEPTED'
        assert all(e[k]==ctx[k] for k in ('scope','lineage','generation'))
        assert e['valid_until']>=ctx['tick']
        used.append({'ENTITY':e['id'],'QUALIFIED_CURRENTNESS':True})
    def predicate(ref):
        v=next((v for v in s['validation_instances'] if v['predicate']==ref),None)
        if v:
            assert enum(v['result'])=='PASS' and enum(v['currentness'])=='ACCEPTED'
            used.append({'VALIDATION_INSTANCE':v,'PREDICATE':ref}); return
        p=find(s['predicates'],ref); assert p.get('unavailable') is None
        kind=enum(p['kind'])
        if kind=='KNOWLEDGE_ACCEPTED':
            k=find(s['knowledge'],p['knowledge'])
            assert enum(k.get('validation'),'ACCEPTED')=='ACCEPTED' and enum(k['state'])=='KNOWN_COMPLETE'
            if p.get('expected') is not None:
                assert k['provenance']['identity']==p['expected'] and k['producer']==p['action'] and k['outcome']==p['required_outcome']
            used.append({'KNOWLEDGE':k['id'],'PREDICATE':ref});return
        assert kind=='AUTHORITY', 'Unsupported predicate in sealed resume proof'
        e=find(s['entities'],p['entity']); usable(e)
        assert enum(e['kind'])=='AUTHORITY' and enum(e['identity']['kind'])=='AUTHORITY_IDENTITY'
        assert p['permission'] in e['permissions'] and e['target']==p['expected'] and not e['consumed']
    witnesses=[]
    for req in sorted(s['evidence_requirements'], key=lambda r:canonical(r['id'])):
        assert req.get('rule_known',False) or any(enum(v['result'])=='PASS' and enum(v['currentness'])=='ACCEPTED' and v['proposition']==req['proposition'] for v in s['validation_instances'])
        outcomes=set()
        for obs in s['receipt_observations']:
            if not obs['accepted']:continue
            gate=find(s['external_gates'],obs['gate']);assert enum(gate['validation'])=='ACCEPTED' and gate['contract_complete']
            ad=next(a for a in s['receipt_admissions'] if a['artifact']==obs['artifact']); e=find(s['entities'],obs['artifact']);usable(e)
            assert enum(e['kind'])=='EVIDENCE'
            body={'producer':ad['producer'],'target':ad['target'],'claims':sorted(ad['claims'],key=canonical)}
            assert e['identity']['namespace']=='raw-file-sha256' and e['identity']['sha256']==hashlib.sha256(canonical(body)).hexdigest() and e['provenance']['identity']==e['identity']
            p=find(s['predicates'],ad['authentication']);owner=find(s['entities'],p['entity'])
            assert enum(p['kind'])=='AUTHORITY' and enum(p['permission'])=='ATTEST'
            assert owner['provenance']['identity']!=e['provenance']['identity'] and owner['provenance']['path']!=e['provenance']['path']
            if ad.get('attestation'):
                assert ad['attestation']['namespace']=='planner-evidence-attestation-v1'
            else: assert owner['identity']==ad['producer'] and p['expected']==e['identity']
            predicate(ad['authentication'])
            assert ad['claims'] and all(c['requirement'] in gate['requirements'] for c in ad['claims'])
            for c in ad['claims']:
                r=find(s['evidence_requirements'],c['requirement'])
                assert r['producers'] and ad['target']==r['target'] and ad['producer'] in r['producers']
            outcomes.update(enum(c['outcome']) for c in obs['claims'] if c['requirement']==req['id'])
        assert outcomes=={'PROVED'}
        witnesses.append({'requirement':req['id'],'proof':{'qualification_type':'Proof','state':{'$enum':'ProofState','value':'PROVED'},'reasons':[]}})
    binding=hashlib.sha256(canonical({'schema':'RESUME-EVENT-BINDING-1','policy':bundle['policy'],'policy_version':bundle['policy_version'],'scope':bundle['scope']})).hexdigest()
    routes=[]
    for g in s['external_gates']:
        assert enum(g['stage'])=='DEPENDENT_ACTION_REENTRY' and enum(g['validation'])=='ACCEPTED' and g['contract_complete']
        assert all(any(w['requirement']==r for w in witnesses) for r in g['requirements'])
        events=[e for e in bundle['events'] if e['result']['$type']=='ExternalEvent' and e['result']['gate']==g['id'] and enum(e['result']['stage'])=='DEPENDENT_ACTION_REENTRY']
        routes.append(('EXTERNAL:'+g['id']['value'],g['reentry'],events))
    for d in s['decisions']:
        if enum(d['stage'])!='DOWNSTREAM_REEVALUATION':continue
        dossier=d['dossier'];assert enum(dossier.get('validation'),'ACCEPTED')!='STALE'
        for r in dossier['required_facts']:predicate(r)
        checks={enum(c['kind']):c for c in dossier['checks']}
        # Native supported dossier checks, exact enum domain from model.py.
        from pathlib import Path
        text=Path('adapter/planner/model.py').read_text()
        import re
        block=text.split('SUPPORTED_DOSSIER_CHECKS =',1)[1].split('\n\n',1)[0]
        names=re.findall(r'DossierCheck\.([A-Z_]+)',block)
        assert names
        for name in names:predicate(checks[name]['predicate'])
        assert all(dossier[k] for k in ('question','scope','alternatives','authority_granted_if_approved','authority_excluded')) and all(dossier['alternatives'])
        record=find(s['entities'],d['record']);usable(record)
        assert enum(record['kind'])=='AUTHORITY' and not record['consumed'] and record['decision']==d['action'] and record['choice']==d['recorded_choice']
        assert {'$enum':'AuthorityClass','value':'DECIDE'} in record['permissions'] and record['target']==dossier['provenance']['identity']
        events=[e for e in bundle['events'] if e['result']['$type']=='DecisionReentry' and e['result']['decision']==d['action']]
        routes.append(('DECISION:'+d['action']['value'],d['downstream'],events))
    assert len(routes)==2
    reasons=[]
    for name,actions,events in routes:
        assert events and events[-1]['resume_binding']['namespace']=='planner-resume-binding-v1' and events[-1]['resume_binding']['sha256']==binding
        assert not any(a in actionable for a in actions)
        reasons.append(name+':NAMED_REENTRY_NOT_ACTIONABLE')
        for a in sorted(actions,key=lambda a:a['value']):
            why=next((r for i,r in blocked if i==a),['COMPLETED_OR_UNAVAILABLE'])
            reasons.extend(name+':'+a['value']+':'+r for r in why)
    return {'$type':'ResumeEligibility','allowed':False,'actions':[],'reasons':sorted(set(reasons)),'supporting_identities':[]},witnesses,{'BINDING_HASH':binding,'QUALIFIED_ROUTE_EVIDENCE':used,'NO_ELIGIBLE_SOURCE_CHECK_BRANCH':True,'FINISH_NOT_A_NAMED_RESUME_ROUTE':True}
