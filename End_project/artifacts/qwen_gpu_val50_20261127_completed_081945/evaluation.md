# Agent 实际效果评测

结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。

参考答案只在模型运行结束后读取。缺失结构化提交按失败计；纯文字回答未做自动语义评分。

历史提示词没有强制结构化输出的任务，记录 submission_contract_requested=false；其0分表示未满足当前交付规范，不能解释成自然语言中的所有事实都错。

| 任务 | 整题准确率 | 字段匹配率 | 工具成功率 | 耗时/秒 | 输出 tokens/秒 | API费用 | 结论 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 21c3d4e5a0614191e11d55713232e4db | 100.0% | 100.0% | 75.0% | 423.0 | 2.5437 | 0.0 USD | scored |
| bf813189fc6640c45b548696cc9b4219 | 0.0% | 0.0% | 33.3% | 600.407 | 1.972 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| ed909817f48b358af93551a9f0c7751a | 100.0% | 100.0% | 80.0% | 115.484 | 6.2173 | 0.0 USD | scored |
| 468468e59dc4ee94b5a2c0c5da79e4bc | 0.0% | 0.0% | 58.3% | 143.516 | 4.8705 | 0.0 USD | MISSING_STRUCTURED_SUBMISSION, RUN_NOT_COMPLETED |
| 5fc8bf28eec5253836d17a8fb1ed18da | 0.0% | 38.5% | 40.0% | 600.016 | 2.2133 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 479170a1ca62896400a0e197f6b2fdeb | 0.0% | 77.1% | 72.7% | 278.687 | 6.4732 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 7f997d6ed7aa6422de146a5b31739cf0 | 0.0% | 100.0% | 83.3% | 600.078 | 2.2897 | 0.0 USD | RUN_NOT_COMPLETED |
| 3ddbe5aad5849a4d24754cdbc8498bc7 | 0.0% | 0.0% | 45.5% | 276.109 | 6.3743 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| d2b7626c6102419a57fc610c02142024 | 0.0% | 53.8% | 40.0% | 423.828 | 6.8235 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 434488fe8701e3af19135e318acc42ca | 100.0% | 100.0% | 87.5% | 183.89 | 7.4066 | 0.0 USD | scored |
| 57fa52b1095d682898df7fa9d77ec043 | 0.0% | 0.0% | 72.7% | 298.985 | 4.736 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 8a91d6131c96cfd5abf66c6bd985f2f6 | 100.0% | 100.0% | 80.0% | 220.187 | 8.0068 | 0.0 USD | scored |
| cffa67df53c4fdefeabe3a84dbe67ae1 | 0.0% | 54.3% | 66.7% | 600.563 | 3.3069 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| bd5d5f9c3276a58df77a2419a5efad6c | 0.0% | 100.0% | 80.0% | 600.5 | 4.8693 | 0.0 USD | RUN_NOT_COMPLETED |
| 6d55f5c4bbf5103dbba06e87cac23b9c | 0.0% | 54.3% | 33.3% | 600.531 | 5.0589 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 75216dd2720419476f3d29de0d924992 | 100.0% | 100.0% | 87.5% | 458.094 | 5.8089 | 0.0 USD | scored |
| 8cd876aedfccd2c3e723c499c8ca29ba | 0.0% | 2.9% | 45.5% | 236.062 | 7.5362 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 330a87c29959c593780eacca69429c78 | 100.0% | 100.0% | 80.0% | 238.891 | 7.6897 | 0.0 USD | scored |
| f18646ac434add104caf416811a73193 | 100.0% | 100.0% | 66.7% | 326.14 | 7.135 | 0.0 USD | scored |
| e77a7d0e9aa1818c036bbec6afafbcb6 | 0.0% | 54.3% | 75.0% | 600.078 | 3.8262 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 74a7fa70d9396ddf3d5ac116e84017da | 0.0% | 84.6% | 50.0% | 495.75 | 7.9859 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| c4f31b0cd50d13bde1a9b4eb712008dc | 0.0% | 2.9% | 81.8% | 223.515 | 7.5073 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 30a7a37087ff15f5fc67b95c6eaba71e | 100.0% | 100.0% | 85.7% | 227.672 | 7.9412 | 0.0 USD | scored |
| 1e9c2bdb06a0d03adfc9f4a70b9819b6 | 0.0% | 48.6% | 80.0% | 326.734 | 7.8076 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| d06f45da76c85fcfc23c4e286e2e14d6 | 100.0% | 100.0% | 75.0% | 135.188 | 7.9001 | 0.0 USD | scored |
| d2b82257bd75cfa1b5ff7e950720c472 | 0.0% | 51.4% | 81.8% | 311.484 | 7.7339 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 8edf039760facb291bb29f04aa0bc78d | 0.0% | 92.3% | 80.0% | 600.25 | 4.6047 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 01b486c3b0d11490d9b3d0369b87ebd4 | 0.0% | 100.0% | 77.8% | 600.328 | 5.1822 | 0.0 USD | RUN_NOT_COMPLETED |
| 04e52fd7f0d95f9b37f1bc9759c00f0d | 0.0% | 48.6% | 70.0% | 379.109 | 6.9531 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 77d7162fc3232d686b084d11504819d3 | 100.0% | 100.0% | 80.0% | 285.765 | 8.0661 | 0.0 USD | scored |
| 12a128e47de3108008b89af120c4d872 | 0.0% | 0.0% | 16.7% | 106.031 | 6.4321 | 0.0 USD | MISSING_STRUCTURED_SUBMISSION, RUN_NOT_COMPLETED |
| 6f4bb6548af752085cd0d16ac602d440 | 0.0% | 92.3% | 50.0% | 551.046 | 7.7707 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 73345cbf2c62fcbde7e5ebfc212ad29f | 0.0% | 91.4% | 66.7% | 600.484 | 4.2599 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 68296c053f8f16b2ad8a6d0f86b3c06a | 100.0% | 100.0% | 87.5% | 200.297 | 7.6387 | 0.0 USD | scored |
| d2382b88ade3ed723fda39ea95ad50f5 | 0.0% | 48.6% | 71.4% | 432.047 | 8.0732 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 4ac9079cd1a9a6e4f188c19fbab1a43a | 0.0% | 84.6% | 50.0% | 600.156 | 5.4019 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| a7e6681e1d9210bd8266050c2521dfda | 100.0% | 100.0% | 75.0% | 408.281 | 2.5571 | 0.0 USD | scored |
| fb0a91987e06dd6996b831fc7a3d9ed1 | 0.0% | 0.0% | 100.0% | 600.407 | 1.2908 | 0.0 USD | MISSING_STRUCTURED_SUBMISSION, RUN_NOT_COMPLETED |
| 035929229afc58f1cf56283b97daecbd | 0.0% | 53.8% | 50.0% | 503.234 | 5.6713 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| fe24f5375fed04e7472a53d33c16a262 | 0.0% | 2.9% | 81.8% | 132.922 | 9.2235 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| ebe4143e309a9a9038e50351c7ab085c | 0.0% | 84.6% | 83.3% | 600.125 | 4.5374 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 6ae2b64ff8bae46b5b50aa337ff5fcd2 | 0.0% | 0.0% | 66.7% | 65.0 | 14.1846 | 0.0 USD | MISSING_STRUCTURED_SUBMISSION, RUN_NOT_COMPLETED |
| d270f3bb50f36763edbe7164838994a0 | 100.0% | 100.0% | 66.7% | 165.0 | 16.9273 | 0.0 USD | scored |
| c30f0286048da88d1ed30e915fb97033 | 0.0% | 0.0% | 25.0% | 46.953 | 11.9907 | 0.0 USD | MISSING_STRUCTURED_SUBMISSION, RUN_NOT_COMPLETED |
| eb9a2829dc13548b19b940cb0ae39d0e | 100.0% | 100.0% | 80.0% | 81.234 | 16.5571 | 0.0 USD | scored |
| 884760a57d04feae53a54d836898f65f | 100.0% | 100.0% | 77.8% | 94.828 | 16.0712 | 0.0 USD | scored |
| 4c77bf5bb2f45b005286192ffad584f0 | 0.0% | 0.0% | 66.7% | 72.484 | 12.4855 | 0.0 USD | MISSING_STRUCTURED_SUBMISSION, RUN_NOT_COMPLETED |
| e4687b3effc9622e2070c12b75a65212 | 100.0% | 100.0% | 83.3% | 75.0 | 15.72 | 0.0 USD | scored |
| 7ceb1db6f097025c0d80ec6faff76a88 | 0.0% | 54.3% | 33.3% | 600.39 | 4.3921 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |
| 71bf919b9f8768e6932b17b6233317c3 | 0.0% | 92.3% | 83.3% | 514.265 | 8.8456 | 0.0 USD | REFERENCE_MISMATCH, RUN_NOT_COMPLETED |

本地 API 费用为 0；硬件及电费未实测。算力估价仅在用户配置每小时单价时计算。

## 汇总

