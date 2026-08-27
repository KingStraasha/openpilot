import capnp
schema = """
@0x934efea7f017fff0;
struct Progress { status @0 :Text; }
struct Artifact { progress @0 :Progress; }
struct ModelBundle { artifact @0 :Artifact; }
"""
with open("test.capnp", "w") as f:
    f.write(schema)
test_capnp = capnp.load("test.capnp")

bundle = test_capnp.ModelBundle()
# Try assigning to a nested field directly
try:
    bundle.artifact.progress.status = "hello"
    print("SUCCESS MUTATING NESTED FIELD")
except Exception as e:
    print(f"FAILED: {e}")
