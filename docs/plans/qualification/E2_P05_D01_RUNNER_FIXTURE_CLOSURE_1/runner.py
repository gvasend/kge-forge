"""Prospective aggregate orchestration. Static preflight invokes no case.

All Planner semantics dispatch to the closed existing native registry. A trusted
application scope verifier and a complete sealed matrix are required to run.
Expected files are opened only after native execution/capture, never as operands.
"""
import argparse
import ast
from dataclasses import fields, is_dataclass
from enum import Enum
import importlib
import os
from pathlib import Path
import subprocess
import sys
from common import ROOT,OUT,TYPE,OPERATIONS,read,ref,demand,filehash,canonical,qid

RESPONSIBILITIES=('fixture_loading','native_invocation','sealed_phase_control','isolated_mutation','native_invalidation','writer_termination','cold_reader_launch','declared_permutations','result_capture','full_output_comparison','exact_failure_capture')

def check_pin(pin):demand(filehash(ROOT/pin['path'])==pin['raw_sha256'],'PIN_CHANGED:'+pin['path'])

def typed_load(value):
    # Codec decoding performs structural type admission, not a case operation.
    from adapter.planner import codec
    if isinstance(value,dict) and ('$type' in value or '$enum' in value):return codec._unwire(value)
    if isinstance(value,list):return codec._unwire(value)
    if isinstance(value,dict) and value.get('qualification_type')=='SelectionTrace':
        from adapter.planner.selector import SelectionTrace
        return SelectionTrace(codec._unwire(value['selected']),value['criterion'],tuple(value['steps']))
    return value

