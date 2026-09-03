# Session Continuity & Multi-Device Synchronization Rule

## Objective
Ensure that all relevant session context, vehicle configurations, active git branches, evaluation history, and work-in-progress notes are continuously recorded and preserved. This enables seamless continuation of work across multiple machines/laptops via repository sync.

---

## Protocols

### 1. Mandatory Context File: `.agents/ACTIVE_CONTEXT.md`
- Always maintain and consult [ACTIVE_CONTEXT.md](file:///srv/workspaces/bluepilot/.agents/ACTIVE_CONTEXT.md) at the start of any conversation.
- This file acts as the persistent project memory shared across all laptops.

### 2. Information to Track and Maintain
Whenever any of the following change or are referenced in a session, update `.agents/ACTIVE_CONTEXT.md`:
1. **Target Vehicle & Hardware**:
   - Make, model, model year, trim/package.
   - Platform type (e.g. Ford CAN-FD vs CAN, radar type, steering control type).
   - Device hardware (comma 3X / TICI / MICI, AGNOS version).
2. **Repository & Git State**:
   - Active working branch and upstream/fork tracking associations.
   - Pending upstream evaluation results, sync status, and decisions made (e.g., why a merge was skipped or approved).
3. **Work-in-Progress & Decisions**:
   - Current tasks, active investigations, bug fixes, or tuning experiments.
   - Key architectural decisions, rationale, and next planned steps.
4. **Handoff Log**:
   - Short timestamped summary of what was accomplished in each session and what remains to be done on the next machine.

### 3. Workflow for Multi-Device Continuity
- **Start of Session**: Read `.agents/ACTIVE_CONTEXT.md` to load vehicle context, active branch, and recent status.
- **During Session**: If changes to decisions, branch plans, or vehicle configuration occur, record them in `.agents/ACTIVE_CONTEXT.md`.
- **End of Session / Handoff**: Ensure `.agents/ACTIVE_CONTEXT.md` is updated and remind the user to push/pull git commits so the other laptop receives the latest context.
