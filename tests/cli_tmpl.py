# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


from contextlib import redirect_stdout
import io
import os
from progshot.cli import CLI
import subprocess
import sys
import unittest


class CLITestCase(unittest.TestCase):
    def __init__(self, infile):
        self.infile = infile
        super().__init__()
        self.commands = []
        self.checks = {}

    def command(self, cmd):
        self.commands.append(cmd)

    def _add_check(self, check):
        cmd_idx = len(self.commands)
        if cmd_idx not in self.checks:
            self.checks[cmd_idx] = []
        self.checks[cmd_idx].append(check)

    def check_in(self, s):
        self._add_check({"type": "in", "args": s})

    def check_not_in(self, s):
        self._add_check({"type": "notin", "args": s})

    def check_true(self, func):
        self._add_check({"type": "true", "args": func})

    def run(self):
        stdin = sys.stdin
        self.commands.append("q\n")
        sys.stdin = io.StringIO("\n".join(self.commands))
        cli = CLI(self.infile, enable_rich=False)
        with io.StringIO() as buf, redirect_stdout(buf):
            cli.run()
            result = buf.getvalue()
            self.do_checks(result)
        sys.stdin = stdin

    def do_checks(self, result):
        outputs = result.split(">>>")
        for idx, output in enumerate(outputs):
            if idx in self.checks:
                for check in self.checks[idx]:
                    self.do_check(output, check)

    def do_check(self, output, check):
        if check["type"] == "in":
            self.assertIn(check["args"], output)
        elif check["type"] == "notin":
            self.assertNotIn(check["args"], output)
        elif check["type"] == "true":
            self.assertTrue(check["args"](output))
        else:
            raise ValueError("Unknown Check!")


class CLITmpl(unittest.TestCase):
    def run_cmd(self, cmd):
        if os.getenv("COVERAGE_RUN"):
            if "python" in cmd[0]:
                cmd = ["coverage", "run", "--parallel-mode", "--pylib"] + cmd[1:]
            elif cmd[0] == "psview":
                cmd = ["coverage", "run", "--parallel-mode", "--pylib", "-m", "progshot.cli"] + cmd[1:]

    def generate_progshot(self, infile):
        if os.getenv("COVERAGE_RUN"):
            cmd = ["coverage", "run", "--parallel-mode", "--pylib", infile]
        else:
            cmd = ["python", infile]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=30)
        self.assertEqual(result.returncode, 0)

    def create_test(self, infile):
        return CLITestCase(infile)
