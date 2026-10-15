import pathlib,json,hashlib
Q=pathlib.Path('docs/plans/qualification');g=json.loads((Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json').read_text());b=json.loads(pathlib.Path(g['CAPSULE_SOURCE']['path']).read_text())['canonical_content']['bundle']
rows=[]
for p in b['sources']+[b['policy']]:
 assert p['identity']['kind']['value']=='CONTENT_IDENTITY' and p['profile']['value']=='raw-file-sha256' and p['pointer']==''
 assert hashlib.sha256(pathlib.Path(p['path']).read_bytes()).hexdigest()==p['identity']['sha256']
 rows.append({'id':p['identity'],'pin':p})
proofs=[{'id':p['id'],'target':p['target'],'supports':p['supports'],'source':p['provenance']['identity']} for p in b['current']['typed_proofs']]
a=next(a for a in b['current']['actions'] if a['id']['value']=='E2-FINISH');status=next(r for r in b['current']['statuses'] if r['id']==a['id'])
print(json.dumps({'PIN_COUNT':len(rows),'DISTINCT_CONTENT_COUNT':len({json.dumps(r['id'],sort_keys=True) for r in rows}),'PINS':rows,'PROOFS':proofs,'FINISH':{'id':a['id'],'prerequisites':a['prerequisites'],'status':status}},sort_keys=True))
