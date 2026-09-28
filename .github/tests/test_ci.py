"""Behavior tests for CI filtering and the migrated validators (stdlib only)."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("ci_changes", ROOT / ".github/scripts/ci-changes.py")
changes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(changes)


class ChangeDetectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        previous = os.getcwd()
        os.chdir(self.temp.name)
        self.addCleanup(os.chdir, previous)
        self.git("init", "-q")
        self.git("config", "user.name", "CI Test")
        self.git("config", "user.email", "ci@example.invalid")
        Path("README.md").write_text("Initial\n")
        Path("App.swift").write_text("// Source\n")
        self.base = self.commit()

    def git(self, *args):
        return subprocess.check_output(["git", *args], stderr=subprocess.DEVNULL).decode().strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD")

    def test_documentation_only(self):
        Path("README.md").write_text("Updated\n")
        self.assertEqual(changes.selected_checks("pull_request", self.base, self.commit()),
                         {"ios": False, "docs": True, "config": False})

    def test_ios_only_skips_docs_and_config(self):
        Path("App.swift").write_text("// Changed source\n")
        self.assertEqual(changes.selected_checks("pull_request", self.base, self.commit()),
                         {"ios": True, "docs": False, "config": False})

    def test_detector_writes_workflow_outputs(self):
        Path("README.md").write_text("Updated\n")
        head = self.commit()
        output = Path("outputs.txt").resolve()
        subprocess.run(
            ["python3", str(ROOT / ".github/scripts/ci-changes.py")], check=True,
            capture_output=True,
            env={**os.environ, "EVENT_NAME": "pull_request", "BASE_SHA": self.base,
                 "HEAD_SHA": head, "GITHUB_OUTPUT": str(output)},
        )
        self.assertEqual(output.read_text().splitlines(),
                         ["should-run-ios=false", "should-run-docs=true", "should-run-config=false"])

    def test_mixed_changes_run_ios_and_docs(self):
        Path("App.swift").write_text("// Changed source\n")
        Path("README.md").write_text("Updated\n")
        self.assertEqual(changes.selected_checks("pull_request", self.base, self.commit()),
                         {"ios": True, "docs": True, "config": False})

    def test_validator_changes_run_docs_and_config(self):
        path = Path(".github/scripts/validate-markdown.rb")
        path.parent.mkdir(parents=True)
        path.write_text("# Changed validator\n")
        checks = changes.selected_checks("pull_request", self.base, self.commit())
        self.assertTrue(checks["docs"])
        self.assertTrue(checks["config"])

    def test_code_configuration_and_unknown_files(self):
        for path in ["App/Test.swift", "Resources/icon.png", "Resources/help.md", "Package.swift", "Package.resolved",
                     "Scout.xcodeproj/project.pbxproj", "Tests/test.swift", "Makefile",
                     "scripts/select-simulator.py", ".github/workflows/ios.yml", "unknown.file"]:
            with self.subTest(path=path):
                file = Path(path)
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text("fixture\n")
                head = self.commit()
                self.assertTrue(changes.should_run("push", self.base, head))
                self.base = head

    def test_deleted_source(self):
        Path("App.swift").unlink()
        self.assertTrue(changes.should_run("pull_request", self.base, self.commit()))

    def test_source_renamed_to_documentation(self):
        Path("App.swift").rename("App.md")
        self.assertTrue(changes.should_run("pull_request", self.base, self.commit()))

    def test_deleted_documentation(self):
        Path("README.md").unlink()
        self.assertFalse(changes.should_run("push", self.base, self.commit()))

    def test_manual_and_missing_baselines_run(self):
        expected = {"ios": True, "docs": True, "config": True}
        self.assertEqual(changes.selected_checks("workflow_dispatch", self.base, self.base), expected)
        for base in ["", "0" * 40, "f" * 40]:
            self.assertEqual(changes.selected_checks("push", base, self.base), expected)


class ValidatorTests(unittest.TestCase):
    def validate(self, kind, path, content):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".github").mkdir()
            shutil.copy(ROOT / f".github/{kind}-validation.yml", root / ".github")
            file = root / path
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(content)
            return subprocess.run(
                ["ruby", str(ROOT / f".github/scripts/validate-{kind}.rb")],
                cwd=root, capture_output=True,
            )

    def test_markdown_passes_valid_fences(self):
        result = self.validate("markdown", ".github/CI.md", b"# CI\n\n```sh\nmake test\n```\n")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_markdown_rejects_invalid_content(self):
        for content in [b"# Bad\n\xff", b"<<<<<<< HEAD\n", b"```swift\nunfinished\n"]:
            with self.subTest(content=content):
                self.assertNotEqual(self.validate("markdown", "docs/guide.md", content).returncode, 0)

    def test_yaml_passes_workflow_and_reusable_job(self):
        content = b"name: Test\non: push\njobs:\n  test:\n    uses: owner/repo/.github/workflows/test.yml@main\n"
        result = self.validate("yaml", ".github/workflows/test.yml", content)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_yaml_rejects_syntax_and_missing_workflow_fields(self):
        for content in [b"name: [broken", b"name: Test\non: push\n",
                        b"name: Test\non: push\njobs:\n  test:\n    steps: []\n"]:
            with self.subTest(content=content):
                self.assertNotEqual(self.validate("yaml", ".github/workflows/test.yml", content).returncode, 0)


if __name__ == "__main__":
    unittest.main()
