import os
import pty
import select
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from time import monotonic


SCRIPTS = Path(__file__).resolve().parents[1] / "skills/meta-ads-setup/scripts"


def read_until(terminal, marker):
    output = bytearray()
    deadline = monotonic() + 5
    while marker not in output:
        remaining = deadline - monotonic()
        if remaining <= 0 or not select.select([terminal], [], [], remaining)[0]:
            raise AssertionError(f"Timed out waiting for {marker!r}: {output!r}")
        chunk = os.read(terminal, 8192)
        if not chunk:
            raise AssertionError(f"Terminal closed before {marker!r}: {output!r}")
        output.extend(chunk)
    return output


class TokenInputTest(unittest.TestCase):
    def test_pasted_token_at_maximum_length_is_read_without_echo(self):
        token = b"EA" * 2048
        with tempfile.TemporaryDirectory() as state:
            terminal, slave = pty.openpty()
            process = subprocess.Popen(
                [sys.executable, "-B", "-c", (
                    "from runtime import hidden_input; "
                    "assert hidden_input('Token: ') == 'EA' * 2048; "
                    "print('complete', flush=True)"
                )],
                cwd=SCRIPTS,
                env={**os.environ, "FAPI_META_ADS_STATE_DIR": state},
                stdin=slave,
                stdout=slave,
                stderr=slave,
            )
            os.close(slave)
            try:
                read_until(terminal, b"Token: ")
                with os.fdopen(os.dup(terminal), "wb") as writer:
                    writer.write(token + b"\n")
                output = read_until(terminal, b"complete")
                self.assertNotIn(b"EA" * 16, output)
                self.assertEqual(process.wait(timeout=5), 0)
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait()
                os.close(terminal)
