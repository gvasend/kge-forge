"""Disposable recovery tests. Run only in an independently permitted environment.
No real adapter, profile destination, or authoritative store is accessed.
"""
import importlib.util
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('recovery_under_test', Path(__file__).with_name('recover.py'))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
DATA = Path(__file__).with_name('recover_test_source.toml').read_bytes()

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='synthetic-recovery-')
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'empty-profile'
        self.path.touch(mode=0o600)
        st = self.path.stat()
        self.expected = (st.st_dev, st.st_ino)
        self.used = False
        # Fixture principal only; CLI still requires the approved real principal.
        self.uid = patch.object(r, 'EXPECTED_UID', os.getuid())
        self.gid = patch.object(r, 'EXPECTED_GID', os.getgid())
        self.uid.start(); self.gid.start()
        self.addCleanup(self.uid.stop); self.addCleanup(self.gid.stop)
    def consume(self, key, device, inode, *, held_fd):
        if self.used:
            raise r.Stop('synthetic attempt consumed')
        self.assertEqual((device, inode), self.expected)
        self.assertEqual(os.fstat(held_fd).st_ino, inode)
        self.used = True
        return {'synthetic': True}
    def run_transaction(self, consume=None):
        return r.recover_transaction(DATA, self.path, self.expected, consume or self.consume)
    def test_success_same_inode(self):
        self.run_transaction()
        self.assertTrue(self.used)
        self.assertEqual(self.path.read_bytes(), DATA)
        self.assertEqual(self.path.stat().st_ino, self.expected[1])
    def test_symlink_rejected(self):
        alias = self.path.with_name('alias')
        alias.symlink_to(self.path)
        with self.assertRaises(OSError):
            r.recover_transaction(DATA, alias, self.expected, self.consume)
        self.assertFalse(self.used)
    def test_ancestor_symlink_rejected(self):
        alias = self.path.parent.with_name(self.path.parent.name + '-alias')
        alias.symlink_to(self.path.parent, target_is_directory=True)
        self.addCleanup(alias.unlink)
        with self.assertRaises(OSError):
            r.recover_transaction(DATA, alias / self.path.name, self.expected, self.consume)
        self.assertFalse(self.used)
    def test_wrong_inode(self):
        with self.assertRaises(r.Stop):
            r.recover_transaction(DATA, self.path, (self.expected[0], self.expected[1] + 1), self.consume)
        self.assertFalse(self.used)
    def test_wrong_mode(self):
        self.path.chmod(0o644)
        with self.assertRaises(r.Stop): self.run_transaction()
        self.assertFalse(self.used)
    def test_wrong_owner(self):
        with patch.object(r, 'EXPECTED_UID', os.getuid() + 1):
            with self.assertRaises(r.Stop): self.run_transaction()
        self.assertFalse(self.used)
    def test_hardlink(self):
        os.link(self.path, self.path.with_name('second-link'))
        with self.assertRaises(r.Stop): self.run_transaction()
        self.assertFalse(self.used)
    def test_nonempty(self):
        self.path.write_bytes(b'x')
        with self.assertRaises(r.Stop): self.run_transaction()
        self.assertFalse(self.used)
    def test_existing_consumption(self):
        self.used = True
        with self.assertRaises(r.Stop): self.run_transaction()
        self.assertEqual(self.path.read_bytes(), b'')
    def test_unknown_consumption_no_write(self):
        def unknown(*args, **kwargs):
            self.used = True
            raise r.Stop('unknown publication')
        with self.assertRaises(r.Stop): self.run_transaction(unknown)
        self.assertTrue(self.used)
        self.assertEqual(self.path.read_bytes(), b'')
    def test_no_consumption_result(self):
        with self.assertRaises(r.Stop): self.run_transaction(lambda *a, **kw: None)
        self.assertEqual(self.path.read_bytes(), b'')
    def test_short_write_suffix_only(self):
        parts = []
        def short(fd, data):
            parts.append(data[:17])
            return min(17, len(data))
        r.write_authenticated(-1, DATA, short)
        self.assertEqual(b''.join(parts), DATA)
    def test_zero_write_stops(self):
        with self.assertRaises(r.Stop): r.write_authenticated(-1, DATA, lambda fd, data: 0)
    def test_partial_failure_no_retry(self):
        calls = []
        def failing(fd, data):
            calls.append(data)
            if len(calls) == 1: return 10
            raise OSError('synthetic write failure')
        with self.assertRaises(OSError): r.write_authenticated(-1, DATA, failing)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[1], DATA[10:])
    def test_path_replaced_after_consumption(self):
        def replace(*args, **kwargs):
            result = self.consume(*args, **kwargs)
            self.path.rename(self.path.with_name('original'))
            self.path.touch(mode=0o600)
            return result
        with self.assertRaises(r.Stop): self.run_transaction(replace)
        self.assertTrue(self.used)
        self.assertEqual(self.path.read_bytes(), b'')
    def test_fsync_failure_remains_consumed(self):
        with patch.object(r.os, 'fsync', side_effect=OSError('synthetic sync failure')):
            with self.assertRaises(OSError): self.run_transaction()
        self.assertTrue(self.used)
        with self.assertRaises(r.Stop): self.run_transaction()
    def test_bad_source_never_consumes(self):
        with self.assertRaises(r.Stop):
            r.recover_transaction(b'wrong', self.path, self.expected, self.consume)
        self.assertFalse(self.used)
    def test_store_existing_record_rejected(self):
        domain = Path(self.tmp.name)
        marker = domain / 'synthetic-consumed.json'
        marker.write_text('{}')
        with patch.object(r, 'DOMAIN', domain), patch.object(r, 'CONSUMPTION', marker):
            with self.assertRaises(r.Stop): r.check_dispositions()
    def test_store_revocation_rejected(self):
        domain = Path(self.tmp.name)
        (domain / 'revocation.json').write_text(r.canonical({'RECORD': {
            'RECORD_TYPE': 'RECOVERY_GRANT_REVOCATION', 'GRANT': r.GRANT_SHA}}).decode())
        with patch.object(r, 'DOMAIN', domain), patch.object(r, 'CONSUMPTION', domain / 'unused.json'):
            with self.assertRaises(r.Stop): r.check_dispositions()

if __name__ == '__main__':
    unittest.main()
