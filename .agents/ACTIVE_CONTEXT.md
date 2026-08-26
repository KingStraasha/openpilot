# Active Project Context & Multi-Device Memory

*Last Updated: 2026-08-25*

---

## 1. Vehicle & Hardware Profile

- **Vehicle**: 2023 Ford F-150 Lightning
- **Platform**: `FORD_F_150_LIGHTNING_MK1` (`FordCANFDPlatformConfig`)
- **Bus Architecture**: Ford CAN-FD
- **Radar**: `RADAR.STEER_ASSIST_DATA` (over CAN-FD, not Delphi MRR)
- **Steering Control Type**: `SteerControlType.angle` (Angle-based lateral control)
- **Device**: comma 4 (`mici`) / AGNOS 18.5+

---

## 2. Git & Repository Status

- **Active Branch**: `bp-7.0` (clean 1-to-1 baseline synced with `origin/bp-7.0` at `e1d051d7ba`)
- **Remotes**:
  - `fork`: `https://github.com/KingStraasha/openpilot.git`
  - `origin`: `https://github.com/BluePilotDev/bluepilot.git`
  - `upstream`: `https://github.com/sunnypilot/sunnypilot.git`

---

## 3. Workflow Preferences & Automation Rules

- **Auto-Commit on Validated Merges**: When upstream/feature merges or backports are successful and pass all verification tests, automatically create clean commits directly to the branch.

---

## 4. Session Handoff Log

| Date | Machine/Session Summary | Next Steps / Notes |
| :--- | :--- | :--- |
| **2026-08-24** | Evaluated upstream changes (`upstream/master`, `origin/bp-dev`, `origin/bp-7.0`). Confirmed `bp70` is clean and stable. Established vehicle profile (2023 F-150 Lightning) and created cross-device continuity rules. | Ready for driving or future testing. |
| **2026-08-25** | Backported SunnyPilot model persistence & cache safety fixes (`b75337502f`) and BluePilot stability debounces (`15f41299b0`). Validated with `py_compile`. Configured auto-commit rule. | Push `bp70` to `fork/bp70` (`git push fork bp70`). |
| **2026-08-26** | Phase 1: Extracted full Comma 4 (`mici`), Ford F-150 Lightning CAN-FD, Antigravity 2.0 toolchain constraints, and build blocker mitigations into `AGENTS.md`. Prepared for clean workspace reset. | Completed Phase 1. |
| **2026-08-26** | Phase 2: Performed clean 1-to-1 baseline clone of `bluepilot/bp-7.0` (`origin/bp-7.0`), verified submodules, remotes, and preserved `AGENTS.md` and `.agents/`. | Ready for Phase 3: Baseline Deployment & Device Verification. |

