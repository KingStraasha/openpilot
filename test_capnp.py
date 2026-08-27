from cereal import custom
import cereal.messaging as messaging

bundle = custom.ModelManagerSP.ModelBundle()
bundle.index = 1
bundle.internalName = "test"

model = custom.ModelManagerSP.Model()
model.type = custom.ModelManagerSP.Model.Type.supercombo
# Try assigning list
try:
    bundle.models = [model]
    print("List assignment SUCCESS")
except Exception as e:
    print(f"List assignment FAILED: {e}")