def normalize(value):
    """Native unordered declarations only; all other list/tuple order stays."""
    from adapter.planner import codec
    if codec.TYPES.get(type(value).__name__) is type(value):return codec._wire(value)
    if isinstance(value,Enum):return {'$enum':type(value).__name__,'value':value.value}
    if is_dataclass(value):return {'qualification_type':type(value).__name__,**{f.name:normalize(getattr(value,f.name)) for f in fields(value)}}
    if isinstance(value,dict):return {k:normalize(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [normalize(v) for v in value]
    if isinstance(value,bytes):return {'qualification_bytes_hex':value.hex()}
    if isinstance(value,Path):return {'qualification_process_path':str(value)}
    return value

def native_function(symbol):
    demand(symbol in OPERATIONS,'UNKNOWN_OPERATION')
    module,name,*_=OPERATIONS[symbol]
    demand(module is not None,'QUALIFICATION_METADATA_IS_NOT_NATIVE_TRANSITION')
    return getattr(importlib.import_module(module),name)

def resolve(binding,fixture,context):
    # Strict references; matrix cannot serialize a callable, module or heuristic.
    if isinstance(binding,dict) and set(binding)=={'fixture_field'}:
        field=binding['fixture_field'];demand(field in fixture['arguments'],'MISSING_OPERATIVE_FIXTURE_ARGUMENT:'+field)
        return typed_load(fixture['arguments'][field])
    if isinstance(binding,dict) and set(binding)=={'context_field'}:
        demand(binding['context_field'] in context,'UNKNOWN_CONTEXT_INPUT')
        return context[binding['context_field']]
    if isinstance(binding,dict) and set(binding)=={'literal'}:return binding['literal']
    raise ValueError('INVALID_ARGUMENT_BINDING')

def capture(subject,bundle,result,error,context):
    from adapter.planner import codec,core,gates
    current=getattr(result,'snapshot',None) or getattr(result,'current',None) or subject
    if isinstance(result,tuple) and result and type(result[0]).__name__=='PersistenceBundle':bundle=result[0];current=bundle.current
    if type(result).__name__=='Snapshot':current=result
    if type(result).__name__=='PersistenceBundle':bundle=result;current=bundle.current
    computation=result if type(result).__name__=='Computation' else core.recompute(current)
    resume=core.resume_eligibility(bundle,context['source_root']) if bundle else None
    proofs=[{'requirement':normalize(r.id),'proof':normalize(gates.obligation_proof(current,r.id))} for r in sorted(current.evidence_requirements,key=lambda r:canonical(normalize(r.id)))]
    return dict(qualification_label={'type':TYPE,'historical_reconstruction':False,'native_context':normalize(current.context)},typed_snapshot=normalize(current),typed_bundle=normalize(bundle),Computation=normalize(computation),selection=normalize(computation.selection),resume=normalize(resume),branches=normalize(computation.branches),witnesses=normalize(proofs),rejections=error,policy=normalize(bundle.policy) if bundle else None,source_pins=sorted(normalize(bundle.sources),key=canonical) if bundle else None,snapshot_identity=normalize(codec.snapshot_id(current)),bundle_identity=normalize(codec.bundle_id(bundle,snapshot_resolver=context.get('snapshot_resolver'))) if bundle else None,event_identities=normalize(bundle.events) if bundle else [],native_result=normalize(result))

def execute_job(row,path,fixture,context):
    demand(row['RUNNER_DISPATCH_ID']==path['dispatch_id'],'WRONG_DISPATCH')
    demand(path['obligation_id']==row['OBLIGATION_ID'],'DISPATCH_OBLIGATION_MISMATCH')
    demand(fixture['execution_inputs_complete'],'INCOMPLETE_FIXTURE_CANNOT_EXECUTE')
    packet=fixture
    fixture=dict(packet['canonical_content'],metadata_inputs={'source_pins':packet['provenance']})
    subject=typed_load(fixture['subject']);bundle=typed_load(fixture['bundle']) if fixture.get('bundle') else None
    result=None;error=None
    if path['operation_ids']==['QUALIFICATION_METADATA']:
        for pin in fixture['metadata_inputs']['source_pins']:check_pin(pin)
        result={'input_pin_count':len(fixture['metadata_inputs']['source_pins']),'dispatch_obligation':row['OBLIGATION_ID']}
        return capture(subject,bundle,result,None,context)
    for step in path['steps']:
        args=[resolve(b,fixture,context) for b in step['args']]
        kwargs={k:resolve(v,fixture,context) for k,v in step['kwargs'].items()}
        try:result=native_function(step['operation_id'])(*args,**kwargs)
        except Exception as exc:
            error={'exception':type(exc).__name__,'message':str(exc),'operation_id':step['operation_id']}
            break
        # Sequence chaining is explicit metadata; no Planner decisions made here.
        if step['bind_result_as'] is not None:context[step['bind_result_as']]=result
    return capture(subject,bundle,result,error,context)

def run_preapproved(config,scope_verifier):
    demand(config['construction_ready'] is True,'MATRIX_NOT_CONSTRUCTION_READY')
    # Trusted application hook, never decoded from wire or inferred from a hash.
    demand(callable(scope_verifier),'TRUSTED_SCOPE_VERIFIER_REQUIRED')
    demand(scope_verifier(config) is True,'SCOPE_NOT_AUTHORIZED')
    for pin in config['runner_and_runtime_pins']:check_pin(pin)
    matrix=read(ROOT/config['matrix']['path']);dispatch=read(ROOT/config['dispatch']['path'])
    check_pin(config['matrix']);check_pin(config['dispatch'])
    result=[]
    for row in matrix['rows']:
        demand(row['RUNNER_DISPATCH_ID'] in dispatch,'MISSING_DISPATCH')
        fixture=read(ROOT/row['fixture_reference']['path']);check_pin(row['fixture_reference'])
        context={'source_root':ROOT/row['source_root'],'store_root':ROOT/row['isolated_store_root']}
        observed=execute_job(row,dispatch[row['RUNNER_DISPATCH_ID']],fixture,context)
        # Independent expectation is not visible to native operands.
        oracle=read(ROOT/row['oracle_reference']['path']);check_pin(row['oracle_reference'])
        demand(observed==oracle['expected_full_output'],'FULL_OUTPUT_MISMATCH:'+row['OBLIGATION_ID'])
        result.append({'obligation':row['OBLIGATION_ID'],'output':observed})
    return result

def cold_readers(writer_command,reader_commands,context):
    # Arguments and environment are presealed; no inherited writer object graph.
    w=subprocess.run(writer_command,cwd=context['cwd'],env=context['environment'],capture_output=True)
    demand(w.returncode==0,'WRITER_FAILED') # wait() establishes process termination.
    rows=[]
    for argv in reader_commands:
        r=subprocess.run(argv,cwd=context['cwd'],env=context['environment'],capture_output=True)
        demand(r.returncode==0,'COLD_READER_FAILED');rows.append(r.stdout)
    return rows

def static_preflight():
    paths=read(OUT/'dispatch-table.json');seen=[];targets=[]
    for did,p in paths.items():
        demand(did==p['dispatch_id'],'DISPATCH_KEY_MISMATCH');seen.append(p['obligation_id'])
        for op in p['operation_ids']:
            demand(op in OPERATIONS,'UNKNOWN_OPERATION')
            module,fn,*_=OPERATIONS[op]
            if module:
                source=ROOT/(module.replace('.','/')+'.py')
                tree=ast.parse(source.read_text())
                demand(any(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==fn for n in tree.body),'MISSING_NATIVE_TARGET:'+module+'.'+fn)
                targets.append(module+'.'+fn)
    demand(len(seen)==len(set(seen))==128,'MISSING_OR_AMBIGUOUS_DISPATCH')
    catalog=read(OUT/'fixture-catalog.json');loads=[]
    for entry in catalog.values():
        pin=entry['artifact'];check_pin(pin);f=read(ROOT/pin['path'])
        demand(f['fixture_id']==entry['fixture_id'],'WRONG_FIXTURE_ID')
        demand(qid('fixture-content',f['canonical_content'])==f['content_identity'],'WRONG_FIXTURE_CONTENT')
        # Decode ordinary native structural records only, not validate_model/recompute.
        typed_load(f['canonical_content']['subject'])
        loads.append(f['fixture_id'])
    return dict(dispatch='PASS_128_OF_128_STATIC',native_targets='PASS_EXISTING_FUNCTIONS',fixture_structural_loads=len(loads),qualification_case_calls=0,runner_execution=False,construction_readiness=False,complete_matrix_validation='NOT_AVAILABLE')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['static-preflight'])
    args=parser.parse_args();print(__import__('json').dumps(static_preflight(),sort_keys=True))
