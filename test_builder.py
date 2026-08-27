import capnp
schema = """
@0x934efea7f017fff0;
struct ModelBundle { status @0 :Text; }
"""
with open("test.capnp", "w") as f:
    f.write(schema)
test_capnp = capnp.load("test.capnp")

try:
    bundle = test_capnp.ModelBundle()
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
