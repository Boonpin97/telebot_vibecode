from __future__ import annotations

import subprocess
from unittest.mock import MagicMock, patch


def test_kill_venv_python_windows_targets_current_venv_and_skips_self() -> None:
    from ductor_bot.infra import process_tree

    completed = subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout="100\n101\n",
        stderr="",
    )

    with (
        patch.object(process_tree, "_IS_WINDOWS", True),
        patch.object(process_tree.sys, "executable", r"C:\repo\.venv\Scripts\python.exe"),
        patch.object(process_tree.subprocess, "run", return_value=completed) as mock_run,
        patch.object(process_tree, "_run_taskkill") as mock_taskkill,
    ):
        killed = process_tree._kill_venv_python_windows(100)

    assert killed == 1
    mock_taskkill.assert_called_once_with(101, force=True)
    command_text = mock_run.call_args.args[0][-1]
    assert r"c:\repo\.venv\scripts" in command_text.lower()
    assert "*pipx*ductor*" in command_text

