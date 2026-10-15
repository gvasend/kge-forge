"""Versioned corrections proven by static source/schema inconsistencies."""
import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;OLD=O.with_name('E2_P05_D01_RUNNER_FIXTURE_CLOSURE_1')
def read(p):return json.loads(Path(p).read_bytes())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def save(n,v):(O/n).write_bytes(canon(v)+b'\n')
def ref(p):return dict(path=str(Path(p).relative_to(R)),raw_sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest())
old=read(OLD/'dispatch-table.json');table=deepcopy(old);findings=[]
# No native case invoked: prove original source carries result bindings but no consumers.
for name in ['E2-A06_OPERANDS','E2-A06_ORACLE','E2-A11_OPERANDS','E2-A11_ORACLE']:
 p=old['D01-DISPATCH:'+name]
 assert p['steps'][0]['args']==p['steps'][1]['args']
 assert not any('context_field' in b for b in p['steps'][1]['args'])
 findings.append(dict(id='REUSED_ORIGINAL_COMMIT:'+name,source=ref(OLD/'dispatch-table.json'),pointer='/D01-DISPATCH:'+name,proof='Both commits use same original fixture bundle/event; bind_result_as values are never referenced. This cannot implement successive distinct native phases.'))
 tree=ast.parse((OLD/'runner.py').read_text())
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='capture');ret=next(n for n in fn.body if isinstance(n,ast.Return));fields={k.arg for k in ret.value.keywords}
expected=set(read(OLD/'normalization-and-output-schema.json')['fields']);assert expected-fields=={'output_field_set'}
findings.append(dict(id='OUTPUT_SCHEMA_FIELD_MISSING',source=ref(OLD/'runner.py'),proof='capture return keywords omit output_field_set required by sealed schema',missing=['output_field_set']))
findings.append(dict(id='RESTORE_RESULT_NOT_USED',source=ref(OLD/'dispatch-table.json'),pointer='/D01-DISPATCH:PHASE_COLD_RESTORED',proof='RECOMPUTE reads fixture.snapshot, not restored result.current'))
findings.append(dict(id='N05_VARIANT_INCOMPATIBLE_PATH',source=ref(OLD/'dispatch-table.json'),pointer='/D01-DISPATCH:E2-N05_OPERANDS',proof='Domain-only variant is marked complete with pin but path first requires LOAD_PIN(source_root,pin); variants require distinct exact paths'))
findings.append(dict(id='ROOT_SCOPE_FLAGS_INSUFFICIENT',source=ref(OLD/'runner.py'),proof='Completeness only checks packet boolean; original static preflight does not resolve args, result dependencies or authoritative defaults'))
for did,path in table.items():
 for i,step in enumerate(path['steps']):
  op=step['operation_id']
  for j,b in enumerate(step['args']):
   if b.get('fixture_field') in ['repo_root','source_root']:step['args'][j]={'context_field':'source_root'}
   elif b.get('fixture_field')=='output_dir':step['args'][j]={'context_field':'store_root'}
   elif i and op=='COMMIT_EVENT' and b.get('fixture_field')=='bundle':step['args'][j]={'prior_result':'step_'+str(i-1)+'_native_result','selector':[0]}
   elif i and op=='RESUME' and b.get('fixture_field')=='bundle':step['args'][j]={'prior_result':'step_'+str(i-1)+'_native_result','selector':[0]}
  if op=='COMMIT_EVENT':
   for j,b in enumerate(step['args']):
    if b.get('fixture_field')=='event':step['args'][j]={'fixture_field':'event_'+str(i)}
  if i and op=='RECOMPUTE' and path['steps'][i-1]['operation_id']=='RESTORE':step['args'][0]={'prior_result':'step_'+str(i-1)+'_native_result','selector':['current']}
  step['sealed_native_defaults']={}
  module,pathfn=read(OLD/'supported-operation-set.json')[op]['module'],read(OLD/'supported-operation-set.json')[op]['entrypoint']
  if module:
   tree=ast.parse((R/(module.replace('.','/')+'.py')).read_text());f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==pathfn)
   positional=f.args.args;start=len(positional)-len(f.args.defaults)
   for arg,default in zip(positional[start:],f.args.defaults):step['sealed_native_defaults'][arg.arg]=ast.dump(default)
   for arg,default in zip(f.args.kwonlyargs,f.args.kw_defaults):
    if default is not None:step['sealed_native_defaults'][arg.arg]=ast.dump(default)
