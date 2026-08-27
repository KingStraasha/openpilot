import os
os.makedirs("test_dir", exist_ok=True)
os.makedirs("test_dir/subdir", exist_ok=True)
try:
    os.remove("test_dir/subdir")
    print("REMOVED DIR")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
