param([switch]$Apply)
$ErrorActionPreference = 'Stop'
$taskPython = Get-Command python -ErrorAction SilentlyContinue | Where-Object Source -NotMatch 'WindowsApps'
if ($taskPython) {
    $taskPythonPath = $taskPython.Source
} else {
    $taskPythonPath = Get-ChildItem -LiteralPath (Join-Path $HOME '.workbuddy/binaries/python/versions') -Filter python.exe -Recurse -ErrorAction SilentlyContinue |
        Sort-Object FullName -Descending | Select-Object -First 1 -ExpandProperty FullName
}
if (-not $taskPythonPath) { throw 'Python 3 unavailable. Install Python 3 or run sync.py with an existing interpreter.' }
$taskArgs = @((Join-Path $PSScriptRoot 'sync.py'))
if ($Apply) { $taskArgs += '--apply' }
& $taskPythonPath @taskArgs
if ($LASTEXITCODE -ne 0) { throw "AgentKit sync failed: $LASTEXITCODE" }
