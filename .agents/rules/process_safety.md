# Background Process Safety & Execution Timeout Rule

## Objective
Prevent background tasks, shell loops, or subprocesses from hanging, blocking terminal sessions, or remaining orphaned indefinitely.

---

## Mandatory Execution Constraints

### 1. Mandatory Timeouts for All Network and Subshell Commands
- Every network inspection command (`curl`, `wget`, `nc`, `ssh`, etc.) **MUST** specify strict execution and connection timeouts:
  - `curl -m 3 --connect-timeout 2 --no-keepalive ...`
- Every shell command or script that could potentially block **MUST** be wrapped with `timeout`:
  - `timeout 5s <command>`

### 2. No Keep-Alive or Unbounded Pipe Streaming
- Never pipe unbounded HTTP streams directly into line filters like `head` or `grep` inside bash loops (e.g., `curl ... | head`).
- When inspecting HTTP responses, use `-s -o /dev/null -w "%{http_code}"` or save to a temporary file, or use Python with explicit `socket.setdefaulttimeout(2.0)`.

### 3. Avoid Shared Shell Blocking
- Never leave long-running synchronous loops running in the interactive terminal.
- If a command takes more than a few seconds, structure it to complete deterministically or use a standalone one-shot script.

### 4. Background Task Lifecycle Discipline
- If a background task is spawned unexpectedly or stalls, immediately inspect and terminate it via `manage_task` (`kill`) rather than leaving it in `RUNNING` state.
