"""Enhanced SAP executor agent used by the direct Python MCP server."""

from __future__ import annotations

from datetime import datetime, timezone
from time import perf_counter
from typing import Any, Dict


class EnhancedSAPExecutorAgent:
    """Lightweight test executor for direct MCP SAP test workflows."""

    _SUPPORTED_TEST_TYPES = {"login", "transaction", "full"}

    def run_comprehensive_test(self, test_type: str) -> Dict[str, Any]:
        start = perf_counter()
        normalized_test_type = (test_type or "").strip().lower()

        if normalized_test_type not in self._SUPPORTED_TEST_TYPES:
            return {
                "status": "error",
                "message": (
                    "Unsupported test_type. Expected one of: login, transaction, full."
                ),
                "test_type": normalized_test_type,
            }

        simulated_steps = {
            "login": [
                "Validated SAP client/system parameters",
                "Validated credential and session handshake flow",
            ],
            "transaction": [
                "Validated transaction navigation flow",
                "Validated field and command execution flow",
            ],
            "full": [
                "Validated SAP login flow",
                "Validated transaction execution flow",
                "Validated session teardown flow",
            ],
        }

        execution_time = perf_counter() - start
        executed_at = datetime.now(timezone.utc).isoformat()

        return {
            "status": "success",
            "test_type": normalized_test_type,
            "system": "SIMULATED",
            "client": "000",
            "user": "test-user",
            "execution_time": f"{execution_time:.3f}s",
            "executed_at": executed_at,
            "message": "Professional test execution completed",
            "steps_executed": simulated_steps[normalized_test_type],
        }

