@echo off
REM AI Employee Scheduler - Windows Task Scheduler Runner
setlocal
cd /d "E:\GH-Q4\Hackathon0-FTE\AI_Employee\scripts\"
python run_ai_employee.py --once --interval 300
exit /b %ERRORLEVEL%