# Explicit subvariant paths, never guessed from runtime operand content.
for name in ['E2-N05_OPERANDS','E2-N05_ORACLE']:
 p=table['D01-DISPATCH:'+name]
 p['variant_paths']={
  'D01-VARIANT:E2-N05:WRONG_RAW_BYTES':[dict(operation_id='LOAD_PIN',args=[{'context_field':'source_root'},{'fixture_field':'pin'}],kwargs={},bind_result_as='step_0_native_result',sealed_native_defaults={})],
  'D01-VARIANT:E2-N05:SAME_DIGEST_WRONG_IDENTITY_DOMAIN':[dict(operation_id='VALIDATE_PIN',args=[{'fixture_field':'pin'}],kwargs={},bind_result_as='step_0_native_result',sealed_native_defaults={})]}
 p['variant_selection']='EXACT_SEALED_STATE_VARIANT_ID_ONLY'
save('internal-inconsistency-evidence.json',dict(findings=findings,prior_files_changed=False,classification='VERSIONED_ORCHESTRATION_AND_BINDING_CORRECTION; no native capability change'))
save('dispatch-table-v2.json',table)
# Copy source version, preserving old source as authority/provenance.
text=(OLD/'runner.py').read_text()
text=text.replace('from common import ROOT,OUT,TYPE,OPERATIONS,read,ref,demand,filehash,canonical,qid','from common_v2 import ROOT,OUT,TYPE,OPERATIONS,read,ref,demand,filehash,canonical,qid')
text=text.replace("    raise ValueError('INVALID_ARGUMENT_BINDING')", "    if isinstance(binding,dict) and set(binding)=={'prior_result','selector'}:\n        demand(binding['prior_result'] in context,'UNRESOLVED_PRIOR_RESULT')\n        value=context[binding['prior_result']]\n        for part in binding['selector']:\n            value=value[part] if isinstance(part,int) else getattr(value,part)\n        return value\n    raise ValueError('INVALID_ARGUMENT_BINDING')")
text=text.replace("    return dict(qualification_label=", "    captured=dict(qualification_label=")
text=text.replace("native_result=normalize(result))\n\ndef execute_job", "native_result=normalize(result))\n    captured['output_field_set']=sorted(list(captured)+['output_field_set'])\n    return captured\n\ndef execute_job")
text=text.replace("    for step in path['steps']:","    steps=path.get('variant_paths',{}).get(packet['state_variant_id'],path['steps'])\n    if 'variant_paths' in path:demand(packet['state_variant_id'] in path['variant_paths'],'UNKNOWN_SEALED_VARIANT_PATH')\n    for step in steps:")
text=text.replace("read(OUT/'dispatch-table.json')","read(OUT/'dispatch-table-v2.json')")
# Retain last returned native bundle/report when later observation returns no state.
text=text.replace("        # Sequence chaining is explicit metadata; no Planner decisions made here.","        if isinstance(result,tuple) and result and type(result[0]).__name__=='PersistenceBundle':bundle=result[0];subject=bundle.current\n        elif type(result).__name__=='PersistenceBundle':bundle=result;subject=bundle.current\n        elif type(result).__name__=='TransitionReport':subject=result.snapshot\n        # These are native returned states, never runner-created transitions.")
(O/'runner_v2.py').write_text(text)
common=(OLD/'common.py').read_text();(O/'common_v2.py').write_text(common)
save('runner-v2-source-seal.json',dict(label='PROSPECTIVE_RUNNER_VERSIONED_CORRECTION_NOT_FULLY_READY',source=ref(O/'runner_v2.py'),helpers=ref(O/'common_v2.py'),dispatch=ref(O/'dispatch-table-v2.json'),supersedes=ref(OLD/'runner-source-seal.json'),qualification_cases_invoked=0,complete_output_oracles=False))
print('PROVEN_INCONSISTENCIES_VERSIONED; NATIVE_OPERATIONS_NOT_EXECUTED')
