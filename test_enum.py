import capnp
schema = """
@0x934efea7f017fff0;
struct ModelBundle { 
    status @0 :DownloadStatus; 
    enum DownloadStatus { notDownloading @0; downloading @1; downloaded @2; failed @3; }
}
"""
with open("test.capnp", "w") as f:
    f.write(schema)

test_capnp = capnp.load("test.capnp")

try:
    print(test_capnp.ModelBundle.DownloadStatus.downloading)
except Exception as e:
    print(f"FAILED accessing enum: {type(e).__name__}: {e}")

bundle = test_capnp.ModelBundle.new_message()
try:
    bundle.status = test_capnp.ModelBundle.DownloadStatus.downloading
    print("SUCCESS enum assignment")
except Exception as e:
    print(f"FAILED enum assignment: {type(e).__name__}: {e}")
