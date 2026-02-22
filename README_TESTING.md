# AI Employee System - Testing Guide (Master Index)

Complete guide to testing the AI Employee system and all its skills.

---

## Quick Start (Choose Your Path)

### 🚀 I Have 5 Minutes
**Run:** `QUICK_TEST.bat`

This automated script checks:
- Python environment
- Vault structure
- Skills installed
- Scheduler functional
- All log files

**Result:** Quick pass/fail status

---

### ⚡ I Have 30 Minutes
**Read:** `TESTING_WORKFLOW.md`

Follow one of these paths:
1. **Scheduler Path** (5 min) - Test task detection and planning
2. **Gmail Path** (10 min) - Test email sending
3. **Vault Path** (5 min) - Test file operations
4. **Approval Path** (5 min) - Test human approval workflow
5. **LinkedIn Path** (10 min) - Test LinkedIn posting

---

### 🎯 I Have 1-2 Hours
**Read:** `FULL_TESTING_GUIDE.md`

Comprehensive testing of:
- All 6 components (scheduler, planner, vault, gmail, linkedin, approval)
- Integration between components
- End-to-end workflows
- Error handling and edge cases
- Performance and stress testing
- Complete checklist included

---

### 📊 I Want a Testing Strategy
**Read:** `TESTING_MATRIX.md`

Visual overview of:
- System architecture
- Testing coverage map
- Testing paths and timelines
- Component test matrix
- Success criteria by level
- Troubleshooting decision tree

---

## Documentation Files

### Testing Guides

| File | Purpose | Time | Best For |
|------|---------|------|----------|
| **QUICK_TEST.bat** | Automated basic checks | 5 min | CI/CD pipelines |
| **TESTING_WORKFLOW.md** | Step-by-step practical testing | 30 min | Quick validation |
| **FULL_TESTING_GUIDE.md** | Comprehensive testing coverage | 2 hours | Pre-production |
| **TESTING_MATRIX.md** | Visual strategy and overview | 15 min | Planning tests |
| **README_TESTING.md** | This file - master index | 5 min | Finding info |

### Setup Guides

| File | Purpose |
|------|---------|
| **SETUP_EMAIL_CREDENTIALS.bat** | Set up Gmail for sending emails |
| **HOW_TO_USE_GMAIL_SEND_SKILL.md** | Complete gmail-send guide |
| **GMAIL_SEND_QUICK_START.txt** | Quick start for email sending |
| **EMAIL_TASK_DEMO.txt** | Email task workflow example |

### Skills Documentation

| Skill | Documentation |
|-------|---------------|
| gmail-send | `.claude/skills/gmail-send/SKILL.md` |
| linkedin-post | `.claude/skills/linkedin-post/SKILL.md` |
| vault-file-manager | `.claude/skills/vault-file-manager/SKILL.md` |
| human-approval | `.claude/skills/human-approval/SKILL.md` |
| task-planner | `AI_Employee/scripts/task_planner.py` |

---

## Testing Paths

### Path 1: Quick Smoke Test (5 min)
✓ **For:** Quick validation, CI/CD checks
✓ **Tests:** Basic functionality only
✓ **Command:** `QUICK_TEST.bat`

**Checks:**
- Python installed
- Vault structure exists
- Skills installed
- Scheduler runs without errors
- Registry created

---

### Path 2: Component Testing (30 min)
✓ **For:** Testing individual skills
✓ **Tests:** Each component in isolation
✓ **Follow:** `TESTING_WORKFLOW.md` paths 1-5

**Tests:**
- Scheduler & Task Planner (5 min)
- Gmail-Send Skill (10 min)
- Vault File Manager (5 min)
- Human Approval Skill (5 min)
- LinkedIn-Post Skill (10 min)

---

### Path 3: Integration Testing (1 hour)
✓ **For:** Testing component interactions
✓ **Tests:** How skills work together
✓ **Follow:** `FULL_TESTING_GUIDE.md` Phase 8

**Tests:**
- Scheduler → Task Planner integration
- Planner → Vault File Manager
- Approval → Skills workflow
- Complete end-to-end email campaign

---

### Path 4: Comprehensive Testing (2 hours)
✓ **For:** Pre-production validation
✓ **Tests:** Everything including edge cases
✓ **Follow:** `FULL_TESTING_GUIDE.md` all phases

**Tests:**
- All paths 1-3
- Error handling
- Edge cases
- Stress testing (multiple tasks)
- Long-running stability
- Performance benchmarks

---

### Path 5: Production Monitoring (Ongoing)
✓ **For:** Production stability
✓ **Tests:** Continuous operation
✓ **Commands:** Monitor logs and statistics

