import capnp
schema = """
@0x934efea7f017fff0;
struct ModelBundle { status @0 :Text; }
struct Msg {
    selectedBundle @0 :ModelBundle;
    availableBundles @1 :List(ModelBundle);
}
"""
with open("test.capnp", "w") as f:
    f.write(schema)
test_capnp = capnp.load("test.capnp")

bundle1 = test_capnp.ModelBundle.new_message()
bundle1.status = "idle"

bundle2 = test_capnp.ModelBundle.new_message()
bundle2.status = "downloading"

msg = test_capnp.Msg.new_message()
msg.selectedBundle = bundle2
msg.availableBundles = [bundle1, bundle2]
data = msg.to_bytes()

# Now try to deserialize
try:
    parsed_msg = test_capnp.Msg.from_bytes(data)
    print("SUCCESS DESERIALIZATION")
    print(parsed_msg.selectedBundle.status)
except Exception as e:
    print(f"FAILED: {type(e).__name__}: {e}")
