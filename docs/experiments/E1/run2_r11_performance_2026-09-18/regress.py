import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'candidate'))
suite=unittest.defaultTestLoader.loadTestsFromNames(['adapter.tests.test_invocation_ownership','adapter.tests.test_run_control','adapter.tests.test_immutable_witness','adapter.tests.test_controller_authority_store'])
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(not r.wasSuccessful())
