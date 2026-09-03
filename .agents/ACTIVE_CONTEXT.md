# ACTIVE_CONTEXT.md — bp70-rebuild (2026-09-03)

## Mission Complete: Clean Baseline & Surgical Model Port

**Branch:** `bp70-rebuild`
**Tracking:** `fork/bp70-rebuild` → `https://github.com/KingStraasha/openpilot`
**Status:** ✅ All 5 phases complete. Ready for on-device deployment.

---

## Baseline

| Field | Value |
|---|---|
| Base branch | `origin/bp-7.0` |
| Base commit | `e1d051d7ba` — "Merge pull request #184 from BluePilotDev/bp-dev" |
| Rebuild commit | `ae9dd67703` — "fix(models): register params keys, restore capnp metadata field, and fix mici fallback" |
| Preceding commit | `9cfc9c4aad` — "feat(models): port post-April 2026 SunnyPilot manifests and harden updater" |
| Tinygrad pin | `ac1632ab966c77ba96a7048b893a30f1a714dc87` (clean origin/bp-7.0 pin) |
| AGNOS | 18.5 (dynamic fallback in launch_env.sh — not hardcoded) |

---

## P0 Audit Remediations Applied (Commit ae9dd67703)

1. **`common/params_keys.h`**: Registered three missing parameters:
   - `{"ModelManager_ActiveJson", {CLEAR_ON_MANAGER_START, JSON}}`
   - `{"ModelManager_LastSyncTime_Chestnut", {CLEAR_ON_MANAGER_START | CLEAR_ON_OFFROAD_TRANSITION, INT, "0"}}`
   - `{"ModelManager_ModelsCache_Chestnut", {PERSISTENT | BACKUP, JSON}}`
   Prevents fatal `openpilot.common.params_pyx.UnknownKeyName` daemon crash on startup.

2. **`cereal/custom.capnp`**: Restored `metadata @2 :Artifact;` on `struct Model`.
   Maintains Cap'n Proto wire protocol backward/forward compatibility and prevents `AttributeError` in `model_runner.py`.

3. **`selfdrive/ui/sunnypilot/mici/layouts/models.py`**:
   Updated fallback to call `get_bundles_for_source("qcom")` (replacing obsolete `get_available_bundles()`).

---

## What Was Done (vs. bp70)

This branch is **NOT bp70**. It is a clean rebuild containing **only** verified,
Python-space surgical additions on top of `origin/bp-7.0`.

The following bp70 changes were **explicitly excluded** to preserve the pristine
C++ ABI and build system:
- ❌ `common/glibcxx_compat.cc` (ABI shim — root cause of boot failures)
- ❌ `SConstruct` modifications
- ❌ `common/SConscript` modifications
- ❌ `sunnypilot/SConscript` modifications
- ❌ `sunnypilot/modeld_v2/SConscript` deletion
- ❌ `selfdrive/modeld/SConscript` device probe changes
- ❌ `tools/replay/SConscript`, `tools/cabana/SConscript`
- ❌ `tinygrad_repo` submodule re-pin (stays at clean origin/bp-7.0 pin)

---

## Files Modified (21 files, all Python/schema/data)

### Model Subsystem — `sunnypilot/models/`
| File | Change |
|---|---|
| `fetcher.py` | v21.json (qcom) + chestnut_v22.json manifests; `system.hardware.hw` import path fixed |
| `manager.py` | `requests` library (sync), `DownloadCancelled`, ref-based cancellation, dual-source |
| `helpers.py` | `REQUIRED_JSON_VERSION=18`, `ACTIVE_BUNDLE_KEYS`, dual-source bundle helpers |
| `model_name.py` | Minor addition |
| `split_model_constants.py` | Minor addition |
| `tests/test_manager_download.py` | **NEW** — 813-line comprehensive download test suite |
| `tests/test_default_model.py` | Updated |
| `tests/test_tinygrad_ref.py` | Updated to OpenpilotTestCase format |

### Schema
| File | Change |
|---|---|
| `cereal/custom.capnp` | Added `ModelManagerSP.Chunk {fileName, sha256}`, `Artifact.chunks @3 :List(Chunk)`, restored `Model.metadata @2` |
| `common/params_keys.h` | Added `ModelManager_ActiveBundleChestnut`, `ModelManager_ActiveJson`, `ModelManager_DownloadRef`, `ModelManager_CancelDownload`, `ModelManager_LastSyncTime_Chestnut`, `ModelManager_ModelsCache_Chestnut`, `ModelRunnerTypeCache` |

### Infrastructure
| File | Change |
|---|---|
| `common/file_chunker.py` | Chunked model file streaming: `open_file_chunked()`, `get_chunk_name()`, `get_manifest_path()` |
| `system/hardware/__init__.py` | `TICI = /TICI or /MICI or /TIZI` (Comma 4 detection) |
| `system/updated/updated.py` | `_log_to_file()` → `updater.log`, `--no-recurse-submodules`, try/except submodule ops, mici-aware skip logic |

