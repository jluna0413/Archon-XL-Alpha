<#
dev-start.ps1
Small helper to start mock-archon detached, verify MCP handshake and health_check.
Usage:
  - From repo root: .\dev-start.ps1           # starts mock and verifies
  - To add hosts entry (requires elevated PowerShell): .\dev-start.ps1 -AddHosts
#>
param(
    [switch]$AddHosts
)

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$mockDir = Join-Path $scriptRoot 'mock-archon'
if (-not (Test-Path $mockDir)) {
    Write-Error "mock-archon directory not found at $mockDir"
    exit 1
}

# Preferred ports (user-specified)
$env:PORT = $env:ARCHON_MCP_PORT -or '8054'

# Start mock detached and print PID
try {
    $proc = Start-Process -FilePath 'node' -ArgumentList 'server.js' -WorkingDirectory $mockDir -WindowStyle Hidden -PassThru
    Write-Output "Started mock-archon PID=$($proc.Id) (working dir: $mockDir)"
} catch {
    Write-Error "Failed to start mock server: $_"
    exit 1
}

# Wait for handshake to become available
$maxAttempts = 12
$attempt = 0
$handshakeUrl = "http://127.0.0.1:$($env:PORT)/mcp"
while ($attempt -lt $maxAttempts) {
    try {
        $resp = Invoke-RestMethod -Uri $handshakeUrl -Method Get -TimeoutSec 2
        Write-Output "Handshake OK (attempt $($attempt+1))"
        break
    } catch {
        Start-Sleep -Seconds 1
        $attempt++
    }
}
if ($attempt -ge $maxAttempts) {
    Write-Error "Mock did not respond at $handshakeUrl after $maxAttempts attempts. Check process logs or ports."
    Write-Output "To stop: Stop-Process -Id $($proc.Id)"
    exit 2
}

# JSON-RPC health_check
try {
    $body = @{ jsonrpc='2.0'; id=1; method='health_check'; params=@{} } | ConvertTo-Json -Compress
    $res = Invoke-RestMethod -Uri $handshakeUrl -Method Post -Body $body -ContentType 'application/json' -TimeoutSec 5
    Write-Output "health_check response:`n$($res | ConvertTo-Json -Depth 5)"
} catch {
    Write-Error "health_check failed: $_"
}

# Optional: add hosts entry for archon-xl -> 127.0.0.1 (requires admin)
if ($AddHosts) {
    $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $isAdmin) {
        Write-Warning 'Add-Hosts requires an elevated PowerShell. Re-run in an Administrator session.'
    } else {
        $hostsFile = 'C:\Windows\System32\drivers\etc\hosts'
        $entry = '127.0.0.1 archon-xl'
        if (-not (Select-String -Path $hostsFile -Pattern '^[ \t]*127\.0\.0\.1[ \t]+archon-xl' -Quiet)) {
            Add-Content -Path $hostsFile -Value $entry
            Write-Output 'Added hosts entry: 127.0.0.1 archon-xl'
        } else {
            Write-Output 'hosts entry already present.'
        }
    }
}

Write-Output "dev-start completed. To stop the mock: Stop-Process -Id $($proc.Id)"
