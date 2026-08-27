import capnp
schema = """
@0x934efea7f017fff0;
struct ModelBundle { status @0 :Text; }
"""
with open("test.capnp", "w") as f:
    f.write(schema)
test_capnp = capnp.load("test.capnp")

bundle = test_capnp.ModelBundle()
print(type(bundle))
try:
    bundle.status = "hello"
    print("MUTABLE")
except Exception as e:
    print(f"IMMUTABLE: {e}")
