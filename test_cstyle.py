import sys, os
from dataclasses import replace
sys.path.append(os.path.abspath('tinygrad_repo'))
from tinygrad.runtime.ops_cpu import CPUDevice
from tinygrad.helpers import Context
import sys
with Context(DEV="CPU"):
  try:
    dev = CPUDevice("CPU")
    print("SUCCESS")
  except Exception as e:
    import traceback
    traceback.print_exc()
