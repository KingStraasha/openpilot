import capnp
schema = """
@0x934efea7f017fff0;
struct Model { type @0 :Text; }
struct ModelBundle { models @0 :List(Model); }
struct Msg { selectedBundle @0 :ModelBundle; }
"""
with open("test.capnp", "w") as f:
    f.write(schema)

test_capnp = capnp.load("test.capnp")

bundle = test_capnp.ModelBundle.new_message()
model = test_capnp.Model.new_message()
model.type = "supercombo"
bundle.models = [model] 

msg = test_capnp.Msg.new_message()
msg.selectedBundle = bundle
print("Models count in msg:", len(msg.selectedBundle.models))
