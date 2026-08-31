# ACTIVE_CONTEXT.md

## Verified State — Opus 4.6 Audit (2026-08-31)

**Branch:** `bp70`
**Status:** ✅ All subsystems pass structural audit — ready for on-device testing.

### Architectural Remediation Summary

The following patches were applied across two sessions (Gemini 3.1 Pro + Opus 4.6 audit/cleanup):

#### 1. Model Download Subsystem
- **`common/file_chunker.py`**: Implemented `_ChunkedFile(io.RawIOBase)` and `open_file_chunked()` for transparent streaming of chunked model files on Comma 4.
- **`sunnypilot/models/fetcher.py`**: Model manifest URLs point to `driving_models_v21.json` (qcom) and `driving_models_chestnut_v22.json` (chestnut) on `gh-pages`.
- **`sunnypilot/models/helpers.py`**: SHA256 verification via `hashlib.file_digest()` through `open_file_chunked()` — supports both whole-file and per-chunk hashes.
- **`sunnypilot/models/manager.py`**: Chunked download with per-chunk SHA256 validation, resume semantics, and progress reporting.

#### 2. Updater Crash Remediation
- **`system/updated/updated.py`**: Added `_log_to_file()` writing to `/data/openpilot/updater.log` with silent exception swallow. Submodule operations individually wrapped in `try/except`. `git fetch` uses `--no-recurse-submodules` (Submodule Fetch Guard). `set-upstream-to` is non-fatal. Main loop catches both `CalledProcessError` and generic `Exception`, logging to both `cloudlog` and file.

#### 3. Build System
- **Tinygrad Submodule**: Pinned to `cb6fb2e4a` (sunnypilot fork), which includes:
  - `66ee3cfb4f`: ONNX IR fix for AGNOS 18.5 LLVM 17
  - `4b86e9205`: `libpthread.so.0` fallback for `sem_open` on AGNOS
  - `cb6fb2e4a`: LLVM intrinsics fix + direct sem pointer (avoids `Tensor.arange(device=...)` kwarg issue)
- **`selfdrive/modeld/compile_modeld.py`**: `Tensor.arange()` calls use `.to(WARP_DEV)` instead of deprecated `device=` kwarg.
- **`common/glibcxx_compat.cc`**: Built as separate static library (`compat_lib`) to resolve cyclic dependency with `_common`/`zmq`/`json11`.
- **`SConstruct`**: Imports `compat_lib`, adds `rt` to messaging libs, provides LLVM_PATH fallback.
- **`common/SConscript`**: Exports `compat_lib`, links it into test and Cython targets.
- **`tools/replay/SConscript`**: `stdc++fs` added (legitimate: `route.cc` uses `std::filesystem`).

#### 4. Audit Cleanup (Opus 4.6)
- Removed 5 orphaned debug files from repo root: `test_cstyle.py`, `test_llvm.py`, `test_worker.py`, `test.ll`, `scons_dryrun.txt`.

### On-Device Verification Command Sequence
```bash
# 1. Clean build
uv run scons -c && uv run scons -j$(nproc)

# 2. Verify model downloader daemon
# Boot the UI, select a post-April 2026 model, and check logs:
tail -f /data/openpilot/updater.log
```

### Active Vehicle Profile
- **Target Vehicle**: 2023 Ford F-150 Lightning
- **Platform**: `CAR.FORD_F_150_LIGHTNING_MK1` (CAN-FD, Q4 harness)
- **Device**: Comma 4 (`mici`), AGNOS 18.5