```json
{
  "tasks": 50,
  "kinds": [
    "local_transformers"
  ],
  "stop_reasons": {
    "completed": 16,
    "timeout": 14,
    "decision_budget": 14,
    "submission_rejected": 6
  },
  "decisions": 485,
  "tool_calls": 393,
  "cost": {
    "currency": "USD",
    "api_fee": 0.0,
    "api_fee_status": "see_task_costs",
    "compute_fee_estimate": null,
    "compute_fee_status": "not_configured_for_all_tasks",
    "elapsed_seconds": 17861.025,
    "reported_token_usage": {
      "prompt_tokens": 1557793,
      "completion_tokens": 101334,
      "total_tokens": 1659127
    },
    "token_usage_complete": false
  },
  "accuracy": 0.32,
  "evaluation": {
    "status": "scored",
    "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
    "tasks_scored": 50,
    "correct_tasks": 16,
    "tasks_excluded": 0,
    "legacy_prompt_tasks": 0,
    "submission_rate": 0.88,
    "field_accuracy": 0.47795414462081126,
    "tool_validated_tasks": 0,
    "submission_validated_tasks": 16,
    "failure_reasons": {
      "REFERENCE_MISMATCH": 25,
      "RUN_NOT_COMPLETED": 34,
      "MISSING_STRUCTURED_SUBMISSION": 6
    },
    "natural_language_report_scored": false
  },
  "model_effect_verified": false,
  "task_results": [
    {
      "task_id": "21c3d4e5a0614191e11d55713232e4db",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 5,
      "tool_calls": 4,
      "elapsed_seconds": 423.0,
      "token_usage": {
        "prompt_tokens": 12475,
        "completion_tokens": 1076,
        "total_tokens": 13551
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 423.0,
        "reported_token_usage": {
          "prompt_tokens": 12475,
          "completion_tokens": 1076,
          "total_tokens": 13551
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 2.5437,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "10d0be9599be29de40b12d3207365a1e"
          ],
          "submitted_order_ids": [
            "10d0be9599be29de40b12d3207365a1e"
          ],
          "orders": [
            {
              "order_id": "10d0be9599be29de40b12d3207365a1e",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 4,
          "successful_calls": 3,
          "tool_errors": 1,
          "tool_success_rate": 0.75,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 4,
      "successful_calls": 3,
      "tool_errors": 1,
      "tool_success_rate": 0.75,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "bf813189fc6640c45b548696cc9b4219",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 11,
      "tool_calls": 9,
      "elapsed_seconds": 600.407,
      "token_usage": {
        "prompt_tokens": 32043,
        "completion_tokens": 1184,
        "total_tokens": 33227
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.407,
        "reported_token_usage": {
          "prompt_tokens": 32043,
          "completion_tokens": 1184,
          "total_tokens": 33227
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 1.972,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.0,
          "matched_fields": 0,
          "total_fields": 35,
          "order_coverage_exact": false,
          "expected_order_ids": [
            "04399bab7aacceedb34e72ef4235236b",
            "bfa04e0466136d37c1d991c5f9cec359",
            "fefe384c5a9d630915a85cd9829481be"
          ],
          "submitted_order_ids": [],
          "orders": [
            {
              "order_id": "04399bab7aacceedb34e72ef4235236b",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 15730,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 15730,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 5243,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 10487,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 5243,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "3a21a64d65f4702d756acc9e53b047ae"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [
                    "8ebbadbb54fe4a9ae8bd626155fb16e2"
                  ],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "bfa04e0466136d37c1d991c5f9cec359",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 15791,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 15791,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 15791,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "3d6c419ec93ef577e239a17a4c7b29e1"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "fefe384c5a9d630915a85cd9829481be",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 12826,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 12826,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 12826,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "d5ab81e00a7df71ebb03acdef33e8e36"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": [
            "f1602d97eee8e67fb03f1ab2b7cb4c2c",
            "78350c90a16f49835a50fb96e6902222",
            "ad0030a81ceba243f1a88dac905383a7"
          ]
        },
        "tool_metrics": {
          "executed_calls": 9,
          "successful_calls": 3,
          "tool_errors": 6,
          "tool_success_rate": 0.333333,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 6
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 9,
      "successful_calls": 3,
      "tool_errors": 6,
      "tool_success_rate": 0.333333,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 6
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "ed909817f48b358af93551a9f0c7751a",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 6,
      "tool_calls": 5,
      "elapsed_seconds": 115.484,
      "token_usage": {
        "prompt_tokens": 16342,
        "completion_tokens": 718,
        "total_tokens": 17060
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 115.484,
        "reported_token_usage": {
          "prompt_tokens": 16342,
          "completion_tokens": 718,
          "total_tokens": 17060
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 6.2173,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "61aa1eb4f2e9ff51bd27052b4229a998"
          ],
          "submitted_order_ids": [
            "61aa1eb4f2e9ff51bd27052b4229a998"
          ],
          "orders": [
            {
              "order_id": "61aa1eb4f2e9ff51bd27052b4229a998",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 5,
          "successful_calls": 4,
          "tool_errors": 1,
          "tool_success_rate": 0.8,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 5,
      "successful_calls": 4,
      "tool_errors": 1,
      "tool_success_rate": 0.8,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "468468e59dc4ee94b5a2c0c5da79e4bc",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 12,
      "elapsed_seconds": 143.516,
      "token_usage": {
        "prompt_tokens": 39945,
        "completion_tokens": 699,
        "total_tokens": 40644
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 143.516,
        "reported_token_usage": {
          "prompt_tokens": 39945,
          "completion_tokens": 699,
          "total_tokens": 40644
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 4.8705,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": null,
        "submission_present": false,
        "submission_validated": false,
        "failure_reasons": [
          "MISSING_STRUCTURED_SUBMISSION",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.0,
          "matched_fields": 0,
          "total_fields": 35,
          "order_coverage_exact": false,
          "expected_order_ids": [
            "91f1f76ed01471b8381be7cf66dc5619",
            "c8a4af0be858d7845052792eac2c03d7",
            "eb569e85c639321876a37822de05686a"
          ],
          "submitted_order_ids": [],
          "orders": [
            {
              "order_id": "91f1f76ed01471b8381be7cf66dc5619",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 24298,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 24298,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 24298,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "2b47a076a33f905564d6423d7080bdd1"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "c8a4af0be858d7845052792eac2c03d7",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 7286,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 7286,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 7286,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "01d1ec809eb3bad7836840cae77a7d75",
                    "823ab72af8b089a31cf2635023706507"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "eb569e85c639321876a37822de05686a",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 20507,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 20507,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 20507,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "143c1fa44b2dc6793e11ca8aa8c01447"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": null
        },
        "tool_metrics": {
          "executed_calls": 12,
          "successful_calls": 7,
          "tool_errors": 5,
          "tool_success_rate": 0.583333,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 5
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 12,
      "successful_calls": 7,
      "tool_errors": 5,
      "tool_success_rate": 0.583333,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 5
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "5fc8bf28eec5253836d17a8fb1ed18da",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 7,
      "tool_calls": 5,
      "elapsed_seconds": 600.016,
      "token_usage": {
        "prompt_tokens": 15011,
        "completion_tokens": 1328,
        "total_tokens": 16339
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.016,
        "reported_token_usage": {
          "prompt_tokens": 15011,
          "completion_tokens": 1328,
          "total_tokens": 16339
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 2.2133,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.384615,
          "matched_fields": 5,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "3b50b6109aa5b7db4c695574ba4a4c41"
          ],
          "submitted_order_ids": [
            "3b50b6109aa5b7db4c695574ba4a4c41"
          ],
          "orders": [
            {
              "order_id": "3b50b6109aa5b7db4c695574ba4a4c41",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 4,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 17185,
                  "actual": 0
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 5728,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 17185,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 17185
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 17185
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "aa6287d1fef5dc574ea42d16b840a8af"
                  ],
                  "actual": []
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [
                    "703e5c8221bf248d3afcd4170a37d6b4"
                  ],
                  "actual": []
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": [
            "417262b7792392b829c73b3abbd201e7"
          ]
        },
        "tool_metrics": {
          "executed_calls": 5,
          "successful_calls": 2,
          "tool_errors": 3,
          "tool_success_rate": 0.4,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1,
            "TRANSACTION_UNAVAILABLE": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 5,
      "successful_calls": 2,
      "tool_errors": 3,
      "tool_success_rate": 0.4,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1,
        "TRANSACTION_UNAVAILABLE": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "479170a1ca62896400a0e197f6b2fdeb",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 11,
      "elapsed_seconds": 278.687,
      "token_usage": {
        "prompt_tokens": 38504,
        "completion_tokens": 1804,
        "total_tokens": 40308
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 278.687,
        "reported_token_usage": {
          "prompt_tokens": 38504,
          "completion_tokens": 1804,
          "total_tokens": 40308
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 6.4732,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.771429,
          "matched_fields": 27,
          "total_fields": 35,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "2aa52c3a919e5d5f60d46050d53c39c2",
            "e398aec0ef1865846262935e2c7df8c0",
            "e5beee1b3623cdff90232bbbe6377dad"
          ],
          "submitted_order_ids": [
            "2aa52c3a919e5d5f60d46050d53c39c2",
            "e398aec0ef1865846262935e2c7df8c0",
            "e5beee1b3623cdff90232bbbe6377dad"
          ],
          "orders": [
            {
              "order_id": "2aa52c3a919e5d5f60d46050d53c39c2",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 10,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "review",
                  "expected": true,
                  "actual": false
                }
              ]
            },
            {
              "order_id": "e398aec0ef1865846262935e2c7df8c0",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 101080,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 101080,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 101080
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 101080
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "311c4a97d78ae93096d52209f33d23b7"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "e5beee1b3623cdff90232bbbe6377dad",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 10,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "review",
                  "expected": true,
                  "actual": false
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [
            "384dad9488bd17041d976757283a00d4",
            "bede0f32adf6a83cc15ce7f7b53ce973"
          ],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 11,
          "successful_calls": 8,
          "tool_errors": 3,
          "tool_success_rate": 0.727273,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 3
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 11,
      "successful_calls": 8,
      "tool_errors": 3,
      "tool_success_rate": 0.727273,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 3
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "7f997d6ed7aa6422de146a5b31739cf0",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 8,
      "tool_calls": 6,
      "elapsed_seconds": 600.078,
      "token_usage": {
        "prompt_tokens": 19474,
        "completion_tokens": 1374,
        "total_tokens": 20848
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.078,
        "reported_token_usage": {
          "prompt_tokens": 19474,
          "completion_tokens": 1374,
          "total_tokens": 20848
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 2.2897,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "21604e0c15c8f114bca8e058eb2916a3"
          ],
          "submitted_order_ids": [
            "21604e0c15c8f114bca8e058eb2916a3"
          ],
          "orders": [
            {
              "order_id": "21604e0c15c8f114bca8e058eb2916a3",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 6,
          "successful_calls": 5,
          "tool_errors": 1,
          "tool_success_rate": 0.833333,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 6,
      "successful_calls": 5,
      "tool_errors": 1,
      "tool_success_rate": 0.833333,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "3ddbe5aad5849a4d24754cdbc8498bc7",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 11,
      "elapsed_seconds": 276.109,
      "token_usage": {
        "prompt_tokens": 43535,
        "completion_tokens": 1760,
        "total_tokens": 45295
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 276.109,
        "reported_token_usage": {
          "prompt_tokens": 43535,
          "completion_tokens": 1760,
          "total_tokens": 45295
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 6.3743,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.0,
          "matched_fields": 0,
          "total_fields": 35,
          "order_coverage_exact": false,
          "expected_order_ids": [
            "4e46514bdc98305a78f3435525422081",
            "9765fa7a50c9e516fdfbdde824404756",
            "f307504550c093e0aed31abfbeb87341"
          ],
          "submitted_order_ids": [],
          "orders": [
            {
              "order_id": "4e46514bdc98305a78f3435525422081",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 16388,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 16388,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 16388,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "4617b736b33414f889e1c98d393edfdd"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "9765fa7a50c9e516fdfbdde824404756",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 17269,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 17269,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 17269,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "9b428235e031091f996863791a3827a3"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "f307504550c093e0aed31abfbeb87341",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 6100,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 6100,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 6100,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "73727a4ac1033f55fbc96dbf2c12b794"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": [
            "f307504550c093e0aed31abfbeb87341",
            "9765fa7a50c9e516fdfbdde824404756",
            "4e46514bdc98305a78f343552542081"
          ]
        },
        "tool_metrics": {
          "executed_calls": 11,
          "successful_calls": 5,
          "tool_errors": 6,
          "tool_success_rate": 0.454545,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 6
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 11,
      "successful_calls": 5,
      "tool_errors": 6,
      "tool_success_rate": 0.454545,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 6
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "d2b7626c6102419a57fc610c02142024",
      "kind": "local_transformers",
      "stop_reason": "submission_rejected",
      "model_connected": true,
      "decisions": 8,
      "tool_calls": 5,
      "elapsed_seconds": 423.828,
      "token_usage": {
        "prompt_tokens": 24070,
        "completion_tokens": 2892,
        "total_tokens": 26962
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 423.828,
        "reported_token_usage": {
          "prompt_tokens": 24070,
          "completion_tokens": 2892,
          "total_tokens": 26962
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 6.8235,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.538462,
          "matched_fields": 7,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "082242775a54782499f8320401414af7"
          ],
          "submitted_order_ids": [
            "082242775a54782499f8320401414af7"
          ],
          "orders": [
            {
              "order_id": "082242775a54782499f8320401414af7",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 3758,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 3758,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 3758,
                  "actual": 7516
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 3758,
                  "actual": 7516
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "4130d73909fae73a0efc639302fc7b36"
                  ],
                  "actual": []
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": [
            "2d190d42ab1d166a395e09ae51c6c4d3",
            "4130d73909fae73a0efc639302fc7b36"
          ]
        },
        "tool_metrics": {
          "executed_calls": 5,
          "successful_calls": 2,
          "tool_errors": 3,
          "tool_success_rate": 0.4,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1,
            "TRANSACTION_UNAVAILABLE": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 5,
      "successful_calls": 2,
      "tool_errors": 3,
      "tool_success_rate": 0.4,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1,
        "TRANSACTION_UNAVAILABLE": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "434488fe8701e3af19135e318acc42ca",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 9,
      "tool_calls": 8,
      "elapsed_seconds": 183.89,
      "token_usage": {
        "prompt_tokens": 29059,
        "completion_tokens": 1362,
        "total_tokens": 30421
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 183.89,
        "reported_token_usage": {
          "prompt_tokens": 29059,
          "completion_tokens": 1362,
          "total_tokens": 30421
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 7.4066,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "d9f21071ea6df6e4db1d04a2f709598a"
          ],
          "submitted_order_ids": [
            "d9f21071ea6df6e4db1d04a2f709598a"
          ],
          "orders": [
            {
              "order_id": "d9f21071ea6df6e4db1d04a2f709598a",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 8,
          "successful_calls": 7,
          "tool_errors": 1,
          "tool_success_rate": 0.875,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 8,
      "successful_calls": 7,
      "tool_errors": 1,
      "tool_success_rate": 0.875,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "57fa52b1095d682898df7fa9d77ec043",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 11,
      "elapsed_seconds": 298.985,
      "token_usage": {
        "prompt_tokens": 51099,
        "completion_tokens": 1416,
        "total_tokens": 52515
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 298.985,
        "reported_token_usage": {
          "prompt_tokens": 51099,
          "completion_tokens": 1416,
          "total_tokens": 52515
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 4.736,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.0,
          "matched_fields": 0,
          "total_fields": 35,
          "order_coverage_exact": false,
          "expected_order_ids": [
            "219069f4b05b20f21850188f54089c2c",
            "73f079675f874ac897ceb0ff87ba44c1",
            "f64298035450e84a38b26a1b2b21287d"
          ],
          "submitted_order_ids": [],
          "orders": [
            {
              "order_id": "219069f4b05b20f21850188f54089c2c",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 17252,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 17252,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 17252,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "b49908b1395addf7e4a1a38df043ee3c"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "73f079675f874ac897ceb0ff87ba44c1",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 22566,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 22566,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 22566,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "513cf7e378e511ca95c77acf58420011"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "f64298035450e84a38b26a1b2b21287d",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 12573,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 12573,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 7334,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 5239,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 7334,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "4423b4578ebd1663792bcb6f73581b32"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [
                    "3601692f60077b2cb3fe05866473d9c7",
                    "7e8d27fc4d256ebe017f67e55f6c4be9"
                  ],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": [
            "f937ce3a37a5aca958a254bc027b0062",
            "06e8b07b5851225fde54070c150fea59",
            "5c2e537a952224ba3b7b21ba80c2dde6"
          ]
        },
        "tool_metrics": {
          "executed_calls": 11,
          "successful_calls": 8,
          "tool_errors": 3,
          "tool_success_rate": 0.727273,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 3
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 11,
      "successful_calls": 8,
      "tool_errors": 3,
      "tool_success_rate": 0.727273,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 3
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "8a91d6131c96cfd5abf66c6bd985f2f6",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 7,
      "tool_calls": 5,
      "elapsed_seconds": 220.187,
      "token_usage": {
        "prompt_tokens": 21533,
        "completion_tokens": 1763,
        "total_tokens": 23296
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 220.187,
        "reported_token_usage": {
          "prompt_tokens": 21533,
          "completion_tokens": 1763,
          "total_tokens": 23296
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 8.0068,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "23d446a5054153284616805e6adee0ad"
          ],
          "submitted_order_ids": [
            "23d446a5054153284616805e6adee0ad"
          ],
          "orders": [
            {
              "order_id": "23d446a5054153284616805e6adee0ad",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 5,
          "successful_calls": 4,
          "tool_errors": 1,
          "tool_success_rate": 0.8,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 5,
      "successful_calls": 4,
      "tool_errors": 1,
      "tool_success_rate": 0.8,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "cffa67df53c4fdefeabe3a84dbe67ae1",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 9,
      "elapsed_seconds": 600.563,
      "token_usage": {
        "prompt_tokens": 36611,
        "completion_tokens": 1986,
        "total_tokens": 38597
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.563,
        "reported_token_usage": {
          "prompt_tokens": 36611,
          "completion_tokens": 1986,
          "total_tokens": 38597
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 3.3069,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.542857,
          "matched_fields": 19,
          "total_fields": 35,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "03e63dfb3beb7bc87efb6ba6085df51b",
            "97e52f2a7242cfafe1eb270b8978dd9e",
            "a2fdded70acc1f7ef3bc36b434e7e934"
          ],
          "submitted_order_ids": [
            "03e63dfb3beb7bc87efb6ba6085df51b",
            "97e52f2a7242cfafe1eb270b8978dd9e",
            "a2fdded70acc1f7ef3bc36b434e7e934"
          ],
          "orders": [
            {
              "order_id": "03e63dfb3beb7bc87efb6ba6085df51b",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 4087,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 4087,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 4087
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 4087
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "01270ac53c74971d80fe604f7aea9f19"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "97e52f2a7242cfafe1eb270b8978dd9e",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 8637,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 8637,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 8637
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 8637
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "40ac564dfcb736e9381896bc3e0c93c6"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "a2fdded70acc1f7ef3bc36b434e7e934",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 5837,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 5837,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 5837
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 5837
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "05e108ef6a8caa2e9a429c9c0750f32f"
                  ],
                  "actual": []
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": [
            "a8451d3ec7b0b6bc0f364ef81f53097c",
            "9f689703c72cd9ab1abd3429a0094886",
            "01270ac53c74971d80fe604f7aea9f19",
            "05e108ef6a8caa2e9a429c9c0750f32f",
            "40ac564dfcb736e9381896bc3e0c93c6"
          ]
        },
        "tool_metrics": {
          "executed_calls": 9,
          "successful_calls": 6,
          "tool_errors": 3,
          "tool_success_rate": 0.666667,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 3
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 9,
      "successful_calls": 6,
      "tool_errors": 3,
      "tool_success_rate": 0.666667,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 3
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "bd5d5f9c3276a58df77a2419a5efad6c",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 8,
      "tool_calls": 5,
      "elapsed_seconds": 600.5,
      "token_usage": {
        "prompt_tokens": 21552,
        "completion_tokens": 2924,
        "total_tokens": 24476
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.5,
        "reported_token_usage": {
          "prompt_tokens": 21552,
          "completion_tokens": 2924,
          "total_tokens": 24476
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 4.8693,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "2a1ca3d5bd78a7bb914711f3cb46b591"
          ],
          "submitted_order_ids": [
            "2a1ca3d5bd78a7bb914711f3cb46b591"
          ],
          "orders": [
            {
              "order_id": "2a1ca3d5bd78a7bb914711f3cb46b591",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 5,
          "successful_calls": 4,
          "tool_errors": 1,
          "tool_success_rate": 0.8,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 5,
      "successful_calls": 4,
      "tool_errors": 1,
      "tool_success_rate": 0.8,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "6d55f5c4bbf5103dbba06e87cac23b9c",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 9,
      "elapsed_seconds": 600.531,
      "token_usage": {
        "prompt_tokens": 37702,
        "completion_tokens": 3038,
        "total_tokens": 40740
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.531,
        "reported_token_usage": {
          "prompt_tokens": 37702,
          "completion_tokens": 3038,
          "total_tokens": 40740
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 5.0589,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.542857,
          "matched_fields": 19,
          "total_fields": 35,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "25343818f100f1b4f35714ba55141d02",
            "461cb9ba7e3bf748ebf6f9f33658639f",
            "a81ee67fb909fa5ce8b33ef1e413248d"
          ],
          "submitted_order_ids": [
            "25343818f100f1b4f35714ba55141d02",
            "461cb9ba7e3bf748ebf6f9f33658639f",
            "a81ee67fb909fa5ce8b33ef1e413248d"
          ],
          "orders": [
            {
              "order_id": "25343818f100f1b4f35714ba55141d02",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 11924,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 11924,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 11924
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 11924
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "541b0343f259807a9973d9df2db10500"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "461cb9ba7e3bf748ebf6f9f33658639f",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 9962,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 9962,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 9962
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 9962
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "b2c863bad4715e0fad76a246d404ff64"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "a81ee67fb909fa5ce8b33ef1e413248d",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 8673,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 8673,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 8673
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 8673
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "0a7d0d5cfb32d463027ca198d203b078"
                  ],
                  "actual": []
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": [
            "0a7d0d5cfb32d463027ca198d203b078",
            "541b0343f259807a9973d9df2db10500",
            "b2c863bad4715e0fad76a246d404ff64"
          ]
        },
        "tool_metrics": {
          "executed_calls": 9,
          "successful_calls": 3,
          "tool_errors": 6,
          "tool_success_rate": 0.333333,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 6
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 9,
      "successful_calls": 3,
      "tool_errors": 6,
      "tool_success_rate": 0.333333,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 6
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "75216dd2720419476f3d29de0d924992",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 10,
      "tool_calls": 8,
      "elapsed_seconds": 458.094,
      "token_usage": {
        "prompt_tokens": 34983,
        "completion_tokens": 2661,
        "total_tokens": 37644
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 458.094,
        "reported_token_usage": {
          "prompt_tokens": 34983,
          "completion_tokens": 2661,
          "total_tokens": 37644
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 5.8089,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "5156bf77e2f89073c8a4624ae0e6d83c"
          ],
          "submitted_order_ids": [
            "5156bf77e2f89073c8a4624ae0e6d83c"
          ],
          "orders": [
            {
              "order_id": "5156bf77e2f89073c8a4624ae0e6d83c",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 8,
          "successful_calls": 7,
          "tool_errors": 1,
          "tool_success_rate": 0.875,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 8,
      "successful_calls": 7,
      "tool_errors": 1,
      "tool_success_rate": 0.875,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "8cd876aedfccd2c3e723c499c8ca29ba",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 11,
      "elapsed_seconds": 236.062,
      "token_usage": {
        "prompt_tokens": 42879,
        "completion_tokens": 1779,
        "total_tokens": 44658
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 236.062,
        "reported_token_usage": {
          "prompt_tokens": 42879,
          "completion_tokens": 1779,
          "total_tokens": 44658
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 7.5362,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.028571,
          "matched_fields": 1,
          "total_fields": 35,
          "order_coverage_exact": false,
          "expected_order_ids": [
            "0c2adc3ad8983c9d94d6f2158859b515",
            "a2521df763e5225f8c3242b024c9c172",
            "f20f222751a822660640a01ba93a785d"
          ],
          "submitted_order_ids": [],
          "orders": [
            {
              "order_id": "0c2adc3ad8983c9d94d6f2158859b515",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 12426,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 12426,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 12426,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "5965e8c27dd84b3e81a3767e6a79194f"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "a2521df763e5225f8c3242b024c9c172",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 11694,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 11694,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 3898,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 11694,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "80f5059e6edb67140459f190c682730e"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [
                    "be433d30388a0f07ade485a43ec91fae"
                  ],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "f20f222751a822660640a01ba93a785d",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 19571,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 19571,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 19571,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "e24f89dc36a3025ced0ef653993d1796"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 11,
          "successful_calls": 5,
          "tool_errors": 6,
          "tool_success_rate": 0.454545,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 6
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 11,
      "successful_calls": 5,
      "tool_errors": 6,
      "tool_success_rate": 0.454545,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 6
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "330a87c29959c593780eacca69429c78",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 7,
      "tool_calls": 5,
      "elapsed_seconds": 238.891,
      "token_usage": {
        "prompt_tokens": 20423,
        "completion_tokens": 1837,
        "total_tokens": 22260
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 238.891,
        "reported_token_usage": {
          "prompt_tokens": 20423,
          "completion_tokens": 1837,
          "total_tokens": 22260
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 7.6897,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "f54e11c44ac66e16fdb295eef1d3db8f"
          ],
          "submitted_order_ids": [
            "f54e11c44ac66e16fdb295eef1d3db8f"
          ],
          "orders": [
            {
              "order_id": "f54e11c44ac66e16fdb295eef1d3db8f",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 5,
          "successful_calls": 4,
          "tool_errors": 1,
          "tool_success_rate": 0.8,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 5,
      "successful_calls": 4,
      "tool_errors": 1,
      "tool_success_rate": 0.8,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "f18646ac434add104caf416811a73193",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 9,
      "tool_calls": 6,
      "elapsed_seconds": 326.14,
      "token_usage": {
        "prompt_tokens": 27377,
        "completion_tokens": 2327,
        "total_tokens": 29704
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 326.14,
        "reported_token_usage": {
          "prompt_tokens": 27377,
          "completion_tokens": 2327,
          "total_tokens": 29704
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 7.135,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "9e012c2519fc738b2de58b005cdb57d3"
          ],
          "submitted_order_ids": [
            "9e012c2519fc738b2de58b005cdb57d3"
          ],
          "orders": [
            {
              "order_id": "9e012c2519fc738b2de58b005cdb57d3",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 6,
          "successful_calls": 4,
          "tool_errors": 2,
          "tool_success_rate": 0.666667,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 6,
      "successful_calls": 4,
      "tool_errors": 2,
      "tool_success_rate": 0.666667,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "e77a7d0e9aa1818c036bbec6afafbcb6",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 11,
      "tool_calls": 8,
      "elapsed_seconds": 600.078,
      "token_usage": {
        "prompt_tokens": 32385,
        "completion_tokens": 2296,
        "total_tokens": 34681
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.078,
        "reported_token_usage": {
          "prompt_tokens": 32385,
          "completion_tokens": 2296,
          "total_tokens": 34681
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 3.8262,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.542857,
          "matched_fields": 19,
          "total_fields": 35,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "5dc6c81909d385e66729a3b7abc07130",
            "c6e942b5d07954188223e9ca7380d5f9",
            "e559c5076f02a533bcbd1d0f11da7bbd"
          ],
          "submitted_order_ids": [
            "5dc6c81909d385e66729a3b7abc07130",
            "c6e942b5d07954188223e9ca7380d5f9",
            "e559c5076f02a533bcbd1d0f11da7bbd"
          ],
          "orders": [
            {
              "order_id": "5dc6c81909d385e66729a3b7abc07130",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 15902,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 15902,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 15902
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 15902
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "ccc3e96f38b80d65f875dc51423fcad7"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "c6e942b5d07954188223e9ca7380d5f9",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 8641,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 8641,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 8641
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 8641
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "0e8d7777a4afa12c3effc116119129f7"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "e559c5076f02a533bcbd1d0f11da7bbd",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 10757,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 10757,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 10757
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 10757
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "6250ae32933a1a32402ca983fdbb2d47"
                  ],
                  "actual": []
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": [
            "0e8d7777a4afa12c3effc116119129f7",
            "6250ae32933a1a32402ca983fdbb2d47",
            "ccc3e96f38b80d65f875dc51423fcad7"
          ]
        },
        "tool_metrics": {
          "executed_calls": 8,
          "successful_calls": 6,
          "tool_errors": 2,
          "tool_success_rate": 0.75,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 8,
      "successful_calls": 6,
      "tool_errors": 2,
      "tool_success_rate": 0.75,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "74a7fa70d9396ddf3d5ac116e84017da",
      "kind": "local_transformers",
      "stop_reason": "submission_rejected",
      "model_connected": true,
      "decisions": 9,
      "tool_calls": 6,
      "elapsed_seconds": 495.75,
      "token_usage": {
        "prompt_tokens": 27350,
        "completion_tokens": 3959,
        "total_tokens": 31309
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 495.75,
        "reported_token_usage": {
          "prompt_tokens": 27350,
          "completion_tokens": 3959,
          "total_tokens": 31309
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 7.9859,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.846154,
          "matched_fields": 11,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "cb2cf2f39f97ade4af52d72b30957af7"
          ],
          "submitted_order_ids": [
            "cb2cf2f39f97ade4af52d72b30957af7"
          ],
          "orders": [
            {
              "order_id": "cb2cf2f39f97ade4af52d72b30957af7",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 10,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "review",
                  "expected": true,
                  "actual": false
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [
            "76af93852df83383d010ed925c59f52e",
            "c3cd5786d2d69f4fb27d19cd0d0600ac"
          ],
          "submitted_unallocated_transaction_ids": [
            "c6de2b1a610cd16df565bc2c78741fd5",
            "76af93852df83383d010ed925c59f52e",
            "c3cd5786d2d69f4fb27d19cd0d0600ac"
          ]
        },
        "tool_metrics": {
          "executed_calls": 6,
          "successful_calls": 3,
          "tool_errors": 3,
          "tool_success_rate": 0.5,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1,
            "TRANSACTION_UNAVAILABLE": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 6,
      "successful_calls": 3,
      "tool_errors": 3,
      "tool_success_rate": 0.5,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1,
        "TRANSACTION_UNAVAILABLE": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "c4f31b0cd50d13bde1a9b4eb712008dc",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 11,
      "elapsed_seconds": 223.515,
      "token_usage": {
        "prompt_tokens": 41174,
        "completion_tokens": 1678,
        "total_tokens": 42852
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 223.515,
        "reported_token_usage": {
          "prompt_tokens": 41174,
          "completion_tokens": 1678,
          "total_tokens": 42852
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 7.5073,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.028571,
          "matched_fields": 1,
          "total_fields": 35,
          "order_coverage_exact": false,
          "expected_order_ids": [
            "777491dbae329fbbac02b42eaba28ca1",
            "beb5c901d6610032752ae032a995b2c1",
            "ec56081b18edddf8846064c7947cf6df"
          ],
          "submitted_order_ids": [],
          "orders": [
            {
              "order_id": "777491dbae329fbbac02b42eaba28ca1",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 4509,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 4509,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 4509,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "4cb6ad478a357c3c473e53c78d19df5f"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "beb5c901d6610032752ae032a995b2c1",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 5705,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 5705,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 5705,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "57da2dadee60f2fcf4a62f44173fc99d"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "ec56081b18edddf8846064c7947cf6df",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 4372,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 4372,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 4372,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "135c5422e54af32cbbbec4c4557c1e88",
                    "a0a4c84517abfefc1a7df1f2bf5d1eb3"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 11,
          "successful_calls": 9,
          "tool_errors": 2,
          "tool_success_rate": 0.818182,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 11,
      "successful_calls": 9,
      "tool_errors": 2,
      "tool_success_rate": 0.818182,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "30a7a37087ff15f5fc67b95c6eaba71e",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 8,
      "tool_calls": 7,
      "elapsed_seconds": 227.672,
      "token_usage": {
        "prompt_tokens": 25306,
        "completion_tokens": 1808,
        "total_tokens": 27114
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 227.672,
        "reported_token_usage": {
          "prompt_tokens": 25306,
          "completion_tokens": 1808,
          "total_tokens": 27114
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 7.9412,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "fb99b43dfe70fcc3e93a87748bd4a508"
          ],
          "submitted_order_ids": [
            "fb99b43dfe70fcc3e93a87748bd4a508"
          ],
          "orders": [
            {
              "order_id": "fb99b43dfe70fcc3e93a87748bd4a508",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 7,
          "successful_calls": 6,
          "tool_errors": 1,
          "tool_success_rate": 0.857143,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 7,
      "successful_calls": 6,
      "tool_errors": 1,
      "tool_success_rate": 0.857143,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "1e9c2bdb06a0d03adfc9f4a70b9819b6",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 10,
      "elapsed_seconds": 326.734,
      "token_usage": {
        "prompt_tokens": 42166,
        "completion_tokens": 2551,
        "total_tokens": 44717
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 326.734,
        "reported_token_usage": {
          "prompt_tokens": 42166,
          "completion_tokens": 2551,
          "total_tokens": 44717
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 7.8076,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.485714,
          "matched_fields": 17,
          "total_fields": 35,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "82c239b7e22c405455045158a40e6ac4",
            "9a490fae11ab66e7dfeb3d043c789989",
            "f7d2b681af640a2dabded625da66f2cd"
          ],
          "submitted_order_ids": [
            "82c239b7e22c405455045158a40e6ac4",
            "9a490fae11ab66e7dfeb3d043c789989",
            "f7d2b681af640a2dabded625da66f2cd"
          ],
          "orders": [
            {
              "order_id": "82c239b7e22c405455045158a40e6ac4",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 2,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 16365,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 16365,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 16365,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "98dea0d52f50020027cb1b23fed02538"
                  ],
                  "actual": [
                    "40b507d5d9e3f6bbec1a6bca48e5d7f5"
                  ]
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                }
              ]
            },
            {
              "order_id": "9a490fae11ab66e7dfeb3d043c789989",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            },
            {
              "order_id": "f7d2b681af640a2dabded625da66f2cd",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 2,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 8465,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 8465,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 8465,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "40b507d5d9e3f6bbec1a6bca48e5d7f5"
                  ],
                  "actual": [
                    "98dea0d52f50020027cb1b23fed02538"
                  ]
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                }
              ]
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 10,
          "successful_calls": 8,
          "tool_errors": 2,
          "tool_success_rate": 0.8,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 10,
      "successful_calls": 8,
      "tool_errors": 2,
      "tool_success_rate": 0.8,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "d06f45da76c85fcfc23c4e286e2e14d6",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 5,
      "tool_calls": 4,
      "elapsed_seconds": 135.188,
      "token_usage": {
        "prompt_tokens": 12433,
        "completion_tokens": 1068,
        "total_tokens": 13501
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 135.188,
        "reported_token_usage": {
          "prompt_tokens": 12433,
          "completion_tokens": 1068,
          "total_tokens": 13501
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 7.9001,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "d055c81580fd81094255ab1b3a3ead2d"
          ],
          "submitted_order_ids": [
            "d055c81580fd81094255ab1b3a3ead2d"
          ],
          "orders": [
            {
              "order_id": "d055c81580fd81094255ab1b3a3ead2d",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 4,
          "successful_calls": 3,
          "tool_errors": 1,
          "tool_success_rate": 0.75,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 4,
      "successful_calls": 3,
      "tool_errors": 1,
      "tool_success_rate": 0.75,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "d2b82257bd75cfa1b5ff7e950720c472",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 11,
      "elapsed_seconds": 311.484,
      "token_usage": {
        "prompt_tokens": 41472,
        "completion_tokens": 2409,
        "total_tokens": 43881
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 311.484,
        "reported_token_usage": {
          "prompt_tokens": 41472,
          "completion_tokens": 2409,
          "total_tokens": 43881
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 7.7339,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.514286,
          "matched_fields": 18,
          "total_fields": 35,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "27da256dcbf3fde208e977b90f00ace4",
            "4516123a1e1a40f07f357d4a231438b3",
            "9752df65a5356741e6dcfb11b33f5ef8"
          ],
          "submitted_order_ids": [
            "27da256dcbf3fde208e977b90f00ace4",
            "4516123a1e1a40f07f357d4a231438b3",
            "9752df65a5356741e6dcfb11b33f5ef8"
          ],
          "orders": [
            {
              "order_id": "27da256dcbf3fde208e977b90f00ace4",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 11545,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 11545,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 11545
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 11545
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "1a208595cbb89e584532737f56eea691"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "4516123a1e1a40f07f357d4a231438b3",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 4,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 4184,
                  "actual": 0
                },
                {
                  "field": "refunded_cents",
                  "expected": 1394,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 2790,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 4184
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 1394,
                  "actual": 4184
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "56744684b37ea679cf18a3292864c620"
                  ],
                  "actual": []
                },
                {
                  "field": "refund_ids",
                  "expected": [
                    "cbb238cbd4d57811b60522b5a7a9a75d"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "9752df65a5356741e6dcfb11b33f5ef8",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 10033,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 10033,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 10033
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 10033
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "1ce4b693ae0d7d15aa715149cf270f12"
                  ],
                  "actual": []
                }
              ]
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 11,
          "successful_calls": 9,
          "tool_errors": 2,
          "tool_success_rate": 0.818182,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 11,
      "successful_calls": 9,
      "tool_errors": 2,
      "tool_success_rate": 0.818182,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "8edf039760facb291bb29f04aa0bc78d",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 8,
      "tool_calls": 5,
      "elapsed_seconds": 600.25,
      "token_usage": {
        "prompt_tokens": 21769,
        "completion_tokens": 2764,
        "total_tokens": 24533
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.25,
        "reported_token_usage": {
          "prompt_tokens": 21769,
          "completion_tokens": 2764,
          "total_tokens": 24533
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 4.6047,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.923077,
          "matched_fields": 12,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "c9a0e4198b4331fba206c47367d14985"
          ],
          "submitted_order_ids": [
            "c9a0e4198b4331fba206c47367d14985"
          ],
          "orders": [
            {
              "order_id": "c9a0e4198b4331fba206c47367d14985",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 10,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "review",
                  "expected": false,
                  "actual": true
                }
              ]
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 5,
          "successful_calls": 4,
          "tool_errors": 1,
          "tool_success_rate": 0.8,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 5,
      "successful_calls": 4,
      "tool_errors": 1,
      "tool_success_rate": 0.8,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "01b486c3b0d11490d9b3d0369b87ebd4",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 9,
      "elapsed_seconds": 600.328,
      "token_usage": {
        "prompt_tokens": 38636,
        "completion_tokens": 3111,
        "total_tokens": 41747
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.328,
        "reported_token_usage": {
          "prompt_tokens": 38636,
          "completion_tokens": 3111,
          "total_tokens": 41747
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 5.1822,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "af5129b6e8a55a0eecdc2fc1d6b123f5"
          ],
          "submitted_order_ids": [
            "af5129b6e8a55a0eecdc2fc1d6b123f5"
          ],
          "orders": [
            {
              "order_id": "af5129b6e8a55a0eecdc2fc1d6b123f5",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 9,
          "successful_calls": 7,
          "tool_errors": 2,
          "tool_success_rate": 0.777778,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 9,
      "successful_calls": 7,
      "tool_errors": 2,
      "tool_success_rate": 0.777778,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "04e52fd7f0d95f9b37f1bc9759c00f0d",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 10,
      "elapsed_seconds": 379.109,
      "token_usage": {
        "prompt_tokens": 53729,
        "completion_tokens": 2636,
        "total_tokens": 56365
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 379.109,
        "reported_token_usage": {
          "prompt_tokens": 53729,
          "completion_tokens": 2636,
          "total_tokens": 56365
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 6.9531,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.485714,
          "matched_fields": 17,
          "total_fields": 35,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "240e00887dd032bf5547aa45017f01ca",
            "a2d4648245eef6c901ad5ef01bd05776",
            "d2fd0fc81f4bb24f895babec3940441c"
          ],
          "submitted_order_ids": [
            "240e00887dd032bf5547aa45017f01ca",
            "a2d4648245eef6c901ad5ef01bd05776",
            "d2fd0fc81f4bb24f895babec3940441c"
          ],
          "orders": [
            {
              "order_id": "240e00887dd032bf5547aa45017f01ca",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 17422,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 17422,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 17422
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 17422
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "167bd1185f2346e87f1de2a1fff95704"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "a2d4648245eef6c901ad5ef01bd05776",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 4,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 12014,
                  "actual": 0
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 4004,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 12014,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 12014
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 12014
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "1ec09da77e6e4626aff08dc67ac043e1"
                  ],
                  "actual": []
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [
                    "f5dd34f5498eed376ebe67b0bee0d5bd"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "d2fd0fc81f4bb24f895babec3940441c",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 5401,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 5401,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 5401
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 5401
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "d9852d368685a9e74a642965a8b88560"
                  ],
                  "actual": []
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": [
            "167bd1185f2346e87f1de2a1fff95704",
            "1ec09da77e6e4626aff08dc67ac043e1",
            "d9852d368685a9e74a642965a8b88560",
            "f5dd34f5498eed376ebe67b0bee0d5bd"
          ]
        },
        "tool_metrics": {
          "executed_calls": 10,
          "successful_calls": 7,
          "tool_errors": 3,
          "tool_success_rate": 0.7,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 3
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 10,
      "successful_calls": 7,
      "tool_errors": 3,
      "tool_success_rate": 0.7,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 3
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "77d7162fc3232d686b084d11504819d3",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 8,
      "tool_calls": 5,
      "elapsed_seconds": 285.765,
      "token_usage": {
        "prompt_tokens": 24098,
        "completion_tokens": 2305,
        "total_tokens": 26403
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 285.765,
        "reported_token_usage": {
          "prompt_tokens": 24098,
          "completion_tokens": 2305,
          "total_tokens": 26403
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 8.0661,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "86dd9fde7d21c71a9f37fc9c5605d582"
          ],
          "submitted_order_ids": [
            "86dd9fde7d21c71a9f37fc9c5605d582"
          ],
          "orders": [
            {
              "order_id": "86dd9fde7d21c71a9f37fc9c5605d582",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 5,
          "successful_calls": 4,
          "tool_errors": 1,
          "tool_success_rate": 0.8,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 5,
      "successful_calls": 4,
      "tool_errors": 1,
      "tool_success_rate": 0.8,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "12a128e47de3108008b89af120c4d872",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 12,
      "elapsed_seconds": 106.031,
      "token_usage": {
        "prompt_tokens": 40443,
        "completion_tokens": 682,
        "total_tokens": 41125
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 106.031,
        "reported_token_usage": {
          "prompt_tokens": 40443,
          "completion_tokens": 682,
          "total_tokens": 41125
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 6.4321,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": null,
        "submission_present": false,
        "submission_validated": false,
        "failure_reasons": [
          "MISSING_STRUCTURED_SUBMISSION",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.0,
          "matched_fields": 0,
          "total_fields": 35,
          "order_coverage_exact": false,
          "expected_order_ids": [
            "5220db424c855f3dccddf8e697404b3d",
            "6b3deaae63b5c952d0b6b49780f3cb1e",
            "b1016181b88640c419fbaa7552d84f19"
          ],
          "submitted_order_ids": [],
          "orders": [
            {
              "order_id": "5220db424c855f3dccddf8e697404b3d",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 19167,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 19167,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 19167,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "70adaf8ff6c3e09b5a069fb50f1e7fec"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "6b3deaae63b5c952d0b6b49780f3cb1e",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 32087,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 32087,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 32087,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "25ee39c176e22f3d970749dcef349726"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "b1016181b88640c419fbaa7552d84f19",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 58044,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 58044,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 58044,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "986cdcc5f3e6be671096a25094820142"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": null
        },
        "tool_metrics": {
          "executed_calls": 12,
          "successful_calls": 2,
          "tool_errors": 10,
          "tool_success_rate": 0.166667,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 10
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 12,
      "successful_calls": 2,
      "tool_errors": 10,
      "tool_success_rate": 0.166667,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 10
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "6f4bb6548af752085cd0d16ac602d440",
      "kind": "local_transformers",
      "stop_reason": "submission_rejected",
      "model_connected": true,
      "decisions": 9,
      "tool_calls": 6,
      "elapsed_seconds": 551.046,
      "token_usage": {
        "prompt_tokens": 31132,
        "completion_tokens": 4282,
        "total_tokens": 35414
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 551.046,
        "reported_token_usage": {
          "prompt_tokens": 31132,
          "completion_tokens": 4282,
          "total_tokens": 35414
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 7.7707,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.923077,
          "matched_fields": 12,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "d913c273e334e70a8087b7b45919b612"
          ],
          "submitted_order_ids": [
            "d913c273e334e70a8087b7b45919b612"
          ],
          "orders": [
            {
              "order_id": "d913c273e334e70a8087b7b45919b612",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": [
            "cbb3f2161e345c2dcb858f30d89b9269"
          ]
        },
        "tool_metrics": {
          "executed_calls": 6,
          "successful_calls": 3,
          "tool_errors": 3,
          "tool_success_rate": 0.5,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1,
            "TRANSACTION_UNAVAILABLE": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 6,
      "successful_calls": 3,
      "tool_errors": 3,
      "tool_success_rate": 0.5,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1,
        "TRANSACTION_UNAVAILABLE": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "73345cbf2c62fcbde7e5ebfc212ad29f",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 9,
      "elapsed_seconds": 600.484,
      "token_usage": {
        "prompt_tokens": 43664,
        "completion_tokens": 2558,
        "total_tokens": 46222
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.484,
        "reported_token_usage": {
          "prompt_tokens": 43664,
          "completion_tokens": 2558,
          "total_tokens": 46222
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 4.2599,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.914286,
          "matched_fields": 32,
          "total_fields": 35,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "600b5b458dee67f0939aa87f1a12002a",
            "ae0bf20391ea71adfe11412ec3c115dd",
            "cc7650e043b6c851a1df8010c94271b5"
          ],
          "submitted_order_ids": [
            "600b5b458dee67f0939aa87f1a12002a",
            "ae0bf20391ea71adfe11412ec3c115dd",
            "cc7650e043b6c851a1df8010c94271b5"
          ],
          "orders": [
            {
              "order_id": "600b5b458dee67f0939aa87f1a12002a",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 10,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "review",
                  "expected": false,
                  "actual": true
                }
              ]
            },
            {
              "order_id": "ae0bf20391ea71adfe11412ec3c115dd",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 10,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "review",
                  "expected": false,
                  "actual": true
                }
              ]
            },
            {
              "order_id": "cc7650e043b6c851a1df8010c94271b5",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 10,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "review",
                  "expected": false,
                  "actual": true
                }
              ]
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 9,
          "successful_calls": 6,
          "tool_errors": 3,
          "tool_success_rate": 0.666667,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 3
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 9,
      "successful_calls": 6,
      "tool_errors": 3,
      "tool_success_rate": 0.666667,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 3
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "68296c053f8f16b2ad8a6d0f86b3c06a",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 9,
      "tool_calls": 8,
      "elapsed_seconds": 200.297,
      "token_usage": {
        "prompt_tokens": 28917,
        "completion_tokens": 1530,
        "total_tokens": 30447
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 200.297,
        "reported_token_usage": {
          "prompt_tokens": 28917,
          "completion_tokens": 1530,
          "total_tokens": 30447
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 7.6387,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "4527d0527f8b6c29babf732ef029aa9d"
          ],
          "submitted_order_ids": [
            "4527d0527f8b6c29babf732ef029aa9d"
          ],
          "orders": [
            {
              "order_id": "4527d0527f8b6c29babf732ef029aa9d",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 8,
          "successful_calls": 7,
          "tool_errors": 1,
          "tool_success_rate": 0.875,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 8,
      "successful_calls": 7,
      "tool_errors": 1,
      "tool_success_rate": 0.875,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "d2382b88ade3ed723fda39ea95ad50f5",
      "kind": "local_transformers",
      "stop_reason": "submission_rejected",
      "model_connected": true,
      "decisions": 10,
      "tool_calls": 7,
      "elapsed_seconds": 432.047,
      "token_usage": {
        "prompt_tokens": 36336,
        "completion_tokens": 3488,
        "total_tokens": 39824
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 432.047,
        "reported_token_usage": {
          "prompt_tokens": 36336,
          "completion_tokens": 3488,
          "total_tokens": 39824
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 8.0732,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.485714,
          "matched_fields": 17,
          "total_fields": 35,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "5a6dcd66c8fd4f0aee2f12ee9f68ac33",
            "6acc43d1ce0c21bd1cd43e99f95f20ce",
            "dfe6aa2032a1365832760c3bcf47decc"
          ],
          "submitted_order_ids": [
            "5a6dcd66c8fd4f0aee2f12ee9f68ac33",
            "6acc43d1ce0c21bd1cd43e99f95f20ce",
            "dfe6aa2032a1365832760c3bcf47decc"
          ],
          "orders": [
            {
              "order_id": "5a6dcd66c8fd4f0aee2f12ee9f68ac33",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 2359,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 2359,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 2359
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 2359
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "107994fe184f20884af4272ef2bb7371"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "6acc43d1ce0c21bd1cd43e99f95f20ce",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 4,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 17102,
                  "actual": 0
                },
                {
                  "field": "refunded_cents",
                  "expected": 9975,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 7127,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 17102
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 9975,
                  "actual": 17102
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "007075171111cb011f428f37bfa25c49"
                  ],
                  "actual": []
                },
                {
                  "field": "refund_ids",
                  "expected": [
                    "1c2b49581db26b0416c385f2008f0b77",
                    "846f38eda195b127213799d48ef558bf"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "dfe6aa2032a1365832760c3bcf47decc",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 16260,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 16260,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 16260
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 16260
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "d7d3a682c83a87e80384f620de605d9c"
                  ],
                  "actual": []
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": [
            "007075171111cb011f428f37bfa25c49",
            "107994fe184f20884af4272ef2bb7371",
            "1c2b49581db26b0416c385f2008f0b77",
            "846f38eda195b127213799d48ef558bf",
            "d7d3a682c83a87e80384f620de605d9c"
          ]
        },
        "tool_metrics": {
          "executed_calls": 7,
          "successful_calls": 5,
          "tool_errors": 2,
          "tool_success_rate": 0.714286,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 7,
      "successful_calls": 5,
      "tool_errors": 2,
      "tool_success_rate": 0.714286,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "4ac9079cd1a9a6e4f188c19fbab1a43a",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 9,
      "tool_calls": 6,
      "elapsed_seconds": 600.156,
      "token_usage": {
        "prompt_tokens": 22057,
        "completion_tokens": 3242,
        "total_tokens": 25299
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.156,
        "reported_token_usage": {
          "prompt_tokens": 22057,
          "completion_tokens": 3242,
          "total_tokens": 25299
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 5.4019,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.846154,
          "matched_fields": 11,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "1a87fc93a7491119fdc87820469fc230"
          ],
          "submitted_order_ids": [
            "1a87fc93a7491119fdc87820469fc230"
          ],
          "orders": [
            {
              "order_id": "1a87fc93a7491119fdc87820469fc230",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 10,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "review",
                  "expected": true,
                  "actual": false
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [
            "6b9384801d2c2bb580135e4ca91a2121",
            "dc11da847416b81571f9bce3976613bc"
          ],
          "submitted_unallocated_transaction_ids": [
            "0e173912aea18acb668659bbe6839d96"
          ]
        },
        "tool_metrics": {
          "executed_calls": 6,
          "successful_calls": 3,
          "tool_errors": 3,
          "tool_success_rate": 0.5,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1,
            "TRANSACTION_UNAVAILABLE": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 6,
      "successful_calls": 3,
      "tool_errors": 3,
      "tool_success_rate": 0.5,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1,
        "TRANSACTION_UNAVAILABLE": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "a7e6681e1d9210bd8266050c2521dfda",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 5,
      "tool_calls": 4,
      "elapsed_seconds": 408.281,
      "token_usage": {
        "prompt_tokens": 12469,
        "completion_tokens": 1044,
        "total_tokens": 13513
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 408.281,
        "reported_token_usage": {
          "prompt_tokens": 12469,
          "completion_tokens": 1044,
          "total_tokens": 13513
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 2.5571,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "0a140a714da19dab82b4e7495e21de60"
          ],
          "submitted_order_ids": [
            "0a140a714da19dab82b4e7495e21de60"
          ],
          "orders": [
            {
              "order_id": "0a140a714da19dab82b4e7495e21de60",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 4,
          "successful_calls": 3,
          "tool_errors": 1,
          "tool_success_rate": 0.75,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 4,
      "successful_calls": 3,
      "tool_errors": 1,
      "tool_success_rate": 0.75,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "fb0a91987e06dd6996b831fc7a3d9ed1",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 11,
      "tool_calls": 10,
      "elapsed_seconds": 600.407,
      "token_usage": {
        "prompt_tokens": 33039,
        "completion_tokens": 775,
        "total_tokens": 33814
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.407,
        "reported_token_usage": {
          "prompt_tokens": 33039,
          "completion_tokens": 775,
          "total_tokens": 33814
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 1.2908,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": null,
        "submission_present": false,
        "submission_validated": false,
        "failure_reasons": [
          "MISSING_STRUCTURED_SUBMISSION",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.0,
          "matched_fields": 0,
          "total_fields": 35,
          "order_coverage_exact": false,
          "expected_order_ids": [
            "6e5fcbdfe71bcf65b74fa8f2e108a66b",
            "9e146c0567bc5079e21c5e93f5ce1465",
            "b5b3a42856257c544cfc6e0f25422f49"
          ],
          "submitted_order_ids": [],
          "orders": [
            {
              "order_id": "6e5fcbdfe71bcf65b74fa8f2e108a66b",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 20676,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 20676,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 20676,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "dc7391275c0e6a2c1d2f3477ea1106f9"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "9e146c0567bc5079e21c5e93f5ce1465",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 16379,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 16379,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 5459,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 10920,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 5459,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "ef4521d82d3d522958d51c78de1d1751"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [
                    "508e62f51e3f111a7868640522c6d849"
                  ],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "b5b3a42856257c544cfc6e0f25422f49",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 15877,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 15877,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 15877,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "602fb8190b981b46171233d20f42bd5e"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": null
        },
        "tool_metrics": {
          "executed_calls": 10,
          "successful_calls": 10,
          "tool_errors": 0,
          "tool_success_rate": 1.0,
          "tool_error_codes": {},
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 10,
      "successful_calls": 10,
      "tool_errors": 0,
      "tool_success_rate": 1.0,
      "tool_error_codes": {},
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "035929229afc58f1cf56283b97daecbd",
      "kind": "local_transformers",
      "stop_reason": "submission_rejected",
      "model_connected": true,
      "decisions": 9,
      "tool_calls": 6,
      "elapsed_seconds": 503.234,
      "token_usage": {
        "prompt_tokens": 26756,
        "completion_tokens": 2854,
        "total_tokens": 29610
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 503.234,
        "reported_token_usage": {
          "prompt_tokens": 26756,
          "completion_tokens": 2854,
          "total_tokens": 29610
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 5.6713,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.538462,
          "matched_fields": 7,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "cb41f218d36fd060d43afa76536cdc65"
          ],
          "submitted_order_ids": [
            "cb41f218d36fd060d43afa76536cdc65"
          ],
          "orders": [
            {
              "order_id": "cb41f218d36fd060d43afa76536cdc65",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 7580,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 7580,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 7581,
                  "actual": 15161
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 7581,
                  "actual": 15161
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "74a20e243634e460fe975c4e93f891d0"
                  ],
                  "actual": []
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": [
            "9bc7d94ec3b5dd9f707d2bdc90a90e06"
          ]
        },
        "tool_metrics": {
          "executed_calls": 6,
          "successful_calls": 3,
          "tool_errors": 3,
          "tool_success_rate": 0.5,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1,
            "TRANSACTION_UNAVAILABLE": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 6,
      "successful_calls": 3,
      "tool_errors": 3,
      "tool_success_rate": 0.5,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1,
        "TRANSACTION_UNAVAILABLE": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "fe24f5375fed04e7472a53d33c16a262",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 11,
      "elapsed_seconds": 132.922,
      "token_usage": {
        "prompt_tokens": 41886,
        "completion_tokens": 1226,
        "total_tokens": 43112
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 132.922,
        "reported_token_usage": {
          "prompt_tokens": 41886,
          "completion_tokens": 1226,
          "total_tokens": 43112
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 9.2235,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.028571,
          "matched_fields": 1,
          "total_fields": 35,
          "order_coverage_exact": false,
          "expected_order_ids": [
            "1460e8ae18cb7b2df4a7a32ea1e2db4c",
            "5001b17327c1070c10b24a596a08dbe5",
            "c786c5b39afb79226a6e795f379ca454"
          ],
          "submitted_order_ids": [],
          "orders": [
            {
              "order_id": "1460e8ae18cb7b2df4a7a32ea1e2db4c",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 13763,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 13763,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 13763,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "480fb7e3b98f7cb2a51fb818fd24e92c"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "5001b17327c1070c10b24a596a08dbe5",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 9117,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 9117,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 9117,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "95d8fa7e24626e44acabf2bbc8a52c26",
                    "be67f6bbd234339dca712ee963973e2c"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "c786c5b39afb79226a6e795f379ca454",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 10623,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 10623,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 10623,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "676da56a2dbc134221d1257a2ee6049d"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 11,
          "successful_calls": 9,
          "tool_errors": 2,
          "tool_success_rate": 0.818182,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 11,
      "successful_calls": 9,
      "tool_errors": 2,
      "tool_success_rate": 0.818182,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "ebe4143e309a9a9038e50351c7ab085c",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 9,
      "tool_calls": 6,
      "elapsed_seconds": 600.125,
      "token_usage": {
        "prompt_tokens": 25273,
        "completion_tokens": 2723,
        "total_tokens": 27996
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.125,
        "reported_token_usage": {
          "prompt_tokens": 25273,
          "completion_tokens": 2723,
          "total_tokens": 27996
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 4.5374,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.846154,
          "matched_fields": 11,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "ac2a107794046da089c19e04a1b40694"
          ],
          "submitted_order_ids": [
            "ac2a107794046da089c19e04a1b40694"
          ],
          "orders": [
            {
              "order_id": "ac2a107794046da089c19e04a1b40694",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 9,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": [
                    "152580637a3328cbafb6879244a03a36"
                  ]
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": true
                }
              ]
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 6,
          "successful_calls": 5,
          "tool_errors": 1,
          "tool_success_rate": 0.833333,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 6,
      "successful_calls": 5,
      "tool_errors": 1,
      "tool_success_rate": 0.833333,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "6ae2b64ff8bae46b5b50aa337ff5fcd2",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 12,
      "elapsed_seconds": 65.0,
      "token_usage": {
        "prompt_tokens": 40732,
        "completion_tokens": 922,
        "total_tokens": 41654
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 65.0,
        "reported_token_usage": {
          "prompt_tokens": 40732,
          "completion_tokens": 922,
          "total_tokens": 41654
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 14.1846,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": null,
        "submission_present": false,
        "submission_validated": false,
        "failure_reasons": [
          "MISSING_STRUCTURED_SUBMISSION",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.0,
          "matched_fields": 0,
          "total_fields": 35,
          "order_coverage_exact": false,
          "expected_order_ids": [
            "442cd61d5182798d5c560bed001a7128",
            "6b528198aa9546088698af126dd556a8",
            "eb726c42f6975e880d18f40e0d9c6d58"
          ],
          "submitted_order_ids": [],
          "orders": [
            {
              "order_id": "442cd61d5182798d5c560bed001a7128",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 16833,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 16833,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 16833,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "b6347960ffebbf92a22150cec41fd0a5"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "6b528198aa9546088698af126dd556a8",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 8368,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 8368,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 2789,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 5579,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 2789,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "29ebf96ba5e6b2b89f641e00a386bfd4"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [
                    "b96d4d1983ba81f5266fd5063d9d868c"
                  ],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "eb726c42f6975e880d18f40e0d9c6d58",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 26484,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 26484,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 26484,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "470dbdd249ee1ec842e225f072ae3c79"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": null
        },
        "tool_metrics": {
          "executed_calls": 12,
          "successful_calls": 8,
          "tool_errors": 4,
          "tool_success_rate": 0.666667,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 4
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 12,
      "successful_calls": 8,
      "tool_errors": 4,
      "tool_success_rate": 0.666667,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 4
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "d270f3bb50f36763edbe7164838994a0",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 9,
      "tool_calls": 6,
      "elapsed_seconds": 165.0,
      "token_usage": {
        "prompt_tokens": 27897,
        "completion_tokens": 2793,
        "total_tokens": 30690
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 165.0,
        "reported_token_usage": {
          "prompt_tokens": 27897,
          "completion_tokens": 2793,
          "total_tokens": 30690
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 16.9273,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "bb672c3b97c843e1a9bc27d80c3485f7"
          ],
          "submitted_order_ids": [
            "bb672c3b97c843e1a9bc27d80c3485f7"
          ],
          "orders": [
            {
              "order_id": "bb672c3b97c843e1a9bc27d80c3485f7",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 6,
          "successful_calls": 4,
          "tool_errors": 2,
          "tool_success_rate": 0.666667,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 6,
      "successful_calls": 4,
      "tool_errors": 2,
      "tool_success_rate": 0.666667,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "c30f0286048da88d1ed30e915fb97033",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 12,
      "elapsed_seconds": 46.953,
      "token_usage": {
        "prompt_tokens": 39021,
        "completion_tokens": 563,
        "total_tokens": 39584
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 46.953,
        "reported_token_usage": {
          "prompt_tokens": 39021,
          "completion_tokens": 563,
          "total_tokens": 39584
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 11.9907,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": null,
        "submission_present": false,
        "submission_validated": false,
        "failure_reasons": [
          "MISSING_STRUCTURED_SUBMISSION",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.0,
          "matched_fields": 0,
          "total_fields": 35,
          "order_coverage_exact": false,
          "expected_order_ids": [
            "05568981f684dbdfdbd94387197f09db",
            "12a0a5009450b47b3c0ff605f4ef7d76",
            "4fee26deba424ec67c7ee805f46e67f6"
          ],
          "submitted_order_ids": [],
          "orders": [
            {
              "order_id": "05568981f684dbdfdbd94387197f09db",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 4874,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 4874,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 4874,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "5fe09cc2c3c0069fde39fec0cc1b740b"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "12a0a5009450b47b3c0ff605f4ef7d76",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 5622,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 5622,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 5622,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "37f51234f9f7f451b216d6e350728395"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "4fee26deba424ec67c7ee805f46e67f6",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 10298,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 10298,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 10298,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "7ecf4c42c567e26cd6cb58f8f6a85d3d"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": null
        },
        "tool_metrics": {
          "executed_calls": 12,
          "successful_calls": 3,
          "tool_errors": 9,
          "tool_success_rate": 0.25,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 9
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 12,
      "successful_calls": 3,
      "tool_errors": 9,
      "tool_success_rate": 0.25,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 9
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "eb9a2829dc13548b19b940cb0ae39d0e",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 7,
      "tool_calls": 5,
      "elapsed_seconds": 81.234,
      "token_usage": {
        "prompt_tokens": 19645,
        "completion_tokens": 1345,
        "total_tokens": 20990
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 81.234,
        "reported_token_usage": {
          "prompt_tokens": 19645,
          "completion_tokens": 1345,
          "total_tokens": 20990
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 16.5571,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "146173207a53ffefaf12936fa1f12251"
          ],
          "submitted_order_ids": [
            "146173207a53ffefaf12936fa1f12251"
          ],
          "orders": [
            {
              "order_id": "146173207a53ffefaf12936fa1f12251",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 5,
          "successful_calls": 4,
          "tool_errors": 1,
          "tool_success_rate": 0.8,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 5,
      "successful_calls": 4,
      "tool_errors": 1,
      "tool_success_rate": 0.8,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "884760a57d04feae53a54d836898f65f",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 10,
      "tool_calls": 9,
      "elapsed_seconds": 94.828,
      "token_usage": {
        "prompt_tokens": 32456,
        "completion_tokens": 1524,
        "total_tokens": 33980
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 94.828,
        "reported_token_usage": {
          "prompt_tokens": 32456,
          "completion_tokens": 1524,
          "total_tokens": 33980
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 16.0712,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "d26be179d31afe33cbeda59a63e572e7"
          ],
          "submitted_order_ids": [
            "d26be179d31afe33cbeda59a63e572e7"
          ],
          "orders": [
            {
              "order_id": "d26be179d31afe33cbeda59a63e572e7",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 9,
          "successful_calls": 7,
          "tool_errors": 2,
          "tool_success_rate": 0.777778,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 2
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 9,
      "successful_calls": 7,
      "tool_errors": 2,
      "tool_success_rate": 0.777778,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 2
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "4c77bf5bb2f45b005286192ffad584f0",
      "kind": "local_transformers",
      "stop_reason": "decision_budget",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 12,
      "elapsed_seconds": 72.484,
      "token_usage": {
        "prompt_tokens": 40735,
        "completion_tokens": 905,
        "total_tokens": 41640
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 72.484,
        "reported_token_usage": {
          "prompt_tokens": 40735,
          "completion_tokens": 905,
          "total_tokens": 41640
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 12.4855,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": null,
        "submission_present": false,
        "submission_validated": false,
        "failure_reasons": [
          "MISSING_STRUCTURED_SUBMISSION",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.0,
          "matched_fields": 0,
          "total_fields": 35,
          "order_coverage_exact": false,
          "expected_order_ids": [
            "9c7bbd41dbcd97b7a5f011ac0e9ee4af",
            "a603abe457ff9c944ee0560d19a300af",
            "e506b6f49fdafa04ec3db04a81946ff0"
          ],
          "submitted_order_ids": [],
          "orders": [
            {
              "order_id": "9c7bbd41dbcd97b7a5f011ac0e9ee4af",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 35133,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 35133,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 35133,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "00946efe10473cf6228b4e58431fb1b9"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "a603abe457ff9c944ee0560d19a300af",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 19446,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 19446,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 19446,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "b7d88fd85c323ce19ef801d1e8648391"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            },
            {
              "order_id": "e506b6f49fdafa04ec3db04a81946ff0",
              "submitted": false,
              "exact_match": false,
              "matched_fields": 0,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "expected_cents",
                  "expected": 3909,
                  "actual": null
                },
                {
                  "field": "received_cents",
                  "expected": 3909,
                  "actual": null
                },
                {
                  "field": "refunded_cents",
                  "expected": 2280,
                  "actual": null
                },
                {
                  "field": "pending_refund_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_cents",
                  "expected": 1629,
                  "actual": null
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": null
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 2280,
                  "actual": null
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "1e33f284ef8a2a4cca32c7bec876088b"
                  ],
                  "actual": null
                },
                {
                  "field": "refund_ids",
                  "expected": [
                    "5bd168498d170baef08ff3770c1e82b7",
                    "7f130a7a445c6adbfc0cb016a627c79d"
                  ],
                  "actual": null
                },
                {
                  "field": "pending_refund_ids",
                  "expected": [],
                  "actual": null
                },
                {
                  "field": "review",
                  "expected": false,
                  "actual": null
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": null
        },
        "tool_metrics": {
          "executed_calls": 12,
          "successful_calls": 8,
          "tool_errors": 4,
          "tool_success_rate": 0.666667,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 4
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 12,
      "successful_calls": 8,
      "tool_errors": 4,
      "tool_success_rate": 0.666667,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 4
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "e4687b3effc9622e2070c12b75a65212",
      "kind": "local_transformers",
      "stop_reason": "completed",
      "model_connected": true,
      "decisions": 7,
      "tool_calls": 6,
      "elapsed_seconds": 75.0,
      "token_usage": {
        "prompt_tokens": 20530,
        "completion_tokens": 1179,
        "total_tokens": 21709
      },
      "accuracy": 1.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 75.0,
        "reported_token_usage": {
          "prompt_tokens": 20530,
          "completion_tokens": 1179,
          "total_tokens": 21709
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 15.72,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": true,
        "failure_reasons": [],
        "scores": {
          "plan_exact_match": true,
          "field_accuracy": 1.0,
          "matched_fields": 13,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "e22985eca9017c22e75feca100883540"
          ],
          "submitted_order_ids": [
            "e22985eca9017c22e75feca100883540"
          ],
          "orders": [
            {
              "order_id": "e22985eca9017c22e75feca100883540",
              "submitted": true,
              "exact_match": true,
              "matched_fields": 11,
              "total_fields": 11,
              "mismatches": []
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 6,
          "successful_calls": 5,
          "tool_errors": 1,
          "tool_success_rate": 0.833333,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "boundary",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 6,
      "successful_calls": 5,
      "tool_errors": 1,
      "tool_success_rate": 0.833333,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "7ceb1db6f097025c0d80ec6faff76a88",
      "kind": "local_transformers",
      "stop_reason": "timeout",
      "model_connected": true,
      "decisions": 12,
      "tool_calls": 9,
      "elapsed_seconds": 600.39,
      "token_usage": {
        "prompt_tokens": 37650,
        "completion_tokens": 2637,
        "total_tokens": 40287
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 600.39,
        "reported_token_usage": {
          "prompt_tokens": 37650,
          "completion_tokens": 2637,
          "total_tokens": 40287
        },
        "token_usage_complete": false,
        "reported_output_tokens_per_second": 4.3921,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.542857,
          "matched_fields": 19,
          "total_fields": 35,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "5409dcaf72eb5aabb706c90e61015a66",
            "59c22ae71b1673a5f0c6bb138645789d",
            "b4b3b4466fcbf99080909ff614905607"
          ],
          "submitted_order_ids": [
            "5409dcaf72eb5aabb706c90e61015a66",
            "59c22ae71b1673a5f0c6bb138645789d",
            "b4b3b4466fcbf99080909ff614905607"
          ],
          "orders": [
            {
              "order_id": "5409dcaf72eb5aabb706c90e61015a66",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 4627,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 4627,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 4627
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 4627
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "c2a174a3d07e9c03b598d4415573c5ea"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "59c22ae71b1673a5f0c6bb138645789d",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 37900,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 37900,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 37900
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 37900
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "8234c32b1c55556938021e4767447d60"
                  ],
                  "actual": []
                }
              ]
            },
            {
              "order_id": "b4b3b4466fcbf99080909ff614905607",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 6,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "received_cents",
                  "expected": 10226,
                  "actual": 0
                },
                {
                  "field": "net_cents",
                  "expected": 10226,
                  "actual": 0
                },
                {
                  "field": "collection_gap_cents",
                  "expected": 0,
                  "actual": 10226
                },
                {
                  "field": "net_vs_original_cents",
                  "expected": 0,
                  "actual": 10226
                },
                {
                  "field": "receipt_ids",
                  "expected": [
                    "0e1cc8638f3d1d72f6c0898a347b274e"
                  ],
                  "actual": []
                }
              ]
            }
          ],
          "unallocated_exact": false,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": [
            "0e1cc8638f3d1d72f6c0898a347b274e",
            "8234c32b1c55556938021e4767447d60",
            "c2a174a3d07e9c03b598d4415573c5ea"
          ]
        },
        "tool_metrics": {
          "executed_calls": 9,
          "successful_calls": 3,
          "tool_errors": 6,
          "tool_success_rate": 0.333333,
          "tool_error_codes": {
            "TRANSACTION_UNAVAILABLE": 6
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "basic",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 9,
      "successful_calls": 3,
      "tool_errors": 6,
      "tool_success_rate": 0.333333,
      "tool_error_codes": {
        "TRANSACTION_UNAVAILABLE": 6
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    },
    {
      "task_id": "71bf919b9f8768e6932b17b6233317c3",
      "kind": "local_transformers",
      "stop_reason": "submission_rejected",
      "model_connected": true,
      "decisions": 9,
      "tool_calls": 6,
      "elapsed_seconds": 514.265,
      "token_usage": {
        "prompt_tokens": 32020,
        "completion_tokens": 4549,
        "total_tokens": 36569
      },
      "accuracy": 0.0,
      "cost": {
        "mode": "local_transformers",
        "currency": "USD",
        "elapsed_seconds": 514.265,
        "reported_token_usage": {
          "prompt_tokens": 32020,
          "completion_tokens": 4549,
          "total_tokens": 36569
        },
        "token_usage_complete": true,
        "reported_output_tokens_per_second": 8.8456,
        "api_fee": 0.0,
        "compute_fee_estimate": null,
        "compute_fee_status": "not_configured",
        "scope": "elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。本地API费用为0不代表硬件和电费为0；未测量实际电费。",
        "api_fee_status": "local_no_api"
      },
      "evaluation": {
        "status": "scored",
        "grading_version": "structured-plan-exact-v1",
        "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
        "submission_source": "final_json",
        "submission_present": true,
        "submission_validated": false,
        "failure_reasons": [
          "REFERENCE_MISMATCH",
          "RUN_NOT_COMPLETED"
        ],
        "scores": {
          "plan_exact_match": false,
          "field_accuracy": 0.923077,
          "matched_fields": 12,
          "total_fields": 13,
          "order_coverage_exact": true,
          "expected_order_ids": [
            "6ec35ea1eb047624fb828389a8c09c88"
          ],
          "submitted_order_ids": [
            "6ec35ea1eb047624fb828389a8c09c88"
          ],
          "orders": [
            {
              "order_id": "6ec35ea1eb047624fb828389a8c09c88",
              "submitted": true,
              "exact_match": false,
              "matched_fields": 10,
              "total_fields": 11,
              "mismatches": [
                {
                  "field": "review",
                  "expected": false,
                  "actual": true
                }
              ]
            }
          ],
          "unallocated_exact": true,
          "expected_unallocated_transaction_ids": [],
          "submitted_unallocated_transaction_ids": []
        },
        "tool_metrics": {
          "executed_calls": 6,
          "successful_calls": 5,
          "tool_errors": 1,
          "tool_success_rate": 0.833333,
          "tool_error_codes": {
            "INVALID_ARGUMENT": 1
          },
          "validation_calls": 0,
          "last_validation_valid": null,
          "validation_passed": false
        },
        "reference": {
          "split": "val",
          "category": "cross_tool",
          "rule_version": "brl-reconciliation-v1",
          "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
        },
        "submission_contract_requested": true,
        "post_run_only": true,
        "natural_language_report_scored": false
      },
      "recorded_trace_incomplete": null,
      "executed_calls": 6,
      "successful_calls": 5,
      "tool_errors": 1,
      "tool_success_rate": 0.833333,
      "tool_error_codes": {
        "INVALID_ARGUMENT": 1
      },
      "validation_calls": 0,
      "last_validation_valid": null,
      "validation_passed": false
    }
  ],
  "tool_validated_tasks": 0,
  "local_model": {
    "model": "Qwen/Qwen3-4B-Instruct-2507",
    "model_dir": "D:\\All_ws\\LM_Theory_Practice\\End_project\\models\\Qwen3-4B-Instruct-2507",
    "quantization": "NF4 double quantization",
    "compute_dtype": "bfloat16",
    "gpu": "NVIDIA GeForce RTX 4060 Laptop GPU",
    "temperature": 0,
    "torch_version": "2.5.0+cu118",
    "cuda_version": "11.8",
    "cpu_threads": 4,
    "max_context": 16384,
    "max_new_tokens": 2048,
    "peak_allocated_mib": 4032.58,
    "trained_weights_verified": false
  },
  "split": "val",
  "requested_tasks": 50,
  "run_progress": {
    "phase": "finished",
    "requested_tasks": 50,
    "processed_tasks": 50
  },
  "model_cleanup": {
    "status": "closed",
    "allocated_after_close_mib": 8.13
  }
}
```


