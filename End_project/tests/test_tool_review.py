"""Independent regressions for evidence recovery and per-order isolation."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from business_tools import ToolSession
from tool_demo import run_demo

T = "2020-01-10T12:00:00-03:00"


def make_order(oid):
    return {"order_id": oid, "expected_cents": 1000, "currency": "BRL",
            "merchant_reference": "m" + oid, "created_at": "2020-01-01T00:00:00-03:00"}


def make_event(tx="p1", oid="o1", **changes):
    result = {"event_id": "e" + tx, "transaction_id": tx, "kind": "receipt", "amount_cents": 1000,
              "currency": "BRL", "status": "success", "effective_at": T, "observed_at": T,
              "order_id": oid, "merchant_reference": "m" + oid, "original_transaction_id": None}
    result.update(changes)
    return result


def make_session(events, orders=None):
    return ToolSession({"orders": orders or [make_order("o1")], "events": events},
                       {"mode": "single_order", "order_id": "o1", "cutoff": T})


class ToolReviewTests(unittest.TestCase):
    def test_conflicting_evidence_remains_inspectable(self):
        events = [make_event(), make_event(event_id="replay", amount_cents=900)]
        result = make_session(events).call("get_transaction_evidence", {"transaction_id": "p1"})
        self.assertTrue(result["ok"], result)
        self.assertEqual({e["event_id"] for e in result["data"]["events"]}, {"ep1", "replay"})
        self.assertIsNone(result["data"].get("transaction"), "Conflicting records must not be presented as one verified transaction")

    def test_unrelated_conflict_does_not_block_refund_query(self):
        events = [make_event(), make_event("p2", "o2"),
                  make_event("p2", "o2", event_id="bad", amount_cents=900)]
        result = make_session(events, [make_order("o1"), make_order("o2")]).call("query_refunds", {"order_id": "o1"})
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["data"]["events"], [])

    def test_unrelated_conflict_does_not_invalidate_target_plan(self):
        clean = make_session([make_event()])
        plan = run_demo(clean)["plan"]
        events = [make_event(), make_event("p2", "o2"),
                  make_event("p2", "o2", event_id="bad", amount_cents=900)]
        result = make_session(events, [make_order("o1"), make_order("o2")]).call("validate_reconciliation", {"plan": plan})
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["data"]["valid"], result)

    def test_demo_does_not_allocate_pending_receipt(self):
        session = make_session([make_event(), make_event("pending", status="pending")])
        demo = run_demo(session)
        self.assertTrue(demo["validation"]["valid"], demo)
        self.assertEqual(demo["plan"]["orders"][0]["receipt_ids"], ["p1"])
        self.assertEqual(demo["plan"]["orders"][0]["balance"]["received_cents"], 1000)

    def test_review_cannot_claim_present_reference_is_missing(self):
        session = make_session([make_event()])
        plan = copy.deepcopy(run_demo(session)["plan"])
        plan["orders"][0].update(review=True, review_reason="缺少订单引用", missing_fields=["order_id"])
        result = session.call("validate_reconciliation", {"plan": plan})
        self.assertTrue(result["ok"], result)
        self.assertFalse(result["data"]["valid"], "A fully evidenced order must not pass with fabricated missing fields")


if __name__ == "__main__":
    unittest.main()
