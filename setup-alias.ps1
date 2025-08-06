# JSearch Alias Setup Script for Windows PowerShell
# This script helps set up global functions for jsearch in PowerShell

Write-Host "JSearch Alias Setup (PowerShell)" -ForegroundColor Blue
Write-Host "=================================" -ForegroundColor Blue

# Check execution policy
$executionPolicy = Get-ExecutionPolicy
Write-Host "Current execution policy: $executionPolicy"

if ($executionPolicy -eq "Restricted") {
    Write-Host "WARNING: PowerShell execution policy is Restricted" -ForegroundColor Yellow
    Write-Host "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    $setPolicyChoice = Read-Host "Would you like to set the execution policy now? (y/N)"
    if ($setPolicyChoice -match '^[Yy]') {
        try {
            Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
            Write-Host "Execution policy updated successfully" -ForegroundColor Green
        }
        catch {
            Write-Host "ERROR: Failed to update execution policy: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "Please run as administrator or manually set the policy" -ForegroundColor Yellow
        }
    }
}

# Get the current directory (jsearch project directory)
$JSearchDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Host "JSearch directory: $JSearchDir"

# Check if PowerShell profile exists
if (!(Test-Path -Path $PROFILE)) {
    Write-Host "Creating PowerShell profile..." -ForegroundColor Yellow
    New-Item -ItemType File -Path $PROFILE -Force | Out-Null
}

Write-Host "PowerShell profile: $PROFILE"

# Check if functions already exist
$profileContent = Get-Content -Path $PROFILE -ErrorAction SilentlyContinue
if ($profileContent -and ($profileContent -match "function jsearch")) {
    Write-Host "WARNING: JSearch functions already exist in PowerShell profile" -ForegroundColor Yellow
    Write-Host "Please remove existing functions before running this script." -ForegroundColor Yellow
    exit 1
}

# Add functions to profile
Write-Host ""
Write-Host "Adding functions to PowerShell profile..." -ForegroundColor Green

$functionsToAdd = @"

# JSearch functions (added by setup-alias.ps1)
function jsearch { python "$JSearchDir\jsearch.py" `$args }
function jsearch-cli { python "$JSearchDir\cli.py" `$args }
"@

Add-Content -Path $PROFILE -Value $functionsToAdd

Write-Host "SUCCESS: Functions added successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the functions in your current session, run:" -ForegroundColor Cyan
Write-Host ". `$PROFILE" -ForegroundColor White
Write-Host ""
Write-Host "After that, you can use jsearch from anywhere:" -ForegroundColor Green
Write-Host "jsearch -u example.com" -ForegroundColor White
Write-Host "jsearch-cli --check-tools" -ForegroundColor White
Write-Host ""

# Ask if user wants to reload now
$reload = Read-Host "Would you like to reload your PowerShell profile now? (y/N)"
if ($reload -match '^[Yy]') {
    Write-Host "Reloading PowerShell profile..." -ForegroundColor Cyan
    try {
        . $PROFILE
        Write-Host "SUCCESS: Profile reloaded!" -ForegroundColor Green
        Write-Host ""
        Write-Host "JSearch is now available globally!" -ForegroundColor Green
        Write-Host "Try: jsearch --help" -ForegroundColor White
    }
    catch {
        Write-Host "ERROR: Error reloading profile: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Please restart PowerShell to use the new functions." -ForegroundColor Yellow
    }
}
else {
    Write-Host "REMINDER: Run '. `$PROFILE' to activate the functions." -ForegroundColor Cyan
    Write-Host "Or restart PowerShell for the changes to take effect." -ForegroundColor Cyan
}
