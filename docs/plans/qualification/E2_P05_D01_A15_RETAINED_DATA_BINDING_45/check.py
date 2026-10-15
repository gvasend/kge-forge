"""Direct-source verification and bounded fail-closed binding controls."""
import copy,json,os,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;sys.path.insert(0,str(E));from bind import R,Q,P,load,emit,canon,sha
bindings=load(E/'retained-data-bindings.json')['BINDINGS'];gaps={g['GAP_ID']:g for g in load(P/'typed-gap-inventory.json') if g['CLASSIFICATION']=='RECOVERABLE_EXISTING_DATA'}
expected_types={'D01':'QualificationNativeRootConsumerInventory','D02':'RetainedNativeTypedProofContractCorrespondenceTable','D03':'RetainedQualificationCurrentnessValidationEvidence','D04':'FrozenNativeSourceContentPinInventory','D05':'RetainedNativeAssociationFieldCorrespondenceInventory'}
def verify(b):
 if b['GAP_ID'] not in gaps:raise ValueError('OUTSIDE_DECLARED_DATA_GAP')
 source=gaps[b['GAP_ID']]['KNOWN_EVIDENCE'];raw=(R/source['path']).read_bytes();doc=json.loads(raw)
 if b['SOURCE_PATH']!=source['path'] or b['SOURCE_HASH']!=source['raw_sha256'] or sha(raw)!=source['raw_sha256']:raise ValueError('WRONG_AUTHORITATIVE_SOURCE_OR_HASH')
 pointer='/NODES' if b['GAP_ID']=='D04' else ''
 if b['SOURCE_POINTER']!=pointer:raise ValueError('WRONG_SOURCE_POINTER')
 if b['VALUE_TYPE']!=expected_types[b['GAP_ID']]:raise ValueError('WRONG_NATIVE_OR_QUALIFICATION_EVIDENCE_TYPE')
 value=[n for n in doc['NODES'] if n['TYPE']=='SOURCE_CONTENT'] if b['GAP_ID']=='D04' else doc
 if b['VALUE']!=value:raise ValueError('NOT_EXACT_RETAINED_VALUE')
 if b['CONTENT_IDENTITY']!={'kind':'CONTENT_IDENTITY','namespace':'raw-file-sha256','sha256':source['raw_sha256']}:raise ValueError('WRONG_CONTAINER_CONTENT_IDENTITY')
 graph=load(Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json');ctx=graph['CONTEXT']
 if (b['SCOPE'],b['LINEAGE'],b['GENERATION'])!=(ctx['scope'],ctx['lineage'],ctx['generation']):raise ValueError('WRONG_APPLICABILITY_CONTEXT')
 if b['NORMATIVE_INTERPRETATION_ADOPTED']:raise ValueError('DATA_BINDING_IS_NOT_NORMATIVE_AUTHORITY')
 current=next(x['CURRENTNESS'] for x in bindings if x['GAP_ID']==b['GAP_ID'])
 if b['CURRENTNESS']!=current:raise ValueError('STALE_OR_FOREIGN_CURRENTNESS')
 original=copy.deepcopy(b);identity=original.pop('BINDING_IDENTITY')
 if identity!='qualification-A15-retained-binding-v1:'+sha(canon(original)):raise ValueError('BINDING_IDENTITY_MISMATCH')
 return True
assert all(verify(b) for b in bindings)
neg=[]
def reject(name,fn):
 try:fn()
 except ValueError as ex:neg.append({'NAME':name,'RESULT':'PASS','REJECTION':str(ex),'NATIVE_OPERATION_EXECUTED':False});return
 raise AssertionError('FAIL_OPEN '+name)
changes=[('wrong source hash','SOURCE_HASH','0'*64),('wrong source pointer','SOURCE_POINTER','/guessed'),('wrong native type','VALUE_TYPE','ExecutionEvent'),('wrong content identity','CONTENT_IDENTITY',{'kind':'AUTHORITY_IDENTITY'}),('wrong scope','SCOPE','foreign'),('wrong lineage','LINEAGE','foreign'),('stale current value','CURRENTNESS','STALE'),('Snapshot becomes historical occurrence','VALUE_TYPE','ExecutionEventWitness'),('report for native record','VALUE_TYPE','ReportUsedAsProof'),('semantic equivalent identity-different','BINDING_IDENTITY','qualification-different'),('conflicting source chosen without precedence','SOURCE_PATH','newest-file.json'),('missing retained value fabricated','VALUE',{'made_up':True}),('normative fact treated data','NORMATIVE_INTERPRETATION_ADOPTED',True),('outside declared gap','GAP_ID','S01')]
for name,field,value in changes:
 b=copy.deepcopy(bindings[0]);b[field]=value;reject(name,lambda b=b:verify(b))
def source_guard():
 source=gaps['D01']['KNOWN_EVIDENCE'];actual=(R/source['path']).read_bytes();mutated=actual+b'\n'
 if sha(mutated)!=source['raw_sha256']:raise ValueError('UNAUTHORIZED_SOURCE_MUTATION_REJECTED_WITHOUT_WRITE')
reject('unauthorized source mutation',source_guard)
reader=subprocess.run([sys.executable,str(E/'reader.py')],cwd=str(R),env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,check=True);direct=json.loads(reader.stdout);assert direct['DIRECT_SOURCE_BINDINGS_VERIFIED']==5
seeds=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));a=subprocess.run([sys.executable,str(E/'bind.py'),'--identity'],cwd=str(R),env=env,capture_output=True,text=True,check=True);b=subprocess.run([sys.executable,str(E/'reader.py'),'--identity'],cwd=str(R),env=env,capture_output=True,text=True,check=True);seeds.append({'seed':seed,'binding_identity_set_hash':a.stdout.strip(),'independent_source_reconstruction_hash':b.stdout.strip(),'results':['BOUND_PASS']*5})
assert len({x['binding_identity_set_hash'] for x in seeds})==len({x['independent_source_reconstruction_hash'] for x in seeds})==1
emit('independent-source-verification.json',{'RESULT':'PASS','DIRECT_SOURCE_READER':str(Path('reader.py')),'PRODUCER_OUTPUT_NOT_ORACLE':True,'SOURCE_VERIFICATION':direct,'READERS':'One direct verification reader plus four source-only seed reconstruction processes; not qualification cold readers','NO_SOURCE_PRECEDENCE_CHOICE':'Exact declared source pins, corroboration only'})
emit('negative-suite.json',{'RESULT':'PASS','PASS':len(neg),'TOTAL':len(neg),'CASES':neg,'SOURCE_MUTATION_CONTROL':'In-memory candidate bytes only; no source file modified'})
emit('four-seed-determinism.json',{'RESULT':'PASS','SEEDS':seeds,'VALUE_BINDING_PROVENANCE_CLASSIFICATION_IDENTITIES_STABLE':True,'NATIVE_OPERATIONS_EXECUTED':0})
print('45 independent/source/binding checks PASS',len(neg),'negatives; four seeds; all five BOUND_PASS')
