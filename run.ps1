# Load .env and run the MuleSoft app
$envFile = "$PSScriptRoot\.env"

if (-not (Test-Path $envFile)) {
    Write-Error ".env file not found. Copy .env.example to .env and fill in your credentials."
    exit 1
}

# Parse .env into environment variables
Get-Content $envFile | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]+)=(.+)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process')
        Write-Host "Loaded: $($matches[1].Trim())"
    }
}

Write-Host "`nStarting Salesforce CDC flow..."
Set-Location $PSScriptRoot
mvn mule:run
