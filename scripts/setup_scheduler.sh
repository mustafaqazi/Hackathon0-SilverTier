#!/bin/bash
# setup_scheduler.sh - Easy scheduler setup for Linux/Mac

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}AI Employee Scheduler Setup${NC}"
echo -e "${BLUE}Linux/Mac Version${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Check Python
echo -e "${YELLOW}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 not found${NC}"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"
echo ""

# Check scheduler script
echo -e "${YELLOW}Checking scheduler script...${NC}"
if [ ! -f "$SCRIPT_DIR/run_ai_employee.py" ]; then
    echo -e "${RED}✗ Scheduler script not found at $SCRIPT_DIR/run_ai_employee.py${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Scheduler script found${NC}"
echo ""

# Make script executable
echo -e "${YELLOW}Making script executable...${NC}"
chmod +x "$SCRIPT_DIR/run_ai_employee.py"
echo -e "${GREEN}✓ Script is executable${NC}"
echo ""

# Test run
echo -e "${YELLOW}Running health check...${NC}"
python3 "$SCRIPT_DIR/run_ai_employee.py" --health
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Health check failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Health check passed${NC}"
echo ""

# Get current crontab
echo -e "${YELLOW}Checking for existing cron job...${NC}"
CRON_ENTRY="*/5 * * * * cd $SCRIPT_DIR && python3 run_ai_employee.py --once >> logs/cron.log 2>&1"

if crontab -l 2>/dev/null | grep -q "run_ai_employee"; then
    echo -e "${YELLOW}⚠ Cron job already exists${NC}"
    read -p "Replace existing cron job? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Remove old job and add new one
        (crontab -l 2>/dev/null | grep -v "run_ai_employee"; echo "$CRON_ENTRY") | crontab -
        echo -e "${GREEN}✓ Cron job updated${NC}"
    else
        echo "Setup cancelled"
        exit 0
    fi
else
    # Add new cron job
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo -e "${GREEN}✓ Cron job added${NC}"
fi
echo ""

# Verify cron job
echo -e "${YELLOW}Verifying cron job...${NC}"
if crontab -l 2>/dev/null | grep -q "run_ai_employee"; then
    echo -e "${GREEN}✓ Cron job verified${NC}"
else
    echo -e "${RED}✗ Failed to add cron job${NC}"
    exit 1
fi
echo ""

# Show cron job
echo -e "${BLUE}Current cron job:${NC}"
crontab -l 2>/dev/null | grep "run_ai_employee"
echo ""

# Options menu
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Setup Complete!${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo "Options:"
echo "1. View logs"
echo "2. Test scheduler"
echo "3. Show cron job"
echo "4. Edit cron job"
echo "5. Disable scheduler"
echo "6. Exit"
echo ""

read -p "Enter choice (1-6): " choice

case $choice in
    1)
        echo -e "${BLUE}=== Scheduler Log ====${NC}"
        if [ -f "$SCRIPT_DIR/logs/scheduler.log" ]; then
            tail -20 "$SCRIPT_DIR/logs/scheduler.log"
        else
            echo "No log file yet (will be created on first run)"
        fi
        ;;
    2)
        echo -e "${BLUE}=== Running Test ====${NC}"
        python3 "$SCRIPT_DIR/run_ai_employee.py" --once --verbose
        ;;
    3)
        echo -e "${BLUE}=== Current Cron Job ====${NC}"
        crontab -l 2>/dev/null | grep "run_ai_employee"
        ;;
    4)
        echo -e "${BLUE}=== Editing Cron Job ====${NC}"
        crontab -e
        ;;
    5)
        echo -e "${YELLOW}Disabling scheduler...${NC}"
        (crontab -l 2>/dev/null | sed '/run_ai_employee/s/^/# /') | crontab -
        echo -e "${GREEN}✓ Scheduler disabled${NC}"
        echo "To enable: crontab -e and remove the # from the line"
        ;;
    6)
        echo "Exiting"
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
