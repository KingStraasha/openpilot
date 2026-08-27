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

available_models = [bundle1, bundle2]
selected_bundle = bundle2 # Reference the exact same builder

msg = test_capnp.Msg.new_message()
try:
    msg.selectedBundle = selected_bundle
    msg.availableBundles = available_models
    print("SUCCESS assignment")
    data = msg.to_bytes()
    print("SUCCESS serialization")
except Exception as e:
    print(f"FAILED: {type(e).__name__}: {e}")
