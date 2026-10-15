"""Read-only P04 semantic comparison; never a source substitution or execution."""
import hashlib,json
from pathlib import Path
from adapter.planner import codec
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;D=R/'docs/plans'
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,ptr=''):return {'path':str(p.relative_to(R)),'pointer':ptr,'raw_sha256':sha(p.read_bytes())}
def save(n,v):(O/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
a14path=O.parent/'E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7/corrected-prospective-snapshot.json';a14=read(a14path)['snapshot'];old=next(a for a in a14['actions'] if a['id']['value']=='E2-FINISH');oldidx=a14['actions'].index(old)
resultpath=D/'DETERMINISTIC_PLANNER_V0_1_E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT.json';result=read(resultpath);ref=result['execution_evidence']['target_bundle'];targetpath=R/ref['path'];assert sha(targetpath.read_bytes())==ref['sha256'];current=read(targetpath)['bundle']['current'];new=next(a for a in current['actions'] if a['id']['value']=='E2-FINISH');newidx=current['actions'].index(new)
assert result['E2_P04_RESULT']=='PASS' and result['FINISH']=='PASS'
na=codec._unwire(old);nb=codec._unwire(new)
sourcepath=codec._path(R,new['source']['path']);physical=sourcepath.read_bytes();assert sha(physical)==new['source']['identity']['sha256'];assert physical==new['source']['excerpt'].encode()
oldraw=old['source']['excerpt'].encode();assert sha(oldraw)==old['source']['identity']['sha256'] and physical!=oldraw
def summary(a,context,path,ptr):
 n=codec._unwire(a)
 return {'ACTION_SOURCE':pin(path,ptr),'NATIVE_ACTION_ID':a['id'],'ACTION_COMPARISON_CONTENT_IDENTITY':{'DOMAIN':'qualification-FINISH-action-comparison-v1','SHA256':sha(codec.canonical_bytes(codec._wire(n)))},'NATIVE_ACTION_FIELDS':a,'SOURCE_CONTENT_IDENTITY':a['source']['identity'],'ACCEPTED_INVENTORY':a['accepted_inventory'],'DEPENDENCIES':a['prerequisites'],'REQUIREMENTS':codec._wire(n.requirements),'RESULT_CONTRACT':{'accepted_result':codec._wire(n.accepted_result),'accepted_inventory':a['accepted_inventory'],'pass_model_complete':n.pass_model_complete,'stage':codec._wire(n.stage)},'SCOPE':context['scope'],'LINEAGE':context['lineage'],'GENERATION':context['generation'],'PHYSICAL_SOURCE_PATH':a['source']['path'],'SOURCE_RAW_BYTE_LENGTH':len(a['source']['excerpt'].encode()),'SOURCE_RAW_SHA256':a['source']['identity']['sha256']}
left=summary(old,a14['context'],a14path,'/snapshot/actions/'+str(oldidx));right=summary(new,current['context'],targetpath,'/bundle/current/actions/'+str(newidx))
fields={name:{'A14':old.get(name),'P04':new.get(name),'EQUAL':old.get(name)==new.get(name)} for name in sorted(set(old)|set(new))}
out={'A14_EXPECTED_FINISH_SOURCE':left,'CURRENT_P04_FINISH_DEFINITION':right,'CURRENT_P04_QUALIFICATION_RESULT':pin(resultpath),'CURRENT_P04_FINISH_RESULT':'PASS_RETAINED_QUALIFICATION_ONLY_NOT_RERUN','CURRENT_P04_PHYSICAL_SOURCE':pin(sourcepath),'HISTORICAL_CURRENT_RELATIONSHIP':'DIFFERENT_VERSION','CURRENT_FINISH_SUBSTITUTION_ALLOWED':False,'SOURCE_BYTE_EQUALITY':False,'SOURCE_HASH_EQUALITY':False,'FIELD_COMPARISON':fields,'CONTEXT_COMPARISON':{k:{'A14':a14['context'][k],'P04':current['context'][k],'EQUAL':a14['context'][k]==current['context'][k]} for k in ['scope','lineage','generation']},'RATIONALE':'A14 has PC01 raw marker and only ACTION_COMPLETED E2-REENTER gate. Qualified P04 has authored prospective source wrapper and an additional CONDITION_SATISFIED E2-ROOT gate; lineage/generation differ. Knowledge IDs and PASS labels overlap but full definition/provenance and source bytes do not. Nested template provenance is not the physical wrapper source.','SOURCE_COMPARISON_ONLY_NOT_RECOVERY_AUTHORITY':True,'NATIVE_OPERATIONS_EXECUTED':0}
assert any(g['target']['value']=='E2-ROOT' for g in new['prerequisites']) and all(g['target']['value']!='E2-ROOT' for g in old['prerequisites'])
save('historical-current-finish-comparison.json',out)
print(json.dumps({'RELATIONSHIP':'DIFFERENT_VERSION','A14_BYTES':len(oldraw),'P04_BYTES':len(physical),'P04_SOURCE_HASH':sha(physical),'SUBSTITUTION_ALLOWED':False}))
