$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$env:PYTHONUTF8 = "1"

if (-not (Test-Path $venvPython)) {
  throw "Missing virtualenv Python at $venvPython"
}

& $venvPython -m ductor_bot service install
& $venvPython -m ductor_bot service start
