"""Independent graph-protocol regressions; no external API or held-out data."""
import importlib.util
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from business_tools import ToolSession, TOOL_NAMES
from tool_demo import run_demo
from agent_runtime import Budget, run_agent
from model_backends import ScriptedBackend, SmokeBackend, tool_message
from agent_cli import summarize

HAS_GRAPH = importlib.util.find_spec("langgraph") is not None
TIME = "2020-01-10T12:00:00-03:00"
SCOPE = {"mode": "single_order", "order_id": "o1", "cutoff": TIME}


def session(amount=1000):
    return ToolSession({"orders": [{"order_id": "o1", "expected_cents": amount, "currency": "BRL",
        "merchant_reference": "m1", "created_at": "2020-01-01T00:00:00-03:00"}], "events": [{
        "event_id": "e1", "transaction_id": "p1", "kind": "receipt", "amount_cents": amount,
        "currency": "BRL", "status": "success", "effective_at": TIME, "observed_at": TIME,
        "order_id": "o1", "merchant_reference": "m1", "original_transaction_id": None}]}, SCOPE)


@unittest.skipUnless(HAS_GRAPH, "Use project .venv for LangGraph integration tests")
class AgentReviewTests(unittest.TestCase):
    def test_every_requested_call_has_result_when_budget_truncates(self):
        backend = ScriptedBackend([tool_message(("query_orders", {}), ("search_receipts", {}),
                                                ("get_transaction_evidence", {"transaction_id": "p1"}))])
        result = run_agent(session(), "核查o1", SCOPE, {}, backend, Budget(max_tools=1))
        self.assertEqual(result["stop_reason"], "tool_budget")
        calls = next(m for m in result["messages"] if m.get("tool_calls"))["tool_calls"]
        returns = [m for m in result["messages"] if m["role"] == "tool"]
        self.assertEqual([m["tool_call_id"] for m in returns], [c["id"] for c in calls])
        actual = [e for e in result["trace"] if e["event"] == "tool_result"]
        self.assertEqual(sum(e["executed"] for e in actual), 1)
        self.assertEqual([e["result"]["error"]["code"] for e in actual[1:]], ["RUN_STOPPED", "RUN_STOPPED"])

    def test_all_eight_tools_execute_inside_real_graph(self):
        fixture = session()
        demonstration = run_demo(fixture)
        # Fixture arguments drive a declared script, not a model or training trajectory.
        queue = [tool_message((row["tool"], row["arguments"])) for row in demonstration["calls"]]
        queue.append({"role": "assistant", "content": "脚本协议验收完成；不是模型评测。"})
        result = run_agent(session(), "核查o1", SCOPE, {}, ScriptedBackend(queue), Budget(max_decisions=30))
        self.assertEqual(result["stop_reason"], "completed")
        actual = [e for e in result["trace"] if e["event"] == "tool_result"]
        self.assertEqual({e["tool"] for e in actual}, set(TOOL_NAMES))
        self.assertTrue(all(e["executed"] and e["result"]["ok"] for e in actual))
        self.assertFalse(result["model_connected"])
        self.assertEqual(result["kind"], "scripted_mock")
        self.assertIsNone(summarize([result])["accuracy"])

    def test_new_run_does_not_inherit_budget_or_snapshot(self):
        first = run_agent(session(1000), "第一次", SCOPE, {}, SmokeBackend(), Budget(max_decisions=1))
        second = run_agent(session(900), "第二次", SCOPE, {}, SmokeBackend())
        self.assertEqual(first["stop_reason"], "decision_budget")
        self.assertEqual(second["stop_reason"], "completed")
        orders = next(e for e in second["trace"] if e["event"] == "tool_result" and e["tool"] == "query_orders")
        self.assertEqual(orders["result"]["data"]["orders"][0]["expected_cents"], 900)
        self.assertEqual(second["decisions"], 3)

    def test_empty_usage_is_not_reported_as_complete(self):
        class EmptyUsage(ScriptedBackend):
            def complete(self, messages, schemas, deadline):
                return {"message": {"role": "assistant", "content": "测试"}, "usage": {}, "attempts": 1}
        result = run_agent(session(), "核查", SCOPE, {}, EmptyUsage([]))
        self.assertIsNone(result["token_usage"])
        self.assertFalse(result["token_usage_complete"])

    def test_retry_usage_does_not_claim_complete_accounting(self):
        class RetryUsage(ScriptedBackend):
            def complete(self, messages, schemas, deadline):
                return {"message": {"role": "assistant", "content": "测试"},
                        "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12}, "attempts": 2}
        result = run_agent(session(), "核查", SCOPE, {}, RetryUsage([]))
        self.assertEqual(result["token_usage"]["total_tokens"], 12)
        self.assertFalse(result["token_usage_complete"], "Usage for a retried request may be unknown")

    def test_plain_final_text_is_not_scored_as_correct(self):
        backend = ScriptedBackend([{"role": "assistant", "content": "所有订单都正确，无需查询。"}])
        result = run_agent(session(), "核查o1", SCOPE, {}, backend)
        report = summarize([result])
        self.assertEqual(result["tool_calls"], 0)
        self.assertEqual(result["stop_reason"], "completed")
        self.assertIsNone(report["accuracy"])
        self.assertFalse(report["model_effect_verified"])


if __name__ == "__main__":
    unittest.main()
