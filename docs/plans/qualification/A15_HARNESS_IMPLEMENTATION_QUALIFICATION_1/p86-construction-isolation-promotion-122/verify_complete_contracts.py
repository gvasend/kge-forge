"""Additional independent documentary coverage; does not execute candidate code."""
import pathlib,json,hashlib,subprocess,sys,os
O=pathlib.Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def need(x,r):
 if not x:raise ValueError(r)
files=['a-versus-b-comparison.json','disposable-isolation-contract.json','candidate-handoff-contract.json','independent-static-verifier-contract.json','two-file-promotion-contract.json','protected-evidence-contract.json','threat-and-failure-analysis.json','existing-isolation-promotion-mechanism-assessment.json','authority-and-amendment-assessment.json','remaining-gap-dossier.json','lessons-review.json']
d={n:load(n) for n in files}
a=d['a-versus-b-comparison.json'];need([r['ID'] for r in a['ALTERNATIVES']]==['A','B'] and a['OUTCOME']=='C_NEITHER_CURRENTLY_QUALIFIED','A/B/C comparison');need(all(not r['CURRENT_QUALIFIED'] for r in a['ALTERNATIVES']),'no qualified selection')
for r in a['ALTERNATIVES']:
 for k in ['ENGINEERING_EFFORT','AUTHORITY_COMPLEXITY','REPOSITORY_BLAST_RADIUS','RECOVERY','RESOURCE_ACCOUNTING','TIME_TO_FIRST_INERT_QUALIFICATION','NEW_TRUSTED_COMPONENT_COUNT','ASSURANCE_EVIDENCE','RESIDUAL_UNCERTAINTY']:need(bool(r[k]),'risk comparison '+k)
i=d['disposable-isolation-contract.json'];need(not i['ROOT_CREATED'] and not i['ACTIVE_BOUNDARY_VERIFIED'],'no isolation entry');need('UNDETERMINED' in i['FILESYSTEM_AND_MOUNT_IDENTITY'],'missing mount identity explicit');need('not directory naming alone' in i['ROOT_ROLE'],'no directory-as-boundary');need(len(i['PROTECTED_HOST_PATHS'])==6,'protected domain inventory')
h=d['candidate-handoff-contract.json'];need(h['STATUS']=='PROSPECTIVE_NOT_SEALED' and len(h['REQUIRED_FIELDS'])==13,'handoff required fields');need('no promotion grant' in h['AUTHORITY'],'handoff not authority')
s=d['independent-static-verifier-contract.json'];need(len(s['CHECKS'])==10 and s['RESULT']=='NOT_EXECUTED_ON_CANDIDATE_NO_SOURCE_EXISTS','static verification scope/limitations')
p=d['two-file-promotion-contract.json'];need(not p['CONTRACT_COMPLETE'] and not p['BOUNDARY_QUALIFIED'] and p['NO_ACTIVE_PROMOTION'],'no qualified promotion');need(len(p['DURABILITY'])==4 and 'not physical all-or-nothing' in p['ATOMICITY'],'no false pair atomicity')
f=d['threat-and-failure-analysis.json'];need(len(f['CASES'])==13 and len({r['THREAT_OR_FAILURE'] for r in f['CASES']})==13,'threat inventory');need(all(r['PROBABILITY_BASIS'].startswith('UNKNOWN') for r in f['CASES']),'no fabricated probabilities')
need(d['existing-isolation-promotion-mechanism-assessment.json']['QUALIFIED_SELECTED']=='NONE','no mechanism selected');need(d['authority-and-amendment-assessment.json']['GOVERNANCE_CHANGE_REQUIRED']=='NO' and d['authority-and-amendment-assessment.json']['NO_AUTHORITY_ISSUED'],'nonweakening scope only');need(d['lessons-review.json']['APPENDED'] is False,'no append authority')
cp=subprocess.run([sys.executable,str(O/'verify_independent.py')],capture_output=True,text=True);need(cp.returncode==0,'underlying independent pin/arithmetic/phase/negative reconstruction');base=json.loads(cp.stdout)
semantic={'BASE_RECONSTRUCTION':base['RECONSTRUCTION'],'BASE_SEMANTIC_SHA256':base['SEMANTIC_SHA256'],'ADDITIONAL_CONTRACT_IDENTITIES':{n:hashlib.sha256(canon(v)).hexdigest() for n,v in d.items()},'ADDITIONAL_CONTRACT_COVERAGE':'PASS','OPERATIONAL_QUALIFICATION':False,'OVERALL_PACKAGE':'PARTIAL'}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':semantic,'SEMANTIC_SHA256':hashlib.sha256(canon(semantic)).hexdigest()},sort_keys=True))
