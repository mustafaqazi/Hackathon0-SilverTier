# Task Planner Skill

## Overview

**Skill Name:** Task Planner

**Tier:** Silver

**Status:** Active

**Purpose:** Transform unstructured tasks into detailed, actionable execution plans

## Description

The Task Planner skill reads incoming tasks from the Inbox folder, analyzes their requirements, and generates structured execution plans. Each plan is saved as a markdown document with clear steps, priorities, dependencies, and approval requirements.

## Workflow

### Step 1: Read Task
- Scan `vault/Inbox/` for new markdown files
- Extract task metadata (title, description, requirements)
- Identify task type (feature, bug fix, documentation, etc.)
- Log task reception timestamp

### Step 2: Analyze Intent
- Parse task description and requirements
- Identify goals and success criteria
- Determine affected systems and dependencies
- Extract any constraints or special requirements
- Note any ambiguities requiring clarification

### Step 3: Break Into Steps
- Decompose task into discrete, actionable steps
- Arrange steps in logical execution order
- Identify parallel vs. sequential work
- Estimate effort for each step
- Flag complex or high-risk steps

### Step 4: Assign Priority
- Evaluate urgency (deadline, business impact)
- Assess complexity (time, resources, skill required)
- Determine blocking dependencies
- Assign priority level: **Critical**, **High**, **Medium**, **Low**
- Add estimated completion time

### Step 5: Check Human Approval
- Determine if task requires human approval
- Identify decision points requiring stakeholder input
- Flag resource constraints or conflicts
- Note any tasks outside standard scope
- Document approval requirements clearly

### Step 6: Save Plan to Needs_Action
- Create `ActionPlan_[taskname]_[timestamp].md`
- Save to `vault/Needs_Action/` folder
- Include full execution plan with all metadata
- Maintain consistent formatting and structure
- Update task tracking registry

## Plan Document Structure

```
# ActionPlan: [Task Name]

## Task Metadata
- **Source:** [Inbox filename]
- **Received:** [ISO timestamp]
- **Priority:** [Critical/High/Medium/Low]
- **Est. Hours:** [number]
- **Type:** [feature/bugfix/documentation/other]

## Task Summary
[Concise description of what needs to be done]

## Goals & Success Criteria
- Goal 1: [specific, measurable outcome]
- Goal 2: [specific, measurable outcome]
- Success Metric: [how success is measured]

## Execution Steps
1. [Step description]
   - Sub-action 1
   - Sub-action 2
   - Expected outcome

2. [Step description]
   - Estimated time: [duration]
   - Dependencies: [previous steps]
   - Resources needed: [skills, tools]

## Risks & Mitigations
- Risk 1: [potential issue] → Mitigation: [how to prevent]
- Risk 2: [potential issue] → Mitigation: [how to prevent]

## Human Approval Required
- **Type:** [Technical Review / Budget / Scope / None]
- **Approver:** [role/person]
- **Deadline:** [when approval needed]
- **Decision Points:** [what needs approval]

## Dependencies
- External: [systems, data, resources]
- Internal: [other tasks that must complete first]
- Blocking: [what this task blocks]

## Notes
[Any additional context, assumptions, or special requirements]
```

## Configuration

### Input
- **Source:** `vault/Inbox/*.md`
- **Watch Interval:** 15 seconds
- **File Pattern:** `*.md`

### Output
- **Destination:** `vault/Needs_Action/`
- **Filename:** `ActionPlan_[taskname]_[YYYYMMDD_HHMMSS].md`
- **Format:** Markdown
- **Registry:** `logs/task_registry.json`

## Integration Points

- **Upstream:** Vault Watcher (File Triage Skill)
- **Downstream:** Task Executor, Approval Workflow
- **Data Exchange:** Task registry, plan documents
- **Logging:** `logs/planning.log`

## Performance Metrics

- **Plan Generation Time:** < 30 seconds
- **Accuracy:** Complete coverage of all task requirements
- **Approval Rate:** % of plans requiring human approval
- **Turnaround:** Time from inbox to Needs_Action

## Error Handling

- **Missing Task Data:** Flag for clarification, save draft plan
- **Ambiguous Requirements:** Add decision points in plan
- **Resource Conflicts:** Note in risks section, flag for approval
- **Invalid Format:** Log error, skip file, notify admin

## Approval Requirements

Plans are automatically routed to `vault/Needs_Action/` where human reviewers can:
- Approve execution as-is
- Request modifications
- Request additional information
- Reject and return to inbox for clarification

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-18 | Initial skill implementation |

## Related Skills

- [File Triage Skill](../file-triage/SKILL.md) - Pre-processes inbox files
- [Task Executor Skill](../task-executor/SKILL.md) - Executes approved plans
- [Vault Watcher](../vault-watcher/SKILL.md) - Monitors vault changes

---

**Last Updated:** 2026-02-18
**Maintainer:** AI Employee System
**Status:** Production Ready
