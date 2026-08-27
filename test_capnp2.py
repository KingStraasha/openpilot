import capnp
import sys

# Define a simple capnp schema string
schema = """
@0x934efea7f017fff0;
struct Model { type @0 :Text; }
struct ModelBundle { models @0 :List(Model); }
"""
with open("test.capnp", "w") as f:
    f.write(schema)

# Load it
capnp.remove_import_hook()
test_capnp = capnp.load("test.capnp")

bundle = test_capnp.ModelBundle.new_message()
model = test_capnp.Model.new_message()
model.type = "supercombo"

try:
    bundle.models = [model]
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {type(e).__name__}: {e}")
