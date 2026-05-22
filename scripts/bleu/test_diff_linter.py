import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diff_linter.py")


class TestDiffLinterCLI(unittest.TestCase):
    def test_json_format_does_not_crash(self):
        """--format json must produce valid JSON, not NameError (regression: missing import json)."""
        with tempfile.TemporaryDirectory() as tmp:
            ap_dir = os.path.join(tmp, "blueprint", "action-points")
            os.makedirs(ap_dir)
            with open(os.path.join(ap_dir, "AP-01-example.md"), "w", encoding="utf-8") as f:
                f.write("# AP-01\n\n## Depends on\nNone\n")

            result = subprocess.run(
                [sys.executable, SCRIPT,
                 "--files", "blueprint/action-points/AP-01-example.md",
                 "--format", "json"],
                cwd=tmp, capture_output=True, text=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            parsed = json.loads(result.stdout)
            self.assertIsInstance(parsed, list)

    def test_json_format_empty_is_valid_array(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "blueprint"))
            result = subprocess.run(
                [sys.executable, SCRIPT, "--files", "blueprint/missing.md", "--format", "json"],
                cwd=tmp, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            json.loads(result.stdout)


if __name__ == "__main__":
    unittest.main()