**Monitoring:**
- Check scheduler logs daily
- Monitor email delivery logs
- Review error logs
- Track performance metrics
- Verify approvals processed

---

## Component Testing Reference

### Scheduler & Task Planner
```bash
python AI_Employee/scripts/run_ai_employee.py --once --verbose
```
**Tests:** Task detection, plan generation, registry updates

### Vault File Manager
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py ^\
  --action list ^\
  --source Inbox
```
**Tests:** File listing, copying, moving, audit trail

### Gmail-Send
```bash
python .claude/skills/gmail-send/scripts/send_email.py ^\
  --to your.email@gmail.com ^\
  --subject "Test" ^\
  --body "Test message"
```
**Tests:** Email sending, error handling, delivery

### LinkedIn-Post
```bash
python .claude/skills/linkedin-post/scripts/post_linkedin.py ^\
  --message "Test message"
```
**Tests:** Post creation, content verification

### Human-Approval
```bash
python .claude/skills/human-approval/scripts/request_approval.py ^\
  --action "Do something" ^\
  --reason "Testing" ^\
  --timeout 120
```
**Tests:** Approval request, detection, timeout

---

## Testing Status Checklist

### Basic Testing (Must Pass)
- [ ] Python 3.10+ installed
- [ ] All vault folders exist
- [ ] All skill folders exist
- [ ] Scheduler runs
- [ ] Task planner generates plan
- [ ] Plan file created in Needs_Action/
- [ ] Registry file created

### Standard Testing (Should Pass)
- [ ] Email credentials working
- [ ] Email sent successfully
- [ ] Email received in inbox
- [ ] Vault operations work
- [ ] Approval workflow responds
- [ ] LinkedIn credentials set up
- [ ] All logs created

### Full Testing (For Production)
- [ ] Error handling tested
- [ ] Multiple tasks processed
- [ ] Large payloads handled
- [ ] Special characters work
- [ ] Timeouts trigger correctly
- [ ] Recovery from failures works
- [ ] Performance acceptable
- [ ] End-to-end workflow complete
- [ ] Long-running stability verified

---

## Common Testing Scenarios

### Scenario 1: Email Campaign
1. Create task in `vault/Inbox/email_task.md`
2. Run scheduler: detects task
3. Plan generated in `vault/Needs_Action/`
4. Request approval (optional)
5. Send emails using gmail-send skill
6. Move task to `vault/Done/`

**Time:** 15 minutes
**Skills used:** Scheduler, Planner, Gmail-Send, Vault, Approval

### Scenario 2: Feature Request
1. Create task in `vault/Inbox/feature_task.md`
2. Run scheduler: detects and plans
3. Post announcement on LinkedIn
4. Archive in `vault/Done/`

**Time:** 10 minutes
**Skills used:** Scheduler, Planner, LinkedIn-Post, Vault

### Scenario 3: Complete Workflow
1. Setup email credentials
2. Create multiple tasks
3. Run scheduler
4. Process approvals
5. Execute all planned actions
6. Archive completed tasks
7. Review logs

**Time:** 60 minutes
**Skills used:** All

---

## Troubleshooting Guide

### Issue: Scheduler not detecting tasks
```bash
# Check vault structure
dir AI_Employee\vault\Inbox\

# Verify file size (minimum 10 bytes)
dir /-N AI_Employee\vault\Inbox\

# Check for permission issues
# Solution: Delete tiny files, try again
```

### Issue: Email not sending
```bash
# Check credentials
echo %EMAIL_ADDRESS%
echo %EMAIL_PASSWORD%

# Verify app password (not regular password)
# Get from: https://myaccount.google.com/security

# Check logs
type .claude\skills\gmail-send\scripts\logs\actions.log
```

### Issue: LinkedIn posting fails
```bash
# Check credentials
echo %LINKEDIN_EMAIL%
echo %LINKEDIN_PASSWORD%

# Verify 2FA isn't blocking automation
# Check internet connection
```

### Issue: Vault operations not working
```bash
# Check folder permissions
dir AI_Employee\vault\

# Verify file exists
dir AI_Employee\vault\Inbox\filename.md

# Check logs for details
type .claude\skills\vault-file-manager\logs\vault.log
```

---

## Performance Baselines

| Operation | Expected Time | Actual |
|-----------|---------------|--------|
| Scheduler single-pass | <1 sec | _____ |
| Task detection | <0.5 sec | _____ |
| Plan generation | <2 sec | _____ |
| Email send | 3-5 sec | _____ |
| LinkedIn post | 5-10 sec | _____ |
| Vault list | <1 sec | _____ |
| Vault copy | <2 sec | _____ |
| Vault move | <2 sec | _____ |
| Approval request | <1 sec | _____ |

---

## Continuous Integration

### Automated Testing (CI/CD)
```bash
# Run quick test
QUICK_TEST.bat

