# Vault Watcher Skill - BRONZE Tier

## Skill Name
**Vault Watcher**

## Skill Tier
BRONZE (Foundational)

## Description
The Vault Watcher is a lightweight file system monitoring daemon that continuously watches the AI Employee vault Inbox folder for new markdown files. When new files are detected, it logs the detection event and automatically triggers the AI processing workflow without processing duplicate files.

## Core Purpose
Automate the detection and initial processing of new tasks dropped into the vault Inbox, eliminating manual intervention and ensuring consistent, timely processing of incoming work items.

## Key Features

### 1. Continuous Monitoring
- **Watch Folder**: `AI_Employee/vault/Inbox`
- **File Type**: `.md` (Markdown) files only
- **Scan Interval**: 10-30 seconds (configurable)
- **Watch Mode**: Event-based (reacts to file creation in real-time)

### 2. Duplicate Prevention
- Maintains a processed files registry
- Tracks file creation timestamps
- Prevents re-processing of already-handled files
- Registry stored in: `logs/processed_files.json`

### 3. Logging
- **Detection Log**: `logs/actions.log`
- **Processed Registry**: `logs/processed_files.json`
- **Format**: Timestamp, File Name, Action, Status
- **Log Rotation**: Daily rotation at 00:00 UTC
- **Retention**: 30 days of logs

### 4. Workflow Integration
When a new `.md` file is detected:
1. Log file detection with timestamp
2. Record file metadata (size, creation time)
3. Add file to processed registry
4. Trigger AI processing workflow
5. Monitor processing status
6. Log completion status

## Deployment

### Installation
```bash
# Copy watch_inbox.py to scripts/
cp scripts/watch_inbox.py /path/to/project/scripts/

# Set execution permissions
chmod +x scripts/watch_inbox.py

# Verify the script
python scripts/watch_inbox.py --check
```

### Running the Watcher

#### Interactive Mode
```bash
python scripts/watch_inbox.py
```

#### Background Mode
```bash
# Unix/Linux
nohup python scripts/watch_inbox.py > logs/watcher.log 2>&1 &

# Windows (using start /B or Task Scheduler)
python scripts/watch_inbox.py --daemon
```

#### Single Pass Mode
For integration with schedulers or CI/CD:
```bash
python scripts/watch_inbox.py --once
```

### Environment Variables
- `VAULT_ROOT`: Path to vault root (default: `AI_Employee/vault`)
- `LOG_DIR`: Path to logs directory (default: `logs`)
- `CHECK_INTERVAL`: Scan interval in seconds (default: `15`)

### Configuration
Edit `scripts/watch_inbox.py`:

```python
# Configuration section at top of file
VAULT_ROOT = Path("AI_Employee/vault")
INBOX_FOLDER = VAULT_ROOT / "Inbox"
LOG_DIR = Path("logs")
CHECK_INTERVAL = 15  # seconds (10-30 recommended)
```

## Workflow Details

### Detection Process
1. **Scan Phase**: Check Inbox folder for files
2. **Validation Phase**: Filter for `.md` files only
3. **Deduplication Phase**: Check processed registry
4. **Metadata Phase**: Collect file info (name, size, timestamp)
5. **Logging Phase**: Record detection in actions.log
6. **Processing Phase**: Trigger AI workflow
7. **Registry Phase**: Add to processed_files.json

### AI Processing Workflow Trigger
When new file detected, the script:
```
1. Calls orchestrator or AI processor
2. Passes file path to processor
3. Monitors processing status
4. Logs completion/failure
5. Updates registry with result
```

### File Registry Format
```json
{
  "file_name.md": {
    "detected_at": "2026-02-18T10:30:45",
    "size_bytes": 2048,
    "status": "processed",
    "processed_at": "2026-02-18T10:31:02",
    "result": "success"
  }
}
```

### Log Format
```
2026-02-18 10:30:45 [INFO] New file detected: task_001.md (2.0 KB)
2026-02-18 10:30:46 [INFO] Starting AI processing for: task_001.md
2026-02-18 10:31:02 [INFO] Processing complete: task_001.md (status: success)
2026-02-18 10:31:03 [DEBUG] File added to processed registry
```

## Production Readiness Checklist

- [x] Duplicate detection (prevents reprocessing)
- [x] Comprehensive logging
- [x] Error handling with graceful recovery
- [x] Lightweight resource usage
- [x] Configurable scan intervals
- [x] Log rotation support
- [x] Daemon/background mode support
- [x] Single-pass execution support
- [x] Clear status output
- [x] Environment variable support

## Monitoring & Health Checks

### Health Check Command
```bash
python scripts/watch_inbox.py --health
```

### Metrics to Monitor
- Files detected per hour
- Processing success rate
- Average processing time
- Watcher uptime
- Log file size
- Registry file size

### Alert Conditions
- Watcher process dies unexpectedly
- Processing failure rate > 5%
- Log file size exceeds 100MB
- Stale processed registry (no updates in 24 hours)

## Integration with AI Employee System

This skill integrates with:
1. **Orchestrator** (`AI_Employee/orchestrator.py`)
2. **File Triage Skill** (downstream processing)
3. **Task Planner Skill** (downstream processing)
4. **Vault Structure** (Inbox → Needs_Action → Done)

## Troubleshooting

### Issue: "No files detected"
**Check**:
- Is Inbox folder created? `AI_Employee/vault/Inbox/`
- Are you adding `.md` files?
- Check logs for errors
- Verify file system permissions

### Issue: "Files being processed twice"
**Check**:
- Delete or reset `logs/processed_files.json`
- Check registry format
- Verify file timestamps

### Issue: "High CPU usage"
**Solution**:
- Increase `CHECK_INTERVAL` (15-30 seconds recommended)
- Reduce log verbosity
- Check for stuck AI processing

### Issue: "Processing failures"
**Check**:
- Verify AI processor is installed and working
- Check AI processor logs
- Validate file formats
- Check system resources

## Performance Characteristics

- **Memory Usage**: < 50 MB (baseline)
- **CPU Usage**: < 1% idle (event-driven)
- **Disk I/O**: Minimal, only on detection events
- **Startup Time**: < 1 second
- **File Detection Latency**: < 30 seconds (poll interval)

## Security Considerations

- Validates file extensions (`.md` only)
- Runs with same permissions as calling user
- Logs do not contain sensitive file contents
- Registry file contains only metadata
- No external network calls required
- Can be run with restricted file permissions

## Version History

### v1.0 (2026-02-18)
- Initial release
- File detection and logging
- Duplicate prevention
- AI workflow integration
- Production-ready

## Status

**Version**: 1.0
**Tier**: BRONZE
**Status**: READY FOR DEPLOYMENT
**Last Updated**: 2026-02-18

## Related Skills

- **File Triage Skill**: Analyzes detected files
- **Task Planner Skill**: Creates execution plans
- **Filesystem Watcher**: Lower-level monitoring (deprecated in favor of Vault Watcher)

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review logs in `logs/actions.log`
3. Check registry in `logs/processed_files.json`
4. Verify vault folder structure exists
