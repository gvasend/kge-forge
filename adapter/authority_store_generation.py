"""Bounded immutable authority-store generation selection.

This module never infers selection from a candidate generation.  An external,
content-bound selection record is required and is written only to the supplied
store root.  Callers can qualify against a faithful copy before touching a live
store.
"""
from __future__ import annotations
import copy, hashlib, json, os, shutil, tempfile
from pathlib import Path

class GenerationDenied(ValueError):
    pass

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
def digest(data): return hashlib.sha256(data).hexdigest()
def file_digest(path): return digest(Path(path).read_bytes())

def lineage(root, controller_lineage, purpose="controller-authority"):
    root=Path(root); cat=json.loads((root/'catalog.json').read_text())
    return {
      "schema":"AUTHORITY-STORE-LINEAGE-1", "purpose":purpose,
      "controller_lineage":controller_lineage,
      "store_locator":str(root.resolve()),
      "catalog_sha256":file_digest(root/'catalog.json'),
      "generation":"AUTHORITY-STORE-GENERATION-sha256:"+file_digest(root/'catalog.json'),
      "catalog_schema":cat.get('schema'),
    }

def build_successor(source, destination, *, selection_bytes, selection_identity,
                    delta_identity, architect_selection, controller_lineage):
    """Build G(n+1) from exact source bytes; source is never mutated."""
    source=Path(source); destination=Path(destination)
    if destination.exists(): raise GenerationDenied("destination already exists")
    if not (source/'catalog.json').is_file(): raise GenerationDenied('source catalog missing')
    shutil.copytree(source,destination)
    old_catalog=json.loads((source/'catalog.json').read_text())
    old_hash=file_digest(source/'catalog.json')
    selection_hash=digest(selection_bytes)
    # Selection object is added to the immutable catalog; applicability is
    # unchanged so every inherited object remains byte/content-valid.
    objects=copy.deepcopy(old_catalog['objects'])
    if selection_identity in objects: raise GenerationDenied('selection already present')
    objects[selection_identity]={
      'sha256':selection_hash, 'evidence':[],
      'authority_source':{'authority_id':'Architect','sha256':selection_hash},
      'release_identities':copy.deepcopy(old_catalog['applicability']),
      'temporal_applicability':copy.deepcopy(old_catalog['applicability']),
      'mutation':'IMMUTABLE'}
    out_catalog=copy.deepcopy(old_catalog); out_catalog['objects']=objects
    cat_bytes=canonical(out_catalog); new_hash=digest(cat_bytes)
    obj_path=destination/selection_hash; obj_path.write_bytes(selection_bytes); os.chmod(obj_path,0o600)
    (destination/'catalog.json').write_bytes(cat_bytes); os.chmod(destination/'catalog.json',0o600)
    generation={
      'schema':'AUTHORITY-STORE-GENERATION-1',
      'predecessor_catalog_sha256':old_hash,
      'predecessor_generation':'AUTHORITY-STORE-GENERATION-sha256:'+old_hash,
      'resulting_catalog_sha256':new_hash,
      'id':'AUTHORITY-STORE-GENERATION-sha256:'+new_hash,
      'delta':delta_identity, 'added_records':[selection_identity],
      'controller_lineage':controller_lineage,
      'selection':'CONSTRUCTED_NOT_SELECTED', 'transition_authority':architect_selection,
    }
    delta={'schema':'AUTHORITY-STORE-GENERATION-DELTA-1','id':delta_identity,
      'predecessor_generation':'AUTHORITY-STORE-GENERATION-sha256:'+old_hash,
      'scope':'EXACT_SINGLE_SELECTION_RECORD','added_records':[selection_identity],
      'selection_sha256':selection_hash,'transition_authority':architect_selection}
    selection_body={'schema':'AUTHORITY-STORE-GENERATION-SELECTION-1',
      'predecessor_generation':'AUTHORITY-STORE-GENERATION-sha256:'+old_hash,
      'selected_generation':'AUTHORITY-STORE-GENERATION-sha256:'+new_hash,
      'delta':delta_identity,'store_lineage':lineage(source,controller_lineage),
      'architect_authority':architect_selection,'replay':'REJECT','scope':'EXACT_G0_TO_G1'}
    selection={'id':'AUTHORITY-STORE-GENERATION-SELECTION-sha256:'+digest(canonical(selection_body)), **selection_body}
    for name,data in [('GENERATION.json',generation),('GENERATION_DELTA.json',delta),('SELECTION.json',selection)]:
      (destination/name).write_bytes(canonical(data)); os.chmod(destination/name,0o600)
    return generation,delta,selection

def select(root, selection, *, expected_source_generation, expected_lineage):
    """Select only a prebuilt generation in a qualified store copy."""
    root=Path(root); cat_hash=file_digest(root/'catalog.json')
    if expected_source_generation != selection['predecessor_generation']:
        raise GenerationDenied('wrong predecessor generation')
    if selection['store_lineage']['catalog_sha256'] != expected_lineage['catalog_sha256']:
        raise GenerationDenied('wrong store lineage')
    if selection.get('selected_generation','').startswith('AUTHORITY-STORE-GENERATION-sha256:') is False:
        raise GenerationDenied('invalid selected generation')
    journal=root/'generation-selection.jsonl'
    if journal.exists() and journal.stat().st_size: raise GenerationDenied('replayed or competing selection')
    row={**selection,'status':'SELECTED','selected_catalog_sha256':cat_hash}
    with journal.open('wb') as f: f.write(canonical(row)+b'\n'); f.flush(); os.fsync(f.fileno())
    return row

def reconstruct(root, controller_lineage):
    root=Path(root); cat_hash=file_digest(root/'catalog.json')
    journal=root/'generation-selection.jsonl'
    if not journal.exists():
        return {'selected_generation':'AUTHORITY-STORE-GENERATION-sha256:'+cat_hash,'selection_source':None}
    rows=[json.loads(x) for x in journal.read_bytes().splitlines() if x]
    if len(rows)!=1 or rows[0].get('status')!='SELECTED': raise GenerationDenied('ambiguous selection')
    row=rows[0]
    if row['selected_generation'] != 'AUTHORITY-STORE-GENERATION-sha256:'+cat_hash: raise GenerationDenied('selected catalog mismatch')
    if row['store_lineage']['controller_lineage'] != controller_lineage: raise GenerationDenied('lineage mismatch')
    return {'selected_generation':row['selected_generation'],'selection_source':digest(canonical(row))}
