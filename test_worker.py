import sys, os
from dataclasses import replace
sys.path.append(os.path.abspath('tinygrad_repo'))
from tinygrad.runtime.ops_cpu import worker_prog
from tinygrad.renderer.cstyle import ClangRenderer
from tinygrad.codegen import do_to_program
from tinygrad.device import Device
from tinygrad.helpers import Context
from tinygrad.engine.realize import graph_rewrite
from tinygrad.uop.ops import UOp, Ops
from tinygrad.dtype import dtypes
def patched_worker_prog():
  import tinygrad.runtime.ops_cpu as cpu
  ring = UOp.param(0, dtypes.uint64, (cpu.RING_SLOTS * cpu.CMD_SIZE,), volatile=True)
  wait, sem = UOp.param(1, dtypes.uint64, (1,), volatile=True), UOp.param(2, dtypes.uint64, (1,))
  cur = UOp.range(2**64-1, 0, dtype=dtypes.uint64)

  # PASS sem.after(cur) INSTEAD OF sem.after(cur)[0]
  ready = (rv:=wait.after(lw:=UOp.loop(1), cur)[0].load().call(sem.after(cur), ret_dtype=dtypes.int)).end(lw, rv != 0)

  entry = [ring.after(ready).index((cur % cpu.RING_SLOTS) * cpu.CMD_SIZE + i).load() for i in range(cpu.CMD_SIZE)]
  return entry[0].call(*entry[1:], ret_dtype=dtypes.void).end(cur)

with Context(DEV="CPU"):
  prg = patched_worker_prog()
  from tinygrad.engine.realize import pm_compile
  prg = graph_rewrite(prg, pm_compile, walk=True)
  renderer = ClangRenderer(replace(Device["CPU"].renderer.target, renderer="CLANG"))
  prog = do_to_program(prg, renderer)
  print(prog.src)
