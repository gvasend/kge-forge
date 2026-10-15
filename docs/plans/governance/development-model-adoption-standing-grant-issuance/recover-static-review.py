import ast,hashlib,json,pathlib,sys
root=pathlib.Path('/home/gvasend/app/kge-forge');d=root/'docs/plans/governance/development-model-adoption-standing-grant-issuance'
t=ast.parse((root/'recover.py').read_text(),feature_version=(3,8));compile(t,'recover.py','exec')
vals={}
for n in t.body:
 if isinstance(n,ast.Assign):
  try:v=ast.literal_eval(n.value)
  except (ValueError,TypeError):continue
  for target in n.targets:
   if isinstance(target,ast.Name):vals[target.id]=v
pins={}
for name,pin in vals['PINS'].items():
 b=(d/name).read_bytes();assert hashlib.sha256(b).hexdigest()==pin; pins[name]=pin
 if name.endswith('.json'):
  v=json.loads(b)
  if 'IDENTITY' in v:
   payload=v.get('RECORD',v.get('CONTENT'))
   assert hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()).hexdigest()==v['IDENTITY']['sha256']
source=(root/'recover_test_source.toml').read_bytes();assert len(source)==1091 and hashlib.sha256(source).hexdigest()==vals['SOURCE_SHA']
functions={n.name:n for n in t.body if isinstance(n,ast.FunctionDef)}
def function_name(n):
 if isinstance(n,ast.Name):return n.id
 if isinstance(n,ast.Attribute):return function_name(n.value)+'.'+n.attr
 return '?'
transaction=functions['recover_transaction'];calls=[(n.lineno,function_name(n.func)) for n in ast.walk(transaction) if isinstance(n,ast.Call)]
def at(name):return min(line for line,fn in calls if fn==name)
assert at('fcntl.flock')<at('consume')<at('write_authenticated')<at('os.fsync')
assert all(not isinstance(n,ast.Attribute) or n.attr not in ('O_CREAT','O_TRUNC') for n in ast.walk(transaction))
assert any(k.arg=='held_fd' and isinstance(k.value,ast.Name) and k.value.id=='fd' for n in ast.walk(transaction) if isinstance(n,ast.Call) for k in n.keywords)
assert [ord(c) for c in next(n for n in ast.walk(functions['durable_consume_and_independently_verify']) if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='serialized' for x in n.targets)).value.func.value.right.value]==[10]
assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='main' for n in t.body)
compile(ast.parse((root/'test_recover.py').read_text(),feature_version=(3,8)),'test_recover.py','exec')
manifest=json.loads((d/'recover-implementation-preservation-before.json').read_text());changed=[]
for name,pin in manifest.items():
 if name=='recover.py':continue
 p=root/name
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=pin:changed.append(name)
assert not changed,changed
result={'AUTHORITY_RAW_PINS':pins,'UTILITY_SHA256':hashlib.sha256((root/'recover.py').read_bytes()).hexdigest(),'TEST_SOURCE_SHA256':hashlib.sha256((root/'test_recover.py').read_bytes()).hexdigest(),'PRESERVED_PRIOR_FILES':len(manifest)-1,'STATIC_PARSE_AND_ORDER':'PASS','RUNTIME_TESTS_EXECUTED':0}
print(json.dumps(result,sort_keys=True))
