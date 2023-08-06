import subprocess
import tempfile


def test_cli():
    """Test the CLI."""
    # create a temporary directory for the test
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.check_call(
            [
                "dd", "if=/dev/urandom", "of=example.bin", "bs=1M", "count=10",
            ],
            cwd=tmpdir,
        )

        # split the file
        subprocess.check_call(
            [
                "python", "-m", "tally_token", "split", f"{tmpdir}/example.bin",
                f"{tmpdir}/example.bin.1", f"{tmpdir}/example.bin.2", f"{tmpdir}/example.bin.3",
            ],
        )

        # merge the split files
        subprocess.check_call(
            [
                "python", "-m", "tally_token", "merge", f"{tmpdir}/example-merged.bin",
                f"{tmpdir}/example.bin.1", f"{tmpdir}/example.bin.2", f"{tmpdir}/example.bin.3",
            ],
        )

        # check that the original file and the merged file are the same
        subprocess.check_call(
            [
                "diff", "-s", f"{tmpdir}/example.bin", f"{tmpdir}/example-merged.bin",
            ],
        )