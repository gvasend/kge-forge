import unittest
from adapter.responses_orchestrator import tool_definitions, TOOL_NAMES
class ContractTests(unittest.TestCase):
 def test_exact_caller_owned_registry(self):
  tools=tool_definitions(); self.assertEqual([x['name'] for x in tools],list(TOOL_NAMES)); self.assertTrue(all(x['type']=='function' and x['strict'] for x in tools)); self.assertNotIn('web_search',str(tools)); self.assertNotIn('code_interpreter',str(tools)); self.assertNotIn('shell',str(tools))
if __name__=='__main__': unittest.main()
