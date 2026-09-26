"""Controller-owned disclosure policy. Read authority never grants disclosure."""
import hashlib
import json
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def production_policy(binding):
    return {'schema': 1,
            'authority_source': 'Architect PD-06 blocker-closure instruction, 2026-09-16',
            'default': 'DENY',
            'initial_clearances': [], 'file_clearances': [],
            'private_paths': [], 'credential_paths': [],
            'evidence_paths': [str(binding.repos['forge'] / 'docs/experiments/E1/pre_dispatch')] if hasattr(binding, 'repos') else [],
            'hard_denied_components': ['.git', '.codex', '.agents'],
            'permitted_result_category': 'cleared file bytes or constant redaction indication only',
            'excluded_categories': ['credentials', 'secrets', 'controller-private state'],
            'protected_material': 'separate exact-content clearance required',
            'evidence_material': 'separate exact-content clearance required',
            'context_sha256': binding.digest}


class TransmissionBoundary:
    def __init__(self, host):
        self.host = host
        raw = host.auth.model_transmission
        self.policy = json.loads(raw) if raw else None
        if self.policy is not None:
            if (self.policy.get('schema') != 1 or self.policy.get('default') != 'DENY'
                    or not self.policy.get('authority_source')
                    or self.policy.get('hard_denied_components') != ['.git', '.codex', '.agents']
                    or self.policy.get('excluded_categories') !=
                    ['credentials', 'secrets', 'controller-private state']):
                raise ValueError('invalid model transmission policy')
        self.policy_digest = digest(self.policy)

    def audit(self, kind, outcome):
        # No content, path, error text, credential, or model-controlled label.
        self.host._write({'event': 'model_transmission', 'category': kind,
                          'decision': outcome, 'policy_sha256': self.policy_digest,
                          'authorization_id': self.host.auth.authorization_id,
                          'authorization_revision': self.host.auth.revision})

    def initial(self, task, context):
        value = {'task': task, 'context': context}
        allowed = self.policy is not None and any(
            row.get('sha256') == digest(value) and row.get('authority_source')
            and row.get('category') == 'cleared-reasoning-context'
            for row in self.policy.get('initial_clearances', []))
        self.audit('initial-context', 'ALLOW' if allowed else 'DENY')
        if not allowed:
            raise ValueError('initial model context lacks separate transmission clearance')
        return value

    def result(self, call, result):
        # Even status can encode a predicate over protected execution inputs.
        # Unclearable bodies and outcomes therefore receive an identical indication.
        # Never copy diagnostics, paths, hashes, status/evidence, or echoes.
        status = result.get('result')
        safe = {'transmission': 'REDACTED',
                'notice': 'Content unavailable under model transmission authority'}
        allowed = False
        from .governed_host import Denied
        if self.policy is not None and call.get('name') == 'governed_read' and status == 'SUCCEEDED':
            try:
                args = json.loads(call['arguments'])
                path = self.host._path(args['repository'], args['path'])
                data = result['data']
                # Check the actual returned bytes, not a later filesystem read.
                hidden = any(x in path.parts for x in ('.git', '.codex', '.agents'))
                def within(entries):
                    return any(path == Path(p) or Path(p) in path.parents for p in entries)
                forbidden = within(self.policy.get('private_paths', []) +
                                   self.policy.get('credential_paths', []))
                evidence = within(self.policy.get('evidence_paths', []))
                for row in self.policy.get('file_clearances', []):
                    if (not hidden and not forbidden and row.get('path') == str(path)
                            and data.get('path') == str(path)
                            and row.get('authority_source')
                            and row.get('category') in ('ordinary', 'explicitly-cleared-governing',
                                                       'explicitly-cleared-evidence')
                            and row.get('sha256') == hashlib.sha256(data['content'].encode()).hexdigest()):
                        if evidence and row['category'] != 'explicitly-cleared-evidence':
                            continue
                        protected = any(path == Path(p) or Path(p) in path.parents
                                        for p in self.host.auth.write_deny_roots)
                        binding = self.host.auth.context_binding
                        protected = protected or (binding is not None and path in binding.protected_paths)
                        if protected and row['category'] not in ('explicitly-cleared-governing',
                                                                 'explicitly-cleared-evidence'):
                            continue
                        safe = {'result': 'SUCCEEDED', 'transmission': 'CLEARED',
                                'content': data['content']}
                        allowed = True
                        break
            except (Denied, KeyError, ValueError, TypeError, OSError):
                pass
        self.audit('tool-result', 'ALLOW' if allowed else 'REDACT')
        return safe
