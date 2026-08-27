from cereal import custom
import cereal.messaging as messaging

model = custom.ModelManagerSP.Model()
model.type = custom.ModelManagerSP.Model.Type.supercombo

bundle = custom.ModelManagerSP.ModelBundle()
bundle.index = 1
bundle.internalName = "test"
bundle.models = [model]

msg = messaging.new_message('modelManagerSP', valid=True)
state = msg.modelManagerSP
state.selectedBundle = bundle
print("Msg assigned.")
try:
    bytes_data = msg.to_bytes()
    print("Msg serialized.")
except Exception as e:
    print(f"FAILED: {e}")

