# File Triage Skill - BRONZE Tier

## Skill Overview

File Triage is the process of reviewing tasks from an Inbox markdown file, understanding their requirements, determining their status, and organizing them into actionable output. This skill is essential for managing task workflows and ensuring nothing falls through the cracks.

## Step 1: Reading a Task from Inbox Markdown

### What to Look For
Each task in the Inbox markdown will have the following structure:

- **Task Title**: A brief description of what needs to be done
- **Description/Details**: Context, background information, or specific requirements
- **Priority Indicator**: Optional flag indicating urgency (URGENT, HIGH, MEDIUM, LOW)
- **Status Marker**: Current state of the task (NEW, IN PROGRESS, BLOCKED, WAITING)
- **Related Files/Links**: Any references to code, documents, or other resources

### How to Read the Task
1. Scan the task title first to get the main objective
2. Read the full description to understand context and requirements
3. Identify any constraints or dependencies mentioned
4. Note any deadline or priority information
5. Look for tags or labels that indicate task category or type

### Example Structure
```markdown
## Task: [Title]
- **Status**: NEW/IN PROGRESS/BLOCKED
- **Priority**: HIGH/MEDIUM/LOW
- **Description**: [Full context and requirements]
- **Related**: [Files, links, or dependencies]
```

## Step 2: Summarizing the Task

### Create a Concise Summary
Your summary should be brief but complete. It should answer these questions:

1. **What is being asked?** - One sentence describing the core request
2. **Why does it matter?** - Context about impact or importance
3. **What are the constraints?** - Any dependencies, deadlines, or limitations
4. **What does success look like?** - Clear definition of completion

### Summary Length
- Keep to 2-3 sentences maximum
- Use clear, actionable language
- Avoid copying the original text verbatim
- Include any critical details that affect action decisions

### Example Summary
**Original**: "Need to fix the login button styling. It doesn't match the design system colors. Check Figma for the exact color codes. This is blocking the designer from continuing work on the auth flow."

**Good Summary**: "Fix login button styling to match design system. Get color codes from Figma. Blocks designer's auth flow work."

## Step 3: Deciding Whether Action is Needed

### Evaluation Criteria

Run through these checks in order:

#### 1. Is the task clearly defined?
- Do you understand what needs to be done?
- Are there enough details to begin work?
- **If NO**: Task needs clarification → Mark as NEEDS_CLARIFICATION

#### 2. Is there a blocker preventing action?
- Is this waiting on someone else's work?
- Are required resources unavailable?
- Is there a missing dependency?
- **If YES**: Task needs to stay in INBOX as BLOCKED → Identify the blocker

#### 3. Has the task already been completed?
- Check if the work is already done in the codebase
- Verify if this was a duplicate of already-completed work
- Look for evidence that the requirement is satisfied
- **If YES**: Mark as DONE → No action needed

#### 4. Should this task be actioned now?
- Does it have HIGH priority or urgent deadline?
- Is it blocking other work?
- Do you have the context and resources to start?
- **If YES**: Task needs ACTION → Move to action queue

#### 5. Can this be deferred?
- Is it LOW priority or nice-to-have?
- Are there other higher-priority items?
- Is there dependency that will be ready later?
- **If YES**: Task needs DEFERRED → Keep in INBOX for later review

### Decision Tree
```
Task is clear?
├─ NO → NEEDS_CLARIFICATION
└─ YES → Is there a blocker?
    ├─ YES → BLOCKED (document blocker)
    └─ NO → Already done?
        ├─ YES → DONE (document evidence)
        └─ NO → Should be actioned now?
            ├─ YES → ACTION (move to action queue)
            └─ NO → DEFERRED (keep in inbox)
```

## Step 4: Writing Output Markdown

### Output File Structure

Create a markdown file with results organized by decision category:

```markdown
# File Triage Results - [Date]

## Action Required (X tasks)
[List tasks that need immediate action]

## Blocked (X tasks)
[List tasks with blockers and what's blocking them]

## Done / Closed (X tasks)
[List tasks that are already completed]

## Needs Clarification (X tasks)
[List tasks missing critical information]

## Deferred (X tasks)
[List tasks to revisit later]
```

### Format for Each Task Entry

For every task in output, include:

**Task Title**
- **Status**: [ACTION/BLOCKED/DONE/NEEDS_CLARIFICATION/DEFERRED]
- **Summary**: [Your 2-3 sentence summary]
- **Notes**: [Any additional context, blockers, or reasoning]

### Example Output

```markdown
# File Triage Results - 2026-02-18

## Action Required (2 tasks)

**Fix login button styling**
- **Status**: ACTION
- **Summary**: Update login button colors to match design system. Requires color codes from Figma. Currently blocking designer's work.
- **Notes**: High priority, designer waiting. Figma link available in related files.

**Update API documentation**
- **Status**: ACTION
- **Summary**: Add endpoint documentation for new user search feature. Should include example requests and responses.
- **Notes**: Medium priority. API endpoints already finalized and tested.

## Blocked (1 task)

**Implement payment gateway**
- **Status**: BLOCKED
- **Summary**: Integrate Stripe payment processing into checkout flow.
- **Notes**: Blocked on account setup - awaiting Finance team approval for Stripe account. Expected completion by 2026-02-25.

## Done / Closed (1 task)

**Setup CI/CD pipeline**
- **Status**: DONE
- **Summary**: Configure GitHub Actions for automated testing and deployment.
- **Notes**: Completed in commit 3a7f92d. All tests passing, deployed to staging.
```

### Output Quality Checklist

Before finalizing output, verify:

- [ ] Every task from Inbox has been classified into a category
- [ ] Summaries are concise (2-3 sentences max)
- [ ] Reasoning for each decision is clear
- [ ] Blockers are explicitly documented with timeline if known
- [ ] Done tasks reference completion evidence (commit, link, etc.)
- [ ] Formatting is consistent across all entries
- [ ] No tasks are left unclassified or ambiguous

## Common Triage Scenarios

### Scenario 1: Duplicate Task
**What to do**: Mark as DONE with note "Duplicate of [original task]. Work completed in [reference]."

### Scenario 2: Task Missing Critical Info
**What to do**: Mark as NEEDS_CLARIFICATION. Specify exactly what information is missing.

### Scenario 3: Task Dependent on External Person
**What to do**: Mark as BLOCKED. Name the dependency and estimate when it will be unblocked.

### Scenario 4: Nice-to-Have Feature
**What to do**: Mark as DEFERRED if there are higher priorities, or ACTION if capacity exists.

### Scenario 5: Task Already Partially Done
**What to do**: Clarify the remaining work needed. If small remainder, mark ACTION. If majority is done, mark DONE and note what remains.

## Tips for Effective Triage

1. **Be objective**: Separate what the task says from what you assume
2. **Document blockers**: Future triagers need to know what's preventing action
3. **Use consistent language**: Keep summaries in similar style and tone
4. **Question ambiguity**: If you're confused, the task needs clarification
5. **Look for patterns**: Multiple related tasks might be consolidated or reprioritized
6. **Verify completion**: Don't assume something is done without checking
7. **Keep history**: Reference previous triage decisions when relevant

## Triage Workflow Summary

1. Read the task completely
2. Write a concise summary
3. Apply the decision tree to classify the task
4. Document your reasoning
5. Format output according to the template
6. Review all tasks are classified before finalizing
7. Generate output markdown file
