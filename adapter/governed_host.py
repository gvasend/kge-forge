"""Minimal A2 governed execution interface.

The host owns immutable authorization, path policy, audit, and a turn supervisor.
It is a substrate component; no product semantics live here.
"""
from dataclasses import dataclass, field
from pathlib import Path
import hashlib, json, os, shutil, signal, subprocess, tempfile, time, uuid

class Denied(Exception): pass

@dataclass(frozen=True)
class WorkAuthorization:
    authorization_id: str; revision: int; work_package_id: str; session_id: str; turn_id: str
    read_roots: tuple = (); write_roots: tuple = (); deny_roots: tuple = ()
    exec_bins: tuple = (); shell: bool = False; network: bool = False; state: str = "ACTIVE"

@dataclass
class Invocation:
    id: str; tool: str; decision: str; authorization_id: str; scope_id: str = ""
    start: float = 0.0; end: float = 0.0; result: dict = field(default_factory=dict)

class Scope:
    def __init__(self, root):
        self.id = "scope-" + uuid.uuid4().hex; self.root = Path(root).resolve(); self.state="ACTIVE"
        self.proc = None; self.created = time.monotonic(); self.revoked = None; self.quiescent = None
        self.process_group = None
    def launch(self, argv, cwd):
        if self.state != "ACTIVE": raise Denied("scope is not active")
        cwd = Path(cwd).resolve()
        if self.root not in cwd.parents and cwd != self.root: raise Denied("cwd outside scope")
        self.proc = subprocess.Popen(['/usr/bin/bwrap','--die-with-parent','--unshare-pid','--new-session','--proc','/proc','--dev','/dev','--bind',str(self.root),'/scope','--chdir','/scope','--ro-bind','/usr','/usr','--ro-bind','/bin','/bin','--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64','--unshare-net',*argv], start_new_session=True)
        self.process_group = os.getpgid(self.proc.pid)
        return self.proc
    def members(self):
        """Independently observe host processes in this launch process group."""
        if self.process_group is None: return []
        try: return [p.pid for p in os.scandir('/proc') if p.name.isdigit() and os.getpgid(int(p.name)) == self.process_group]
        except (OSError, ProcessLookupError): return []
    def revoke(self):
        self.state="REVOKING"; self.revoked=time.monotonic()
        if self.proc and self.proc.poll() is None:
            try: os.killpg(self.process_group, signal.SIGTERM); self.proc.wait(.5)
            except subprocess.TimeoutExpired:
                try: os.killpg(self.process_group, signal.SIGKILL)
                except ProcessLookupError: pass
                self.proc.wait(2)
        deadline=time.monotonic()+2
        while self.members() and time.monotonic()<deadline: time.sleep(.02)
        self.state="QUIESCENT" if not self.members() else "REVOCATION_FAILED"
        self.quiescent=time.monotonic() if self.state=="QUIESCENT" else None

class GovernedHost:
    def __init__(self, authorization, audit_path):
        self.auth=authorization; self.audit=Path(audit_path); self.audit.parent.mkdir(parents=True,exist_ok=True)
        self.scope=None; self.invocations=[]; self.architectural_state="AUTHORIZED"
        self._write({"event":"authorization_issued","authorization":authorization.__dict__})
    def _write(self, event):
        with self.audit.open("a") as f: f.write(json.dumps({"time":time.monotonic(),**event})+"\n")
    def _path(self, repo, rel, write=False):
        root=Path(repo).resolve(); p=(root/rel).resolve()
        if root not in p.parents and p != root: raise Denied("path escape")
        if any(p==Path(d).resolve() or Path(d).resolve() in p.parents for d in self.auth.deny_roots): raise Denied("denied path")
        roots=self.auth.write_roots if write else self.auth.read_roots
        if not any(p==Path(x).resolve() or Path(x).resolve() in p.parents for x in roots): raise Denied("outside grant")
        return p
    def _inv(self, tool, fn):
        i=Invocation("inv-"+uuid.uuid4().hex,tool,"AUTHORIZED",self.auth.authorization_id,self.scope.id if self.scope else "",time.monotonic())
        try: i.result=fn(); i.decision="SUCCEEDED"
        except Denied as e: i.decision="DENIED"; i.result={"error":str(e)}; raise
        finally: i.end=time.monotonic(); self.invocations.append(i); self._write({"event":"invocation","invocation":i.__dict__})
        return i.result
    def governed_read(self, repo, rel, limit=65536):
        return self._inv("governed_read",lambda:{"path":str(self._path(repo,rel)),"content":self._path(repo,rel).read_bytes()[:limit].decode(errors="replace")})
    def governed_write(self, repo, rel, content):
        def f():
            p=self._path(repo,rel,True); p.parent.mkdir(parents=True,exist_ok=True); fd,tmp=tempfile.mkstemp(dir=p.parent); os.write(fd,content.encode()); os.fsync(fd); os.close(fd); os.replace(tmp,p); return {"path":str(p),"sha256":hashlib.sha256(content.encode()).hexdigest()}
        return self._inv("governed_write",f)
    def governed_patch(self, repo, changes):
        def f():
            paths=[self._path(repo,c["path"],True) for c in changes]
            for c,p in zip(changes,paths):
                if c["op"]!="write": raise Denied("unsupported patch operation")
            originals={p:p.read_bytes() if p.exists() else None for p in paths}
            try:
                for c,p in zip(changes,paths): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(c["content"])
            except Exception:
                for p,v in originals.items():
                    if v is None and p.exists(): p.unlink()
                    elif v is not None: p.write_bytes(v)
                raise
            return {"count":len(paths)}
        return self._inv("governed_patch",f)
    def governed_exec(self, argv, cwd):
        if not argv or Path(argv[0]).name not in self.auth.exec_bins: raise Denied("executable denied")
        if not self.scope: self.scope=Scope(cwd); self.architectural_state="RUNNING"
        return self._inv("governed_exec",lambda:{"scope":self.scope.id,"pid":self.scope.launch(list(argv),cwd).pid})
    def expansion(self, capability, action, resources, reason):
        e={"event":"authority_expansion","id":"exp-"+uuid.uuid4().hex,"authorization_id":self.auth.authorization_id,"capability":capability,"action":action,"resources":resources,"reason":reason,"decision":"PENDING"};self._write(e);return e
    def revoke(self):
        self.architectural_state="INTERRUPTING"; self._write({"event":"revoke"})
        if self.scope: self.scope.revoke()
        self.architectural_state="QUIESCENT" if not self.scope or self.scope.state=="QUIESCENT" else "FAILED"
        self._write({"event":"architectural_state","state":self.architectural_state,"scope":self.scope.state if self.scope else "NONE"}); return self.architectural_state
    def status(self): return {"authorization_id":self.auth.authorization_id,"turn_id":self.auth.turn_id,"scope_id":self.scope.id if self.scope else None,"scope_state":self.scope.state if self.scope else "NONE","architectural_state":self.architectural_state,"active_invocations":sum(i.end==0 for i in self.invocations)}
