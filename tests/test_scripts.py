from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
BOOTSTRAP = REPO / ".claude/skills/sdd-main/bootstrap.sh"
SYNC = REPO / ".opencode/sync-agents.sh"


class ScriptTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory(prefix="sdd checks ")
        self.addCleanup(scratch.cleanup)
        self.project = Path(scratch.name)
        subprocess.run(
            ["git", "init", "--quiet", "--initial-branch=checks", str(self.project)],
            check=True,
        )

    def run_bash(self, *args):
        result = subprocess.run(
            ["bash", *map(str, args)],
            cwd=self.project,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def prepare_sync(self):
        shutil.copytree(REPO / ".claude/agents", self.project / ".claude/agents")
        (self.project / ".opencode/agents").mkdir(parents=True)
        script = self.project / ".opencode/sync-agents.sh"
        shutil.copy2(SYNC, script)
        return script

    def test_bootstrap_initializes_artifacts_without_permissions(self):
        self.run_bash(BOOTSTRAP)
        self.assertEqual(
            {path.name for path in self.project.iterdir()},
            {".git", ".ai", "docs", "tickets"},
        )
        for name in ("docs/briefs", "docs/specs", "docs/adrs", "tickets"):
            with self.subTest(path=name):
                self.assertTrue((self.project / name).is_dir())
        self.assertTrue((self.project / "docs/CONTEXT.md").is_file())
        self.assertEqual(
            (self.project / ".ai/PROJECT_STATE.md").read_text(),
            """goal: null
feature: null
context: docs/CONTEXT.md
brief: null
spec: null
tickets_index: null
active_ticket: null
base_sha: null
head_sha: null
review: null
review_round: 0
blockers: []
next_action: run sizing / discovery for the current request
""",
        )

    def test_bootstrap_is_idempotent(self):
        self.run_bash(BOOTSTRAP)
        before = {
            path.relative_to(self.project): path.read_bytes()
            for path in self.project.rglob("*")
            if path.is_file()
        }
        self.run_bash(BOOTSTRAP)
        after = {
            path.relative_to(self.project): path.read_bytes()
            for path in self.project.rglob("*")
            if path.is_file()
        }
        self.assertEqual(after, before)

    def test_bootstrap_preserves_existing_files(self):
        originals = {
            ".ai/PROJECT_STATE.md": b"active_ticket: 02\nreview_round: 2\n",
            "docs/CONTEXT.md": b"# Existing context\n",
            ".claude/settings.json": b'{"permissions":{"deny":["Bash(*)"]}}\n',
            ".claude/settings.local.json": b'{"permissions":{"allow":["Read"]}}\n',
            ".codex/config.toml": b'approval_policy = "on-request"\n',
            ".opencode/opencode.jsonc": b'{"permissions":[]}\n',
            "notes.txt": b"User notes\n",
        }
        for name, content in originals.items():
            path = self.project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        for _ in range(2):
            self.run_bash(BOOTSTRAP)
            for name, content in originals.items():
                with self.subTest(path=name):
                    self.assertEqual((self.project / name).read_bytes(), content)

    def test_bootstrap_preserves_local_only_permissions(self):
        local = self.project / ".claude/settings.local.json"
        local.parent.mkdir()
        original = b'{"permissions":{"deny":["Bash(*)"]}}\n'
        local.write_bytes(original)
        self.run_bash(BOOTSTRAP)
        self.assertEqual(local.read_bytes(), original)
        self.assertFalse((local.parent / "settings.json").exists())

    def test_shell_syntax(self):
        for script in (BOOTSTRAP, SYNC):
            with self.subTest(script=script.name):
                self.run_bash("-n", script)

    def test_generated_profiles_are_current(self):
        self.run_bash(self.prepare_sync())
        generated = self.project / ".opencode/agents"
        tracked = REPO / ".opencode/agents"
        expected = {path.name for path in (REPO / ".claude/agents").glob("*.md")}
        self.assertEqual({path.name for path in generated.glob("*.md")}, expected)
        self.assertEqual({path.name for path in tracked.glob("*.md")}, expected)
        for name in expected:
            with self.subTest(agent=name):
                self.assertEqual(
                    (generated / name).read_bytes(), (tracked / name).read_bytes()
                )

    def test_sync_uses_updated_source_and_keeps_reviewer_restriction(self):
        script = self.prepare_sync()
        for name in ("sdd-planner", "sdd-implementer", "sdd-reviewer"):
            (self.project / f".claude/agents/{name}.md").write_text(
                f"---\nname: {name}\ndescription: Updated {name}\ntools: Read\n"
                f"---\n\n# Updated {name}\n"
            )
        self.run_bash(script)
        for name in ("sdd-planner", "sdd-implementer", "sdd-reviewer"):
            restriction = (
                'permissions:\n  - action: edit\n    resource: "*"\n    effect: deny\n'
                if name == "sdd-reviewer"
                else ""
            )
            with self.subTest(agent=name):
                self.assertEqual(
                    (self.project / f".opencode/agents/{name}.md").read_text(),
                    f"---\ndescription: Updated {name}\nmode: subagent\n"
                    f"{restriction}---\n\n# Updated {name}\n",
                )