### UI / Sunnylink
| File | Change |
|---|---|
| `selfdrive/ui/sunnypilot/mici/layouts/models.py` | Multi-source model UI |
| `sunnypilot/sunnylink/settings_ui.json` | Chestnut/qcom source awareness |
| `sunnypilot/sunnylink/settings_ui_src/pages/models.yaml` | Source field |
| `sunnypilot/sunnylink/tests/test_settings_changes.py` | Updated |

### Agent Rules
- `.agents/rules/auto_commit.md`
- `.agents/rules/process_safety.md`
- `.agents/rules/session-continuity.md`

---

## Verification Results (Dev Machine)

| Test | Result |
|---|---|
| `py_compile` on 13 modified Python files | ✅ ALL PASS |
| `ModelFetcher` import + URL assertion | ✅ PASS |
| `Helpers` import + `REQUIRED_JSON_VERSION=18` | ✅ PASS |
| `ModelManagerSP` import + `DOWNLOAD_TIMEOUT=(30,30)` | ✅ PASS |
| `file_chunker` import | ✅ PASS |
| `system.hardware` import + `TICI/AGNOS/PC` flags | ✅ PASS |
| `updated.py` compile | ✅ PASS |
| `cereal.messaging` import | ✅ PASS |
| `Ford CAR.FORD_F_150_LIGHTNING_MK1` present | ✅ PASS |
| C++/build-system guardrail (no SConstruct/SConscript/.cc changes) | ✅ CONFIRMED |

**Note:** Full `scons -j$(nproc)` build requires on-device execution (AGNOS 18.5, AARCH64).
The `scons` invocation on this x86_64 Rocky Linux 8 dev machine is blocked by
`tinygrad.Device.get_available_devices()` attempting QCOM driver init (requires sudo/device).
On-device build is the authoritative gate — see SSH commands below.

---

## Active Vehicle Profile

- **Target Vehicle**: 2023 Ford F-150 Lightning
- **Platform**: `CAR.FORD_F_150_LIGHTNING_MK1` (CAN-FD, Q4 harness, angle-based steering)
- **Device**: Comma 4 (`mici`), AGNOS 18.5
- **Key baseline commits**: `a02c06ef37` (2024-25 Lightning VIN), `dba58eb7eb` (VIN PR #177)

---

## On-Device Deployment Commands (SSH to Comma 4)

```bash
# ── Deploy bp70-rebuild to device ──────────────────────────────────────────
cd /data/openpilot

# Fetch the new branch from the fork
git fetch fork bp70-rebuild --no-recurse-submodules

# Switch to the branch and reset to its tip
git checkout -B bp70-rebuild fork/bp70-rebuild
git reset --hard fork/bp70-rebuild

# Update submodules (non-recursive to avoid network issues with nested subs)
git submodule sync
git submodule update --init

# Build (device must be offroad / screen off for QCOM compilation)
scons -j$(nproc)

# Verify the updater log path
ls -la /data/openpilot/updater.log 2>/dev/null || echo "updater.log will be created on first update cycle"

# Reboot to apply
sudo reboot
# ───────────────────────────────────────────────────────────────────────────
```

### Post-Reboot Validation
```bash
# Verify model manager is running
logread | grep -i "ModelManager\|model_manager" | tail -20

# Verify updater logging
tail -f /data/openpilot/updater.log

# Verify model manifest fetch
python3 -c "
from openpilot.sunnypilot.models.fetcher import ModelFetcher
from openpilot.common.params import Params
f = ModelFetcher(Params())
bundles = f.get_model_list('qcom')
print(f'qcom bundles: {len(bundles)}')
"

# If UI crashes on model screen, check:
logread | grep -i "error\|crash\|exception" | grep -i "model" | tail -20
```

---

## Excluded from This Branch (On-Device Remediation Notes)

The following bp70 changes were **not ported** and may require re-evaluation for
future iterations once the baseline build is confirmed stable:

1. **`selfdrive/modeld/SConscript` device probe filter**: bp70 limited the probe to
   `CUDA`/`QCOM` only to prevent an NV PCI driver sudo hang. On a clean mici device
   without CUDA hardware this shouldn't matter — but if the build hangs on the device,
   apply: `for d in ['CUDA','QCOM']: try: Device[d]; print(d); except: pass`

2. **`sunnypilot/modeld_v2/` refactor**: The full modeld_v2 rewrite (268 lines changed,
   warp.py removed) was not ported. The baseline `modeld_v2` from `origin/bp-7.0` is
   used. If model inference fails (not model download), this may need revisiting.

3. **`common/params_keys.h` `BPThemePack` removal**: bp70 removed `BPThemePack` param.
   This branch retains it from baseline to minimize risk surface.