# Check exit code
if errorlevel 1 (
    echo TESTS FAILED
    exit /b 1
) else (
    echo ALL TESTS PASSED
    exit /b 0
)
```

### Before Deployment Checklist
- [ ] All automated tests pass
- [ ] Manual smoke test passes
- [ ] Email sending verified
- [ ] Vault operations confirmed
- [ ] Approval workflow tested
- [ ] Error logs reviewed
- [ ] No critical issues found

---

## Support & Resources

### Quick Reference
- **Scheduler logs:** `AI_Employee/logs/scheduler.log`
- **Email logs:** `.claude/skills/gmail-send/scripts/logs/actions.log`
- **Vault logs:** `.claude/skills/vault-file-manager/logs/vault.log`
- **Scheduler registry:** `AI_Employee/logs/scheduler_registry.json`

### Email Setup
1. Get Gmail App Password: https://myaccount.google.com/security
2. Run setup: `AI_Employee/SETUP_EMAIL_CREDENTIALS.bat`
3. Test: Send email to yourself
4. Verify: Email arrives in inbox

### LinkedIn Setup
1. Have LinkedIn account
2. Set credentials: `setx LINKEDIN_EMAIL "..."`
3. Test: Post message
4. Verify: Post appears on profile

### Troubleshooting Commands
```bash
# Check Python
python --version

# Check vault
dir AI_Employee\vault\

# Check skills
dir .claude\skills\

# Check logs
type AI_Employee\logs\scheduler.log

# Run scheduler
python AI_Employee/scripts/run_ai_employee.py --once --verbose
```

---

## Next Steps

1. **Choose your testing path** based on available time
2. **Follow the appropriate guide** from the documentation
3. **Record your results** using the provided checklists
4. **Fix any issues** found during testing
5. **Monitor logs** after deployment
6. **Report problems** with clear steps to reproduce

---

## Testing Summary

Your AI Employee system includes:

✅ **4 Production-Ready Skills**
- gmail-send (email sending)
- linkedin-post (social media)
- vault-file-manager (task organization)
- human-approval (approval workflow)

✅ **Automatic Task Processing**
- Scheduler (runs every 5 minutes)
- Task Planner (analyzes requirements)
- Windows Task Scheduler (background execution)

✅ **Comprehensive Testing**
- 4 detailed testing guides
- Automated quick test script
- 30-minute practical workflow
- 2-hour full test suite
- Visual testing matrix

✅ **Complete Documentation**
- Setup guides for each skill
- Quick start guides
- Troubleshooting sections
- Success criteria
- Performance baselines

---

## Getting Started Now

### Option A: Quick Smoke Test (5 min)
```bash
cd E:\GH-Q4\Hackathon0-FTE
QUICK_TEST.bat
```

### Option B: Follow Workflow Guide (30 min)
```bash
# Read the workflow guide
type AI_Employee\TESTING_WORKFLOW.md

# Follow any testing path (1-6)
```

### Option C: Comprehensive Test (2 hours)
```bash
# Read the full guide
type AI_Employee\FULL_TESTING_GUIDE.md

# Follow all 10 phases
```

---

**Testing Guide Version:** 1.0
**Last Updated:** 2026-02-18
**Status:** Ready for Testing
**Location:** `E:\GH-Q4\Hackathon0-FTE\AI_Employee\`

---

## Document Index

| Guide | Purpose | Time |
|-------|---------|------|
| README_TESTING.md | This file - master index | 5 min |
| QUICK_TEST.bat | Automated basic tests | 5 min |
| TESTING_WORKFLOW.md | Step-by-step practical tests | 30 min |
| FULL_TESTING_GUIDE.md | Comprehensive test suite | 2 hours |
| TESTING_MATRIX.md | Visual strategy overview | 15 min |

---

## Questions?

Refer to the specific guide for your use case:
- **Quick validation?** → Use `QUICK_TEST.bat`
- **Learning how to test?** → Read `TESTING_WORKFLOW.md`
- **Complete coverage?** → Read `FULL_TESTING_GUIDE.md`
- **Understanding strategy?** → Read `TESTING_MATRIX.md`
- **Specific component?** → Search in `FULL_TESTING_GUIDE.md` Phase 3-9

**Status: All testing documentation complete and ready to use.**
