from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TradingAgentArticleGapAuditTests(unittest.TestCase):
    def test_article_gap_audit_names_done_partial_and_blocked_items(self):
        text = (ROOT / "docs" / "ops" / "trading-agent-article-gap-audit.md").read_text(encoding="utf-8")
        for marker in [
            "Install a Codex trading skill",
            "Use plain language to define trading style",
            "Five-dimensional signal system",
            "Upload/pair with Moss platform",
            "Generate Hyperliquid agent wallet",
            "Copy-trade execution",
            "Safe Next Backlog",
            "Execution-Lane Blockers",
        ]:
            self.assertIn(marker, text)
        self.assertIn("walletAuthorizationAllowed=false", text)
        self.assertIn("copyTradeExecutionAllowed=false", text)


if __name__ == "__main__":
    unittest.main()
