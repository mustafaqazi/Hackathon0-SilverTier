# AI Employee Reasoning Workflow

## Workflow Overview

When a new task appears in `vault/Inbox/`, this workflow executes automatically to create a detailed plan without executing the task.

---

## Workflow Steps

### Step 1: Monitor Inbox
- Check `AI_Employee/vault/Inbox/` for new files
- Identify markdown task files (`.md` extension)
- Exclude documentation and system files

### Step 2: Read the Task
- Open the task file
- Extract task title/subject
- Read complete description and requirements
- Note any deadlines, priorities, or constraints
- Identify related files or dependencies

### Step 3: Create Detailed Plan File
- Generate filename: `Plan_<YYYY-MM-DD_HHmmss>.md`
- Location: `AI_Employee/vault/Needs_Action/Plan_<timestamp>.md`
- Proceed to next section for format

### Step 4: Output Confirmation
- Log plan file creation
- Display plan filename and path
- Mark task as "planned" (do NOT execute)

---

## Plan File Format

### File Naming
```
Plan_2026-02-18_143022.md
     └─ Timestamp format: YYYY-MM-DD_HHmmss
```

### Plan Structure

```markdown
# Task Plan

## Original Task
[Full original task text, exactly as read from Inbox]

## Objective
[Clear, single sentence stating what must be accomplished]

## Step-by-Step Plan

1. [First action]
   - Details or sub-steps

2. [Second action]
   - Details or sub-steps

3. [Third action]
   - Details or sub-steps

[Continue for each major step]

## Priority
- **Level**: HIGH / MEDIUM / LOW
- **Reasoning**: [Why this priority level?]

## Requires Human Approval?
- **Answer**: Yes / No
- **If Yes, Why?**: [Explain what decisions need human input]
- **Decision Points**: [List specific items needing approval]

## Suggested Output
- **Expected Deliverable**: [What will be produced?]
- **Success Criteria**: [How to verify completion]
- **Estimated Effort**: [Time/complexity estimate]
```

---

## Example Plan File

```markdown
# Task Plan

## Original Task
Update the login button styling to match the design system. Get the exact color codes from Figma. This is blocking the designer from continuing work on the authentication flow.

## Objective
Update login button CSS to match design system colors from Figma specifications.

## Step-by-Step Plan

1. Access and review Figma design file
   - Open Figma link
   - Locate login button design specs
   - Document color codes (hex, RGB)
   - Note typography and spacing

2. Locate button styling code
   - Find button component file (likely /components/Button.tsx or /styles/button.css)
   - Review current styling
   - Identify selectors for login button

3. Update color values
   - Replace old color codes with new values from Figma
   - Ensure consistency with design tokens
   - Test on light and dark backgrounds

4. Verify visual changes
   - Run local development server
   - Compare against Figma design
   - Check button states (hover, active, disabled)
   - Verify responsive behavior

5. Test and commit
   - Run all tests
   - Create git commit
   - Notify designer of completion

## Priority
- **Level**: HIGH
- **Reasoning**: Blocking designer's work on authentication flow. Critical path dependency.

## Requires Human Approval?
- **Answer**: No
- **If Yes, Why**: [N/A - Clear technical requirement]
- **Decision Points**: [N/A]

## Suggested Output
- **Expected Deliverable**: Updated button component with new colors, committed to main
- **Success Criteria**: Visual matches Figma design, all tests pass, designer confirms
- **Estimated Effort**: 45 minutes to 1 hour
```

---

## Workflow Execution

### When Task Appears in Inbox

```
New file detected in vault/Inbox/
    ↓
Read task content completely
    ↓
Analyze task requirements and constraints
    ↓
Generate Plan_<timestamp>.md in vault/Needs_Action/
    ↓
Output confirmation: "✅ Plan created: Plan_2026-02-18_143022.md"
    ↓
STOP - Do NOT execute task
    ↓
Await human review or trigger next workflow stage
```

### Plan File Checklist

Before finalizing plan file, verify:

- [ ] Plan file created with correct timestamp format
- [ ] Original task section contains exact task text
- [ ] Objective is single, clear sentence
- [ ] Step-by-step plan has 3-7 logical steps
- [ ] Each step includes necessary details or sub-steps
- [ ] Priority level assigned (HIGH/MEDIUM/LOW) with reasoning
- [ ] Approval requirement clearly stated (Yes/No)
- [ ] If approval needed, specific decision points listed
- [ ] Suggested output describes deliverable clearly
- [ ] Success criteria are measurable
- [ ] Estimated effort provided
- [ ] File saved to `AI_Employee/vault/Needs_Action/`

---

## Key Rules

1. **Read Completely**: Understand entire task before planning
2. **No Execution**: Create plan only, do not execute any steps
3. **Timestamp Format**: Use `YYYY-MM-DD_HHmmss` (24-hour format)
4. **Clear Objective**: State goal in one sentence
5. **Detailed Steps**: Include 3-7 logical action steps
6. **Approval Decision**: Explicitly state if human sign-off needed
7. **Measurable Output**: Define what success looks like
8. **Confirmation**: Report plan file creation
9. **Consistent Format**: Follow template exactly
10. **Stop After Plan**: Do not proceed beyond planning stage

---

## Integration

### Trigger Points
- File created in `vault/Inbox/`
- File added by filesystem watcher
- Manual task submission

### Next Stages
- ✅ Plan creation (this workflow)
- ⏳ Human review of plan (external)
- 🚀 Task execution (separate workflow)
- 📝 Result documentation (separate workflow)

---

## Status

**Version:** 1.0
**Tier:** BRONZE
**Last Updated:** 2026-02-18
**Status:** READY FOR IMPLEMENTATION
