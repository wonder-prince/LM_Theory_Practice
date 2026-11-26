"""离线检查本地模型输出解析；不加载权重或访问 GPU。"""
import json
import unittest

from agent_runtime import ModelError
from local_model_backend import parse_tool_output


class LocalOutputTests(unittest.TestCase):
    def test_multiple_calls_keep_content_and_arguments(self):
        message = parse_tool_output('先查询。<tool_call>{"name":"query_orders","arguments":{}}</tool_call>'
                                    '<tool_call>{"name":"query_refunds","arguments":{"order_id":"o1"}}</tool_call>')
        self.assertEqual(message['content'], '先查询。')
        calls = message['tool_calls']
        self.assertEqual(len(calls), 2)
        self.assertNotEqual(calls[0]['id'], calls[1]['id'])
        self.assertEqual(json.loads(calls[1]['function']['arguments']), {'order_id': 'o1'})

    def test_incomplete_or_invalid_call_cannot_be_final_answer(self):
        for text in ('<tool_call>{', '<tool_call>{}</tool_call>',
                     '<tool_call>{"name":"query_orders","arguments":[]}</tool_call>'):
            with self.subTest(text=text), self.assertRaises(ModelError):
                parse_tool_output(text)

    def test_plain_final_answer(self):
        self.assertEqual(parse_tool_output('已核对。'), {'role': 'assistant', 'content': '已核对。'})


if __name__ == '__main__':
    unittest.main()