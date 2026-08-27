import requests
import json
data = requests.get("https://raw.githubusercontent.com/sunnypilot/sunnypilot-models/refs/heads/gh-pages/docs/driving_models_v21.json").json()
print(json.dumps(data["bundles"][0]["models"][0], indent=2))
