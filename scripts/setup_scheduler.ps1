# Setup AI Employee Scheduler on Windows Task Scheduler

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "AI Employee Scheduler Setup" -ForegroundColor Cyan
Write-Host "Windows Task Scheduler" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')
if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again"
    exit 1
}
Write-Host "Admin privileges verified" -ForegroundColor Green
Write-Host ""

# Get paths
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonPath = (Get-Command python).Source
$schedulerScript = Join-Path $scriptDir "run_ai_employee.py"

Write-Host "Checking Python installation..."
python --version
Write-Host "✓ Python found" -ForegroundColor Green
Write-Host ""

# Check if scheduler script exists
Write-Host "Checking scheduler script..."
if (-not (Test-Path $schedulerScript)) {
    Write-Host "ERROR: Scheduler script not found at $schedulerScript" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Scheduler script found" -ForegroundColor Green
Write-Host ""

# Health check
Write-Host "Running health check..."
& python $schedulerScript --health
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Health check failed" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Health check passed" -ForegroundColor Green
Write-Host ""

# Check if task already exists
Write-Host "Checking for existing scheduled task..."
$taskExists = Get-ScheduledTask -TaskName "AI Employee Scheduler" -ErrorAction SilentlyContinue
if ($taskExists) {
    Write-Host "Task already exists" -ForegroundColor Yellow
    Write-Host "Removing existing task..."
    Unregister-ScheduledTask -TaskName "AI Employee Scheduler" -Confirm:$false -ErrorAction SilentlyContinue
}
Write-Host ""

# Create scheduled task
Write-Host "Creating Windows Task Scheduler task..."

# Create trigger - every 5 minutes
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 365)

# Create action - run Python script
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "`"$schedulerScript`" --once" -WorkingDirectory $scriptDir

# Create settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable:$false

# Register the task
$task = Register-ScheduledTask -TaskName "AI Employee Scheduler" -Trigger $trigger -Action $action -Settings $settings -RunLevel Highest -Description "AI Employee automatic task scheduler (runs every 5 minutes)"

if ($task) {
    Write-Host "✓ Task created successfully!" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to create task" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Verify task
Write-Host "Verifying scheduled task..."
$verifyTask = Get-ScheduledTask -TaskName "AI Employee Scheduler" -ErrorAction SilentlyContinue
if ($verifyTask) {
    Write-Host "✓ Task verified" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    $verifyTask | Format-List TaskName, State, @{Label='Status';Expression={$_.State}}
} else {
    Write-Host "ERROR: Task verification failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Scheduler is now configured!" -ForegroundColor Green
Write-Host "• Task Name: AI Employee Scheduler" -ForegroundColor Green
Write-Host "• Interval: Every 5 minutes" -ForegroundColor Green
Write-Host "• Status: Running" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Add task files to: AI_Employee\vault\Inbox\" -ForegroundColor Cyan
Write-Host "2. Scheduler will process them automatically" -ForegroundColor Cyan
Write-Host "3. View logs: AI_Employee\scripts\logs\scheduler.log" -ForegroundColor Cyan
Write-Host "4. Check status in Task Scheduler" -ForegroundColor Cyan
Write-Host ""

# Run test
Write-Host "Running initial test..." -ForegroundColor Yellow
& python $schedulerScript --once --verbose

Write-Host ""
Write-Host "Setup and test complete!" -ForegroundColor Green
