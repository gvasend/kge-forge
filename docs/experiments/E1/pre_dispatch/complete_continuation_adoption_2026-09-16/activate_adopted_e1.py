from pathlib import Path
import json,os,sys
source=Path('/tmp/adopt_complete_e1.py').read_text().split("if len(sys.argv)>1 and sys.argv[1]=='reconstruct':")[0]
exec(compile(source,'/tmp/adopt_complete_e1.py','exec'))
from adapter.activation_transaction import ActivationTransaction
auth,audit,ref,result=reconstruct()
before=audit.read_bytes();ledger=Path(auth.ownership_ledger);ledger_before=ledger.read_bytes()
try:
 tx=ActivationTransaction.activate(auth,audit,ref)
 tx.close()
 durable('ACTIVATION_RESULT.json',{'result':'DURABLE_ACTIVE_REQUIRES_INDEPENDENT_RECOVERY','dispatch_inheritance':'PASS','audit_before_sha256':sha(before),'audit_after_sha256':sha(audit.read_bytes()),'E1_model_requests':0,'E1_implementation_effects':0})
except Exception as exc:
 durable('ACTIVATION_RESULT.json',{'result':'BLOCKED','failed_operation':'production activation transaction','exception_type':type(exc).__name__,'reason':str(exc),'dispatch_inheritance':'PASS','adoption':'APPLIED','independent_ancestry_reconstruction':'PASS','audit_before_sha256':sha(before),'audit_after_sha256':sha(audit.read_bytes()),'audit_unchanged':audit.read_bytes()==before,'ownership_ledger_unchanged':ledger.read_bytes()==ledger_before,'ownership_ledger_bytes':len(ledger.read_bytes()),'controller_lock_file_exists':Path(str(ledger)+'.controller-lock').exists(),'E1_model_requests':0,'E1_implementation_effects':0,'retry_attempted':False})
 print(canonical(load(O/'ACTIVATION_RESULT.json')));sys.exit(2)
print(canonical(load(O/'ACTIVATION_RESULT.json')))
