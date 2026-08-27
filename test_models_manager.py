import sys
import threading
import time
from openpilot.common.params import Params
from sunnypilot.models.manager import ModelManagerSP

def test():
    params = Params()
    # Mock some data
    params.put("ModelManager_DownloadRef", "some_ref_that_doesnt_exist")
    
    manager = ModelManagerSP()
    
    # Run a few iterations of main_thread manually
    print("Testing models_manager...")
    try:
        manager.main_thread()
    except Exception as e:
        print(f"CRASH: {e}")
        import traceback
        traceback.print_exc()

test()
