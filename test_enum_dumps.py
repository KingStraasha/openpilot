import capnp
import json
schema = """
@0x934efea7f017fff0;
struct ModelBundle { 
    status @0 :DownloadStatus; 
    enum DownloadStatus { notDownloading @0; downloading @1; downloaded @2; }
}
"""
with open("test.capnp", "w") as f:
    f.write(schema)

test_capnp = capnp.load("test.capnp")
bundle = test_capnp.ModelBundle.new_message()
bundle.status = "downloaded"

try:
    d = bundle.to_dict()
    print("Dict:", d)
    json.dumps(d)
    print("SUCCESS json.dumps")
except Exception as e:
    print(f"FAILED: {type(e).__name__}: {e}")