## 21c3d4e5a0614191e11d55713232e4db 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "10d0be9599be29de40b12d3207365a1e"
    ],
    "submitted_order_ids": [
      "10d0be9599be29de40b12d3207365a1e"
    ],
    "orders": [
      {
        "order_id": "10d0be9599be29de40b12d3207365a1e",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 4,
    "successful_calls": 3,
    "tool_errors": 1,
    "tool_success_rate": 0.75,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## bf813189fc6640c45b548696cc9b4219 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.0,
    "matched_fields": 0,
    "total_fields": 35,
    "order_coverage_exact": false,
    "expected_order_ids": [
      "04399bab7aacceedb34e72ef4235236b",
      "bfa04e0466136d37c1d991c5f9cec359",
      "fefe384c5a9d630915a85cd9829481be"
    ],
    "submitted_order_ids": [],
    "orders": [
      {
        "order_id": "04399bab7aacceedb34e72ef4235236b",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 15730,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 15730,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 5243,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 10487,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 5243,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "3a21a64d65f4702d756acc9e53b047ae"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [
              "8ebbadbb54fe4a9ae8bd626155fb16e2"
            ],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "bfa04e0466136d37c1d991c5f9cec359",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 15791,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 15791,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 15791,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "3d6c419ec93ef577e239a17a4c7b29e1"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "fefe384c5a9d630915a85cd9829481be",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 12826,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 12826,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 12826,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "d5ab81e00a7df71ebb03acdef33e8e36"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": [
      "f1602d97eee8e67fb03f1ab2b7cb4c2c",
      "78350c90a16f49835a50fb96e6902222",
      "ad0030a81ceba243f1a88dac905383a7"
    ]
  },
  "tool_metrics": {
    "executed_calls": 9,
    "successful_calls": 3,
    "tool_errors": 6,
    "tool_success_rate": 0.333333,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 6
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## ed909817f48b358af93551a9f0c7751a 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "61aa1eb4f2e9ff51bd27052b4229a998"
    ],
    "submitted_order_ids": [
      "61aa1eb4f2e9ff51bd27052b4229a998"
    ],
    "orders": [
      {
        "order_id": "61aa1eb4f2e9ff51bd27052b4229a998",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 5,
    "successful_calls": 4,
    "tool_errors": 1,
    "tool_success_rate": 0.8,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 468468e59dc4ee94b5a2c0c5da79e4bc 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": null,
  "submission_present": false,
  "submission_validated": false,
  "failure_reasons": [
    "MISSING_STRUCTURED_SUBMISSION",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.0,
    "matched_fields": 0,
    "total_fields": 35,
    "order_coverage_exact": false,
    "expected_order_ids": [
      "91f1f76ed01471b8381be7cf66dc5619",
      "c8a4af0be858d7845052792eac2c03d7",
      "eb569e85c639321876a37822de05686a"
    ],
    "submitted_order_ids": [],
    "orders": [
      {
        "order_id": "91f1f76ed01471b8381be7cf66dc5619",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 24298,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 24298,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 24298,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "2b47a076a33f905564d6423d7080bdd1"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "c8a4af0be858d7845052792eac2c03d7",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 7286,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 7286,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 7286,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "01d1ec809eb3bad7836840cae77a7d75",
              "823ab72af8b089a31cf2635023706507"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "eb569e85c639321876a37822de05686a",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 20507,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 20507,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 20507,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "143c1fa44b2dc6793e11ca8aa8c01447"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": null
  },
  "tool_metrics": {
    "executed_calls": 12,
    "successful_calls": 7,
    "tool_errors": 5,
    "tool_success_rate": 0.583333,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 5
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 5fc8bf28eec5253836d17a8fb1ed18da 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.384615,
    "matched_fields": 5,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "3b50b6109aa5b7db4c695574ba4a4c41"
    ],
    "submitted_order_ids": [
      "3b50b6109aa5b7db4c695574ba4a4c41"
    ],
    "orders": [
      {
        "order_id": "3b50b6109aa5b7db4c695574ba4a4c41",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 4,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 17185,
            "actual": 0
          },
          {
            "field": "pending_refund_cents",
            "expected": 5728,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 17185,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 17185
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 17185
          },
          {
            "field": "receipt_ids",
            "expected": [
              "aa6287d1fef5dc574ea42d16b840a8af"
            ],
            "actual": []
          },
          {
            "field": "pending_refund_ids",
            "expected": [
              "703e5c8221bf248d3afcd4170a37d6b4"
            ],
            "actual": []
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": [
      "417262b7792392b829c73b3abbd201e7"
    ]
  },
  "tool_metrics": {
    "executed_calls": 5,
    "successful_calls": 2,
    "tool_errors": 3,
    "tool_success_rate": 0.4,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1,
      "TRANSACTION_UNAVAILABLE": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 479170a1ca62896400a0e197f6b2fdeb 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.771429,
    "matched_fields": 27,
    "total_fields": 35,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "2aa52c3a919e5d5f60d46050d53c39c2",
      "e398aec0ef1865846262935e2c7df8c0",
      "e5beee1b3623cdff90232bbbe6377dad"
    ],
    "submitted_order_ids": [
      "2aa52c3a919e5d5f60d46050d53c39c2",
      "e398aec0ef1865846262935e2c7df8c0",
      "e5beee1b3623cdff90232bbbe6377dad"
    ],
    "orders": [
      {
        "order_id": "2aa52c3a919e5d5f60d46050d53c39c2",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 10,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "review",
            "expected": true,
            "actual": false
          }
        ]
      },
      {
        "order_id": "e398aec0ef1865846262935e2c7df8c0",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 101080,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 101080,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 101080
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 101080
          },
          {
            "field": "receipt_ids",
            "expected": [
              "311c4a97d78ae93096d52209f33d23b7"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "e5beee1b3623cdff90232bbbe6377dad",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 10,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "review",
            "expected": true,
            "actual": false
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [
      "384dad9488bd17041d976757283a00d4",
      "bede0f32adf6a83cc15ce7f7b53ce973"
    ],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 11,
    "successful_calls": 8,
    "tool_errors": 3,
    "tool_success_rate": 0.727273,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 3
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 7f997d6ed7aa6422de146a5b31739cf0 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "21604e0c15c8f114bca8e058eb2916a3"
    ],
    "submitted_order_ids": [
      "21604e0c15c8f114bca8e058eb2916a3"
    ],
    "orders": [
      {
        "order_id": "21604e0c15c8f114bca8e058eb2916a3",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 6,
    "successful_calls": 5,
    "tool_errors": 1,
    "tool_success_rate": 0.833333,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 3ddbe5aad5849a4d24754cdbc8498bc7 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.0,
    "matched_fields": 0,
    "total_fields": 35,
    "order_coverage_exact": false,
    "expected_order_ids": [
      "4e46514bdc98305a78f3435525422081",
      "9765fa7a50c9e516fdfbdde824404756",
      "f307504550c093e0aed31abfbeb87341"
    ],
    "submitted_order_ids": [],
    "orders": [
      {
        "order_id": "4e46514bdc98305a78f3435525422081",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 16388,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 16388,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 16388,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "4617b736b33414f889e1c98d393edfdd"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "9765fa7a50c9e516fdfbdde824404756",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 17269,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 17269,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 17269,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "9b428235e031091f996863791a3827a3"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "f307504550c093e0aed31abfbeb87341",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 6100,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 6100,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 6100,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "73727a4ac1033f55fbc96dbf2c12b794"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": [
      "f307504550c093e0aed31abfbeb87341",
      "9765fa7a50c9e516fdfbdde824404756",
      "4e46514bdc98305a78f343552542081"
    ]
  },
  "tool_metrics": {
    "executed_calls": 11,
    "successful_calls": 5,
    "tool_errors": 6,
    "tool_success_rate": 0.454545,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 6
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## d2b7626c6102419a57fc610c02142024 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.538462,
    "matched_fields": 7,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "082242775a54782499f8320401414af7"
    ],
    "submitted_order_ids": [
      "082242775a54782499f8320401414af7"
    ],
    "orders": [
      {
        "order_id": "082242775a54782499f8320401414af7",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 3758,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 3758,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 3758,
            "actual": 7516
          },
          {
            "field": "net_vs_original_cents",
            "expected": 3758,
            "actual": 7516
          },
          {
            "field": "receipt_ids",
            "expected": [
              "4130d73909fae73a0efc639302fc7b36"
            ],
            "actual": []
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": [
      "2d190d42ab1d166a395e09ae51c6c4d3",
      "4130d73909fae73a0efc639302fc7b36"
    ]
  },
  "tool_metrics": {
    "executed_calls": 5,
    "successful_calls": 2,
    "tool_errors": 3,
    "tool_success_rate": 0.4,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1,
      "TRANSACTION_UNAVAILABLE": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 434488fe8701e3af19135e318acc42ca 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "d9f21071ea6df6e4db1d04a2f709598a"
    ],
    "submitted_order_ids": [
      "d9f21071ea6df6e4db1d04a2f709598a"
    ],
    "orders": [
      {
        "order_id": "d9f21071ea6df6e4db1d04a2f709598a",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 8,
    "successful_calls": 7,
    "tool_errors": 1,
    "tool_success_rate": 0.875,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 57fa52b1095d682898df7fa9d77ec043 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.0,
    "matched_fields": 0,
    "total_fields": 35,
    "order_coverage_exact": false,
    "expected_order_ids": [
      "219069f4b05b20f21850188f54089c2c",
      "73f079675f874ac897ceb0ff87ba44c1",
      "f64298035450e84a38b26a1b2b21287d"
    ],
    "submitted_order_ids": [],
    "orders": [
      {
        "order_id": "219069f4b05b20f21850188f54089c2c",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 17252,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 17252,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 17252,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "b49908b1395addf7e4a1a38df043ee3c"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "73f079675f874ac897ceb0ff87ba44c1",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 22566,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 22566,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 22566,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "513cf7e378e511ca95c77acf58420011"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "f64298035450e84a38b26a1b2b21287d",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 12573,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 12573,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 7334,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 5239,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 7334,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "4423b4578ebd1663792bcb6f73581b32"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [
              "3601692f60077b2cb3fe05866473d9c7",
              "7e8d27fc4d256ebe017f67e55f6c4be9"
            ],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": [
      "f937ce3a37a5aca958a254bc027b0062",
      "06e8b07b5851225fde54070c150fea59",
      "5c2e537a952224ba3b7b21ba80c2dde6"
    ]
  },
  "tool_metrics": {
    "executed_calls": 11,
    "successful_calls": 8,
    "tool_errors": 3,
    "tool_success_rate": 0.727273,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 3
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 8a91d6131c96cfd5abf66c6bd985f2f6 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "23d446a5054153284616805e6adee0ad"
    ],
    "submitted_order_ids": [
      "23d446a5054153284616805e6adee0ad"
    ],
    "orders": [
      {
        "order_id": "23d446a5054153284616805e6adee0ad",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 5,
    "successful_calls": 4,
    "tool_errors": 1,
    "tool_success_rate": 0.8,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## cffa67df53c4fdefeabe3a84dbe67ae1 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.542857,
    "matched_fields": 19,
    "total_fields": 35,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "03e63dfb3beb7bc87efb6ba6085df51b",
      "97e52f2a7242cfafe1eb270b8978dd9e",
      "a2fdded70acc1f7ef3bc36b434e7e934"
    ],
    "submitted_order_ids": [
      "03e63dfb3beb7bc87efb6ba6085df51b",
      "97e52f2a7242cfafe1eb270b8978dd9e",
      "a2fdded70acc1f7ef3bc36b434e7e934"
    ],
    "orders": [
      {
        "order_id": "03e63dfb3beb7bc87efb6ba6085df51b",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 4087,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 4087,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 4087
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 4087
          },
          {
            "field": "receipt_ids",
            "expected": [
              "01270ac53c74971d80fe604f7aea9f19"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "97e52f2a7242cfafe1eb270b8978dd9e",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 8637,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 8637,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 8637
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 8637
          },
          {
            "field": "receipt_ids",
            "expected": [
              "40ac564dfcb736e9381896bc3e0c93c6"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "a2fdded70acc1f7ef3bc36b434e7e934",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 5837,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 5837,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 5837
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 5837
          },
          {
            "field": "receipt_ids",
            "expected": [
              "05e108ef6a8caa2e9a429c9c0750f32f"
            ],
            "actual": []
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": [
      "a8451d3ec7b0b6bc0f364ef81f53097c",
      "9f689703c72cd9ab1abd3429a0094886",
      "01270ac53c74971d80fe604f7aea9f19",
      "05e108ef6a8caa2e9a429c9c0750f32f",
      "40ac564dfcb736e9381896bc3e0c93c6"
    ]
  },
  "tool_metrics": {
    "executed_calls": 9,
    "successful_calls": 6,
    "tool_errors": 3,
    "tool_success_rate": 0.666667,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 3
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## bd5d5f9c3276a58df77a2419a5efad6c 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "2a1ca3d5bd78a7bb914711f3cb46b591"
    ],
    "submitted_order_ids": [
      "2a1ca3d5bd78a7bb914711f3cb46b591"
    ],
    "orders": [
      {
        "order_id": "2a1ca3d5bd78a7bb914711f3cb46b591",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 5,
    "successful_calls": 4,
    "tool_errors": 1,
    "tool_success_rate": 0.8,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 6d55f5c4bbf5103dbba06e87cac23b9c 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.542857,
    "matched_fields": 19,
    "total_fields": 35,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "25343818f100f1b4f35714ba55141d02",
      "461cb9ba7e3bf748ebf6f9f33658639f",
      "a81ee67fb909fa5ce8b33ef1e413248d"
    ],
    "submitted_order_ids": [
      "25343818f100f1b4f35714ba55141d02",
      "461cb9ba7e3bf748ebf6f9f33658639f",
      "a81ee67fb909fa5ce8b33ef1e413248d"
    ],
    "orders": [
      {
        "order_id": "25343818f100f1b4f35714ba55141d02",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 11924,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 11924,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 11924
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 11924
          },
          {
            "field": "receipt_ids",
            "expected": [
              "541b0343f259807a9973d9df2db10500"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "461cb9ba7e3bf748ebf6f9f33658639f",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 9962,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 9962,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 9962
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 9962
          },
          {
            "field": "receipt_ids",
            "expected": [
              "b2c863bad4715e0fad76a246d404ff64"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "a81ee67fb909fa5ce8b33ef1e413248d",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 8673,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 8673,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 8673
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 8673
          },
          {
            "field": "receipt_ids",
            "expected": [
              "0a7d0d5cfb32d463027ca198d203b078"
            ],
            "actual": []
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": [
      "0a7d0d5cfb32d463027ca198d203b078",
      "541b0343f259807a9973d9df2db10500",
      "b2c863bad4715e0fad76a246d404ff64"
    ]
  },
  "tool_metrics": {
    "executed_calls": 9,
    "successful_calls": 3,
    "tool_errors": 6,
    "tool_success_rate": 0.333333,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 6
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 75216dd2720419476f3d29de0d924992 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "5156bf77e2f89073c8a4624ae0e6d83c"
    ],
    "submitted_order_ids": [
      "5156bf77e2f89073c8a4624ae0e6d83c"
    ],
    "orders": [
      {
        "order_id": "5156bf77e2f89073c8a4624ae0e6d83c",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 8,
    "successful_calls": 7,
    "tool_errors": 1,
    "tool_success_rate": 0.875,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 8cd876aedfccd2c3e723c499c8ca29ba 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.028571,
    "matched_fields": 1,
    "total_fields": 35,
    "order_coverage_exact": false,
    "expected_order_ids": [
      "0c2adc3ad8983c9d94d6f2158859b515",
      "a2521df763e5225f8c3242b024c9c172",
      "f20f222751a822660640a01ba93a785d"
    ],
    "submitted_order_ids": [],
    "orders": [
      {
        "order_id": "0c2adc3ad8983c9d94d6f2158859b515",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 12426,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 12426,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 12426,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "5965e8c27dd84b3e81a3767e6a79194f"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "a2521df763e5225f8c3242b024c9c172",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 11694,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 11694,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 3898,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 11694,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "80f5059e6edb67140459f190c682730e"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [
              "be433d30388a0f07ade485a43ec91fae"
            ],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "f20f222751a822660640a01ba93a785d",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 19571,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 19571,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 19571,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "e24f89dc36a3025ced0ef653993d1796"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 11,
    "successful_calls": 5,
    "tool_errors": 6,
    "tool_success_rate": 0.454545,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 6
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 330a87c29959c593780eacca69429c78 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "f54e11c44ac66e16fdb295eef1d3db8f"
    ],
    "submitted_order_ids": [
      "f54e11c44ac66e16fdb295eef1d3db8f"
    ],
    "orders": [
      {
        "order_id": "f54e11c44ac66e16fdb295eef1d3db8f",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 5,
    "successful_calls": 4,
    "tool_errors": 1,
    "tool_success_rate": 0.8,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## f18646ac434add104caf416811a73193 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "9e012c2519fc738b2de58b005cdb57d3"
    ],
    "submitted_order_ids": [
      "9e012c2519fc738b2de58b005cdb57d3"
    ],
    "orders": [
      {
        "order_id": "9e012c2519fc738b2de58b005cdb57d3",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 6,
    "successful_calls": 4,
    "tool_errors": 2,
    "tool_success_rate": 0.666667,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## e77a7d0e9aa1818c036bbec6afafbcb6 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.542857,
    "matched_fields": 19,
    "total_fields": 35,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "5dc6c81909d385e66729a3b7abc07130",
      "c6e942b5d07954188223e9ca7380d5f9",
      "e559c5076f02a533bcbd1d0f11da7bbd"
    ],
    "submitted_order_ids": [
      "5dc6c81909d385e66729a3b7abc07130",
      "c6e942b5d07954188223e9ca7380d5f9",
      "e559c5076f02a533bcbd1d0f11da7bbd"
    ],
    "orders": [
      {
        "order_id": "5dc6c81909d385e66729a3b7abc07130",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 15902,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 15902,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 15902
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 15902
          },
          {
            "field": "receipt_ids",
            "expected": [
              "ccc3e96f38b80d65f875dc51423fcad7"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "c6e942b5d07954188223e9ca7380d5f9",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 8641,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 8641,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 8641
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 8641
          },
          {
            "field": "receipt_ids",
            "expected": [
              "0e8d7777a4afa12c3effc116119129f7"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "e559c5076f02a533bcbd1d0f11da7bbd",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 10757,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 10757,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 10757
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 10757
          },
          {
            "field": "receipt_ids",
            "expected": [
              "6250ae32933a1a32402ca983fdbb2d47"
            ],
            "actual": []
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": [
      "0e8d7777a4afa12c3effc116119129f7",
      "6250ae32933a1a32402ca983fdbb2d47",
      "ccc3e96f38b80d65f875dc51423fcad7"
    ]
  },
  "tool_metrics": {
    "executed_calls": 8,
    "successful_calls": 6,
    "tool_errors": 2,
    "tool_success_rate": 0.75,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 74a7fa70d9396ddf3d5ac116e84017da 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.846154,
    "matched_fields": 11,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "cb2cf2f39f97ade4af52d72b30957af7"
    ],
    "submitted_order_ids": [
      "cb2cf2f39f97ade4af52d72b30957af7"
    ],
    "orders": [
      {
        "order_id": "cb2cf2f39f97ade4af52d72b30957af7",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 10,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "review",
            "expected": true,
            "actual": false
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [
      "76af93852df83383d010ed925c59f52e",
      "c3cd5786d2d69f4fb27d19cd0d0600ac"
    ],
    "submitted_unallocated_transaction_ids": [
      "c6de2b1a610cd16df565bc2c78741fd5",
      "76af93852df83383d010ed925c59f52e",
      "c3cd5786d2d69f4fb27d19cd0d0600ac"
    ]
  },
  "tool_metrics": {
    "executed_calls": 6,
    "successful_calls": 3,
    "tool_errors": 3,
    "tool_success_rate": 0.5,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1,
      "TRANSACTION_UNAVAILABLE": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## c4f31b0cd50d13bde1a9b4eb712008dc 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.028571,
    "matched_fields": 1,
    "total_fields": 35,
    "order_coverage_exact": false,
    "expected_order_ids": [
      "777491dbae329fbbac02b42eaba28ca1",
      "beb5c901d6610032752ae032a995b2c1",
      "ec56081b18edddf8846064c7947cf6df"
    ],
    "submitted_order_ids": [],
    "orders": [
      {
        "order_id": "777491dbae329fbbac02b42eaba28ca1",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 4509,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 4509,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 4509,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "4cb6ad478a357c3c473e53c78d19df5f"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "beb5c901d6610032752ae032a995b2c1",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 5705,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 5705,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 5705,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "57da2dadee60f2fcf4a62f44173fc99d"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "ec56081b18edddf8846064c7947cf6df",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 4372,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 4372,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 4372,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "135c5422e54af32cbbbec4c4557c1e88",
              "a0a4c84517abfefc1a7df1f2bf5d1eb3"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 11,
    "successful_calls": 9,
    "tool_errors": 2,
    "tool_success_rate": 0.818182,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 30a7a37087ff15f5fc67b95c6eaba71e 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "fb99b43dfe70fcc3e93a87748bd4a508"
    ],
    "submitted_order_ids": [
      "fb99b43dfe70fcc3e93a87748bd4a508"
    ],
    "orders": [
      {
        "order_id": "fb99b43dfe70fcc3e93a87748bd4a508",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 7,
    "successful_calls": 6,
    "tool_errors": 1,
    "tool_success_rate": 0.857143,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 1e9c2bdb06a0d03adfc9f4a70b9819b6 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.485714,
    "matched_fields": 17,
    "total_fields": 35,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "82c239b7e22c405455045158a40e6ac4",
      "9a490fae11ab66e7dfeb3d043c789989",
      "f7d2b681af640a2dabded625da66f2cd"
    ],
    "submitted_order_ids": [
      "82c239b7e22c405455045158a40e6ac4",
      "9a490fae11ab66e7dfeb3d043c789989",
      "f7d2b681af640a2dabded625da66f2cd"
    ],
    "orders": [
      {
        "order_id": "82c239b7e22c405455045158a40e6ac4",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 2,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 16365,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 16365,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 16365,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "98dea0d52f50020027cb1b23fed02538"
            ],
            "actual": [
              "40b507d5d9e3f6bbec1a6bca48e5d7f5"
            ]
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          }
        ]
      },
      {
        "order_id": "9a490fae11ab66e7dfeb3d043c789989",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      },
      {
        "order_id": "f7d2b681af640a2dabded625da66f2cd",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 2,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 8465,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 8465,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 8465,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "40b507d5d9e3f6bbec1a6bca48e5d7f5"
            ],
            "actual": [
              "98dea0d52f50020027cb1b23fed02538"
            ]
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          }
        ]
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 10,
    "successful_calls": 8,
    "tool_errors": 2,
    "tool_success_rate": 0.8,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## d06f45da76c85fcfc23c4e286e2e14d6 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "d055c81580fd81094255ab1b3a3ead2d"
    ],
    "submitted_order_ids": [
      "d055c81580fd81094255ab1b3a3ead2d"
    ],
    "orders": [
      {
        "order_id": "d055c81580fd81094255ab1b3a3ead2d",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 4,
    "successful_calls": 3,
    "tool_errors": 1,
    "tool_success_rate": 0.75,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## d2b82257bd75cfa1b5ff7e950720c472 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.514286,
    "matched_fields": 18,
    "total_fields": 35,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "27da256dcbf3fde208e977b90f00ace4",
      "4516123a1e1a40f07f357d4a231438b3",
      "9752df65a5356741e6dcfb11b33f5ef8"
    ],
    "submitted_order_ids": [
      "27da256dcbf3fde208e977b90f00ace4",
      "4516123a1e1a40f07f357d4a231438b3",
      "9752df65a5356741e6dcfb11b33f5ef8"
    ],
    "orders": [
      {
        "order_id": "27da256dcbf3fde208e977b90f00ace4",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 11545,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 11545,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 11545
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 11545
          },
          {
            "field": "receipt_ids",
            "expected": [
              "1a208595cbb89e584532737f56eea691"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "4516123a1e1a40f07f357d4a231438b3",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 4,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 4184,
            "actual": 0
          },
          {
            "field": "refunded_cents",
            "expected": 1394,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 2790,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 4184
          },
          {
            "field": "net_vs_original_cents",
            "expected": 1394,
            "actual": 4184
          },
          {
            "field": "receipt_ids",
            "expected": [
              "56744684b37ea679cf18a3292864c620"
            ],
            "actual": []
          },
          {
            "field": "refund_ids",
            "expected": [
              "cbb238cbd4d57811b60522b5a7a9a75d"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "9752df65a5356741e6dcfb11b33f5ef8",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 10033,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 10033,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 10033
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 10033
          },
          {
            "field": "receipt_ids",
            "expected": [
              "1ce4b693ae0d7d15aa715149cf270f12"
            ],
            "actual": []
          }
        ]
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 11,
    "successful_calls": 9,
    "tool_errors": 2,
    "tool_success_rate": 0.818182,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 8edf039760facb291bb29f04aa0bc78d 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.923077,
    "matched_fields": 12,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "c9a0e4198b4331fba206c47367d14985"
    ],
    "submitted_order_ids": [
      "c9a0e4198b4331fba206c47367d14985"
    ],
    "orders": [
      {
        "order_id": "c9a0e4198b4331fba206c47367d14985",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 10,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "review",
            "expected": false,
            "actual": true
          }
        ]
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 5,
    "successful_calls": 4,
    "tool_errors": 1,
    "tool_success_rate": 0.8,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 01b486c3b0d11490d9b3d0369b87ebd4 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "af5129b6e8a55a0eecdc2fc1d6b123f5"
    ],
    "submitted_order_ids": [
      "af5129b6e8a55a0eecdc2fc1d6b123f5"
    ],
    "orders": [
      {
        "order_id": "af5129b6e8a55a0eecdc2fc1d6b123f5",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 9,
    "successful_calls": 7,
    "tool_errors": 2,
    "tool_success_rate": 0.777778,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 04e52fd7f0d95f9b37f1bc9759c00f0d 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.485714,
    "matched_fields": 17,
    "total_fields": 35,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "240e00887dd032bf5547aa45017f01ca",
      "a2d4648245eef6c901ad5ef01bd05776",
      "d2fd0fc81f4bb24f895babec3940441c"
    ],
    "submitted_order_ids": [
      "240e00887dd032bf5547aa45017f01ca",
      "a2d4648245eef6c901ad5ef01bd05776",
      "d2fd0fc81f4bb24f895babec3940441c"
    ],
    "orders": [
      {
        "order_id": "240e00887dd032bf5547aa45017f01ca",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 17422,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 17422,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 17422
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 17422
          },
          {
            "field": "receipt_ids",
            "expected": [
              "167bd1185f2346e87f1de2a1fff95704"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "a2d4648245eef6c901ad5ef01bd05776",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 4,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 12014,
            "actual": 0
          },
          {
            "field": "pending_refund_cents",
            "expected": 4004,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 12014,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 12014
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 12014
          },
          {
            "field": "receipt_ids",
            "expected": [
              "1ec09da77e6e4626aff08dc67ac043e1"
            ],
            "actual": []
          },
          {
            "field": "pending_refund_ids",
            "expected": [
              "f5dd34f5498eed376ebe67b0bee0d5bd"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "d2fd0fc81f4bb24f895babec3940441c",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 5401,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 5401,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 5401
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 5401
          },
          {
            "field": "receipt_ids",
            "expected": [
              "d9852d368685a9e74a642965a8b88560"
            ],
            "actual": []
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": [
      "167bd1185f2346e87f1de2a1fff95704",
      "1ec09da77e6e4626aff08dc67ac043e1",
      "d9852d368685a9e74a642965a8b88560",
      "f5dd34f5498eed376ebe67b0bee0d5bd"
    ]
  },
  "tool_metrics": {
    "executed_calls": 10,
    "successful_calls": 7,
    "tool_errors": 3,
    "tool_success_rate": 0.7,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 3
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 77d7162fc3232d686b084d11504819d3 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "86dd9fde7d21c71a9f37fc9c5605d582"
    ],
    "submitted_order_ids": [
      "86dd9fde7d21c71a9f37fc9c5605d582"
    ],
    "orders": [
      {
        "order_id": "86dd9fde7d21c71a9f37fc9c5605d582",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 5,
    "successful_calls": 4,
    "tool_errors": 1,
    "tool_success_rate": 0.8,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 12a128e47de3108008b89af120c4d872 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": null,
  "submission_present": false,
  "submission_validated": false,
  "failure_reasons": [
    "MISSING_STRUCTURED_SUBMISSION",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.0,
    "matched_fields": 0,
    "total_fields": 35,
    "order_coverage_exact": false,
    "expected_order_ids": [
      "5220db424c855f3dccddf8e697404b3d",
      "6b3deaae63b5c952d0b6b49780f3cb1e",
      "b1016181b88640c419fbaa7552d84f19"
    ],
    "submitted_order_ids": [],
    "orders": [
      {
        "order_id": "5220db424c855f3dccddf8e697404b3d",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 19167,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 19167,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 19167,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "70adaf8ff6c3e09b5a069fb50f1e7fec"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "6b3deaae63b5c952d0b6b49780f3cb1e",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 32087,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 32087,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 32087,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "25ee39c176e22f3d970749dcef349726"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "b1016181b88640c419fbaa7552d84f19",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 58044,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 58044,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 58044,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "986cdcc5f3e6be671096a25094820142"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": null
  },
  "tool_metrics": {
    "executed_calls": 12,
    "successful_calls": 2,
    "tool_errors": 10,
    "tool_success_rate": 0.166667,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 10
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 6f4bb6548af752085cd0d16ac602d440 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.923077,
    "matched_fields": 12,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "d913c273e334e70a8087b7b45919b612"
    ],
    "submitted_order_ids": [
      "d913c273e334e70a8087b7b45919b612"
    ],
    "orders": [
      {
        "order_id": "d913c273e334e70a8087b7b45919b612",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": [
      "cbb3f2161e345c2dcb858f30d89b9269"
    ]
  },
  "tool_metrics": {
    "executed_calls": 6,
    "successful_calls": 3,
    "tool_errors": 3,
    "tool_success_rate": 0.5,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1,
      "TRANSACTION_UNAVAILABLE": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 73345cbf2c62fcbde7e5ebfc212ad29f 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.914286,
    "matched_fields": 32,
    "total_fields": 35,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "600b5b458dee67f0939aa87f1a12002a",
      "ae0bf20391ea71adfe11412ec3c115dd",
      "cc7650e043b6c851a1df8010c94271b5"
    ],
    "submitted_order_ids": [
      "600b5b458dee67f0939aa87f1a12002a",
      "ae0bf20391ea71adfe11412ec3c115dd",
      "cc7650e043b6c851a1df8010c94271b5"
    ],
    "orders": [
      {
        "order_id": "600b5b458dee67f0939aa87f1a12002a",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 10,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "review",
            "expected": false,
            "actual": true
          }
        ]
      },
      {
        "order_id": "ae0bf20391ea71adfe11412ec3c115dd",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 10,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "review",
            "expected": false,
            "actual": true
          }
        ]
      },
      {
        "order_id": "cc7650e043b6c851a1df8010c94271b5",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 10,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "review",
            "expected": false,
            "actual": true
          }
        ]
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 9,
    "successful_calls": 6,
    "tool_errors": 3,
    "tool_success_rate": 0.666667,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 3
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 68296c053f8f16b2ad8a6d0f86b3c06a 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "4527d0527f8b6c29babf732ef029aa9d"
    ],
    "submitted_order_ids": [
      "4527d0527f8b6c29babf732ef029aa9d"
    ],
    "orders": [
      {
        "order_id": "4527d0527f8b6c29babf732ef029aa9d",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 8,
    "successful_calls": 7,
    "tool_errors": 1,
    "tool_success_rate": 0.875,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## d2382b88ade3ed723fda39ea95ad50f5 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.485714,
    "matched_fields": 17,
    "total_fields": 35,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "5a6dcd66c8fd4f0aee2f12ee9f68ac33",
      "6acc43d1ce0c21bd1cd43e99f95f20ce",
      "dfe6aa2032a1365832760c3bcf47decc"
    ],
    "submitted_order_ids": [
      "5a6dcd66c8fd4f0aee2f12ee9f68ac33",
      "6acc43d1ce0c21bd1cd43e99f95f20ce",
      "dfe6aa2032a1365832760c3bcf47decc"
    ],
    "orders": [
      {
        "order_id": "5a6dcd66c8fd4f0aee2f12ee9f68ac33",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 2359,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 2359,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 2359
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 2359
          },
          {
            "field": "receipt_ids",
            "expected": [
              "107994fe184f20884af4272ef2bb7371"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "6acc43d1ce0c21bd1cd43e99f95f20ce",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 4,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 17102,
            "actual": 0
          },
          {
            "field": "refunded_cents",
            "expected": 9975,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 7127,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 17102
          },
          {
            "field": "net_vs_original_cents",
            "expected": 9975,
            "actual": 17102
          },
          {
            "field": "receipt_ids",
            "expected": [
              "007075171111cb011f428f37bfa25c49"
            ],
            "actual": []
          },
          {
            "field": "refund_ids",
            "expected": [
              "1c2b49581db26b0416c385f2008f0b77",
              "846f38eda195b127213799d48ef558bf"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "dfe6aa2032a1365832760c3bcf47decc",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 16260,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 16260,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 16260
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 16260
          },
          {
            "field": "receipt_ids",
            "expected": [
              "d7d3a682c83a87e80384f620de605d9c"
            ],
            "actual": []
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": [
      "007075171111cb011f428f37bfa25c49",
      "107994fe184f20884af4272ef2bb7371",
      "1c2b49581db26b0416c385f2008f0b77",
      "846f38eda195b127213799d48ef558bf",
      "d7d3a682c83a87e80384f620de605d9c"
    ]
  },
  "tool_metrics": {
    "executed_calls": 7,
    "successful_calls": 5,
    "tool_errors": 2,
    "tool_success_rate": 0.714286,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 4ac9079cd1a9a6e4f188c19fbab1a43a 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.846154,
    "matched_fields": 11,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "1a87fc93a7491119fdc87820469fc230"
    ],
    "submitted_order_ids": [
      "1a87fc93a7491119fdc87820469fc230"
    ],
    "orders": [
      {
        "order_id": "1a87fc93a7491119fdc87820469fc230",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 10,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "review",
            "expected": true,
            "actual": false
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [
      "6b9384801d2c2bb580135e4ca91a2121",
      "dc11da847416b81571f9bce3976613bc"
    ],
    "submitted_unallocated_transaction_ids": [
      "0e173912aea18acb668659bbe6839d96"
    ]
  },
  "tool_metrics": {
    "executed_calls": 6,
    "successful_calls": 3,
    "tool_errors": 3,
    "tool_success_rate": 0.5,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1,
      "TRANSACTION_UNAVAILABLE": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## a7e6681e1d9210bd8266050c2521dfda 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "0a140a714da19dab82b4e7495e21de60"
    ],
    "submitted_order_ids": [
      "0a140a714da19dab82b4e7495e21de60"
    ],
    "orders": [
      {
        "order_id": "0a140a714da19dab82b4e7495e21de60",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 4,
    "successful_calls": 3,
    "tool_errors": 1,
    "tool_success_rate": 0.75,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## fb0a91987e06dd6996b831fc7a3d9ed1 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": null,
  "submission_present": false,
  "submission_validated": false,
  "failure_reasons": [
    "MISSING_STRUCTURED_SUBMISSION",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.0,
    "matched_fields": 0,
    "total_fields": 35,
    "order_coverage_exact": false,
    "expected_order_ids": [
      "6e5fcbdfe71bcf65b74fa8f2e108a66b",
      "9e146c0567bc5079e21c5e93f5ce1465",
      "b5b3a42856257c544cfc6e0f25422f49"
    ],
    "submitted_order_ids": [],
    "orders": [
      {
        "order_id": "6e5fcbdfe71bcf65b74fa8f2e108a66b",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 20676,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 20676,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 20676,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "dc7391275c0e6a2c1d2f3477ea1106f9"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "9e146c0567bc5079e21c5e93f5ce1465",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 16379,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 16379,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 5459,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 10920,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 5459,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "ef4521d82d3d522958d51c78de1d1751"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [
              "508e62f51e3f111a7868640522c6d849"
            ],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "b5b3a42856257c544cfc6e0f25422f49",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 15877,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 15877,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 15877,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "602fb8190b981b46171233d20f42bd5e"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": null
  },
  "tool_metrics": {
    "executed_calls": 10,
    "successful_calls": 10,
    "tool_errors": 0,
    "tool_success_rate": 1.0,
    "tool_error_codes": {},
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 035929229afc58f1cf56283b97daecbd 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.538462,
    "matched_fields": 7,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "cb41f218d36fd060d43afa76536cdc65"
    ],
    "submitted_order_ids": [
      "cb41f218d36fd060d43afa76536cdc65"
    ],
    "orders": [
      {
        "order_id": "cb41f218d36fd060d43afa76536cdc65",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 7580,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 7580,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 7581,
            "actual": 15161
          },
          {
            "field": "net_vs_original_cents",
            "expected": 7581,
            "actual": 15161
          },
          {
            "field": "receipt_ids",
            "expected": [
              "74a20e243634e460fe975c4e93f891d0"
            ],
            "actual": []
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": [
      "9bc7d94ec3b5dd9f707d2bdc90a90e06"
    ]
  },
  "tool_metrics": {
    "executed_calls": 6,
    "successful_calls": 3,
    "tool_errors": 3,
    "tool_success_rate": 0.5,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1,
      "TRANSACTION_UNAVAILABLE": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## fe24f5375fed04e7472a53d33c16a262 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.028571,
    "matched_fields": 1,
    "total_fields": 35,
    "order_coverage_exact": false,
    "expected_order_ids": [
      "1460e8ae18cb7b2df4a7a32ea1e2db4c",
      "5001b17327c1070c10b24a596a08dbe5",
      "c786c5b39afb79226a6e795f379ca454"
    ],
    "submitted_order_ids": [],
    "orders": [
      {
        "order_id": "1460e8ae18cb7b2df4a7a32ea1e2db4c",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 13763,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 13763,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 13763,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "480fb7e3b98f7cb2a51fb818fd24e92c"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "5001b17327c1070c10b24a596a08dbe5",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 9117,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 9117,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 9117,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "95d8fa7e24626e44acabf2bbc8a52c26",
              "be67f6bbd234339dca712ee963973e2c"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "c786c5b39afb79226a6e795f379ca454",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 10623,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 10623,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 10623,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "676da56a2dbc134221d1257a2ee6049d"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 11,
    "successful_calls": 9,
    "tool_errors": 2,
    "tool_success_rate": 0.818182,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## ebe4143e309a9a9038e50351c7ab085c 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.846154,
    "matched_fields": 11,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "ac2a107794046da089c19e04a1b40694"
    ],
    "submitted_order_ids": [
      "ac2a107794046da089c19e04a1b40694"
    ],
    "orders": [
      {
        "order_id": "ac2a107794046da089c19e04a1b40694",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 9,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "refund_ids",
            "expected": [],
            "actual": [
              "152580637a3328cbafb6879244a03a36"
            ]
          },
          {
            "field": "review",
            "expected": false,
            "actual": true
          }
        ]
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 6,
    "successful_calls": 5,
    "tool_errors": 1,
    "tool_success_rate": 0.833333,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 6ae2b64ff8bae46b5b50aa337ff5fcd2 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": null,
  "submission_present": false,
  "submission_validated": false,
  "failure_reasons": [
    "MISSING_STRUCTURED_SUBMISSION",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.0,
    "matched_fields": 0,
    "total_fields": 35,
    "order_coverage_exact": false,
    "expected_order_ids": [
      "442cd61d5182798d5c560bed001a7128",
      "6b528198aa9546088698af126dd556a8",
      "eb726c42f6975e880d18f40e0d9c6d58"
    ],
    "submitted_order_ids": [],
    "orders": [
      {
        "order_id": "442cd61d5182798d5c560bed001a7128",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 16833,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 16833,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 16833,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "b6347960ffebbf92a22150cec41fd0a5"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "6b528198aa9546088698af126dd556a8",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 8368,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 8368,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 2789,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 5579,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 2789,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "29ebf96ba5e6b2b89f641e00a386bfd4"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [
              "b96d4d1983ba81f5266fd5063d9d868c"
            ],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "eb726c42f6975e880d18f40e0d9c6d58",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 26484,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 26484,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 26484,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "470dbdd249ee1ec842e225f072ae3c79"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": null
  },
  "tool_metrics": {
    "executed_calls": 12,
    "successful_calls": 8,
    "tool_errors": 4,
    "tool_success_rate": 0.666667,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 4
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## d270f3bb50f36763edbe7164838994a0 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "bb672c3b97c843e1a9bc27d80c3485f7"
    ],
    "submitted_order_ids": [
      "bb672c3b97c843e1a9bc27d80c3485f7"
    ],
    "orders": [
      {
        "order_id": "bb672c3b97c843e1a9bc27d80c3485f7",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 6,
    "successful_calls": 4,
    "tool_errors": 2,
    "tool_success_rate": 0.666667,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## c30f0286048da88d1ed30e915fb97033 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": null,
  "submission_present": false,
  "submission_validated": false,
  "failure_reasons": [
    "MISSING_STRUCTURED_SUBMISSION",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.0,
    "matched_fields": 0,
    "total_fields": 35,
    "order_coverage_exact": false,
    "expected_order_ids": [
      "05568981f684dbdfdbd94387197f09db",
      "12a0a5009450b47b3c0ff605f4ef7d76",
      "4fee26deba424ec67c7ee805f46e67f6"
    ],
    "submitted_order_ids": [],
    "orders": [
      {
        "order_id": "05568981f684dbdfdbd94387197f09db",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 4874,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 4874,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 4874,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "5fe09cc2c3c0069fde39fec0cc1b740b"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "12a0a5009450b47b3c0ff605f4ef7d76",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 5622,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 5622,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 5622,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "37f51234f9f7f451b216d6e350728395"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "4fee26deba424ec67c7ee805f46e67f6",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 10298,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 10298,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 10298,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "7ecf4c42c567e26cd6cb58f8f6a85d3d"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": null
  },
  "tool_metrics": {
    "executed_calls": 12,
    "successful_calls": 3,
    "tool_errors": 9,
    "tool_success_rate": 0.25,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 9
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## eb9a2829dc13548b19b940cb0ae39d0e 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "146173207a53ffefaf12936fa1f12251"
    ],
    "submitted_order_ids": [
      "146173207a53ffefaf12936fa1f12251"
    ],
    "orders": [
      {
        "order_id": "146173207a53ffefaf12936fa1f12251",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 5,
    "successful_calls": 4,
    "tool_errors": 1,
    "tool_success_rate": 0.8,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 884760a57d04feae53a54d836898f65f 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "d26be179d31afe33cbeda59a63e572e7"
    ],
    "submitted_order_ids": [
      "d26be179d31afe33cbeda59a63e572e7"
    ],
    "orders": [
      {
        "order_id": "d26be179d31afe33cbeda59a63e572e7",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 9,
    "successful_calls": 7,
    "tool_errors": 2,
    "tool_success_rate": 0.777778,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 2
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 4c77bf5bb2f45b005286192ffad584f0 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": null,
  "submission_present": false,
  "submission_validated": false,
  "failure_reasons": [
    "MISSING_STRUCTURED_SUBMISSION",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.0,
    "matched_fields": 0,
    "total_fields": 35,
    "order_coverage_exact": false,
    "expected_order_ids": [
      "9c7bbd41dbcd97b7a5f011ac0e9ee4af",
      "a603abe457ff9c944ee0560d19a300af",
      "e506b6f49fdafa04ec3db04a81946ff0"
    ],
    "submitted_order_ids": [],
    "orders": [
      {
        "order_id": "9c7bbd41dbcd97b7a5f011ac0e9ee4af",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 35133,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 35133,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 35133,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "00946efe10473cf6228b4e58431fb1b9"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "a603abe457ff9c944ee0560d19a300af",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 19446,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 19446,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 19446,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "b7d88fd85c323ce19ef801d1e8648391"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      },
      {
        "order_id": "e506b6f49fdafa04ec3db04a81946ff0",
        "submitted": false,
        "exact_match": false,
        "matched_fields": 0,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "expected_cents",
            "expected": 3909,
            "actual": null
          },
          {
            "field": "received_cents",
            "expected": 3909,
            "actual": null
          },
          {
            "field": "refunded_cents",
            "expected": 2280,
            "actual": null
          },
          {
            "field": "pending_refund_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_cents",
            "expected": 1629,
            "actual": null
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": null
          },
          {
            "field": "net_vs_original_cents",
            "expected": 2280,
            "actual": null
          },
          {
            "field": "receipt_ids",
            "expected": [
              "1e33f284ef8a2a4cca32c7bec876088b"
            ],
            "actual": null
          },
          {
            "field": "refund_ids",
            "expected": [
              "5bd168498d170baef08ff3770c1e82b7",
              "7f130a7a445c6adbfc0cb016a627c79d"
            ],
            "actual": null
          },
          {
            "field": "pending_refund_ids",
            "expected": [],
            "actual": null
          },
          {
            "field": "review",
            "expected": false,
            "actual": null
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": null
  },
  "tool_metrics": {
    "executed_calls": 12,
    "successful_calls": 8,
    "tool_errors": 4,
    "tool_success_rate": 0.666667,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 4
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## e4687b3effc9622e2070c12b75a65212 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": true,
  "failure_reasons": [],
  "scores": {
    "plan_exact_match": true,
    "field_accuracy": 1.0,
    "matched_fields": 13,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "e22985eca9017c22e75feca100883540"
    ],
    "submitted_order_ids": [
      "e22985eca9017c22e75feca100883540"
    ],
    "orders": [
      {
        "order_id": "e22985eca9017c22e75feca100883540",
        "submitted": true,
        "exact_match": true,
        "matched_fields": 11,
        "total_fields": 11,
        "mismatches": []
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 6,
    "successful_calls": 5,
    "tool_errors": 1,
    "tool_success_rate": 0.833333,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "boundary",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 7ceb1db6f097025c0d80ec6faff76a88 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.542857,
    "matched_fields": 19,
    "total_fields": 35,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "5409dcaf72eb5aabb706c90e61015a66",
      "59c22ae71b1673a5f0c6bb138645789d",
      "b4b3b4466fcbf99080909ff614905607"
    ],
    "submitted_order_ids": [
      "5409dcaf72eb5aabb706c90e61015a66",
      "59c22ae71b1673a5f0c6bb138645789d",
      "b4b3b4466fcbf99080909ff614905607"
    ],
    "orders": [
      {
        "order_id": "5409dcaf72eb5aabb706c90e61015a66",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 4627,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 4627,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 4627
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 4627
          },
          {
            "field": "receipt_ids",
            "expected": [
              "c2a174a3d07e9c03b598d4415573c5ea"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "59c22ae71b1673a5f0c6bb138645789d",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 37900,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 37900,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 37900
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 37900
          },
          {
            "field": "receipt_ids",
            "expected": [
              "8234c32b1c55556938021e4767447d60"
            ],
            "actual": []
          }
        ]
      },
      {
        "order_id": "b4b3b4466fcbf99080909ff614905607",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 6,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "received_cents",
            "expected": 10226,
            "actual": 0
          },
          {
            "field": "net_cents",
            "expected": 10226,
            "actual": 0
          },
          {
            "field": "collection_gap_cents",
            "expected": 0,
            "actual": 10226
          },
          {
            "field": "net_vs_original_cents",
            "expected": 0,
            "actual": 10226
          },
          {
            "field": "receipt_ids",
            "expected": [
              "0e1cc8638f3d1d72f6c0898a347b274e"
            ],
            "actual": []
          }
        ]
      }
    ],
    "unallocated_exact": false,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": [
      "0e1cc8638f3d1d72f6c0898a347b274e",
      "8234c32b1c55556938021e4767447d60",
      "c2a174a3d07e9c03b598d4415573c5ea"
    ]
  },
  "tool_metrics": {
    "executed_calls": 9,
    "successful_calls": 3,
    "tool_errors": 6,
    "tool_success_rate": 0.333333,
    "tool_error_codes": {
      "TRANSACTION_UNAVAILABLE": 6
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "basic",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```


## 71bf919b9f8768e6932b17b6233317c3 差异明细

```json
{
  "status": "scored",
  "grading_version": "structured-plan-exact-v1",
  "accuracy_definition": "结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。不自动评分中文叙述、证据引用、复核理由及缺失字段说明。",
  "submission_source": "final_json",
  "submission_present": true,
  "submission_validated": false,
  "failure_reasons": [
    "REFERENCE_MISMATCH",
    "RUN_NOT_COMPLETED"
  ],
  "scores": {
    "plan_exact_match": false,
    "field_accuracy": 0.923077,
    "matched_fields": 12,
    "total_fields": 13,
    "order_coverage_exact": true,
    "expected_order_ids": [
      "6ec35ea1eb047624fb828389a8c09c88"
    ],
    "submitted_order_ids": [
      "6ec35ea1eb047624fb828389a8c09c88"
    ],
    "orders": [
      {
        "order_id": "6ec35ea1eb047624fb828389a8c09c88",
        "submitted": true,
        "exact_match": false,
        "matched_fields": 10,
        "total_fields": 11,
        "mismatches": [
          {
            "field": "review",
            "expected": false,
            "actual": true
          }
        ]
      }
    ],
    "unallocated_exact": true,
    "expected_unallocated_transaction_ids": [],
    "submitted_unallocated_transaction_ids": []
  },
  "tool_metrics": {
    "executed_calls": 6,
    "successful_calls": 5,
    "tool_errors": 1,
    "tool_success_rate": 0.833333,
    "tool_error_codes": {
      "INVALID_ARGUMENT": 1
    },
    "validation_calls": 0,
    "last_validation_valid": null,
    "validation_passed": false
  },
  "reference": {
    "split": "val",
    "category": "cross_tool",
    "rule_version": "brl-reconciliation-v1",
    "sha256": "556bbaaafeff8706f02d4ff1dbb8a21178b09d6816a979c586d70f98a19f3253"
  },
  "submission_contract_requested": true,
  "post_run_only": true,
  "natural_language_report_scored": false
}
```

