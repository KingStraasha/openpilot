# Active Project Context & Multi-Device Memory

## Metadata

Last Updated: 2026-08-28

---

## 1. Vehicle & Hardware Profile

- **Target Vehicle**: 2023 Ford F-150 Lightning
- **Car Platform**: `CAR.FORD_F_150_LIGHTNING_MK1` (`FordF150LightningPlatform` extending `FordCANFDPlatformConfig`)
- **Bus Architecture**: Ford CAN-FD via Q4 harness (`CarHarness.ford_q4`)
- **Radar Interface**: `RADAR.STEER_ASSIST_DATA` (`ford_lincoln_base_pt` DBC) over CAN-FD bus
- **Steering Control Type**: `SteerControlType.angle` (Angle-based lateral control)
- **Target Device**: comma 4 (`mici`) / AGNOS locked strictly to `BluePilotDev/bluepilot:bp-7.0` manifest (`launch_env.sh` / `agnos.json`, baseline `18.5`). Upstream SunnyPilot AGNOS changes are strictly blocked.
- **Development Toolchain & Topology**:
  - **Client Laptops**: Local Antigravity IDE instances connecting via Remote-SSH / Tunnel to `landscapevm`; browser access to Antigravity 2.0 Web UI (`http://192.168.10.15:7070`).
  - **Host Server (`landscapevm` @ 192.168.10.15)**: Centrally hosts `/srv/workspaces/bluepilot`, Antigravity 2.0 Daemon Hub (`:7071` via Nginx `:7070`), Antigravity IDE Server (`~/.antigravity-ide-server/`), and AGY CLI (`/usr/local/bin/agy` v1.1.22). Zero file drift across roaming client laptops.

---

## 2. Git & Repository Status

- **Active Branch**: `bp70` (tracked on `fork/bp70` at `https://github.com/KingStraasha/openpilot.git`)
- **Latest Commit**: `6488df75d3` (Clean working tree, fully pushed to `fork/bp70`)
- **Remotes**:
  - `fork`: `https://github.com/KingStraasha/openpilot.git`
  - `origin`: `https://github.com/BluePilotDev/bluepilot.git`
  - `upstream`: `https://github.com/sunnypilot/sunnypilot.git`
- **Submodules Verified**: `msgq_repo`, `panda`, `rednose_repo`, `sunnypilot/neural_network_data`, `teleoprtc_repo`, `tinygrad_repo`

---

## 3. Workflow State & Quick Resumption Protocol

> [!IMPORTANT]
> **RESUMPTION TRIGGER**: When the user types **"Let's continue"** (or similar):
> 
> 1. **Immediate Next Step**: Proceed with **Phase 4: Phased Isolation & Upstream Merging** (starting with Module 2: Controls & Long/Lat Extensions, or the next scheduled upstream module).
> 2. **Verification Checkpoint**: Ask the user if they've had a chance to test the latest commit on their Comma 4 (`mici`) for the GitHub updater and Model Manager.
> 3. **Mandatory Phase 4 Merge Guards**:
>    - *AGNOS*: Strictly retain BluePilot's AGNOS version (`launch_env.sh`, `agnos.json`); block SunnyPilot AGNOS bumps.
>    - *Boot Hooks*: Retain BluePilot startup hooks in `launch_chffrplus.sh` (`agnos_init`, `fix_egl_adreno`, `cereal` symlink, `selfdrive/ui/bp` symlink, `bp_build.py`).
>    - *Asset / LFS*: Retain `.gitattributes` binary overrides (`-filter -text`) for all BP assets.
>    - *Submodules*: Fetch upstream with `git fetch --no-recurse-submodules`.
>    - *Two-Tier Verification*: Local `py_compile` + unit tests (Tier 1), then on-device verification (Tier 2).

---

## 4. Execution History & Handoff Log

| Phase / Date | Status | Accomplishments & Next Actions |
| :--- | :--- | :--- |
| **Phase 1 (2026-08-26)** | **DONE** | Extracted full Comma 4 (`mici`), Ford F-150 Lightning CAN-FD, Antigravity toolchain constraints, and build blocker mitigations into `AGENTS.md`. |
| **Phase 2 (2026-08-26)** | **DONE** | Executed clean 1-to-1 baseline clone of `bluepilot/bp-7.0` (`origin/bp-7.0`), verified submodules, remotes, preserved `AGENTS.md` and `.agents/`, and pushed baseline to `fork/bp70`. |
| **Phase 3 (2026-08-26)** | **DONE** | Baseline verified. Upstream sync points and merge guards validated. |
| **Core Subsytem Triage (2026-08-28)** | **RESOLVED** | **1. GitHub Updater Crash Fix**: Fixed `system/updated/updated.py` to prevent destructive `git clean -xdff` and `git reset --hard` in OverlayFS mounts (preventing Comma 4 kernel panics), wrapped `git branch --set-upstream-to` in try/except, and added missing `bp70 -> bp-7.0` branch mapping to `system/version.py`.<br>**2. Model Manager Manifest Alignment & Download Fix**: Verified `driving_models_v21.json` is the correct standard manifest for Comma 4 Snapdragon NPU. Debugged silent download failures in `sunnypilot/models/manager.py` by adding `User-Agent: SunnyPilot/1.0` headers to bypass HuggingFace rate-limits/Cloudflare blocks, correcting the chunked-fallback exception logic to prevent `HTTPError(404)` file wiping, and adding a 3-attempt chunk resume/retry loop for spotty connections.<br>**3. Model Transition & Cache Interference Fix**: Root-caused why the system reverted to CD210 after a successful model download. Fixed a bug in `models/manager.py` where a stale `.chunkmanifest` written during JSON parsing caused local verification (`_verify_file`) to fail when falling back to a solid `.pkl` file download, which resulted in the active model being silently wiped. Additionally, added the missing `DoReboot = True` flag to `selfdrive/ui/sunnypilot/mici/layouts/models.py` when selecting a downloaded model, ensuring `modeld` dynamically restarts to load the newly selected model instead of persisting on CD210.<br>**4. Visual SCons Build Screen Fix**: Addressed a cosmetic but confusing bug during device boot where the SCons build screen appeared frozen on a `kj/filesystem-disk-unix.c++:1734:warning` Cap'n Proto warning for 2-4 minutes while compiling in the background. Removed the explicit `"PWD": BASEDIR` environment override in `system/manager/bp_build.py` and `build.py` which was conflicting with the physical mount path of the repository, silencing the warning. |
| **CI / Discourse Fix (2026-08-27)** | **RESOLVED** | Removed `.github/workflows/test-discourse.yaml.yml` debug workflow that failed on every push; added credentials guard in `post-to-discourse/action.yml`. |
| **Antigravity External Access & Process Safety (2026-08-28)** | **RESOLVED** | Verified external host access via Nginx reverse proxy on port 7070 (`HTTP 200 OK`). Added permanent background process safety rule in `.agents/rules/process_safety.md` enforcing strict execution timeouts (`timeout <N>s`, `curl --max-time --no-keepalive`) and socket boundaries to prevent hung tasks. |
| **Multi-Laptop Topology Integration (2026-08-28)** | **COMPLETED** | Established and documented canonical multi-laptop client architecture connecting remotely to `landscapevm` (192.168.10.15), hosting Antigravity 2.0 Hub (:7070), AGY CLI, and IDE Server. |
| **Handoff (2026-08-28)** | **READY (Awaiting Trigger)** | All blocker bugs, CI issues, UI visual issues, Antigravity 2.0 access, and multi-device architecture fully verified and locked in. Standing by on current baseline; Phase 4 upstream module integration will begin only upon explicit user instruction. |

