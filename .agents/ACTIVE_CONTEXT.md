# Active Project Context & Multi-Device Memory

*Last Updated: 2026-08-26*

---

## 1. Vehicle & Hardware Profile

- **Target Vehicle**: 2023 Ford F-150 Lightning
- **Car Platform**: `CAR.FORD_F_150_LIGHTNING_MK1` (`FordF150LightningPlatform` extending `FordCANFDPlatformConfig`)
- **Bus Architecture**: Ford CAN-FD via Q4 harness (`CarHarness.ford_q4`)
- **Radar Interface**: `RADAR.STEER_ASSIST_DATA` (`ford_lincoln_base_pt` DBC) over CAN-FD bus
- **Steering Control Type**: `SteerControlType.angle` (Angle-based lateral control)
- **Target Device**: comma 4 (`mici`) / AGNOS locked strictly to `BluePilotDev/bluepilot:bp-7.0` manifest (`launch_env.sh` / `agnos.json`, baseline `18.5`). Upstream SunnyPilot AGNOS changes are strictly blocked.

---

## 2. Git & Repository Status

- **Active Branch**: `bp70` (tracked on `fork/bp70` at `https://github.com/KingStraasha/openpilot.git`)
- **Baseline Root Commit**: `e1d051d7ba` (Clean 1-to-1 sync with `origin/bp-7.0` from `BluePilotDev/bluepilot`)
- **Remotes**:
  - `fork`: `https://github.com/KingStraasha/openpilot.git`
  - `origin`: `https://github.com/BluePilotDev/bluepilot.git`
  - `upstream`: `https://github.com/sunnypilot/sunnypilot.git`
- **Submodules Verified**: `msgq_repo`, `panda`, `rednose_repo`, `sunnypilot/neural_network_data`, `teleoprtc_repo`, `tinygrad_repo`

---

## 3. Workflow State & Quick Resumption Protocol

> [!IMPORTANT]
> **RESUMPTION TRIGGER**: When the user types **"Let's Continue"** (or similar):
> 1. Check if the user has tested downloading the baseline `bp70` onto the Comma 4 (`mici`).
> 2. Once on-device SCons compilation and UI boot are confirmed good, proceed immediately to **Phase 4: Phased Isolation & Upstream Merging**.
> 3. **Phase 4 Execution**:
>    - Generate an atomic, module-by-module merge plan for incoming `sunnypilot` upstream changes (`upstream/master` -> `bp70`).
>    - **AGNOS Merge Guard**: Strictly retain BluePilot's AGNOS version (`launch_env.sh` and `agnos.json`); never accept SunnyPilot AGNOS bumps.
>    - Integrate changes incrementally (one subsystem at a time: e.g. Controls/MADS, Navigation/Mapd, UI/MICI, Models, etc.).
>    - Validate with `py_compile` and unit tests after each module.
>    - Auto-commit validated increments and pause for device verification to isolate regressions immediately.

---

## 4. Execution History & Handoff Log

| Phase / Date | Status | Accomplishments & Next Actions |
| :--- | :--- | :--- |
| **Phase 1 (2026-08-26)** | **DONE** | Extracted full Comma 4 (`mici`), Ford F-150 Lightning CAN-FD, Antigravity 2.0 toolchain constraints, and build blocker mitigations into `AGENTS.md` (Section 2). |
| **Phase 2 (2026-08-26)** | **DONE** | Executed clean 1-to-1 baseline clone of `bluepilot/bp-7.0` (`origin/bp-7.0`), verified submodules, remotes, preserved `AGENTS.md` and `.agents/`, and pushed clean baseline to `fork/bp70`. |
| **Phase 3 (2026-08-26)** | **IN PROGRESS** | Baseline pushed to `fork/bp70`. Awaiting user on-device download & boot verification on Comma 4. |
| **Phase 4 (Pending)** | **QUEUED** | Phased isolation & upstream SunnyPilot merge upon resumption signal ("Let's Continue"). |
