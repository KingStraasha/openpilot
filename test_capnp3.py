import capnp
schema = """
@0x934efea7f017fff0;
struct Inner { ref @0 :Text; }
struct Msg { inner @0 :Inner; }
"""
with open("test.capnp", "w") as f:
    f.write(schema)

test_capnp = capnp.load("test.capnp")
msg = test_capnp.Msg.new_message()
reader = msg.as_reader()
print(bool(reader.inner))
print(reader.inner.ref == "")
