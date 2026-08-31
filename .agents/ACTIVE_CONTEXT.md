# ACTIVE_CONTEXT.md

## Handoff Summary & Root-Cause Execution

### What was salvaged
- Opus successfully isolated the root cause of the missing `open_file_chunked` dependency for streaming newer post-April 2026 driving models on Comma 4 (AGNOS 18.5).
- Opus drafted the correct implementation of `_ChunkedFile` in `common/file_chunker.py`.
- Opus drafted robust exception handling and file logging (`updater.log`) in `system/updated/updated.py` to prevent crash loops when fetching upstream models or syncing submodules.

### What was fixed in this continuation session
1. **Tinygrad Submodule Alignment**: 
   - Restored `tinygrad_repo` to `66ee3cfb4f` to correctly parse and generate IR for the August 2026 ONNX models (older `ac1632ab96` produced undefined LLVM IR `llvm.trunc.float` on AGNOS 18.5's LLVM 17).
   - *However*, `66ee3cfb4f` introduced a fatal `libc.sem_open` bug on AGNOS 18.5 (where `sem_open` lives in `libpthread.so.0`). I applied a surgical monkeypatch inside `tinygrad/runtime/support/c.py` (`__getattr__`) to fallback to `libpthread.so.0` if `libc.sem_open` throws an `AttributeError`.
2. **Build System (SCons) Linker Order**: A previous `glibcxx_compat.cc` refactor introduced a cyclic static library dependency between `_common` and `zmq`. This caused `undefined reference to json11::Json` or `zmq_connect` errors. I resolved the cyclic dependency cleanly by compiling `glibcxx_compat.cc` as a separate static library (`compat_lib`) and appending it to the `LIBS` linker command line in both `SConstruct` and `common/SConscript`.
3. **Compilation**: Triggered and verified a clean `uv run scons -j$(nproc)` execution. The codebase now compiles smoothly.

### On-Device Verification Command Sequence
Once pulled to the Comma 4 device, verify with:
```bash
# 1. Clean build
uv run scons -c && uv run scons -j$(nproc)

# 2. Verify model downloader daemon
# Boot the UI, select a post-April 2026 model, and check logs:
tail -f /data/openpilot/updater.log
```
