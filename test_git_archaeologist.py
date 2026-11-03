import os
import shutil
import subprocess
import tempfile
import unittest

import git_archaeologist as ga


def git(cwd, *args, env=None):
    subprocess.run(["git", "-C", cwd, *args], check=True, capture_output=True,
                   env={**os.environ, **(env or {})})


class GitArchaeologistTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(dir=os.path.dirname(__file__))
        git(self.dir, "init", "-q")
        git(self.dir, "config", "user.email", "t@example.com")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def commit(self, author, name, text):
        git(self.dir, "config", "user.name", author)
        with open(os.path.join(self.dir, name), "a") as f:
            f.write(text)
        git(self.dir, "add", name)
        git(self.dir, "commit", "-q", "-m", "c")

    def test_hotspot_and_bus_factor(self):
        for i in range(4):
            self.commit("Asha", "core.py", f"line {i}\n" * 5)
        self.commit("Ravi", "util.py", "x\n")
        commits = ga.load_commits(self.dir)
        self.assertEqual(len(commits), 5)
        self.assertEqual(ga.hotspots(commits, 1)[0][0], "core.py")
        factor, _, _ = ga.bus_factor(commits)
        self.assertEqual(factor, 1)  # Asha owns almost every changed line
        self.assertIn("Bus factor", ga.render(self.dir, 3))


if __name__ == "__main__":
    unittest.main()
