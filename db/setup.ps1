# Run this once to initialize the SQLite database
# Requires sqlite3.exe — download from https://sqlite.org/download.html

$dbPath = "$PSScriptRoot\leads.db"
$initSql = "$PSScriptRoot\init.sql"

sqlite3.exe $dbPath ".read $initSql"
Write-Host "Database initialized at: $dbPath"
